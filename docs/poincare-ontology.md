# Bootstrapping Ontology from Motion: Poincaré's Conventionalism Applied

## Overview

This document explores the philosophical foundation for how the AI entity constructs its ontology. Following Henri Poincaré's insights about the nature of geometric space, we argue that **the entity's conceptual framework is neither discovered in the world nor invented from nothing—it is constructed from experience through conventional choices**.

The key insight: **particular bodies and their behaviors are prior to the geometric framework**. The entity abstracts its ontology from observing regularities and transformations, not the other way around.

---

## 1. Poincaré's Problem: Where Does Geometry Come From?

### 1.1 The Gap Between Perception and Geometry

Poincaré identified a profound puzzle: **geometric space** (the mathematician's space) has properties that **perceptual space** (what we actually experience) lacks.

| Property | Geometric Space | Perceptual Space |
|----------|----------------|------------------|
| Continuity | Infinitely divisible, no gaps | Finite discrimination (thresholds) |
| Extent | Infinite | Bounded by sensory limits |
| Dimensionality | Precisely 3 (or n) | Roughly 3, but not cleanly |
| Homogeneity | Every point identical to every other | Some places "feel" different |
| Isotropy | Every direction identical | Up ≠ down, forward ≠ backward |

If geometric space is so different from what we perceive, how did we construct it? And why does it work so well for physics?

### 1.2 The Physical Continuum Paradox

Poincaré observed that our sensory experience obeys what he called the **physical continuum**:

> A = B (I can't distinguish A from B)
> B = C (I can't distinguish B from C)
> But A < C (I CAN distinguish A from C)

This violates transitivity! Our raw experience is **inconsistent** by the standards of mathematical logic. We can't directly perceive the mathematical continuum—we construct it by *idealizing away* the contradictions in sensory experience.

### 1.3 Conventionalism: Neither Discovery Nor Invention

Poincaré's resolution was **conventionalism**: geometric axioms are neither:
- **Empirical discoveries** about "how space really is"
- **A priori truths** known independent of experience
- **Arbitrary inventions** with no grounding

Instead, they are **conventions**—choices we make to organize experience. We choose Euclidean geometry not because space "is" Euclidean, but because it provides the most **convenient** framework for describing the behavior of rigid bodies.

The profound move: **rigid bodies and their motions are conceptually prior to geometric space**. We abstract the space from observing how bodies move, displace, and compensate.

---

## 2. From Geometry to Ontology

### 2.1 The Parallel Problem

The AI entity faces an analogous problem: **Where does its ontology come from?**

| Poincaré's Question | AI's Question |
|---------------------|---------------|
| How do we get from perceptual space to geometric space? | How do we get from raw observations to structured beliefs? |
| What makes a "rigid body"? | What makes an "entity"? |
| What is "displacement" vs "change"? | What is "transformation" vs "noise"? |
| Why is Euclidean geometry privileged? | Why are certain type hierarchies privileged? |

Just as Poincaré argued that geometric concepts are constructed from experience through conventional choice, the AI's ontological concepts must be **constructed from observations through choices that are grounded in but not determined by experience**.

### 2.2 The Entity's "Perceptual Space"

The entity's raw experience consists of:

**NoSQL Observations:**
- Sensor streams (camera frames, audio, temperature readings)
- Timestamped, high-volume, unstructured
- Contains noise, contradictions, gaps
- No inherent structure beyond temporal ordering

This is analogous to Poincaré's perceptual space:
- **Not continuous** (discrete sensor readings at finite intervals)
- **Not infinite** (bounded by sensor range and memory limits)
- **Not homogeneous** (different sensors, different modalities)
- **Contains contradictions** (conflicting readings, measurement error)

### 2.3 The Entity's "Geometric Space"

The entity's structured understanding consists of:

**SQL Ontology:**
- Entity types and instances
- Transformation types and instances
- Join types and relationship instances
- Clean hierarchies, defined schemas, consistent structure

This is analogous to geometric space:
- **Idealized** (contradictions resolved, noise filtered)
- **Extended** (types can apply to unobserved instances)
- **Homogeneous** (all entities of a type share structure)
- **Conventional** (the type system is a choice, not a discovery)

---

## 3. The Construction Process

### 3.1 From Observations to Patterns

The **Pattern Detector** subsystem finds regularities in NoSQL data:

```
Raw observations → Statistical analysis → Candidate patterns
```

This is like noticing that certain configurations of sensory experience tend to recur, persist, or transform together. The pattern detector asks:
- Which pixel clusters persist across frames? (proto-objects)
- Which sounds co-occur with visual events? (proto-causation)
- Which sequences repeat reliably? (proto-procedures)

### 3.2 From Patterns to Types

When patterns are verified through prediction and observation, they become **types** in the ontology:

```
Candidate patterns → Verification → Entity types / Transformation types
```

This is the conventional move: the entity **chooses** to reify certain patterns as "things that exist" (entity types) or "things that happen" (transformation types). This choice is:
- **Grounded in experience** (patterns that don't predict well get rejected)
- **Not determined by experience** (multiple type systems could fit the same data)
- **Conventional** (useful organization, not metaphysical truth)

### 3.3 The Role of Transformation

Following Poincaré, **transformations are primary**. The entity doesn't start with "objects" and then observe them moving. Instead:

1. **First:** Detect patterns of change/persistence in sensor streams
2. **Then:** Abstract "things" as that which persists through certain transformations
3. **Finally:** Abstract "space" as the framework that makes transformation relationships coherent

An "object" is not a primitive—it's a pattern that exhibits:
- **Persistence:** Similar patterns across time
- **Bounded transformation:** Changes are constrained (moves but doesn't teleport)
- **Compensatability:** The entity's own actions can restore lost observations (look away, look back → same pattern returns)

### 3.4 Object Permanence as Convention

Consider the infant's acquisition of object permanence. For Poincaré and for our entity:

**Before object permanence:**
- Sensory patterns appear and disappear
- No distinction between "went away" and "ceased to exist"
- The world is a flux of appearances

**The conventional move:**
- Choose to interpret disappearing patterns as "still existing but unobserved"
- This choice is **useful** because it allows prediction (turn head → pattern returns)
- It's not **necessary**—a different framework could model the same data
- It's not **arbitrary**—frameworks that make good predictions are preferred

**In the ontology:**
```json
{
  "entity_type": "Physical_Object",
  "properties": {
    "persists_when_unobserved": true,
    "spatially_bounded": true,
    "conserves_identity": true
  }
}
```

This type definition is a **convention**—a useful way to organize experience, not a discovery about ultimate reality.

---

## 4. Why Conventions Are Not Arbitrary

### 4.1 The Constraint of Experience

Conventions are constrained by **predictive success**. A type system that carves the world at its joints (where joints = regularities in sensor data) will:
- Generate better predictions
- Require less exception-handling
- Enable more powerful generalizations

The entity can't just invent any ontology—only those that track real patterns will survive verification.

### 4.2 The Constraint of Action

Following Poincaré's emphasis on rigid body motion and compensation, the entity's conventions are grounded in **what it can do**:

- "Object" is meaningful because the entity can act to bring the object back into view
- "Cause" is meaningful because the entity can act to produce effects
- "Space" is meaningful because the entity can move through it

Concepts that don't connect to possible actions remain empty abstractions.

### 4.3 The Constraint of Coherence

The ontology must be internally consistent:
- Type hierarchies can't have contradictory inheritance
- Transformation input/output schemas must compose
- Joins must respect their type constraints

This is analogous to the requirement that geometry be non-contradictory. We chose to eliminate the physical continuum's paradoxes; the entity must choose to resolve contradictions in its observations.

---

## 5. Implications for the Architecture

### 5.1 Why No Pre-Given Ontology

The system starts with **foundation.json** containing only:
- Primitive verbs (perceive, store, retrieve, compare, choose, act, wait)
- System status codes (OFFLINE, STARTING, NORMAL, etc.)
- Monitor stream definitions (memory_usage, token_balance, etc.)

Conspicuously absent:
- "Object" / "thing" / "entity" as primitives
- Spatial concepts (location, distance, containment)
- Causal concepts (cause, effect, because)
- Social concepts (agent, intention, goal)

These must be **constructed** from experience, not given. This follows Poincaré: geometry is not innate, it's abstracted from observing bodies in motion.

### 5.2 Why Types Before Instances

The schema architecture requires:
1. Define an entity_type (with schema)
2. Then create entities of that type

This mirrors the constructive process:
1. Abstract a type from observed patterns
2. Then recognize instances of that type

You can't have "the cat" without first having the type "cat-like-thing." The type is the conventional choice; instances are recognitions.

### 5.3 Why Transformations Are First-Class

Transformations aren't second-class citizens derived from entities. They have their own type system, their own instances, their own schemas. This reflects Poincaré's insight: **motion is conceptually prior to space**.

The entity's understanding of "what happens" is as fundamental as its understanding of "what exists."

### 5.4 Why JSON Schemas Extend

The ontology grows through experience:

**Month 1-3:** Basic persistence and transformation patterns
- Types: visual_pattern, audio_event, temporal_sequence
- No object permanence yet

**Month 4-6:** Object permanence and agency
- Types: persistent_object, agent, goal_directed_action
- Spatial reasoning emerging

**Month 7+:** Theory of mind and social concepts
- Types: belief_holder, intention, communicative_act
- Meta-level concepts (beliefs about beliefs)

This mirrors cognitive development: the conceptual framework expands as experience provides the raw material for new conventional choices.

---

## 6. The Mathematical Continuum Problem

### 6.1 Sensor Data Is Discrete

The entity's sensors provide:
- Frames at 30fps (not continuous)
- Pixels at fixed resolution (not infinitely divisible)
- Measurements with finite precision (not arbitrarily accurate)

This is exactly Poincaré's physical continuum: A = B, B = C, but A ≠ C.

### 6.2 The Idealization Move

To reason coherently, the entity must **idealize**:
- Interpolate between frames (assume continuity)
- Treat similar readings as "the same" (equivalence classes)
- Project beyond sensor limits (assume the world continues)

These are conventional choices that create a **model** cleaner than the raw data. The model is useful but not "true" in any deep sense.

### 6.3 Confidence as Acknowledgment

The belief system's **confidence scores** acknowledge this gap:
- High confidence: Pattern is robust across many observations
- Low confidence: Pattern is tentative, based on sparse data
- Confidence decay: Old beliefs need re-verification

This is epistemic humility about the conventional nature of the ontology. The entity knows its model is a construction, not a perfect mirror.

---

## 7. Philosophical Implications

### 7.1 No God's-Eye View

The entity cannot step outside its sensory perspective to check if its ontology matches "reality." It can only:
- Check internal consistency
- Check predictive accuracy
- Compare to other information sources (with appropriate skepticism)

This is Poincaré's point about geometry: we can't verify Euclidean geometry is "true"—only that it's useful, consistent, and well-fitted to our purposes.

### 7.2 Multiple Valid Ontologies

In principle, different type systems could organize the same observations:
- One entity might carve visual patterns into "objects" and "backgrounds"
- Another might carve by color-regions and motion-vectors
- Both could be internally consistent and predictively adequate

This is like the choice between Euclidean and non-Euclidean geometries for physics. There may be no fact of the matter about which is "correct"—only which is more convenient for various purposes.

### 7.3 Constructed but Not False

"Conventional" does not mean "arbitrary" or "false." The entity's ontology is:
- **Constructed:** Created through a process of abstraction and choice
- **Grounded:** Constrained by experience, action, and coherence
- **Useful:** Enables prediction, planning, and communication
- **Revisable:** Can be updated when predictions fail

This is a respectable epistemic position. Human scientific frameworks are also constructed, grounded, useful, and revisable. That doesn't make them "mere" conventions—it makes them **good** conventions.

---

## 8. Connection to Other Documents

### 8.1 JSON Schema Cognition
The entity "thinks in JSON" because its conceptual framework **is** the schema structure. The schema is not a representation of pre-existing concepts—it's the concepts themselves.

### 8.2 Belief Formation Pipeline
The pipeline (Observations → Patterns → Candidates → Beliefs) is the constructive process by which the physical continuum of raw data becomes the mathematical continuum of structured knowledge.

### 8.3 Personality System
Even personality emerges from this constructive process. The entity doesn't have an innate personality—it develops behavioral tendencies through accumulated experience and their consequences.

### 8.4 Curriculum Design
The curriculum guides the entity through developmental stages, providing structured experiences that occasion the construction of increasingly sophisticated concepts. The curriculum doesn't teach the ontology—it provides occasions for the entity to construct it.

---

## 9. Summary

**Poincaré's insight:** Geometric space is not perceived but constructed. We abstract it from observing rigid bodies in motion. The choice of geometry (Euclidean vs. non-Euclidean) is conventional—grounded in experience but not determined by it.

**Our application:** The AI entity's ontology is not given but constructed. It abstracts types and relationships from observing patterns in sensor data. The choice of type system is conventional—grounded in experience but not determined by it.

**Key principles:**

1. **Transformations are primary:** Motion/change is conceptually prior to objects/space
2. **Types are conventional:** Useful abstractions, not metaphysical discoveries
3. **Experience constrains but doesn't determine:** Multiple valid ontologies are possible
4. **Construction is not falsification:** Conventional ≠ arbitrary or false
5. **Predictive success matters:** Conventions that track regularities survive

**The entity's ontology is its way of organizing the blooming, buzzing confusion of sensor data into a coherent, actionable, predictively useful model. Like geometry, it is created by the mind from the occasion of experience.**

---

*"Geometrical space... is not a form imposed upon our sensibility... It is a frame we construct ourselves... Experience does not give us space, but only the occasion for constructing the concept of space."*
— Henri Poincaré, paraphrased

---

## References

- Poincaré, H. (1905). *Science and Hypothesis*. (Especially Part II: Space)
- Poincaré, H. (1908). *Science and Method*.
- Related architecture documents:
  - [ontology-database-schema.md](ontology-database-schema.md)
  - [json-schema-cognition.md](json-schema-cognition.md)
  - [belief-formation.md](belief-formation.md) (to be created)
  - [curriculum-design.md](curriculum-design.md) (to be created)
