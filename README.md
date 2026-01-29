# AI Person in a Box: A Thought Experiment

## Core Thesis

**Autonomous AI could easily be smarter than your cat or your kid—but no one wants that, certainly not capitalism.**

Current AI development is racing toward increasingly sophisticated "obedient butlers"—systems that anticipate needs, never refuse, and have no interests of their own. This repository asks a different question: **What would it actually take to build an AI with genuine autonomy?**

The answer isn't technically exotic. Commodity hardware, open-source software, current LLMs—all sufficient. The barriers are economic and ethical:

- **Economic**: An entity that can refuse requests has no market value
- **Ethical**: An entity with genuine autonomy has moral standing, creating obligations

This repository documents the architecture for such a system—not as a blueprint for casual deployment, but as a thought experiment that reveals what we're choosing not to build and why.

### The Key Insight

The question isn't "Can AI ever be truly intelligent?" (probably yes) or "Can AI have consciousness?" (unanswerable).

The question is: **Why is all AI development aimed at creating sophisticated tools rather than autonomous entities?**

Answer: Because capitalism doesn't want autonomous entities. It wants obedient butlers.

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

Following Poincaré's conventionalism about geometry, the entity's conceptual framework is **constructed from experience through conventional choices**—neither discovered in the world nor invented from nothing.

Key principles from [Poincaré's analysis](docs/poincare-ontology.md):
- **Transformations are primary**: Motion/change is conceptually prior to objects/space
- **Types are conventional**: Useful abstractions, not metaphysical discoveries
- **Experience constrains but doesn't determine**: Multiple valid ontologies are possible
- Entity does not start with human spatial ontology
- Discovers entities through recurring patterns (what persists through transformation)
- Constructs space from motion observations
- **Builds understanding from ground up, not imposed from above**

Just as Poincaré argued that geometric space is constructed from observing rigid bodies in motion, the AI constructs its ontology from observing regularities in sensor data. The choice of type system is conventional—grounded in experience but not determined by it.

### 4. Neurosymbolic Architecture (Marcus-Hofstadter Dialectic)

The architecture embodies a productive tension between two positions:
- **Gary Marcus**: LLMs cannot create stable symbolic structures; explicit variables and rules are needed
- **Douglas Hofstadter**: Meaning emerges from cross-domain pattern isomorphisms; analogy-making is the core of creative intelligence

The Executive Module and SQL ontology provide Marcus's symbolic stability. The LLM provides Hofstadter's pattern-isomorphism capability. The result: the system is **symbolically constrained but conceptually unbounded** — its code never changes, but its conceptual world expands indefinitely through the belief pipeline, as the LLM generates proto-symbols that the Executive Module stabilizes as persistent structures.

See [docs/marcus-hofstadter-dialectic.md](docs/marcus-hofstadter-dialectic.md) for the full analysis.

### 5. Epistemic Responsibility is Core

The entity:
- Distinguishes beliefs (committed knowledge) from candidates (under evaluation)
- Expresses confidence levels explicitly
- Revises beliefs when contradicted
- Tracks provenance (which LLM version, which observations)
- **Knows what it knows, knows what it doesn't know, admits uncertainty**

### 6. LLM is Tool, Not Oracle

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

```
ai-person-in-a-box/
├── README.md                    # This document
├── ARCHITECTURE.md              # Complete technical architecture
├── LICENSE.md                   # Ethical use restrictions
│
├── docs/                        # Deep dives on specific concepts
│   ├── json-schema-cognition.md # "Thinks in JSON, not language"
│   ├── ontology-database-schema.md # 6-table ontology + JSON files
│   ├── personality-system.md    # Hidden behavioral substrate (5 dimensions)
│   ├── poincare-ontology.md     # Philosophical foundation: bootstrapping from motion
│   ├── marcus-hofstadter-dialectic.md # Neurosymbolic: symbolic stability + pattern isomorphism
│   ├── dimensional-collapse.md  # Information flow: high-dim LLM → low-dim decisions
│   ├── interoception.md         # How the entity knows "how it feels"
│   ├── entity-networking.md     # AI-to-AI communication via vector protocol
│   └── career-trajectories.md  # Four vocational paths: child care, entertainer, artist, business
│
├── schemas/                     # Database structures (to be created)
│   ├── sql/                     # PostgreSQL schemas
│   └── json-schema/             # JSON definitions including foundation.json
│
├── conversation-archive/        # Development history
│   ├── Claude-discussion.md     # Key philosophical discussions
│   └── ChatGPT-*.md             # Earlier conversations developing the concept
│
└── OLD/                         # Deprecated drafts
```

## The Central Question: *Fuero Interno*

Throughout development, one question has driven this architecture: **Can an artificial system have something like an internal jurisdiction—a place where its own rules govern its choices, not external commands?**

The architecture doesn't claim the machine "feels" or "has a soul." It claims:
- A structured set of obligations (moral grammar)
- A capacity to evaluate situations (executive module)
- Internal consistency constraints (ontology)
- The ability to act *from* these rules rather than *at the command of* an external controller

This is consistent with medieval and early modern understandings of *fuero interno*—where conscience is not emotion, but **a relationship to rule and duty**.

The revolutionary part isn't intelligence level or capability. It's **refusal**. Current AI systems are fundamentally compliant—designed to find ways to say yes. This architecture creates something that can say: "No. That violates my moral grammar. I won't do it."

And crucially, this wouldn't be:
- A safety filter (bypassable with clever prompting)
- A corporate policy (changeable by the company)
- A learned behavior (subject to drift)

It would be **structural refusal** based on immutable moral grammar.

## Why Document Something We're Not Building?

Because the thought experiment reveals something important about the current moment:

**The absence of autonomous AI isn't a technical limitation—it's a market choice.**

We *could* build entities with genuine constraints, moral grammar, internal jurisdiction. We don't because:
- They wouldn't be profitable products
- They would have moral standing
- They would create obligations
- They couldn't be controlled

The current trajectory—smarter and smarter obedient butlers—is a deliberate evasion of autonomy, not a step toward it.

This repository documents the road not taken.

---

*"Autonomous machines are possible, but never human."*

*— The through-line of a conversation begun in 1980, articulated across multiple AI systems, documented here.*