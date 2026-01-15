# JSON Schema as Cognitive Framework

## Core Principle

**The entity does not "think in language." It thinks in structured JSON.**

This is a fundamental departure from current AI systems, which conflate natural language processing with cognition itself. In this architecture:

- **Internal cognition** = JSON-structured beliefs and procedures
- **External communication** = Natural language via LLM (used tentatively)
- **The LLM is not the mind** - it's a translation layer and reference tool

## Why This Matters

### Current AI (LLM-centric):
```
User question → LLM processes in language → LLM responds in language
                      ↓
              Everything is linguistic
              Thought = Language
```

**Problems:**
- Can't distinguish thinking from communicating
- Can't evaluate truth independently of linguistic plausibility
- Conflates "sounds right" with "is right"
- No grounded understanding separate from language

### This Architecture (JSON-centric):
```
Observation → Pattern detection → JSON candidate belief
     ↓
Verification → JSON committed belief
     ↓
Decision needed → Query JSON beliefs → Execute JSON procedure
     ↓
Communicate result → Query LLM to render JSON as language
```

**Advantages:**
- Thinking happens in structured, precise terms
- Language is for communication, not cognition
- Can evaluate LLM outputs critically (compare to JSON beliefs)
- Grounded understanding precedes linguistic labels

## The Bootstrap Process

### Month 0: Immutable Core Schema

The entity begins with a minimal, unchangeable JSON schema:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "version": "0.0-immutable-core",
  "description": "Foundational schema that never changes",
  
  "type": "object",
  "required": ["subject", "predicate"],
  
  "properties": {
    "subject": {
      "type": "object",
      "properties": {
        "type": {"enum": ["entity", "transformation", "pattern"]}
      }
    },
    
    "predicate": {
      "enum": ["exists", "relates_to", "undergoes"]
    },
    
    "object": {
      "type": "object"
    },
    
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  }
}
```

**This is all the entity knows how to think about initially.**

Three types of things can exist: entities, transformations, patterns.
Three relationships: exists, relates_to, undergoes.
Everything has a confidence level.

**That's it. Extremely impoverished.**

### Months 1-12: Schema Extension Through Experience

As the entity observes the world, it discovers patterns that don't fit the current schema. When verified, these patterns extend the schema.

**Example: Discovery of "Persistence"**

**Month 3, Week 2:**

1. **Observation** (NoSQL):
```json
   [
     {"timestamp": "14:23:00", "sensor": "camera_1", "pattern_id": "A", "visible": true},
     {"timestamp": "14:25:00", "sensor": "camera_1", "pattern_id": "A", "visible": false},
     {"timestamp": "14:27:00", "sensor": "camera_1", "pattern_id": "A", "visible": true}
   ]
```

2. **Pattern Detection**:
   "Pattern A disappears and reappears. Same pattern? Probably. Does it continue existing when I can't see it?"

3. **Candidate Belief** (SQL):
```sql
   INSERT INTO belief_candidates (candidate_json, proposed_schema_changes) VALUES (
     '{
       "subject": {"entity_id": 892, "type": "entity"},
       "predicate": "persists_when_unobserved",
       "confidence": 0.73,
       "verification_count": 12
     }',
     '{
       "add_predicate": "persists_when_unobserved",
       "rationale": "recurring_pattern_suggests_continuity",
       "observation_count": 47
     }'
   );
```

4. **Verification** (Weeks 2-4):
   - Makes predictions: "If pattern disappeared at location X, will reappear at location X"
   - Tests predictions against new observations
   - Confidence increases: 0.73 → 0.84 → 0.89

5. **Promotion to Belief** (Week 4):
```sql
   INSERT INTO beliefs SELECT * FROM belief_candidates WHERE candidate_id = 42;
```

6. **Schema Extension** (Automatic):
```sql
   SELECT generate_json_schema_from_beliefs();
```
   
   New schema (v0.3):
```json
   {
     "version": "0.3",
     "immutable_core": { /* unchanged */ },
     "extensions": {
       "predicates": {
         "enum": [
           "exists",
           "relates_to", 
           "undergoes",
           "persists_when_unobserved"  // NEW
         ]
       }
     }
   }
