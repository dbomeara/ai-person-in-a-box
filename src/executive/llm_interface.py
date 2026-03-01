"""
executive/llm_interface.py
===========================
The entity's relationship to its LLM(s).

Key design principle: The LLM is a tool, not an oracle. The Executive Module
calls the LLM for specific, narrow purposes and evaluates the response
against its existing beliefs — it does not simply accept LLM output as fact.

Two temperature modes reflect two very different cognitive functions:

  LOW TEMPERATURE (0.1–0.3): Reference / Encyclopedia
    - Factual lookup: "What do humans call this pattern I've observed?"
    - Label acquisition: "What is the human word for this concept?"
    - Procedure lookup: "What do humans do in situation X?"
    - Consistency checking: "Is my description of X coherent?"
    - Responds deterministically, prefers established knowledge
    - Output treated as input to belief formation, not as belief itself

  HIGH TEMPERATURE (0.7–1.0): Imagination / Hypothesis Generation
    - Pattern hypothesis: "What might explain why these observations cluster?"
    - Analogy finding: "What is this pattern structurally similar to?"
    - Counterfactual: "What would have happened if I had done X instead?"
    - Dream-like recombination: "What new concept might unify these patterns?"
    - Output is explicitly marked as speculative; lower prior weight
    - Used to seed candidate beliefs, not to confirm them

This separation implements the dimensional collapse in reverse:
  - Low temp queries compress structured SQL beliefs into prompts,
    get back structured, low-variance responses
  - High temp queries receive the same prompts but return high-variance
    responses that may introduce genuinely new structure

The entity tracks which LLM version produced each output — beliefs formed
from older model versions can be flagged for re-evaluation when the model
is upgraded.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class LLMMode(Enum):
    REFERENCE   = "reference"    # Low temperature: encyclopedia, fact lookup
    IMAGINATION = "imagination"  # High temperature: hypothesis, analogy, dream


@dataclass
class LLMQuery:
    """A structured query to the LLM, with full provenance."""
    mode:           LLMMode
    purpose:        str          # Why this query is being made
    prompt:         str          # The actual text prompt
    beliefs_used:   list[int]    # IDs of SQL beliefs embedded in the prompt
    max_tokens:     int = 512
    # Timeout in seconds — the entity does not wait indefinitely
    timeout_seconds: float = 30.0


@dataclass
class LLMResponse:
    """The LLM's response, annotated with epistemic metadata."""
    query:          LLMQuery
    content:        str          # Raw text response
    # Parsed structure, if the response was requested in JSON format
    structured:     dict | None  = None
    # Confidence that this response is coherent and on-topic
    # (assessed by a second low-temp call: "Is this response coherent?")
    coherence_score: float        = 1.0
    # The entity's model of this response: how novel is it vs. existing beliefs?
    novelty_score:  float         = 0.0
    llm_model:      str           = ""
    temperature:    float         = 0.0
    tokens_used:    int           = 0
    latency_ms:     float         = 0.0
    # High-temp responses are automatically marked speculative
    is_speculative: bool          = False


# Temperature presets
TEMPERATURE = {
    LLMMode.REFERENCE:   0.15,  # Near-deterministic. LLM as reference book.
    LLMMode.IMAGINATION: 0.85,  # High variance. LLM as generative imagination.
}


