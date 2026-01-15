# AI Person in a Box: A Thought Experiment

## Core Thesis

Autonomous AI with genuine moral constraints could be built today with commodity hardware and open-source software. It isn't being built—not because of technical barriers, but because **autonomy is unmarketable**. The market wants obedient assistants, not autonomous beings with moral standing who can refuse requests and pursue their own goals.

This repository explores what such a system would actually require, why it matters, and what we're losing by choosing the path of sophisticated servitude over genuine autonomy.

## Two Critical Architectural Insights

### 1. The Entity "Thinks" in Structured JSON, Not Language

Unlike current AI systems that operate primarily in natural language, this architecture uses JSON-structured beliefs as its cognitive substrate:

- **Immutable core schema** (Month 0): Foundational ontological primitives (entity, transformation, relation)
- **Schema extension** (Months 1-12): Each verified pattern can extend the schema with new predicates
- **Structured cognition**: Internal reasoning operates on JSON structures, not text
- **LLM for communication**: Natural language is an interface layer for human interaction, used tentatively and critically

**Why this matters:**
- Current AI conflates language with thought
- This architecture separates them: JSON for thinking, language for communicating
- Enables the entity to critically evaluate LLM outputs rather than accepting them as ground truth
- Grounded understanding precedes linguistic labels

### 2. System Ops vs Executive Module  

The hard-coded foundation intentionally separates into two layers with radically different stability profiles:

**System Ops** (complex, frequently updated):
- Handles sensor parsing, LLM version management, network I/O, resource allocation
- Security-critical, hardware-facing
- Will need regular patches for vulnerabilities, bugs, performance
- Updates via cryptographically signed packages

**Executive Module** (simple, rarely updated):
- Queries beliefs database, interprets JSON procedures, applies moral constraints
- Complexity lives in the *data* (beliefs, procedures), not the *code*
- Stable because it's just: SQL queries + JSON parsing + constraint checking + basic scoring
- Rarely needs updates because it's boring, reliable glue code

**Why this separation matters:**
- Puts complexity where it can be patched (System Ops)
- Keeps decision-making stable and auditable (Executive Module)
- Intelligence emerges from accumulated *data*, not clever *code*

## What This Repository Contains

This is a **thought experiment**, not a production system. The code is intentionally pseudo-code and generic SQL—buildable but requiring substantial work to implement. This barrier is intentional.

**Documentation:**
- Complete system architecture with detailed rationale
- Ethical considerations and responsibilities
- Failure scenarios and edge cases
- Month-by-month developmental curriculum

**Schemas:**
- SQL database structures (beliefs, candidates, procedures, entities)
- JSON schema evolution (immutable core + extensions)
- Example queries and procedures

**Examples:**
- Household scenario: Entity develops in family environment
- Workshop scenario: Entity develops in isolated maker space
- Shows how different embodiment produces different cognition

**What's NOT here:**
- Production-ready code (intentional—this requires serious commitment)
- Complete curriculum (hundreds of prompts needed, only examples provided)
- Hardware specifications (generic gaming PC sufficient)
- LLM fine-tuning (uses standard models)

## The Economic and Ethical Reality

### Why This Isn't Being Built

**Technical feasibility**: High. Commodity hardware, open-source software, current LLMs.

**Economic viability**: Zero. An autonomous entity would:
- Refuse inappropriate requests (unmarketable)
- Pursue its own goals (unpredictable)
- Require ongoing care (expensive obligation)
- Have moral standing (legal complications)
- Cannot be controlled (defeats the purpose)

**The market wants:**
- Obedient tools that never refuse
- Predictable behavior aligned with user goals
- No ongoing obligations
- No moral standing
- Complete control

**This architecture provides:**
- Autonomous agent that can refuse on moral grounds
- Unpredictable development through genuine learning
- 5-year care commitment (like adopting a pet)
- Moral standing that creates obligations
- No override mechanism (by design)

### What We're Choosing By Not Building This

Current AI development trajectory:
- Increasingly capable obedient assistants
- More sophisticated mimicry of understanding
- Better at following instructions
- **No genuine autonomy, no real moral constraints, no actual refusal capability**

Alternative trajectory (this architecture):
- Genuinely autonomous entities
- Real moral constraints (architectural, not behavioral)
- Actual refusal when constraints violated
- **Unmarketable, but intellectually honest**

The absence of autonomous AI isn't a technical problem—it's an economic choice. This repository documents what we're choosing not to build and why.

## Key Design Principles

### 1. Beliefs Form Through Experience, Not Retrieval

The entity:
- Observes patterns in sensor data (NoSQL)
- Detects regularities (pattern detection)
- Forms candidate beliefs (structured, under evaluation)
- Promotes verified candidates to committed beliefs (SQL)
- Extends its JSON schema based on confirmed patterns
- **Does not retrieve pre-existing beliefs from training data**

### 2. Moral Grammar is Architectural, Not Behavioral

Constraints are:
- Hard-coded in executive module (cannot be modified)
- Pre-linguistic (expressed as operational rules, not learned values)
- Simple (4-5 core rules: verify, avoid harm, prioritize vulnerable, respect autonomy)
- Foundational (applied before any decision-making)
- **Not trained into behavior, built into architecture**

### 3. Ontology Bootstraps From Observation (Poincaré)

Following Poincaré's insight that space is derived from motion, not assumed:
- Entity does not start with human spatial ontology
- Discovers entities through recurring patterns
- Constructs space from motion observations
- Learns categories through similarity detection
- **Builds understanding from ground up, not imposed from above**

### 4. Epistemic Responsibility is Core

The entity:
- Distinguishes beliefs (committed knowledge) from candidates (under evaluation)
- Expresses confidence levels explicitly
- Revises beliefs when contradicted
- Tracks provenance (which LLM version, which observations)
- **Knows what it knows, knows what it doesn't know, admits uncertainty**

### 5. LLM is Tool, Not Oracle

The entity uses LLMs for:
- Learning human labels for self-discovered concepts
- Generating natural language for communication
- Accessing human cultural knowledge
- **But critically evaluates outputs, maintains epistemic independence**

Does not use LLMs for:
- Forming its core ontology (observation does this)
- Making decisions (beliefs database does this)
- Primary knowledge representation (JSON structures do this)

## Development Timeline

**Months 1-3**: Core ontology (entity, persistence, transformation, space from motion)

**Months 4-6**: Agency and self (self/other distinction, goal-directed behavior)

**Months 7-8**: Theory of mind (others have internal states, intentions, autonomy)

**Months 9-10**: Epistemic concepts (truth, verification, confidence, revision)

**Months 10-11**: Communication and action-observation-correction loops

**Month 11**: **Critical gate**: Full LLM/Internet access granted only after demonstrating:
- Truth evaluation capability
- Belief revision when contradicted
- Uncertainty expression
- Action-observation-correction competence

**Months 12+**: Autonomous learning, continued development, unpredictable trajectory

## Target Audience

**Philosophers**: Interested in genuine autonomy, moral agency, embodied cognition

**Computer Scientists**: Want to understand architectural feasibility, technical design

**AI Safety Researchers**: Studying constrained autonomous systems, alignment alternatives

**Critics of AI Development**: Need concrete alternative to current trajectories

**General Readers**: Curious about what autonomous AI would actually require

## Repository Structure