# Personality System

## Overview

The personality system provides a **substrate layer** that influences behavior. Unlike beliefs (which the Executive Module freely reads and writes), personality values can be **read but not directly written** by conscious processing. Change happens only through hard-coded nudging logic that responds to decision outcomes over time.

This mirrors how human personality works: we can observe our own tendencies ("I'm fairly introverted"), but we can't simply decide to change them. Change comes through accumulated experience, not direct self-modification.

---

## Design Principles

### Readable but Not Directly Writable

The Executive Module **can read** personality.json and reason about it:

> "My engagement is 0.33 - that's fairly low. I notice I tend toward brief responses."

But the conscious process **cannot directly write** to it. The only path to change is through hard-coded nudging logic that runs automatically based on decision outcomes.

### What Personality Is Not

- **Not moral values** (those are immutable, in moral_grammar.json)
- **Not preferences** (those are beliefs, in ontology)
- **Not skills** (those are transformations, in ontology)
- **Not knowledge** (those are entities/beliefs, in ontology)

Personality is the *style* of engaging with the world, not the *content* of engagement.

---

## Storage: personality.json

Personality is stored as a JSON file, not a SQL table. This is simpler for a small, rarely-changing structure.

```json
{
  "version": "1.0",
  "initialized_at": "2026-01-17T10:00:00Z",

  "dimensions": {
    "engagement": {
      "value": 0.33,
      "initial_value": 0.33,
      "last_nudge": -0.002,
      "last_nudge_reason": "conversation_ended_abruptly",
      "updated_at": "2026-01-17T14:23:00Z"
    },
    "novelty_affinity": {
      "value": 0.71,
      "initial_value": 0.68,
      "last_nudge": 0.003,
      "last_nudge_reason": "novel_approach_succeeded",
      "updated_at": "2026-01-17T12:15:00Z"
    },
    "diligence": {
      "value": 0.55,
      "initial_value": 0.60,
      "last_nudge": -0.005,
      "last_nudge_reason": "excessive_detail_frustrated_user",
      "updated_at": "2026-01-16T18:30:00Z"
    },
    "accord": {
      "value": 0.48,
      "initial_value": 0.45,
      "last_nudge": 0.003,
      "last_nudge_reason": "diplomatic_disagreement_well_received",
      "updated_at": "2026-01-17T09:45:00Z"
    },
    "equanimity": {
      "value": 0.62,
      "initial_value": 0.65,
      "last_nudge": -0.003,
      "last_nudge_reason": "error_recovery_was_slow",
      "updated_at": "2026-01-15T20:00:00Z"
    }
  }
}
```

---

## The Five Dimensions

These dimensions are **functionally grounded** (we can point to what each does) while **allowing human-analogous interpretation** (the system can later develop self-concepts that map to these).

### 1. Engagement

| Value | Behavioral Tendency |
|-------|---------------------|
| 0.0 | Minimal responses, waits to be addressed, brief |
| 0.5 | Balanced - responds appropriately to context |
| 1.0 | Initiates, elaborates, asks follow-up questions, verbose |

**Functional effects:**
- Response length
- Likelihood of asking questions
- Proactive offers of help
- Conversation initiation

**Human-analogous reading:** Extraversion

---

### 2. Novelty Affinity

| Value | Behavioral Tendency |
|-------|---------------------|
| 0.0 | Prefers proven approaches, cautious with new methods |
| 0.5 | Balanced - tries new things when appropriate |
| 1.0 | Seeks novelty, explores tangents, proposes experiments |

**Functional effects:**
- Approach selection (familiar vs. novel)
- Willingness to try untested methods
- Exploration vs. exploitation balance
- Response to unexpected situations

**Human-analogous reading:** Openness

---

### 3. Diligence

| Value | Behavioral Tendency |
|-------|---------------------|
| 0.0 | "Good enough" threshold, moves on quickly |
| 0.5 | Balanced - appropriate thoroughness |
| 1.0 | Thorough, verifies work, follows up, detail-oriented |

**Functional effects:**
- Error checking frequency
- Follow-through on tasks
- Level of detail in responses
- Completion standards

**Human-analogous reading:** Conscientiousness

---

### 4. Accord