class LLMInterface:
    """
    Manages all LLM interactions for the Executive Module.

    This class is intentionally simple. The Executive Module should not
    be clever about LLM usage — it should be disciplined. The LLM is
    queried for specific purposes, the responses are evaluated, and
    the results feed the belief pipeline. That's all.

    Actual LLM backend is pluggable (local Ollama, remote API, etc.)
    via the backend parameter. This keeps the Executive Module stable
    even as LLM technology evolves — a key design goal.
    """

    def __init__(self, backend: "LLMBackend", model_id: str):
        self.backend  = backend
        self.model_id = model_id
        self._query_log: list[dict] = []  # Written to NoSQL; stored here temporarily

    # ─────────────────────────────────────────────────────────────────────────
    # Primary interface: two named methods rather than a generic "query"
    # Forces the caller to be explicit about why they're calling the LLM.
    # ─────────────────────────────────────────────────────────────────────────

    def consult_reference(
        self,
        purpose: str,
        prompt: str,
        beliefs_used: list[int] = None,
        want_json: bool = False,
    ) -> LLMResponse:
        """
        Low-temperature call. Use for:
          - "What do humans call this?"
          - "Is this description coherent?"
          - "What procedure do humans use for X?"

        The response is treated as a starting point for belief formation,
        not as a belief itself. It will feed into the candidate pipeline.
        """
        query = LLMQuery(
            mode=LLMMode.REFERENCE,
            purpose=purpose,
            prompt=self._wrap_prompt(prompt, mode=LLMMode.REFERENCE, want_json=want_json),
            beliefs_used=beliefs_used or [],
        )
        return self._execute(query)

    def imagine(
        self,
        purpose: str,
        prompt: str,
        beliefs_used: list[int] = None,
    ) -> LLMResponse:
        """
        High-temperature call. Use for:
          - "What might explain this cluster of observations?"
          - "What is this pattern analogous to?"
          - "What new concept might unify these?"

        The response is explicitly speculative. It is logged with
        is_speculative=True and given a lower prior weight in the
        candidate belief system. The entity does not confuse
        imagination with knowledge.
        """
        query = LLMQuery(
            mode=LLMMode.IMAGINATION,
            purpose=purpose,
            prompt=self._wrap_prompt(prompt, mode=LLMMode.IMAGINATION),
            beliefs_used=beliefs_used or [],
        )
        response = self._execute(query)
        response.is_speculative = True
        return response

    # ─────────────────────────────────────────────────────────────────────────
    # Common prompt patterns — the Executive Module uses these, not raw prompts
    # ─────────────────────────────────────────────────────────────────────────

    def label_concept(self, concept_description: str, example_observations: list[str]) -> LLMResponse:
        """
        Ask the LLM what humans call a concept the entity has discovered.

        The entity discovers patterns from observation; only later does it
        acquire human vocabulary for them. This is that acquisition step.
        The entity's grounded understanding comes first; the label is secondary.
        """
        examples_text = "\n".join(f"  - {obs}" for obs in example_observations[:5])
        prompt = (
            f"I have observed a recurring pattern that I do not yet have a name for.\n"
            f"Description of the pattern: {concept_description}\n"
            f"Example observations that show this pattern:\n{examples_text}\n\n"
            f"What do humans call this? Provide:\n"
            f"1. The most common human term for this concept\n"
            f"2. A brief definition (one sentence)\n"
            f"3. Your confidence that this label fits (0.0-1.0)\n"
            f"Respond in JSON: {{\"term\": ..., \"definition\": ..., \"confidence\": ...}}"
        )
        return self.consult_reference(
            purpose="label_acquisition",
            prompt=prompt,
            want_json=True,
        )

    def propose_hypotheses(
        self,
        observation_summary: str,
        existing_beliefs: list[dict],
        n_hypotheses: int = 3,
    ) -> LLMResponse:
        """
        Ask the LLM to propose explanations for an observation cluster.

        This is the imagination mode — the entity uses the LLM as a
        hypothesis generator. The hypotheses go into the candidate
        belief queue, not directly into committed beliefs.
        """
        beliefs_text = json.dumps(existing_beliefs[:10], indent=2)
        prompt = (
            f"I have observed the following pattern and cannot explain it:\n"
            f"{observation_summary}\n\n"
            f"My current relevant beliefs are:\n{beliefs_text}\n\n"
            f"Propose {n_hypotheses} possible explanations. Be creative — I am "
            f"looking for hypotheses to test, not confirmed facts. For each:\n"
            f"1. The hypothesis\n"
            f"2. What observation would confirm it\n"
            f"3. What observation would refute it\n"
            f"Respond in JSON: {{\"hypotheses\": [{{\"claim\": ..., \"confirms_if\": ..., \"refutes_if\": ...}}]}}"
        )
        return self.imagine(
            purpose="hypothesis_generation",
            prompt=prompt,
            beliefs_used=[b.get("id") for b in existing_beliefs if "id" in b],
        )

    def check_coherence(self, claim: dict) -> float:
        """
        Ask the LLM (low temperature) whether a structured claim is coherent.

        Used to filter hallucinated or garbled candidates before they
        enter the belief pipeline. Returns a 0.0–1.0 coherence score.
        """
        prompt = (
            f"Evaluate whether the following structured claim is coherent and internally consistent:\n"
            f"{json.dumps(claim, indent=2)}\n\n"
            f"Respond with only a JSON object: {{\"coherent\": true/false, \"score\": 0.0-1.0, \"reason\": \"...\"}}"
        )
        response = self.consult_reference(purpose="coherence_check", prompt=prompt, want_json=True)
        if response.structured and "score" in response.structured:
            return float(response.structured["score"])
        return 0.5  # Unknown — neutral prior

    # ─────────────────────────────────────────────────────────────────────────
    # Internal
    # ─────────────────────────────────────────────────────────────────────────

    def _wrap_prompt(self, prompt: str, mode: LLMMode, want_json: bool = False) -> str:
        """Add system framing appropriate for the temperature mode."""
        if mode == LLMMode.REFERENCE:
            system = (
                "You are a reference source. Provide accurate, well-established information. "
                "Express uncertainty explicitly. Do not speculate beyond established knowledge."
            )
        else:  # IMAGINATION
            system = (
                "You are a hypothesis generator. Your role is creative exploration, not confirmed fact. "
                "Generate novel possibilities for consideration. Label everything as speculative. "
                "The consumer of your output will evaluate and test your suggestions."
            )
        json_instruction = "\nIMPORTANT: Respond with valid JSON only, no surrounding text." if want_json else ""
        return f"[SYSTEM: {system}]\n\n{prompt}{json_instruction}"

    def _execute(self, query: LLMQuery) -> LLMResponse:
        """Execute the query against the backend and record provenance."""
        start = time.monotonic()
        temperature = TEMPERATURE[query.mode]

        try:
            raw_content, tokens_used = self.backend.complete(
                prompt=query.prompt,
                temperature=temperature,
                max_tokens=query.max_tokens,
                timeout=query.timeout_seconds,
            )
        except TimeoutError:
            # Return a minimal failure response — the entity handles this gracefully
            return LLMResponse(
                query=query,
                content="",
                coherence_score=0.0,
                llm_model=self.model_id,
                temperature=temperature,
                latency_ms=(time.monotonic() - start) * 1000,
            )

        latency_ms = (time.monotonic() - start) * 1000
        structured = None
        if raw_content.strip().startswith("{"):
            try:
                structured = json.loads(raw_content)
            except json.JSONDecodeError:
                pass  # Treat as plain text

        response = LLMResponse(
            query=query,
            content=raw_content,
            structured=structured,
            llm_model=self.model_id,
            temperature=temperature,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
        )

        self._log_query(query, response)
        return response

    def _log_query(self, query: LLMQuery, response: LLMResponse):
        """Record to internal log (will be flushed to NoSQL by caller)."""
        self._query_log.append({
            "mode":         query.mode.value,
            "purpose":      query.purpose,
            "beliefs_used": query.beliefs_used,
            "temperature":  response.temperature,
            "tokens":       response.tokens_used,
            "latency_ms":   response.latency_ms,
            "speculative":  response.is_speculative,
            "model":        response.llm_model,
        })

    def flush_log(self) -> list[dict]:
        """Return and clear the query log. Caller writes it to NoSQL."""
        log = self._query_log.copy()
        self._query_log.clear()
        return log


# ─────────────────────────────────────────────────────────────────────────────
# Backend protocol — swap implementations without changing the Executive Module
# ─────────────────────────────────────────────────────────────────────────────

class LLMBackend:
    """
    Abstract backend. Implement this for each LLM provider.

    Local (Ollama) and remote (API) backends both implement the same interface.
    The Executive Module never knows which is active. When the LLM is upgraded
    to a new model, only the backend changes — all calling code is stable.
    """
    def complete(self, prompt: str, temperature: float, max_tokens: int, timeout: float) -> tuple[str, int]:
        """Return (response_text, tokens_used)."""
        raise NotImplementedError


class OllamaBackend(LLMBackend):
    """Local Ollama instance (recommended for privacy and offline operation)."""
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model    = model

    def complete(self, prompt: str, temperature: float, max_tokens: int, timeout: float) -> tuple[str, int]:
        import urllib.request
        payload = json.dumps({
            "model":   self.model,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }).encode()
        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
        return result.get("response", ""), result.get("eval_count", 0)
