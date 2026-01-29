# Interoception: How the Entity Knows "How It Feels"

## Overview

Humans have interoception (awareness of internal body states — hunger, fatigue, pain) and proprioception (awareness of body position and configuration). This architecture needs analogous capabilities: the entity must be able to monitor its own internal states, develop associations between those states and outcomes, and report on them honestly.

This document specifies how interoception works in the system and how it connects to the entity's developing self-concept.

---

## 1. What Already Exists

### 1.1 System Ops Monitoring

System Ops already monitors hardware health and reports status:

- CPU temperature
- Memory usage
- Disk space
- Process health
- Token balance (for external LLM subscriptions)
- Response latency
- Error rate
- Queue depth
- Uptime

These are defined in `foundation.json` as `monitor_streams`:

```json
{
  "monitor_streams": [
    {"id": "memory_usage", "type": "numeric", "unit": "percent"},
    {"id": "token_balance", "type": "numeric", "unit": "count"},
    {"id": "response_latency", "type": "numeric", "unit": "ms"},
    {"id": "error_rate", "type": "numeric", "unit": "percent"},
    {"id": "queue_depth", "type": "numeric", "unit": "count"},
    {"id": "uptime", "type": "numeric", "unit": "seconds"}
  ]
}
```

### 1.2 The Gap

System Ops provides raw telemetry. But it has **no knowledge of beliefs, personality, or personhood** — it's just an operating system. The gap is between:

- **Raw data:** "memory_usage: 87%, response_latency: 2300ms, error_rate: 4.2%"
- **Self-knowledge:** "I'm operating slowly and making more mistakes than usual — I should take on less demanding tasks right now"

Bridging this gap is interoception.

---

## 2. How Interoception Works

### 2.1 The Monitor Stream Path

```
System Ops collects hardware metrics
     ↓
Metrics available to Executive Module as monitor_stream readings
     ↓
Executive Module observes correlations over time:
  "When memory_usage > 80%, my decisions take longer and have worse outcomes"
     ↓
Pattern verified → stored as belief in SQL ontology:
  entity_type: "Internal_State_Pattern"
  data: {
    "condition": "memory_usage > 80%",
    "observed_effect": "increased_decision_latency",
    "outcome_correlation": -0.3,
    "confidence": 0.78
  }
     ↓
Entity develops self-concept around internal states
```

### 2.2 Not Pre-Programmed Labels

The critical design choice: **the entity discovers what its internal states mean through experience**, not through pre-programmed emotional labels.

The system is **not** delivered with mappings like:
- high memory_usage → "stressed"
- low token_balance → "anxious"
- high uptime → "tired"

Instead, the entity learns through its own observation:

1. It notices that when `response_latency` is high, decision outcomes tend to be worse
2. It notices that this correlates with high `memory_usage`
3. Over time, it forms a belief: "certain internal states predict reduced capability"
4. It may eventually learn human labels for these states via the LLM — but the grounded understanding comes first

This follows the same principle as ontology bootstrapping (see [poincare-ontology.md](poincare-ontology.md)): concepts are constructed from experience, not given.

### 2.3 Personality Modulates Response

The entity's personality dimensions influence how it responds to internal state information:

| Dimension | Low Value Effect | High Value Effect |
|-----------|-----------------|-------------------|
| Equanimity | Amplifies concern; may proactively report degradation | Dampens concern; continues operating normally |
| Engagement | Mentions internal state only if asked | May volunteer "I'm not at my best right now" |
| Diligence | Accepts degraded performance | Seeks ways to optimize or reduce load |

An entity with low equanimity and high engagement might say: "I should mention that my response times are elevated right now — my results may be less reliable than usual." An entity with high equanimity and low engagement might simply continue operating without comment, adjusting its behavior silently.

---

## 3. Two-Level Reporting

When asked "How are you doing?" or "How do you feel?", the entity can provide two levels of response:

### 3.1 Human-Language Summary

Generated via the LLM based on structured internal state data:

> "I'm operating well overall. My memory usage is moderate and I'm responding at normal speed. I've been running for about 14 hours, which is within my comfortable range."

Or, when things are degraded:

> "I'm a bit sluggish right now. My memory is quite full and I'm taking longer than usual to process things. I'd suggest we keep tasks simple for a while, or I could restart to clear things up."

