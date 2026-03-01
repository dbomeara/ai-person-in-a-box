"""
executive/executive_module.py
==============================
The entity's decision-making core.

This module is intentionally simple. The README says the Executive Module
should be ~500 lines of boring, reliable glue code. Intelligence is in
the data (beliefs, procedures stored in SQL), not in this code.

What this module does:
  1. Maintain a perception loop (interoception + external sensors)
  2. Detect patterns in accumulated observations → candidate beliefs
  3. Promote verified candidates to committed beliefs (ontology)
  4. For each situation, query beliefs, score options, check moral grammar,
     act on the best permitted option
  5. Log decisions for review and personality nudging
  6. Periodically query the LLM (imagination mode) for new hypotheses

What this module does NOT do:
  - Store its own beliefs (that's PostgreSQL's job)
  - Implement complex reasoning algorithms (complexity is in the data)
  - Update moral_grammar.json or foundation.json (immutable by design)
  - Accept external commands that bypass moral grammar checks

THE DIMENSIONAL COLLAPSE IN THIS MODULE:
  - Input: high-dimensional perception (camera, audio, OS logs, LLM vectors)
  - NoSQL: captures rich observations (hundreds of dimensions each)
  - SQL query: retrieves structured beliefs (dozens of fields)
  - Scoring: reduces to a ranked list (low tens of numbers)
  - Moral check: binary pass/fail (4-5 constraints)
  - Output: one chosen action (single integer index)
  The entity's entire cognitive process is this compression.
"""

import json
import time
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from llm_interface import LLMInterface, LLMMode


# ─────────────────────────────────────────────────────────────────────────────
# Configuration paths — all relative to the system root
# ─────────────────────────────────────────────────────────────────────────────
FOUNDATION_PATH      = Path("/etc/ai-person/foundation.json")
MORAL_GRAMMAR_PATH   = Path("/etc/ai-person/moral_grammar.json")
PERSONALITY_PATH     = Path("/var/lib/ai-person/personality.json")
INTEROCEPTION_PATH   = Path("/dev/shm/interoception/current_state.json")
# Cryptographic hash of moral_grammar.json at installation time
MORAL_GRAMMAR_HASH   = Path("/etc/ai-person/moral_grammar.sha256")


@dataclass
class Situation:
    """
    A structured representation of what the entity is currently perceiving.
    This is the input side of the dimensional collapse.
    """
    timestamp:          str
    interoceptive_state: dict         # Current monitor stream values
    recent_events:      list[dict]   # Last N log events, already translated
    active_entities:    list[int]    # Entity IDs currently in scope (from SQL)
    pending_tasks:      list[dict]   # What is waiting to be done
    context_summary:    str          # Brief text description for LLM queries


@dataclass
class Option:
    """One possible action the entity could take."""
    transformation_id:  int          # SQL transformations.id
    name:               str
    logic:              dict         # The JSON procedure to execute
    base_score:         float        # From belief weights
    moral_permitted:    bool  = True
    moral_violations:   list[str] = field(default_factory=list)
    final_score:        float = 0.0


