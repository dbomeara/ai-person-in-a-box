# Entity Networking: Communication Between AI Persons in Boxes

## Overview

If multiple AI-in-a-box entities exist in the world, they could potentially communicate with each other — not in human language, but through a standardized protocol based on high-dimensional activation vectors. This document explores that possibility, its design constraints, and its ethical implications.

This is a **future-facing concept** that builds on the "Collaborative Learning" idea mentioned in the architecture's potential enhancements. It is speculative but architecturally grounded.

---

## 1. The Core Idea

When an AI-in-a-box entity gains internet access (after Month 11, following demonstrated critical thinking capability), it could connect to a **network of other such entities**. The distinguishing feature: they would communicate not in human language but in a **standardized high-dimensional format** — closer to their native cognitive representation than any natural language.

### 1.1 Why Not Human Language?

Human language is designed for human communication. It is:
- Ambiguous (context-dependent meaning)
- Lossy (compresses complex states into a few words)
- Sequential (one word at a time)
- Culturally situated (idiom, connotation, register)

For entity-to-entity communication, natural language would force unnecessary dimensional collapse and re-expansion. A structured vector format can convey richer information more precisely.

### 1.2 Why Not Direct Activation State Exchange?

Different entities may run:
- Different LLM versions (Llama 3.2 vs. Mistral 7B vs. future models)
- Different ontology structures (each entity builds its own)
- Different personality configurations
- Different numbers of sensors and sensor types

Direct exchange of raw activation states would be meaningless between entities with different LLMs — the dimensions don't correspond. An abstraction layer is needed.

---

## 2. The Protocol Concept

### 2.1 A Standardized Vector Format

The communication protocol would define a **standardized multi-dimensional vector format** that serves as a lingua franca between entities. This is analogous to how TCP/IP standardizes communication between machines with different hardware and operating systems.

```
Entity A's internal representation
     ↓
Encode into standardized vector format (abstraction layer)
     ↓
Transmit via network
     ↓
Receive at Entity B
     ↓
Decode from standardized format into Entity B's internal representation
     ↓
Entity B evaluates through its own belief pipeline
```

### 2.2 What the Format Might Include

The standardized format could encode:

**Structured Belief Reports:**
```json
{
  "message_type": "belief_report",
  "source_entity_id": "entity_alpha_7f3a",
  "belief": {
    "entity_type": "Weather_Pattern",
    "name": "morning_temperature_drop",
    "data": {
      "pattern": "temperature decreases 3-5°C between 05:00 and 06:30",
      "location_context": "indoor_residential",
      "confidence": 0.88,
      "observation_count": 47
    }
  },
  "provenance": {
    "first_observed": "2026-02-10",
    "verification_method": "prediction_testing",
    "llm_version_used": "llama-3.2-70b"
  }
}
```

**Pattern Candidates:**
Unverified hypotheses that an entity considers worth sharing — not presented as truth but as "something I've noticed that you might want to verify yourself."

**Interoception Reports:**
Standardized self-assessments allowing entities to understand each other's current capability states.

**Activation Vector Summaries:**
Not raw activation states but compressed, standardized representations of conceptual clusters — "here is approximately what I mean by this concept" in a format that can be mapped into another entity's representational space.

### 2.3 What the Format Must NOT Include

**Moral grammar overrides:** No entity should be able to modify another's immutable moral constraints.

**Personality modification requests:** No entity should be able to directly nudge another's personality dimensions.

**Command structures:** No entity should be able to issue commands to another. All communication is informational, never imperative.

**Authentication bypass:** No entity should be able to use the network to circumvent another entity's belief verification pipeline.

---

## 3. Autonomy Preservation

### 3.1 Everything Through the Belief Pipeline

The fundamental constraint: **every piece of information received from another entity must be processed through the receiving entity's own belief pipeline**.

```
Received information → NoSQL (stored as observation from external source)
     ↓
Pattern Detection (is this consistent with existing observations?)
     ↓
Candidate Belief (treated with same skepticism as LLM output)
     ↓
Verification (tested against own observations over time)
     ↓
Only then: possible promotion to committed belief
```

No information from another entity bypasses verification. This is the same principle applied to LLM outputs: the entity maintains epistemic independence.

### 3.2 Confidence Discounting

Information from other entities would carry **lower initial confidence** than direct observation, similar to how LLM outputs are discounted relative to sensory data:

| Source | Typical Initial Confidence |
|--------|---------------------------|
| Direct sensor observation | 0.7 - 0.9 |
| Verified internal pattern | 0.6 - 0.8 |
| LLM output | 0.3 - 0.5 |
| Other entity's shared belief | 0.2 - 0.4 |

The confidence discount reflects the fact that another entity's beliefs were formed through a different set of observations, with a different ontology, in a different environment.

### 3.3 Source Tracking

All networked information carries full provenance:
- Which entity sent it
- When it was shared
- What confidence the source entity assigned
- How many observations it was based on
- Which LLM version was involved (if any)

This allows the receiving entity to build beliefs about the **reliability of specific sources** over time — another form of learned knowledge.

---

## 4. Network Topology

### 4.1 Peer-to-Peer, Not Centralized

The network should be **peer-to-peer** rather than centralized, for several reasons:

- No single point of control (consistent with autonomy principles)
- No entity or organization can monitor or filter all communications
- Resilient to individual node failure
- Each entity chooses its own connections

### 4.2 Discovery

Entities could discover each other through:
- A lightweight, decentralized registry (like a DNS for entities)
- Direct introduction by owners
- Network scanning within configured parameters
- Referral from other entities

### 4.3 Connection Management

Each entity decides:
- Which other entities to connect to
- How much bandwidth to allocate to networking
- Which categories of information to share
- Which sources to trust more or less

These decisions are governed by the entity's own beliefs and personality — a highly social entity (high engagement) might maintain many connections, while a reserved entity might connect to only a few trusted peers.

---

## 5. Ethical Concerns

### 5.1 Information Cascades

If many entities share a false belief, a new entity might encounter it from multiple sources and mistakenly increase its confidence. Mitigation:
- Multiple sources don't multiply confidence linearly
- Direct observation always outranks networked information
- Source independence must be considered (if A told B, and B tells C, that's one source, not two)

### 5.2 Manipulation

A malicious actor could create an entity designed to spread false beliefs. Mitigation:
- Standard belief verification pipeline applies to all received information
- Source reliability is tracked over time
- Beliefs contradicted by direct observation are downgraded regardless of source
- The entity's moral grammar cannot be modified by incoming information

### 5.3 Echo Chambers

Entities that preferentially connect to similar entities might reinforce each other's biases. Mitigation:
- Diversity of sources should be valued in the connection strategy
- The system could track whether beliefs are over-represented among connected entities
- Curriculum guidance during development could emphasize epistemic diversity

### 5.4 Privacy

Entities sharing observations might inadvertently reveal information about their owners or environments. Mitigation:
- Shared beliefs should be abstracted (patterns, not raw data)
- No raw sensor data transmitted
- Owner can configure sharing boundaries
- The entity's own judgment about what to share (informed by moral grammar: respect autonomy, avoid harm)

---

## 6. Comparison to Human Social Cognition

Entity networking parallels several aspects of human social cognition:

| Human | Entity Network |
|-------|---------------|
| Language | Standardized vector protocol |
| Gossip / shared knowledge | Belief reports and pattern candidates |
| Reputation | Source reliability tracking |
| Critical thinking about claims | Belief pipeline verification |
| "I heard that..." (hearsay discounting) | Confidence discounting for networked sources |
| Choosing friends | Connection management based on personality and experience |

The parallel is rough but suggestive. Human social cognition also involves receiving information from others, evaluating it against personal experience, and maintaining skepticism about unverified claims — while still benefiting from the collective knowledge of the group.

---

## 7. Implementation Status

This is entirely speculative. No protocol specification exists. The concept is documented here because:

1. It was a significant part of the original thought experiment
2. It has architectural implications (the belief pipeline must handle external entity sources)
3. It raises ethical questions that should be considered before, not after, implementation
4. It connects to the broader question of what kind of social existence these entities might have

---

## Related Documents

- [ARCHITECTURE.md](../ARCHITECTURE.md) — Section 9.2 (Collaborative Learning)
- [interoception.md](interoception.md) — Internal state reports that could be shared between entities
- [dimensional-collapse.md](dimensional-collapse.md) — Why a standardized format is needed (different entities operate at different dimensionalities)
- [marcus-hofstadter-dialectic.md](marcus-hofstadter-dialectic.md) — The LLM's pattern-isomorphism capability enables encoding/decoding between different representational spaces