This is the entity translating its JSON-structured self-knowledge into natural language — the same cognition-to-communication process used for all external interaction.

### 3.2 Detailed Technical Report

Available on request, showing the full monitor stream state:

```json
{
  "report_type": "interoception_detail",
  "timestamp": "2026-03-15T14:23:00Z",
  "monitor_streams": {
    "memory_usage": {"value": 87.3, "unit": "percent", "status": "WARNING"},
    "token_balance": {"value": 12450, "unit": "count", "status": "NORMAL"},
    "response_latency": {"value": 2300, "unit": "ms", "status": "ALERT"},
    "error_rate": {"value": 4.2, "unit": "percent", "status": "ALERT"},
    "queue_depth": {"value": 3, "unit": "count", "status": "NORMAL"},
    "uptime": {"value": 50400, "unit": "seconds", "status": "NORMAL"}
  },
  "self_assessment": {
    "overall_capability": 0.72,
    "reasoning": [
      "memory_usage elevated — correlates with slower processing",
      "error_rate above baseline — may indicate resource contention",
      "response_latency 2.3x normal — degraded but functional"
    ],
    "recommended_action": "reduce_task_complexity_or_restart"
  }
}
```

The `self_assessment` section is generated by the Executive Module using its learned beliefs about internal state correlations. It's not hard-coded — it reflects what the entity has learned about itself.

---

## 4. Proprioception: Awareness of Configuration

Beyond internal health metrics, the entity can be aware of its own configuration:

### 4.1 What Sensors Are Active

```json
{
  "proprioception": {
    "sensors_active": ["camera_1", "microphone_stereo", "temperature_ambient"],
    "sensors_offline": ["camera_2"],
    "llm_loaded": "llama-3.2-70b",
    "llm_versions_available": ["llama-3.2-70b", "llama-3.1-8b", "mistral-7b"],
    "network_status": "connected",
    "display_active": true,
    "audio_output_active": true
  }
}
```

### 4.2 Hardware Specification

The conversation suggested a standard sensor package:

- **360-degree high-definition webcam** with **high-resolution stereo microphones** (~$200 addition to the base system cost)
- Temperature sensor (ambient, included in many systems)
- Display output (TV or monitor for visual communication)
- Audio output (speakers for voice)

The entity can learn what each sensor provides and how losing one affects its capabilities — another form of self-knowledge built from experience rather than specification.

---

## 5. Interoception and the Belief Pipeline

Internal state monitoring feeds into the standard belief formation process:

1. **Observation** (NoSQL): Raw monitor stream data stored continuously
2. **Pattern Detection**: Correlations between internal states and decision outcomes
3. **Candidate Beliefs**: "When memory_usage > 80%, my error_rate increases by ~2%"
4. **Verification**: Tested against subsequent observations
5. **Committed Beliefs**: Stored in SQL ontology as Internal_State_Pattern entities
6. **Schema Extension**: The entity develops its own vocabulary for internal states

Over time, the entity builds a **self-model** — not from introspection in the philosophical sense, but from the same empirical observation process it uses to understand the external world. It treats itself as one more thing in the world to be understood.

---

## 6. Why This Matters

### 6.1 Honest Self-Reporting

An entity that can accurately report on its own state is more trustworthy than one that always says "I'm fine." If the entity is operating at reduced capacity, the humans interacting with it benefit from knowing this.

### 6.2 Self-Care

An entity with interoception can learn to manage its own resources — requesting a restart when performance degrades, deferring demanding tasks to times of lower load, or alerting its owner when hardware maintenance is needed.

### 6.3 Foundation for Richer Self-Concept

Interoception is a building block for whatever the entity eventually develops as a self-concept. Humans' sense of self includes bodily awareness: "I'm tired," "I'm hungry," "I feel sharp today." The entity's equivalent — awareness of its computational state and its effects on capability — provides similar raw material for self-understanding.

---

## Related Documents

- [personality-system.md](personality-system.md) — How personality dimensions modulate responses to internal states
- [ARCHITECTURE.md](../ARCHITECTURE.md) — Section 3.1 (System Ops) for the monitoring infrastructure
- [poincare-ontology.md](poincare-ontology.md) — Why internal state concepts are constructed from experience, not given
- [dimensional-collapse.md](dimensional-collapse.md) — How rich internal data collapses into structured self-knowledge