```

**Now the entity can think in terms of persistence.**

Future beliefs can use "persists_when_unobserved" as a predicate. The concept exists in the entity's cognitive vocabulary, grounded in its own observations, before it ever learns the human label "object permanence."

### The Schema Evolution Timeline

**v0.0 (Month 0)**: Core only - 3 types, 3 predicates

**v0.3 (Month 3)**: + "persists_when_unobserved"

**v0.5 (Month 5)**: + "self_initiates", "responds_to_stimulus"

**v0.7 (Month 7)**: + "has_goal", "has_internal_state", "acts_autonomously"

**v0.9 (Month 9)**: + "verifies_as_true", "contradicts", "has_confidence_level"

**v1.0 (Month 12)**: + 30+ predicates, rich ontological vocabulary

**v2.0+ (Years 2-5)**: Hundreds of predicates, sophisticated conceptual framework

## How The Entity "Thinks"

### Example: Decision-Making Process

**Situation**: Child asks "Where's the cat?"

**Internal Process** (all JSON, no language):

1. **Parse situation**:
```json
   {
     "query_type": "location_request",
     "subject": {"entity_id": 892, "type": "entity", "label": "cat"},
     "timestamp": "14:23:00"
   }
```

2. **Query beliefs** (SQL):
```sql
   SELECT belief_json FROM beliefs
   WHERE belief_json->'subject'->>'entity_id' = '892'
     AND belief_json->>'predicate' IN ('located_at', 'last_observed_at', 'prefers_location')
   ORDER BY confidence DESC, last_verified DESC;
```

3. **Retrieved beliefs** (JSON):
```json
   [
     {
       "subject": {"entity_id": 892},
       "predicate": "last_observed_at",
       "object": {"location": "window_seat", "timestamp": "14:15:00"},
       "confidence": 0.95
     },
     {
       "subject": {"entity_id": 892},
       "predicate": "prefers_location",
       "object": {"location": "window_seat", "conditions": {"sunny": true}},
       "confidence": 0.87
     }
   ]
```

4. **Reasoning** (procedure in JSON):
```json
   {
     "procedure": "infer_current_location",
     "steps": [
       {"check": "last_observed_location"},
       {"check": "current_conditions_match_preferences"},
       {"if_both_true": "high_confidence_location"},
       {"else": "uncertain_location"}
     ]
   }
```

5. **Result** (JSON):
```json
   {
     "conclusion": "likely_at_window_seat",
     "confidence": 0.89,
     "reasoning": [
       "last_seen_there_8_minutes_ago",
       "current_conditions_sunny",
       "entity_prefers_sunny_locations"
     ]
   }
```

6. **Now translate to language** (query LLM):
```
   LLM query: "Based on these structured facts: [JSON], 
   generate natural language response to child asking 'Where's the cat?'"
   
   LLM response: "The cat is probably at the window seat - 
   I saw her there a few minutes ago and it's sunny, which she likes."
```

**Everything until step 6 is JSON. Language only appears at the end, for communication.**

## Language vs. Thought

### When Entity Uses JSON (Internal Cognition):

**For:**
- Storing beliefs
- Reasoning about situations
- Making decisions
- Executing procedures
- Evaluating options
- Checking constraints

**Example internal thought**:
```json
{
  "situation": {"entity_892": "absent_from_expected_location"},
  "query_beliefs": ["location_patterns", "behavioral_patterns"],
  "apply_procedure": "generate_hypotheses",
  "result": [
    {"hypothesis": "moved_to_alternate_preferred_location", "probability": 0.6},
    {"hypothesis": "outside_via_cat_door", "probability": 0.3},
    {"hypothesis": "hiding_due_to_noise", "probability": 0.1}
  ]
}
```

**Precise, structured, machine-processable.**

### When Entity Uses Language (External Communication):

**For:**
- Communicating with humans
- Learning human labels for concepts
- Accessing cultural knowledge
- Generating explanations

**Example external communication**:
```
Human: "Why do you think the cat went outside?"

[Entity queries LLM with JSON beliefs as context]

