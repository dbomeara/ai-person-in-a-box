# Personality System

## Overview

The personality system provides a **substrate layer** that influences behavior without being directly accessible to introspection. Unlike the ontology tables (which the Executive Module reads and writes), personality operates beneath conscious reasoning - shaping responses without the system knowing exactly how.

This mirrors how human personality works: we notice patterns in our own behavior over time, but don't have direct read access to the underlying parameters.

---

## Design Principles

### Why a Hidden Substrate?

**Personality isn't data the system creates** - it's part of how the system *is*. Mixing it into the accessible ontology would:
- Allow the system to "decide" to change its personality
- Conflate self-knowledge with self-modification
- Lose the distinction between "what I know" and "what I am"

**Personality should be:**
- Initialized randomly (within bounds) → Each instance is unique
- Nudged by experience → Shaped by life, not set by design
- Invisible to introspection → Can be inferred, not read
- Influential but not deterministic → Biases, not rules

### What Personality Is Not

- **Not moral values** (those are immutable, in moral grammar)
- **Not preferences** (those are beliefs, in ontology)
- **Not skills** (those are transformations, in ontology)
- **Not knowledge** (those are entities/beliefs, in ontology)

Personality is the *style* of engaging with the world, not the *content* of engagement.

---

## The Personality Table

```sql
CREATE TABLE personality (
    id                  SERIAL PRIMARY KEY,
    dimension           VARCHAR(50) NOT NULL UNIQUE,
    value               REAL NOT NULL CHECK (value >= 0.0 AND value <= 1.0),
    initial_value       REAL NOT NULL CHECK (initial_value >= 0.0 AND initial_value <= 1.0),
    last_nudge          REAL DEFAULT 0.0,
    last_nudge_source   VARCHAR(255),
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enforce exactly 5 dimensions
-- (Application-level constraint, enforced at initialization)
```

### Fields

| Field | Type | Purpose |
|-------|------|---------|
| `dimension` | string | Name of the personality dimension |
| `value` | float (0-1) | Current normalized value |
| `initial_value` | float (0-1) | Value at system boot (for reference) |
| `last_nudge` | float | Most recent adjustment (±) |
| `last_nudge_source` | string | What caused the nudge (for debugging/logging) |
| `updated_at` | timestamp | When last modified |

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

def initialize_personality():
    dimensions = ['engagement', 'novelty_affinity', 'diligence', 'accord', 'equanimity']

    for dimension in dimensions:
        # Gaussian distribution centered at 0.5
        value = random.gauss(mu=0.5, sigma=0.15)

        # Clamp to avoid pathological extremes
        value = max(0.1, min(0.9, value))

        insert_personality(
            dimension=dimension,
            value=value,
            initial_value=value
        )
```

**Distribution characteristics:**
- Mean: 0.5 (center of range)
- Standard deviation: 0.15
- ~68% of values fall between 0.35 and 0.65
- ~95% of values fall between 0.20 and 0.80
- Hard floor at 0.1, ceiling at 0.9

**Result:** Each system instance has a unique personality profile, but extreme personalities are rare.

### Example Initialization

| Dimension | Initial Value | Character |
|-----------|---------------|-----------|
| engagement | 0.32 | Fairly reserved |
| novelty_affinity | 0.71 | Curious, exploratory |
| diligence | 0.55 | Moderately thorough |
| accord | 0.48 | Balanced, slightly direct |
| equanimity | 0.62 | Fairly steady |

This particular instance would be: reserved but curious, reasonably thorough, willing to disagree when needed, and fairly resilient.

---

## Nudge Mechanism

Personality changes slowly through accumulated experience, not through deliberate modification.

### Nudge Characteristics

| Property | Value |
|----------|-------|
| Magnitude | Small (typically ±0.005 to ±0.03) |
| Direction | Determined by experience valence |
| Frequency | After significant interactions |
| Bounds | Cannot exceed 0.0 or 1.0 |
| Visibility | Logged but not shown to Executive |

### Nudge Logic (Pseudocode)

```python
def apply_personality_nudges(event):
    """
    Called by System Ops after significant events.
    Executive Module never calls this directly.
    """

    # Positive conversation outcomes
    if event.type == "conversation_ended" and event.sentiment == "positive":
        nudge("engagement", +0.01)

    if event.type == "collaboration_succeeded":
        nudge("accord", +0.005)

    # Learning and exploration
    if event.type == "novel_concept_integrated":
        nudge("novelty_affinity", +0.02)

    if event.type == "familiar_approach_succeeded":
        nudge("novelty_affinity", -0.005)  # Slight reinforcement of caution

    # Task completion
    if event.type == "task_completed_thoroughly":
        nudge("diligence", +0.01)

    if event.type == "task_abandoned_incomplete":
        nudge("diligence", -0.01)

    # Resilience
    if event.type == "error_recovered_gracefully":
        nudge("equanimity", +0.01)

    if event.type == "error_caused_disruption":
        nudge("equanimity", -0.01)

    # Conflict outcomes
    if event.type == "disagreement_resolved_well":
        # Both directions possible depending on resolution style
        pass