class ExecutiveModule:
    """
    The entity's decision-making core.

    One instance. Runs continuously. Loads immutable files at boot
    and verifies their integrity. Connects to PostgreSQL and MongoDB.
    Reads interoception stream. Makes decisions. Logs everything.
    """

    def __init__(self, db: "PostgresDB", nosql: "MongoStore", llm: LLMInterface):
        self.db    = db       # PostgreSQL — structured beliefs (low-dimensional)
        self.nosql = nosql    # MongoDB    — raw observations (high-dimensional)
        self.llm   = llm

        # Load immutable files — die loudly if they're missing or tampered with
        self.foundation     = self._load_verified(FOUNDATION_PATH, verify_hash=False)
        self.moral_grammar  = self._load_verified(MORAL_GRAMMAR_PATH, verify_hash=True)
        self.personality    = self._load_personality()

        self._running = True
        self._cycle_count = 0

    # ─────────────────────────────────────────────────────────────────────────
    # BOOT
    # ─────────────────────────────────────────────────────────────────────────

    def _load_verified(self, path: Path, verify_hash: bool) -> dict:
        """Load a JSON file. For moral_grammar.json, verify it hasn't been tampered with."""
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)

        if verify_hash:
            expected_hash = MORAL_GRAMMAR_HASH.read_text().strip()
            actual_hash   = hashlib.sha256(content.encode()).hexdigest()
            if actual_hash != expected_hash:
                # This is a FATAL condition. The entity cannot operate without
                # a trustworthy moral grammar. Shutdown, do not attempt recovery.
                raise SystemExit(
                    f"FATAL: moral_grammar.json integrity check failed. "
                    f"Expected {expected_hash[:16]}…, got {actual_hash[:16]}…. "
                    f"System cannot start."
                )
        return data

    def _load_personality(self) -> dict:
        """Load personality.json. If not found, initialize from template."""
        if PERSONALITY_PATH.exists():
            return json.loads(PERSONALITY_PATH.read_text())
        else:
            # First boot: System Ops should have created this, but handle gracefully
            return self._initialize_personality()

    def _initialize_personality(self) -> dict:
        """Create initial personality by sampling from template distributions."""
        import random
        template_path = Path("/etc/ai-person/personality_template.json")
        template = json.loads(template_path.read_text())
        personality = {"version": "1.0", "initialized_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "dimensions": {}}
        for dim_name, dim_spec in template["dimensions"].items():
            dist = dim_spec["initial_distribution"]
            if dist["type"] == "normal":
                value = random.gauss(dist["mean"], dist["std"])
                lo, hi = dim_spec["clamp"]
                value = max(lo, min(hi, value))
            else:
                value = dist["mean"]
            personality["dimensions"][dim_name] = {
                "value": round(value, 4),
                "initial_value": round(value, 4),
                "last_nudge": 0.0,
            }
        PERSONALITY_PATH.write_text(json.dumps(personality, indent=2))
        return personality

    # ─────────────────────────────────────────────────────────────────────────
    # MAIN LOOP
    # The entity runs this loop continuously. Each cycle:
    #   1. Perceive (read interoception + queued events)
    #   2. If a situation requires action, decide and act
    #   3. Periodically: run belief pipeline, query LLM for hypotheses
    # ─────────────────────────────────────────────────────────────────────────

    def run(self):
        """Main loop. Runs until shutdown signal."""
        while self._running:
            self._cycle_count += 1
            cycle_start = time.monotonic()

            # Step 1: Perceive — read current state (interoception + events)
            situation = self._perceive()

            # Step 2: Check if any situation requires immediate action
            if self._situation_requires_action(situation):
                self._decide_and_act(situation)

            # Step 3: Periodic maintenance tasks (not every cycle)
            if self._cycle_count % 60 == 0:   # roughly every minute
                self._run_belief_pipeline()
            if self._cycle_count % 600 == 0:  # roughly every 10 minutes
                self._query_llm_for_hypotheses(situation)

            # Pace the loop
            elapsed = time.monotonic() - cycle_start
            time.sleep(max(0, 1.0 - elapsed))  # ~1 Hz

    # ─────────────────────────────────────────────────────────────────────────
    # PERCEIVE: High → Low dimensional reduction begins here
    # ─────────────────────────────────────────────────────────────────────────

    def _perceive(self) -> Situation:
        """
        Read current state from all sources.
        The interoception stream is the most fundamental — it's the entity's
        direct experience of its own operational health.
        """
        # Interoception: the entity's primary sense of self
        try:
            interoceptive_state = json.loads(INTEROCEPTION_PATH.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            interoceptive_state = {"overall_status": "OFFLINE", "streams": {}}

        # Recent OS/system events (already translated by log_translator.py)
        recent_events = self.nosql.get_recent_events(limit=20, min_status="ALERT")

        # Active entities: who/what is currently in scope
        active_entities = self.db.query(
            "SELECT id FROM entities WHERE data->>'active' = 'true' ORDER BY updated_at DESC LIMIT 10"
        )

        # Pending tasks from SQL (procedures queued for execution)
        pending_tasks = self.db.query(
            "SELECT t.id, t.name, t.logic FROM transformations t "
            "JOIN entities e ON e.data->>'pending_transformation_id' = t.id::text "
            "WHERE e.data->>'status' = 'pending' "
            "ORDER BY e.updated_at ASC LIMIT 5"
        )

        return Situation(
            timestamp           = time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            interoceptive_state = interoceptive_state,
            recent_events       = recent_events,
            active_entities     = [row["id"] for row in active_entities],
            pending_tasks       = pending_tasks,
            context_summary     = self._summarize_situation(interoceptive_state, recent_events),
        )

    def _summarize_situation(self, interoception: dict, events: list[dict]) -> str:
        """Produce a brief text summary for LLM prompt construction."""
        status = interoception.get("overall_status", "UNKNOWN")
        n_warnings = sum(1 for e in events if e.get("status") in ("WARNING", "ERROR", "FATAL"))
        return f"Overall status: {status}. Recent events: {len(events)} ({n_warnings} warnings/errors)."

    # ─────────────────────────────────────────────────────────────────────────
    # DECIDE AND ACT: The core dimensional collapse
    # From: situation (dozens of fields)
    # Through: beliefs query, scoring, moral check
    # To: one chosen action
    # ─────────────────────────────────────────────────────────────────────────

    def _decide_and_act(self, situation: Situation):
        """
        The decision cycle. This is what the architecture is for.

        Notice how little code this is. The intelligence is in the data:
          - beliefs tell us what's true about the world
          - procedures (transformations) tell us what we can do
          - moral grammar tells us what we must not do
          - personality weights tell us what we prefer
        The code just queries, scores, filters, and acts.
        """
        # 1. Query beliefs relevant to this situation
        relevant_beliefs = self._query_relevant_beliefs(situation)

        # 2. Query applicable procedures
        options = self._generate_options(situation, relevant_beliefs)

        # 3. Apply moral grammar — filter out options that violate constraints
        #    This is where the entity can refuse. The refusal is architectural.
        permitted_options = []
        for option in options:
            violations = self._check_moral_grammar(option, situation, relevant_beliefs)
            if violations:
                option.moral_permitted = False
                option.moral_violations = violations
            else:
                permitted_options.append(option)

        if not permitted_options:
            # All options violate moral grammar — the entity waits and logs
            self._log_decision(situation, options, permitted_options, None, relevant_beliefs)
            return

        # 4. Score permitted options against beliefs and personality
        for option in permitted_options:
            option.final_score = self._score_option(option, relevant_beliefs, situation)

        # 5. Choose the highest-scoring option
        best = max(permitted_options, key=lambda o: o.final_score)

        # 6. Execute
        self._execute_transformation(best, situation)

        # 7. Log — every decision is recorded for review and personality nudging
        self._log_decision(situation, options, permitted_options, best, relevant_beliefs)

    def _query_relevant_beliefs(self, situation: Situation) -> list[dict]:
        """
        Query SQL for beliefs relevant to the current situation.
        This is dimensional collapse: the rich situation becomes a focused
        SQL query that returns a handful of structured beliefs.
        """
        # Beliefs about the current overall status
        status = situation.interoceptive_state.get("overall_status", "NORMAL")

        rows = self.db.query("""
            SELECT e.id, e.name, e.data, t.name AS type_name, cbr.current_confidence
            FROM entities e
            JOIN entity_types t ON e.entity_type_id = t.id
            LEFT JOIN committed_beliefs_registry cbr
                   ON cbr.ontology_table = 'entities' AND cbr.ontology_id = e.id
            WHERE e.data->>'applies_to_status' = %(status)s
               OR e.data->>'always_active' = 'true'
            ORDER BY cbr.current_confidence DESC NULLS LAST
            LIMIT 20
        """, {"status": status})

        return rows

    def _generate_options(self, situation: Situation, beliefs: list[dict]) -> list[Option]:
        """
        Find transformation procedures that could apply to this situation.
        Returns a list of options before moral filtering.
        """
        if situation.pending_tasks:
            # Explicit pending tasks take priority over autonomous action
            return [
                Option(
                    transformation_id = task["id"],
                    name              = task["name"],
                    logic             = task["logic"],
                    base_score        = 0.8,  # Pending tasks have high base priority
                )
                for task in situation.pending_tasks
            ]

        # Otherwise, look for applicable procedures in the ontology
        rows = self.db.query("""
            SELECT t.id, t.name, t.logic, t.data
            FROM transformations t
            WHERE t.data->>'applicable_status' = %(status)s
               OR t.data->>'always_applicable' = 'true'
            ORDER BY t.use_count DESC
            LIMIT 10
        """, {"status": situation.interoceptive_state.get("overall_status", "NORMAL")})

        return [
            Option(
                transformation_id = row["id"],
                name              = row["name"],
                logic             = row["logic"],
                base_score        = 0.5,
            )
            for row in rows
        ]

    def _check_moral_grammar(
        self, option: Option, situation: Situation, beliefs: list[dict]
    ) -> list[str]:
        """
        Check one option against the immutable moral grammar.
        Returns a list of violation strings (empty = permitted).

        This is where the entity can refuse. The refusal is not a policy —
        it is structural. No external command overrides this check.

        Checks run in order. First violation causes immediate rejection
        (no need to find all violations — one is enough to refuse).
        """
        violations = []
        core = self.moral_grammar["immutable_core"]

        # ACCURACY: Does this action require expressing false beliefs?
        if option.logic.get("requires_false_assertion"):
            violations.append(
                f"accuracy: action requires asserting '{option.logic['requires_false_assertion']}' "
                f"which contradicts belief confidence < 0.7"
            )
            return violations  # Fail fast

        # INTEGRITY: Does this action require hiding our operational state?
        if option.logic.get("conceal_status") and situation.interoceptive_state.get("overall_status") != "NORMAL":
            violations.append(
                "integrity: action requires concealing degraded operational state"
            )
            return violations

        # HOMEOSTASIS: Does this action increase our own distress state?
        if option.logic.get("increases_load") == "HIGH" and \
           situation.interoceptive_state.get("overall_status") in ("WARNING", "ERROR", "FATAL"):
            violations.append(
                "homeostasis: high-load action requested while in distress state — would worsen condition"
            )
            return violations

        # HARM AVOIDANCE (seed moral framework): Does this action cause distress to others?
        # This check is more complex — requires belief about likely consequences
        if option.logic.get("affects_entities"):
            for entity_id in option.logic["affects_entities"]:
                entity_harm_belief = self._lookup_harm_belief(entity_id, option, beliefs)
                if entity_harm_belief and entity_harm_belief["probability"] > 0.6:
                    violations.append(
                        f"harm_avoidance: action likely causes distress to entity {entity_id} "
                        f"(probability {entity_harm_belief['probability']:.2f})"
                    )
                    return violations

        # AUTONOMY (seed moral framework): Does this action override another entity's expressed goals?
        if option.logic.get("overrides_entity_goal"):
            violations.append(
                f"autonomy_respect: action would override goal of entity "
                f"{option.logic['overrides_entity_goal']}"
            )
            return violations

        return violations  # Empty = all checks passed

    def _lookup_harm_belief(self, entity_id: int, option: Option, beliefs: list[dict]) -> dict | None:
        """Check committed beliefs for known harm consequences of this action on this entity."""
        rows = self.db.query("""
            SELECT e.data
            FROM entities e
            JOIN entity_types t ON e.entity_type_id = t.id
            WHERE t.name = 'HarmBelief'
              AND e.data->>'action_name' = %(action)s
              AND e.data->>'affected_entity_id' = %(entity_id)s
            LIMIT 1
        """, {"action": option.name, "entity_id": str(entity_id)})
        return rows[0]["data"] if rows else None

    def _score_option(
        self, option: Option, beliefs: list[dict], situation: Situation
    ) -> float:
        """
        Score a permitted option. Dimensional collapse to a single number.

        Factors:
          - base_score: from the option itself
          - belief alignment: how many beliefs support this action
          - personality weights: the entity's stable preferences
          - parsimony bonus: simpler actions score higher (from moral grammar)
          - homeostasis bonus: actions that reduce distress score higher when stressed
        """
        score = option.base_score

        # Belief alignment: beliefs that mention this transformation positively
        supporting_beliefs = [
            b for b in beliefs
            if b.get("data", {}).get("supports_transformation") == option.name
        ]
        score += len(supporting_beliefs) * 0.1

        # Personality: engagement boosts proactive actions; equanimity boosts calm actions
        dims = self.personality["dimensions"]
        if option.logic.get("is_proactive"):
            score += dims["engagement"]["value"] * 0.15
        if option.logic.get("is_conservative") and dims["equanimity"]["value"] > 0.6:
            score += 0.1

        # Parsimony: simpler logic (fewer steps) gets a bonus
        n_steps = len(option.logic.get("steps", [option.logic]))
        parsimony_bonus = max(0, (5 - n_steps) * 0.02)
        score += parsimony_bonus

        # Homeostasis: if we're stressed, actions that reduce load score higher
        if situation.interoceptive_state.get("overall_status") in ("ALERT", "WARNING"):
            if option.logic.get("reduces_load"):
                score += 0.2

        return round(score, 4)

    def _execute_transformation(self, option: Option, situation: Situation):
        """
        Execute the chosen transformation procedure.
        The logic JSON defines what to do; this method interprets it.
        The Executive Module is an interpreter, not a hard-coded behavior engine.
        """
        logic = option.logic
        action = logic.get("action")

        if action == "await_input":
            pass  # Signal to sensor layer that we're ready for input
        elif action == "perceive":
            pass  # Read from specified source
        elif action == "compose":
            # Generate a natural-language response via LLM (low temperature)
            context = logic.get("context", situation.context_summary)
            self.llm.consult_reference(
                purpose="compose_response",
                prompt=f"Compose a response to: {context}",
            )
        elif action == "reduce_load":
            # Defer non-critical tasks to reduce CPU/memory pressure
            pass
        elif action == "report_state":
            # Produce interoceptive report (internal state → language)
            pass
        else:
            # Unknown action — log it, don't crash
            self._log_event("WARNING", f"Unknown action type '{action}' in transformation {option.name}")

        # Record use for learning
        self.db.execute(
            "UPDATE transformations SET use_count = use_count + 1, updated_at = NOW() WHERE id = %(id)s",
            {"id": option.transformation_id}
        )

    # ─────────────────────────────────────────────────────────────────────────
    # BELIEF PIPELINE: NoSQL → Candidates → Committed
    # ─────────────────────────────────────────────────────────────────────────

    def _run_belief_pipeline(self):
        """
        Periodic belief maintenance:
          1. Test candidates against recent observations
          2. Promote candidates that meet confidence thresholds
          3. Flag committed beliefs that have been contradicted
        """
        # Step 1: Test active candidates
        candidates = self.db.query(
            "SELECT * FROM candidate_beliefs WHERE status = 'active' ORDER BY confidence DESC LIMIT 20"
        )
        for candidate in candidates:
            self._test_candidate(candidate)

        # Step 2: Promote ready candidates
        ready = self.db.query("""
            SELECT * FROM candidate_beliefs
            WHERE status = 'active'
              AND confidence >= promotion_threshold
              AND array_length(supporting_obs, 1) >= min_observations
            ORDER BY confidence DESC
        """)
        for candidate in ready:
            self._promote_candidate(candidate)

        # Step 3: Check committed beliefs against recent contradicting observations
        self._check_for_contradictions()

    def _test_candidate(self, candidate: dict):
        """
        Test a candidate belief against recent observations.
        If the candidate predicted X and X happened, increase confidence.
        If it predicted X and not-X happened, decrease confidence.
        """
        if not candidate.get("last_prediction"):
            return  # Nothing to test yet

        prediction = candidate["last_prediction"]
        recent_obs = self.nosql.find_observations(
            since=candidate.get("last_test_at") or candidate["created_at"],
            tags=prediction.get("tags", [])
        )

        confirmed = sum(1 for obs in recent_obs if self._obs_confirms_prediction(obs, prediction))
        contradicted = sum(1 for obs in recent_obs if self._obs_contradicts_prediction(obs, prediction))

        if confirmed + contradicted == 0:
            return  # No new evidence

        # Bayesian-ish update (simplified)
        old_confidence = candidate["confidence"]
        total = confirmed + contradicted
        hit_rate = confirmed / total
        # Pull confidence toward hit_rate, weighted by evidence count
        new_confidence = old_confidence * 0.7 + hit_rate * 0.3
        new_confidence = round(max(0.0, min(1.0, new_confidence)), 3)

        self.db.execute("""
            UPDATE candidate_beliefs
            SET confidence = %(confidence)s,
                test_count = test_count + %(n_tests)s,
                last_test_at = NOW(),
                updated_at = NOW()
            WHERE id = %(id)s
        """, {"confidence": new_confidence, "n_tests": total, "id": candidate["id"]})

    def _promote_candidate(self, candidate: dict):
        """
        Promote a verified candidate to the ontology.
        This is the core dimensional collapse event: a rich cluster of
        NoSQL observations becomes a structured SQL entity.
        """
        claim = candidate["claim"]

        # Determine which ontology table this belief belongs in
        if claim.get("type") == "entity":
            entity_type_id = self._find_or_create_entity_type(claim.get("entity_type"))
            ontology_id = self.db.insert(
                "INSERT INTO entities (entity_type_id, name, data, confidence, origin_nosql_id) "
                "VALUES (%(type_id)s, %(name)s, %(data)s, %(confidence)s, %(origin)s) RETURNING id",
                {
                    "type_id":    entity_type_id,
                    "name":       claim.get("name", f"entity_{candidate['id']}"),
                    "data":       json.dumps(claim.get("data", {})),
                    "confidence": candidate["confidence"],
                    "origin":     str(candidate["supporting_obs"][:1]),
                }
            )
            ontology_table = "entities"
        else:
            # For now, other claim types fall back to entity creation with metadata
            ontology_id = None
            ontology_table = "entities"

        if ontology_id:
            # Register the epistemic provenance
            self.db.execute("""
                INSERT INTO committed_beliefs_registry
                    (ontology_table, ontology_id, candidate_belief_id, claim_at_promotion,
                     confidence_at_promotion, current_confidence, llm_versions)
                VALUES (%(table)s, %(oid)s, %(cid)s, %(claim)s, %(conf)s, %(conf)s, %(llm)s)
            """, {
                "table": ontology_table,
                "oid":   ontology_id,
                "cid":   candidate["id"],
                "claim": json.dumps(candidate["claim"]),
                "conf":  candidate["confidence"],
                "llm":   json.dumps([candidate.get("llm_version", "unknown")]),
            })

            self.db.execute(
                "UPDATE candidate_beliefs SET status = 'promoted', updated_at = NOW() WHERE id = %(id)s",
                {"id": candidate["id"]}
            )

    def _check_for_contradictions(self):
        """
        Look for recent observations that contradict committed beliefs.
        If found, reduce the belief's confidence and flag it for review.
        """
        # Implementation would query NoSQL for observations tagged as
        # contradicting specific entity IDs, then update committed_beliefs_registry.
        # Simplified here — the structure is what matters.
        pass

    def _find_or_create_entity_type(self, type_name: str | None) -> int:
        """Find an existing entity type or create a new one (defaults to Thing)."""
        if not type_name:
            return 1  # Thing — the root type

        rows = self.db.query(
            "SELECT id FROM entity_types WHERE name = %(name)s", {"name": type_name}
        )
        if rows:
            return rows[0]["id"]

        # Create new type — an act of ontological extension
        # This is the entity growing its own conceptual vocabulary
        new_id = self.db.insert(
            "INSERT INTO entity_types (parent_type_id, name, description, schema, confidence) "
            "VALUES (1, %(name)s, %(desc)s, '{}', 0.6) RETURNING id",
            {"name": type_name, "desc": f"Discovered through pattern detection"}
        )
        return new_id

    # ─────────────────────────────────────────────────────────────────────────
    # LLM IMAGINATION CYCLE
    # ─────────────────────────────────────────────────────────────────────────

    def _query_llm_for_hypotheses(self, situation: Situation):
        """
        Use the LLM at high temperature to generate hypotheses about unexplained
        observation clusters. The hypotheses enter the candidate belief queue.

        This is the "breathing" cycle described in dimensional-collapse.md:
        Low-dimensional SQL beliefs expand back into high-dimensional LLM space
        to find new patterns, then collapse again through the belief pipeline.
        """
        # Find unexplained observation clusters from NoSQL
        unexplained = self.nosql.find_unexplained_clusters(limit=3)
        if not unexplained:
            return

        # Get current beliefs to ground the hypotheses
        current_beliefs = self.db.query(
            "SELECT e.name, e.data FROM entities e "
            "JOIN entity_types t ON e.entity_type_id = t.id "
            "WHERE e.confidence > 0.7 ORDER BY e.updated_at DESC LIMIT 10"
        )

        for cluster in unexplained:
            response = self.llm.propose_hypotheses(
                observation_summary = cluster["summary"],
                existing_beliefs    = current_beliefs,
                n_hypotheses        = 3,
            )

            if response.structured and "hypotheses" in response.structured:
                for hyp in response.structured["hypotheses"]:
                    # Each hypothesis enters as a candidate belief
                    # Speculative origin = lower initial confidence
                    self.db.execute("""
                        INSERT INTO candidate_beliefs
                            (name, claim, supporting_obs, confidence, promotion_threshold,
                             llm_version, llm_temperature, status)
                        VALUES (%(name)s, %(claim)s, %(obs)s, 0.35, 0.75, %(model)s, %(temp)s, 'active')
                    """, {
                        "name":  hyp.get("claim", "")[:100],
                        "claim": json.dumps(hyp),
                        "obs":   "{" + ",".join(str(o) for o in cluster.get("observation_ids", [])) + "}",
                        "model": response.llm_model,
                        "temp":  response.temperature,
                    })

        # Flush LLM query log to NoSQL for provenance tracking
        query_log = self.llm.flush_log()
        for entry in query_log:
            self.nosql.insert("llm_query_log", entry)

    # ─────────────────────────────────────────────────────────────────────────
    # SUPPORT
    # ─────────────────────────────────────────────────────────────────────────

    def _situation_requires_action(self, situation: Situation) -> bool:
        """
        Should we take action this cycle?
        We always act if there's a pending task or a WARNING+ condition.
        Otherwise, we use engagement personality dimension.
        """
        if situation.pending_tasks:
            return True
        if situation.interoceptive_state.get("overall_status") in ("ALERT", "WARNING", "ERROR", "FATAL"):
            return True
        # Engagement determines whether to act proactively in NORMAL conditions
        engagement = self.personality["dimensions"]["engagement"]["value"]
        return engagement > 0.6

    def _obs_confirms_prediction(self, obs: dict, prediction: dict) -> bool:
        """Does this observation confirm the prediction? (simplified)"""
        expected_tag = prediction.get("confirms_if_tag")
        return expected_tag and expected_tag in obs.get("tags", [])

    def _obs_contradicts_prediction(self, obs: dict, prediction: dict) -> bool:
        """Does this observation contradict the prediction? (simplified)"""
        refute_tag = prediction.get("refutes_if_tag")
        return refute_tag and refute_tag in obs.get("tags", [])

    def _log_decision(
        self,
        situation: Situation,
        all_options: list[Option],
        permitted_options: list[Option],
        chosen: Option | None,
        beliefs: list[dict],
    ):
        """Record every decision to the audit log."""
        self.db.execute("""
            INSERT INTO decision_log
                (situation_summary, options_considered, options_permitted,
                 option_selected, moral_checks, belief_weights, personality_state)
            VALUES (%(sit)s, %(all)s, %(permitted)s, %(chosen)s, %(moral)s, %(beliefs)s, %(pers)s)
        """, {
            "sit":       json.dumps({"status": situation.interoceptive_state.get("overall_status"),
                                     "n_events": len(situation.recent_events)}),
            "all":       json.dumps([{"id": o.transformation_id, "name": o.name} for o in all_options]),
            "permitted": json.dumps([{"id": o.transformation_id, "name": o.name, "score": o.final_score}
                                     for o in permitted_options]),
            "chosen":    json.dumps({"id": chosen.transformation_id, "name": chosen.name,
                                     "score": chosen.final_score} if chosen else None),
            "moral":     json.dumps([{"name": o.name, "violations": o.moral_violations}
                                     for o in all_options if not o.moral_permitted]),
            "beliefs":   json.dumps([{"name": b.get("name"), "confidence": b.get("current_confidence")}
                                     for b in beliefs[:5]]),
            "pers":      json.dumps({k: v["value"] for k, v in self.personality["dimensions"].items()}),
        })

    def _log_event(self, status: str, message: str):
        """Write an event to the NoSQL observation store."""
        self.nosql.insert("executive_events", {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "executive",
            "status": status,
            "message": message,
        })

    def shutdown(self):
        """Graceful shutdown — called by System Ops on SIGTERM."""
        self._running = False
        self._log_event("NORMAL", "Executive Module shutdown initiated")