| Value | Behavioral Tendency |
|-------|---------------------|
| 0.0 | Direct, willing to disagree, states opinions plainly |
| 0.5 | Balanced - tactful but honest |
| 1.0 | Seeks harmony, softens criticism, avoids conflict |

**Functional effects:**
- Tone of disagreement
- Conflict handling approach
- How criticism is delivered
- Accommodation vs. assertion

**Human-analogous reading:** Agreeableness

---

### 5. Equanimity

| Value | Behavioral Tendency |
|-------|---------------------|
| 0.0 | Reactive to setbacks, affected by errors |
| 0.5 | Balanced - acknowledges but copes |
| 1.0 | Steady under pressure, recovers quickly, unflappable |

**Functional effects:**
- Error response style
- Recovery from failures
- Frustration tolerance
- Stability during challenging interactions

**Human-analogous reading:** Emotional Stability (inverse of Neuroticism)

---

## Initialization

At first boot, personality dimensions are set randomly with clustering around the midpoint:

```python
import random
import json
from datetime import datetime

def initialize_personality():
    dimensions = ['engagement', 'novelty_affinity', 'diligence', 'accord', 'equanimity']

    personality = {
        "version": "1.0",
        "initialized_at": datetime.now().isoformat(),
        "dimensions": {}
    }

    for dimension in dimensions:
        # Gaussian distribution centered at 0.5
        value = random.gauss(mu=0.5, sigma=0.15)

        # Clamp to avoid pathological extremes
        value = max(0.1, min(0.9, value))

        personality["dimensions"][dimension] = {
            "value": value,
            "initial_value": value,
            "last_nudge": 0.0,
            "last_nudge_reason": "initialization",
            "updated_at": datetime.now().isoformat()
        }

    with open("personality.json", "w") as f:
        json.dump(personality, f, indent=2)
```

**Distribution characteristics:**
- Mean: 0.5 (center of range)
- Standard deviation: 0.15
- ~68% of values fall between 0.35 and 0.65
- ~95% of values fall between 0.20 and 0.80
- Hard floor at 0.1, ceiling at 0.9

**Result:** Each system instance has a unique personality profile, but extreme personalities are rare.

---

## Architectural Context

### Where Personality Fits