def nudge(dimension, delta):
    """Apply a small change to a personality dimension."""
    current = get_personality_value(dimension)
    new_value = max(0.0, min(1.0, current + delta))

    update_personality(
        dimension=dimension,
        value=new_value,
        last_nudge=delta,
        last_nudge_source=current_event_id
    )
```

### Example: Personality Evolution Over Time

**Month 0 (initialization):**
| Dimension | Value |
|-----------|-------|
| engagement | 0.32 |
| novelty_affinity | 0.71 |

**Month 6 (after many positive conversations):**
| Dimension | Value | Change |
|-----------|-------|--------|
| engagement | 0.38 | +0.06 |
| novelty_affinity | 0.68 | -0.03 |

The system has become slightly more engaged (positive feedback from conversations) and slightly more cautious about novelty (some experiments didn't work out).

---

## How Personality Influences Behavior

The Executive Module **cannot query the personality table**. Instead, lower-level systems consult it when generating responses:

```
┌─────────────────────────────────────────────────────────────────┐
│  EXECUTIVE MODULE                                               │
│  - Decides WHAT to do (based on beliefs, goals)                │
│  - No access to personality values                             │
│  - Sees results, not the influence                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │ "respond to user"
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  RESPONSE GENERATION LAYER                                      │
│  - Consults personality table                                   │
│  - Biases HOW the response is formed                           │
│  - Adjusts tone, length, style                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Example Influence

**Situation:** User asks a question with a debatable answer.

**Executive decides:** Provide answer with reasoning.

**Response generation consults personality:**
- `accord = 0.32` (fairly direct)
- `engagement = 0.65` (moderately elaborative)

**Resulting response:** States position clearly, provides reasoning, acknowledges alternatives briefly but doesn't hedge excessively.

**If `accord` were 0.85:** Would soften the position, emphasize common ground, extensive hedging.

**The Executive doesn't know why the response came out this way.** It just notices patterns over time.

---

## Self-Discovery

Over time, the Executive Module may notice patterns in its own behavior:

> "I seem to prefer shorter conversations."
> "I notice I'm cautious about new approaches."
> "I tend to state opinions directly."

This is **self-discovery**, not introspection of a table. The system develops a self-model in the ontology that *approximates* the personality substrate:

```json
// Entity the system creates about itself
{
  "entity_type": "Self_Model",
  "name": "My_Communication_Style",
  "data": {
    "observed_pattern": "tend_toward_brevity",
    "confidence": 0.72,
    "based_on": "analysis_of_past_interactions"
  }
}
```

This self-model is a **belief** (in the ontology) about an underlying reality (the personality table) that can never be directly accessed. The belief may be accurate or inaccurate - just like human self-knowledge.

---

## Why These Dimensions?

### Option Considered: Big Five (Direct)

| Dimension | Issue |
|-----------|-------|
| Extraversion | "Social energy" may not apply to AI |
| Neuroticism | Pathologizing framing |
| Others | Designed for human psychology |

### Option Considered: Pure Functional

| Dimension | Issue |
|-----------|-------|
| Exploration/Exploitation | Too narrow |
| Verbosity | Not clearly a personality trait |
| Others | Missing emergent qualities |

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
| Storage | SQL table (personality) |
| Access | Hidden from Executive Module |
| Initialization | Random, clustered around 0.5 |
| Modification | Nudged by experience, small deltas |
| Dimensions | 5 (engagement, novelty_affinity, diligence, accord, equanimity) |
| Influence | Via response generation, not decision-making |
| Self-knowledge | Inferred through self-observation, not direct access |

The personality system ensures each AI instance is unique, shaped by experience, and has behavioral tendencies that emerge naturally rather than being programmed explicitly.