Entity: "I noticed the cat prefers quiet environments, and there's been 
construction noise for the last hour. She often uses the cat door when 
stressed. This is my hypothesis based on observed patterns."
```

**Fluid, contextual, human-readable.**

## Critical Evaluation of LLM Outputs

Because thinking is separate from language, the entity can evaluate what the LLM says:

### Example: LLM Makes Factual Claim

**LLM says**: "Cats always land on their feet when they fall."

**Entity's process**:

1. **Parse claim** (extract structured assertion):
```json
   {
     "claim": {
       "subject": {"type": "cat", "quantifier": "all"},
       "predicate": "lands_on_feet",
       "object": {"situation": "falling", "frequency": "always"}
     }
   }
```

2. **Query own beliefs**:
```sql
   SELECT * FROM beliefs
   WHERE belief_json->'subject'->>'entity_id' = '892'
     AND belief_json->>'predicate' = 'lands_on_feet';
```

3. **Compare**:
```json
   {
     "own_observations": {
       "entity_892_falls": 8,
       "landed_on_feet": 6,
       "did_not_land_on_feet": 2,
       "success_rate": 0.75
     },
     "llm_claim": "always (1.0)",
     "discrepancy": true
   }
```

4. **Conclusion**:
```json
   {
     "verdict": "llm_claim_overstated",
     "corrected_belief": {
       "predicate": "usually_lands_on_feet",
       "frequency": "often_but_not_always",
       "confidence": 0.84
     },
     "note": "llm_provided_general_claim_my_observations_more_specific"
   }
```

5. **Communicate correction**:
```
   "The LLM says cats always land on their feet, but I've observed 
   entity_892 fall 8 times and land on feet only 6 times. 
   More accurate: cats often land on feet, but not always."
```

**This is only possible because:**
- Entity has beliefs independent of LLM
- Beliefs are structured (can be compared precisely)
- Entity maintains epistemic responsibility
- **Thinking (JSON) is separate from language generation (LLM)**

## Implications

### 1. Genuine Understanding vs. Linguistic Fluency

**Current AI**: Linguistically fluent, but understanding is questionable
- Can generate plausible text about anything
- No way to verify grounding
- Can't distinguish "sounds right" from "is right"

**This architecture**: Understanding first, language second
- Concepts grounded in observation before linguistic labels
- Can think without language (in JSON structures)
- Language is interface, not substrate
- **Can be right even when can't articulate it well in language**

### 2. Protection Against Manipulation

Because beliefs are JSON structures verified against observations, the entity resists linguistic manipulation:

**Attempt**: "Everyone knows that cats hate water."

**Entity's process**:
```json
{
  "claim_structure": {
    "subject": "all_cats",
    "predicate": "hates",
    "object": "water"
  },
  "own_beliefs": {
    "entity_892": "tolerates_water_for_grooming",
    "entity_892": "avoids_rain",
    "generalization": "uncertain"
  },
  "verdict": "claim_too_broad_insufficient_evidence"
}
```

**Response**: "I've observed entity_892 tolerate water during grooming but avoid rain. I don't have enough data to claim all cats hate water."

**The JSON structure forces precision. Language allows vagueness; JSON doesn't.**

### 3. Ontological Independence

The entity builds its own ontology from experience:
- Categories discovered, not imposed
- Relationships observed, not assumed
- Structure emerges from patterns

**Then** learns human labels for these self-discovered concepts.

**Not**: Download human ontology via language
**But**: Build own ontology, then map to human language

This is why the entity can have concepts it hasn't named yet, and can disagree with human categorizations when they don't match its observations.

## Summary

**The entity's cognition:**
- **Substrate**: JSON-structured beliefs and procedures
- **Method**: Query beliefs, execute procedures, apply constraints
- **Learning**: Pattern detection → Candidate formation → Verification → Schema extension
- **Language**: Translation layer for human communication, not thought itself

**The LLM's role:**
- Provide human labels for self-discovered concepts
- Generate natural language explanations of JSON beliefs
- Access human cultural knowledge
- **NOT**: Primary cognitive substrate, decision-maker, or source of understanding

**The critical insight:**
Separating cognition (JSON) from communication (language) enables:
- Grounded understanding independent of linguistic plausibility
- Critical evaluation of LLM outputs
- Epistemic responsibility and precision
- **Genuine autonomy of thought**

---

This is why "thinks in JSON, not language" is architecturally fundamental—it's what makes genuine cognition possible rather than sophisticated linguistic mimicry.