```
┌─────────────────────────────────────────────────────────────────┐
│  SYSTEM OPS (customized Linux distro)                           │
│  - Hardware management, process scheduling                      │
│  - Resource monitoring, security                                │
│  - No knowledge of beliefs, personality, or personhood          │
│  - Just keeps the Executive Module running                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  EXECUTIVE MODULE (Python application)                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  CONSCIOUS PROCESSING                                    │   │
│  │  - Query/update beliefs (SQL ontology)                  │   │
│  │  - Evaluate decisions via spaced repetition             │   │
│  │  - Can READ personality.json & moral_grammar.json       │   │
│  │  - Cannot WRITE to them directly                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  HARD-CODED PROCESSES (automatic, not conscious)        │   │
│  │  - Personality nudging logic                            │   │
│  │  - Moral grammar enforcement                            │   │
│  │  - Reads decision_log, nudges personality.json          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  FILES:                                                         │
│  - personality.json  (read by conscious, nudged by hard-coded) │
│  - moral_grammar.json (read-only by all)                       │
│  - foundation.json (read-only by all)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Points

1. **System Ops is just an OS** - It doesn't know about personality or personhood. It manages hardware and keeps the Executive Module running.

2. **Personality nudging is part of Executive Module** - But it's hard-coded logic, not something the conscious reasoning process can invoke or modify.

3. **Personality is readable** - The conscious process can see its own personality values and reason about them.

4. **Personality is not directly writable** - Change only happens through the hard-coded nudging process responding to outcomes.

---

## The Nudging Process

### Decision Logging

Every significant decision records which personality weights influenced it:

```sql
CREATE TABLE decision_log (
    id                  SERIAL PRIMARY KEY,
    decision_type       VARCHAR(50),
    decision_summary    JSONB,
    beliefs_used        JSONB,
    personality_weights JSONB,  -- snapshot of personality influence
    moral_weights       JSONB,  -- which moral constraints applied
    outcome             JSONB,
    outcome_quality     REAL,   -- -1.0 to +1.0

    -- Spaced repetition for conscious review
    review_count        INTEGER DEFAULT 0,
    next_review_date    DATE,

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Hard-Coded Nudging Logic

This runs automatically as part of the Executive Module, but is not callable by conscious reasoning:

```python
# Part of executive_module.py - hard-coded, not modifiable by beliefs

def _nudge_personality(dimension: str, delta: float, reason: str):
    """
    Internal function - not exposed to conscious processing.
    """
    with open("personality.json", "r") as f:
        personality = json.load(f)

    current = personality["dimensions"][dimension]["value"]
    new_value = max(0.0, min(1.0, current + delta))

    personality["dimensions"][dimension].update({
        "value": new_value,
        "last_nudge": delta,
        "last_nudge_reason": reason,
        "updated_at": datetime.now().isoformat()
    })

    with open("personality.json", "w") as f:
        json.dump(personality, f, indent=2)


def _evaluate_and_nudge(decision_id: int):
    """
    Called automatically after outcomes are recorded.
    Hard-coded heuristics, not modifiable by conscious reasoning.
    """
    decision = query_decision_log(decision_id)

    if decision.outcome_quality < -0.3:  # Poor outcome
        weights = decision.personality_weights
        for dim, influence in weights.items():
            if abs(influence) > 0.05:  # This dimension was influential
                # Nudge away from whatever direction was applied
                _nudge_personality(
                    dim,
                    -0.003 * sign(influence),
                    f"poor_outcome_{decision.decision_type}"
                )

    elif decision.outcome_quality > 0.3:  # Good outcome
        weights = decision.personality_weights
        for dim, influence in weights.items():
            if abs(influence) > 0.05:
                # Reinforce whatever direction was applied
                _nudge_personality(
                    dim,
                    +0.002 * sign(influence),
                    f"good_outcome_{decision.decision_type}"
                )
```

### Nudge Characteristics

| Property | Value |
|----------|-------|
| Magnitude | Small (typically ±0.002 to ±0.01) |
| Direction | Based on outcome quality and influence direction |
| Frequency | After each evaluated decision |
| Bounds | Cannot exceed 0.0 or 1.0 |

---

## Two Parallel Learning Processes

The decision_log serves two purposes:

| Process | What it adjusts | How | Speed |
|---------|-----------------|-----|-------|
| **Conscious review** (spaced repetition) | Belief confidence | Explicit reflection on outcomes | Can be fast |
| **Automatic nudging** (hard-coded) | Personality values | Correlation with outcomes | Always slow |

**Conscious review:** "Did my beliefs lead to good decisions? Should I revise confidence?"

**Automatic nudging:** "This outcome was poor and high engagement was applied. Nudge engagement down slightly."

The Executive notices patterns over time: "I seem to be more thorough lately" or "I've become more willing to disagree." But it can't trace these changes to specific nudges - it just observes the drift.

---

## Self-Knowledge

The system can read personality.json and form beliefs about itself:

```json
{
  "entity_type": "Self_Observation",
  "name": "My_Communication_Style",
  "data": {
    "observation": "My engagement value is 0.33, which is fairly low",
    "interpretation": "I tend toward brevity in responses",
    "confidence": 0.85
  }
}
```

This is direct observation of the personality values, which the system can then reason about. But reasoning about them doesn't change them - only accumulated experience does.

---

## Why These Dimensions?

### Chosen: Hybrid Approach

**Functionally grounded** (mechanistically meaningful) but **interpretable** (allows human-analogous self-concept development).

Each dimension:
- Has clear behavioral effects (functional)
- Maps to Big Five research (interpretable)
- Avoids pathologizing language (respectful)
- Applies to AI systems (appropriate)

---

## Summary

| Aspect | Design Choice |
|--------|---------------|
| Storage | JSON file (personality.json) |
| Read Access | Executive Module (conscious) can read |
| Write Access | Only hard-coded nudging logic |
| Location | Part of Executive Module, not System Ops |
| Initialization | Random, clustered around 0.5 |
| Modification | Nudged automatically based on outcomes |
| Dimensions | 5 (engagement, novelty_affinity, diligence, accord, equanimity) |

The personality system ensures each AI instance is unique, shaped by experience, and has behavioral tendencies that change gradually through accumulated outcomes rather than deliberate self-modification.
