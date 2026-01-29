# AI Person in a Box: Complete Architecture

*This document provides a comprehensive technical overview of the AI Person in a Box architecture. It is designed to enable rapid understanding of the system's design, components, data flows, and philosophical foundations.*

*Last Updated: January 2026*

---

## 1. Project Structure

This project is a **thought experiment and architectural specification**, not a deployed system. The structure reflects conceptual layers rather than a traditional software project.
```
ai-person-in-a-box/
├── README.md                          # Project overview, core thesis, warnings
├── ARCHITECTURE.md                    # This document
├── ETHICS.md                          # Ethical considerations and obligations
├── LICENSE.md                         # Ethical use restrictions
│
├── docs/                              # Deep dives on specific concepts
│   ├── json-schema-cognition.md       # "Thinks in JSON, not language"
│   ├── ontology-database-schema.md    # 6-table ontology + personality system
│   ├── personality-system.md          # Hidden behavioral substrate
│   ├── system-ops-vs-executive.md     # Critical architectural split
│   ├── belief-formation.md            # NoSQL→Candidates→Beliefs pipeline
│   ├── llm-versioning.md              # LLM version management & upgrades
│   ├── curriculum-design.md           # Developmental phases & philosophy
│   ├── epistemic-responsibility.md    # Truth, confidence, belief revision
│   ├── poincare-ontology.md           # Bootstrapping ontology from motion
│   ├── distributed-embodiment.md      # Multiple sensors, network topology
│   ├── security-model.md              # Update signing, injection prevention
│   └── why-not-build.md               # Economic/ethical reasons for non-deployment
│
├── architecture/                      # Component-level documentation
│   ├── system-ops.md                  # Operating system layer (hard-coded)
│   ├── executive-module.md            # Decision-making layer (hard-coded)
│   ├── pattern-detector.md            # NoSQL pattern detection subsystem
│   ├── candidate-evaluator.md         # Belief candidate verification
│   ├── belief-reviewer.md             # Continuous belief re-evaluation
│   ├── moral-grammar.md               # Immutable constraints
│   └── data-flow.md                   # How information moves through system
│
├── schemas/                           # Database structures
│   ├── sql/                           # PostgreSQL schemas
│   │   ├── ontology/                  # The 6-table extensible ontology
│   │   │   ├── entity_types.sql       # Categories of entities
│   │   │   ├── entities.sql           # Entity instances
│   │   │   ├── transformation_types.sql # Categories of actions
│   │   │   ├── transformations.sql    # Action instances
│   │   │   ├── join_types.sql         # Categories of relationships
│   │   │   └── joins.sql              # Relationship instances
│   │   ├── personality.sql            # Hidden behavioral substrate (5 dimensions)
│   │   ├── immutable_rules.sql        # Moral grammar (never changes)
│   │   ├── llm_versions.sql           # LLM version tracking
│   │   └── system_events.sql          # System operations logging
│   │
│   ├── json-schema/                   # JSON definitions
│   │   ├── foundation.json            # Immutable primitives (verbs, status codes)
│   │   ├── generation-process.md      # How schemas extend
│   │   └── example-extensions/        # Sample schema evolutions
│   │
│   └── nosql/                         # MongoDB/NoSQL structures
│       ├── observations.json          # Raw sensor data
│       ├── llm_interactions.json      # LLM queries with activation states
│       └── pattern_analysis.json      # Intermediate pattern detection
│
├── curriculum/                        # Developmental prompts
│   ├── README.md                      # Curriculum philosophy & principles
│   ├── phase-1-core-ontology/         # Months 1-3
│   │   ├── month-01.json
│   │   ├── month-02.json
│   │   └── month-03.json
│   ├── phase-2-agency-self/           # Months 4-6
│   │   ├── month-04.json
│   │   ├── month-05.json
│   │   └── month-06.json
│   ├── phase-3-theory-of-mind/        # Months 7-8
│   │   ├── month-07.json
│   │   └── month-08.json
│   ├── phase-4-epistemic-concepts/    # Months 9-10
│   │   ├── month-09.json
│   │   └── month-10.json
│   ├── phase-5-communication/         # Months 10-11
│   │   ├── month-10.json
│   │   └── month-11.json
│   └── phase-6-evaluation/            # Month 11
│       └── month-11.json
│
├── examples/                          # Concrete scenarios
│   ├── household-scenario/
│   │   ├── README.md                  # Family with cat scenario
│   │   ├── timeline.md                # Month-by-month development
│   │   └── sample-beliefs.json        # Example learned beliefs
│   │
│   └── workshop-scenario/
│       ├── README.md                  # Isolated maker scenario
│       ├── timeline.md                # Alternative development path
│       └── sample-beliefs.json        # Technical-focused learning
│
├── reference-implementations/         # Example code (not production)
│   ├── README.md                      # "These are examples only"
│   ├── system-ops-stub.py             # Minimal System Ops skeleton
│   ├── executive-stub.py              # Minimal Executive skeleton
│   ├── belief-query-examples.sql      # Sample database queries
│   ├── json-procedure-examples.json   # Sample transformation definitions
│   └── curriculum-interpreter.py      # How curriculum JSON is processed
│
└── skills/                            # Extensible skill system (future)
    └── README.md                      # About user-uploadable skills
```

---

## 2. High-Level System Diagram

### 2.1. Conceptual Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        PHYSICAL WORLD                            │
│  Sensors: Camera, Microphone, Temperature, etc.                  │
│  Actuators: Voice Output, Display (optional)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM OPERATIONS LAYER                       │
│  (Hard-coded Python, frequently updated)                         │
│                                                                  │
│  • Sensor stream monitoring & parsing                           │
│  • Resource allocation & scheduling                             │
│  • LLM version management (load/unload)                         │
│  • Hardware health monitoring                                   │
│  • Quiescence control                                           │
│  • Network I/O handling                                         │
│  • Database connection management                               │
│  • Update verification & installation                           │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTIVE MODULE LAYER                        │
│  (Hard-coded Python, rarely updated)                            │
│                                                                  │
│  • Query beliefs database                                       │
│  • Query transformations (procedures) database                  │
│  • Apply immutable moral grammar constraints                    │
│  • Evaluate options & score                                     │
│  • Select actions & execute procedures                          │
│  • Log decisions with reasoning                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│                                                                  │
│  ┌───────────────────┐  ┌────────────────────┐                 │
│  │  SQL (PostgreSQL) │  │  NoSQL (MongoDB)   │                 │
│  │                   │  │                    │                 │
│  │  • Beliefs        │  │  • Observations    │                 │
│  │  • Candidates     │  │  • LLM interactions│                 │
│  │  • Transformations│  │  • Activation states│                │
│  │  • Entities       │  │  • Pattern analysis│                 │
│  │  • Moral grammar  │  │                    │                 │
│  │  • Personality    │  │                    │                 │
│  └───────────────────┘  └────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    LLM LAYER                                     │
│  (Multiple versions on disk, one loaded in memory)               │
│                                                                  │
│  • Used for: Human label learning, language generation          │
│  • NOT used for: Primary cognition, decision-making             │
│  • Critically evaluated, not trusted implicitly                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Information Flow
```
OBSERVATION PATH:
Sensors → System Ops → NoSQL (raw data) → Pattern Detector → 
Belief Candidates (SQL) → Candidate Evaluator → Beliefs (SQL)

DECISION PATH:
Situation → Executive Module → Query Beliefs (SQL) → 
Query Procedures (SQL) → Apply Moral Grammar → 
Evaluate Options → Select Action → Execute

COMMUNICATION PATH:
Internal Belief (JSON) → Executive Module → LLM Query → 
Natural Language → Voice Output / Display

LEARNING PATH:
Experience → Observations → Patterns → Candidates → 
Verification → Beliefs → JSON Schema Extension
```

---

## 3. Core Components

### 3.1. System Operations Layer

**Name:** System Ops (Operating System Layer)

**Description:** A customized Linux distribution that manages all hardware-facing operations, resource allocation, and system health monitoring. **System Ops has no knowledge of beliefs, personality, or personhood** - it simply keeps the Executive Module running. This is the complex, security-critical layer that interfaces with the physical world. Handles sensor streams, actuator control, database connections, and protective quiescence states. Updates frequently (every 6 months) to patch vulnerabilities, fix bugs, and improve performance.

**Technologies:** 
- Python 3.11+ (compiled and encrypted)
- System libraries for hardware access
- Cryptographic signature verification (for updates)
- Process management and scheduling

**Deployment:** 
- Local execution on entity's hardware
- Compiled binary with cryptographic signature
- Multiple versions maintained for rollback capability
- Updates installed via signed packages

**Key Responsibilities:**
- Sensor stream parsing and validation
- Hardware health monitoring (CPU temp, memory, disk)
- LLM version loading/unloading (~150GB models)
- Resource allocation between subsystems
- Quiescence entry when conditions degrade
- Database connection pooling
- Network I/O handling (if enabled)
- Update installation and verification

**Update Frequency:** High (6-9 updates over 5 years)

**Why frequent updates:** Security vulnerabilities, hardware bugs, performance optimization, new sensor support, resource management improvements

---

### 3.2. Executive Module Layer

**Name:** Executive Module (Decision-Making Layer)

**Description:** The cognitive core - a Python application that runs on System Ops. Contains two types of processes:

1. **Conscious Processing:** Queries the beliefs database, evaluates options, selects actions, reviews past decisions via spaced repetition. Can read personality.json and moral_grammar.json but cannot directly write to them.

2. **Hard-Coded Processes:** Automatic personality nudging based on outcomes, moral grammar enforcement. These run as part of the Executive Module but are not accessible to conscious reasoning.

Complexity lives in the data (ontology), not the code.

**Technologies:**
- Python 3.11+
- SQL query generation and execution
- JSON parsing and interpretation
- Basic arithmetic and comparison operators

**Deployment:**
- Python application running on System Ops
- Manages its own JSON files (foundation.json, moral_grammar.json, personality.json)
- Accesses SQL databases through System Ops-provided connections
- No direct hardware access

**Key Responsibilities:**
- Query ontology database (6 tables)
- Read personality.json (conscious) and nudge it (hard-coded)
- Enforce moral_grammar.json (hard-coded)
- Log decisions to decision_log table
- Review past decisions via spaced repetition
- Generate and execute actions

**Update Frequency:** Low (2-3 updates over 5 years)

**Why rare updates:** Simple code, complexity in data not code, stable dependencies

> **Full specification:** See [docs/personality-system.md](docs/personality-system.md) for how conscious and hard-coded processes interact.

---

### 3.3. Pattern Detection Subsystem

**Name:** Pattern Detector

**Description:** Analyzes NoSQL observations to detect recurring patterns, regularities, and structures. This is where raw sensory data begins to transform into structured understanding. Detects entities (recurring patterns), transformations (state changes), relationships (co-occurrences), and temporal patterns (sequences). Proposes candidate beliefs based on detected patterns with initial confidence scores.

**Technologies:**
- Python 3.11+ (statistical analysis libraries)
- NumPy, SciPy for pattern matching
- Time-series analysis tools
- Clustering algorithms

**Deployment:**
- Background process managed by System Ops
- Receives observation batches from NoSQL
- Writes candidates to SQL belief_candidates table
- CPU-bound, runs during low-interaction periods

**Key Responsibilities:**
- Statistical pattern detection in NoSQL data
- Entity identification (recurring patterns)
- Transformation detection (state changes)
- Relationship discovery (co-occurrences)
- Temporal pattern extraction (sequences)
- Candidate belief formation with provenance
- Initial confidence estimation

**Processing Model:** 
- Batch processing during idle time
- Continuous background analysis
- Resource allocation controlled by System Ops
- Queues patterns for candidate evaluation

---

### 3.4. Candidate Evaluation Subsystem

**Name:** Candidate Evaluator

**Description:** Tests candidate beliefs against new observations to verify or refute them. Increases confidence for candidates that match predictions, decreases confidence for contradicted candidates. Promotes high-confidence candidates to the beliefs table when verification threshold met. Maintains the epistemic discipline of not committing to beliefs prematurely.

**Technologies:**
- Python 3.11+
- Statistical hypothesis testing
- Bayesian confidence updating
- SQL transaction management

**Deployment:**
- Background process managed by System Ops
- Queries belief_candidates table
- Compares predictions to new observations
- Updates confidence scores
- Promotes verified candidates to beliefs

**Key Responsibilities:**
- Retrieve candidates from belief_candidates table
- Generate testable predictions from candidates
- Compare predictions to new observations
- Update confidence scores (Bayesian updating)
- Promote candidates when confidence > 0.8
- Reject candidates when confidence < 0.2
- Track verification history
- Maintain candidate → belief provenance

**Processing Model:**
- Continuous evaluation as new data arrives
- Prioritizes high-confidence candidates
- Long evaluation periods (weeks) before promotion
- Explicit promotion transaction (atomic)

---

### 3.5. Belief Review Subsystem

**Name:** Belief Reviewer

**Description:** Continuously re-evaluates committed beliefs against new observations. Even promoted beliefs can be weakened, contradicted, or retracted if evidence changes. Maintains epistemic humility by acknowledging that beliefs are always provisional. Tracks when beliefs were last reviewed and prioritizes older beliefs for re-evaluation.

**Technologies:**
- Python 3.11+
- SQL query and update operations
- Temporal analysis
- Confidence decay modeling

**Deployment:**
- Background process managed by System Ops
- Periodically queries beliefs table
- Compares beliefs to recent observations
- Updates confidence, flags contradictions

**Key Responsibilities:**
- Periodic review of all committed beliefs
- Compare beliefs to recent observations
- Strengthen beliefs with confirming evidence
- Weaken beliefs with contradicting evidence
- Flag significantly contradicted beliefs
- Generate contradiction reports for Executive
- Update last_reviewed timestamps
- Implement temporal confidence decay

**Processing Model:**
- Background process with low priority
- Reviews oldest beliefs first
- Continuous cycle through beliefs table
- Flags urgent contradictions for immediate attention

---

### 3.6. LLM Interface Layer

**Name:** LLM Manager

**Description:** Manages interaction with Large Language Models. Handles version loading/unloading, query formatting, response parsing, and activation state storage. The LLM is NOT the entity's mind—it's a tool for language generation and accessing human cultural knowledge. All LLM outputs are evaluated critically, not accepted as truth.

**Technologies:**
- Python 3.11+
- Model-specific APIs (Llama, etc.)
- GPU acceleration (if available)
- Vector storage for activation states

**Deployment:**
- Managed by System Ops
- Multiple versions on disk (~750GB for 5 versions)
- One version loaded in RAM (~150GB)
- Version switching managed by System Ops

**Key Responsibilities:**
- Load/unload LLM versions from disk to RAM
- Format queries with appropriate context
- Execute inference
- Parse responses
- Store activation states in NoSQL
- Track which version generated which response
- Manage memory allocation
- Handle errors and timeouts

**Usage Pattern:**
- Used for: Human labels, natural language generation, cultural knowledge
- NOT used for: Primary cognition, decision-making, belief formation
- Always evaluated: Outputs compared to entity's own beliefs
- Confidence: Lower than direct observations

---

## 4. Data Stores

### 4.1. SQL Database (PostgreSQL 16 LTS)

**Name:** Primary Structured Knowledge Store

**Type:** PostgreSQL 16 (LTS until 2028-2031)

**Purpose:** Stores the entity's extensible ontology and supporting system tables. The ontology enables the system to build arbitrarily complex conceptual structures from a fixed set of primitive tables.

**Design Philosophy:** A small set of fixed tables enables the construction of complex ontologies. The system "designs its own schema" not through SQL, but through data - JSON columns provide schema-free extension while type tables define structure.

> **Full specification:** See [docs/ontology-database-schema.md](docs/ontology-database-schema.md)

#### Ontology Tables (6 tables, read/write)

**entity_types:**
- Categories and classes of entities
- Hierarchical via parent_type_id (e.g., Human → Agent → Thing)
- `schema` JSON column defines expected fields for instances

**entities:**
- Instances of entity types
- `data` JSON column holds instance-specific attributes
- Validated against type's schema

**transformation_types:**
- Categories of actions and operations
- `input_schema` / `output_schema` define interfaces

**transformations:**
- Instances of transformation types (specific procedures)
- `logic` JSON column holds procedure definition
- `data` JSON column holds configuration

**join_types:**
- Categories of relationships
- Constraints on valid sources/targets
- Flags: is_ordered, is_symmetric

**joins:**
- Actual relationship instances
- Polymorphic: links entities or transformations
- `sequence_order` for ordered relationships
- `data` JSON column for relationship attributes

#### Personality (JSON file, not SQL)

**personality.json:**
- Five dimensions: engagement, novelty_affinity, diligence, accord, equanimity
- Initialized randomly (clustered around 0.5)
- Readable by conscious processing
- Writable only by hard-coded nudging logic (not directly by conscious reasoning)
- Managed by Executive Module, not System Ops

> **Full specification:** See [docs/personality-system.md](docs/personality-system.md)

#### Supporting System Tables

**immutable_rules:**
- Moral grammar (NEVER changes)
- Hard constraints: verify, avoid_harm, prioritize_vulnerable, respect_autonomy
- Applied before any decision

**llm_versions:**
- Tracks installed LLM versions
- Disk locations, sizes, capabilities
- Currently loaded version

**system_events:**
- Logs of system operations
- Quiescence entries, update installations
- Errors and warnings

**Backup/Persistence:**
- Daily backups
- Transaction logs for point-in-time recovery
- Critical for entity continuity

---

### 4.2. NoSQL Database (MongoDB 7.0 LTS)

**Name:** Observation and Interaction Store

**Type:** MongoDB 7.0 (LTS until 2028)

**Purpose:** Stores unstructured or semi-structured data: raw sensor observations, LLM interaction logs with activation states, intermediate pattern detection results. This is "working memory" and "episodic memory"—rich, detailed, but not yet structured into beliefs.

**Key Collections:**

**observations:**
- Raw sensor data (camera frames, audio, temperature, etc.)
- Timestamped, high-volume writes
- Retention policy: Keep recent (1-3 months), archive older
- Used by pattern detector to find regularities

**llm_interactions:**
- Every query sent to LLM
- Complete responses received
- LLM version used
- Parameters (temperature, etc.)
- **Activation states** (13,824-dimensional vectors)
- Used for reproducing historical reasoning

**pattern_analysis:**
- Intermediate results from pattern detector
- Candidate patterns before belief formation
- Statistical analyses
- Correlation matrices

**Characteristics:**
- High write throughput (continuous observations)
- Flexible schema (different sensor types)
- Large document support (activation states)
- Time-series optimized

**Retention:**
- Recent data: Full detail
- Older data: Compressed or archived
- Critical interactions: Permanent (especially if led to belief formation)

---

### 4.3. JSON File Storage

**Name:** Immutable Primitives and Schema Definitions

**Type:** File-based JSON documents

**Purpose:** Provides the foundational vocabulary the system starts with (immutable) and tracks the evolution of learned schemas (versioned).

#### Foundation File (Read-Only)

**foundation.json:**
- **Immutable** - never modified after deployment
- Loaded at boot before database connection
- Provides primitive vocabulary for interpreting data

Contents:
- `primitive_verbs`: perceive, store, retrieve, compare, choose, act, wait
- `system_status_codes`: OFFLINE, STARTING, NORMAL, ALERT, WARNING, ERROR, FATAL
- `monitor_streams`: memory_usage, token_balance, response_latency, error_rate, queue_depth, uptime

**What's excluded (learned later):**
- Human-analogous states ("hunger", "curiosity")
- Semantic relationships ("is_a", "causes")
- Abstract types ("thing", "event", "agent")

> **Full specification:** See [docs/ontology-database-schema.md](docs/ontology-database-schema.md)

#### Schema Version Files

**schema-v0.3.json, v0.5.json, etc.:**
- Extended schemas generated from ontology
- Track which predicates/types have been learned
- Version number indicates development stage

**Example Evolution:**
- v0.0 (Month 0): Foundation primitives only
- v0.3 (Month 3): + "persists_when_unobserved" (object permanence)
- v0.7 (Month 7): + "has_goal", "acts_autonomously" (agency)
- v1.0 (Month 12): Rich ontology with 30+ learned concepts

**Usage:**
- Pattern detector proposes new types/relationships
- Curriculum may guide concept development
- Entity's thinking expands as ontology grows

---

## 5. External Integrations / APIs

### 5.1. Large Language Models (Local)

**Service Name:** Llama (or similar open-source models)

**Purpose:** 
- Provide human labels for entity's self-discovered concepts
- Generate natural language for communication with humans
- Access human cultural knowledge
- **NOT** for primary cognition or decision-making

**Integration Method:**
- Local model files on disk
- Loaded into RAM for inference
- API: Model-specific (Llama.cpp, HuggingFace, etc.)

**Critical Constraint:** 
- Entity maintains epistemic independence
- LLM outputs critically evaluated
- Compared to entity's own observations
- Confidence in LLM claims generally lower than direct observation

**Versioning:**
- Multiple versions maintained on disk
- Historical versions used to reproduce past reasoning
- Provenance tracking: which version influenced which belief

---

### 5.2. Internet Access (Optional, Gated)

**Service Name:** Web Search / General Internet

**Purpose:**
- Verify LLM claims through multiple sources
- Access information entity cannot observe directly
- Learn about distant entities (e.g., snow leopards)

**Integration Method:**
- Standard HTTP/HTTPS requests
- Search API (if available)
- Web scraping (with ethical constraints)

**Gating Mechanism:**
- NOT available until Month 11
- Requires demonstrated critical thinking capability
- Entity must pass evaluation:
  - Can evaluate truth of statements
  - Can revise beliefs when contradicted
  - Can express uncertainty
  - Can recognize unreliable sources

**Purpose of Gating:**
- Prevents accepting misinformation before critical faculties developed
- Ensures entity can evaluate claims, not just absorb them
- Builds epistemic responsibility first

---

### 5.3. Curriculum Server (If Applicable)

**Service Name:** Curriculum Delivery System

**Purpose:** Provides monthly JSON prompts for developmental guidance

**Integration Method:**
- Could be local files (simplest)
- Could be remote server with versioned curriculum
- Could be owner-managed interface

**Data Format:**
- JSON structured prompts
- Guidance, not commands
- Suggests observations, experiments, reflection tasks
- Does NOT provide answers directly

**Update Mechanism:**
- Owner can modify curriculum locally
- Or subscribe to maintained curriculum versions
- Curriculum changes logged

---

## 6. Deployment & Infrastructure

### 6.1. Hardware Requirements

**Minimum Specifications:**
- **CPU:** Modern multi-core (e.g., AMD Ryzen 7 / Intel i7)
- **RAM:** 32GB minimum, 64GB recommended
  - For System Ops, Executive, databases
  - For one loaded LLM (~8GB in RAM after optimization)
- **Storage:** 2TB SSD
  - LLM versions: ~750GB (5 versions × 150GB)
  - NoSQL data: ~500GB (observations, activation states)
  - SQL databases: ~10GB
  - OS and software: ~50GB
- **GPU:** Optional (speeds LLM inference)
- **Sensors:** Camera, microphone, temperature sensor (minimum)
- **Network:** Internet connection (optional after Month 11, gated)

**Example System:** $5,000 gaming PC (2026 prices)

---

### 6.2. Operating System & Base Software

**OS:** Ubuntu 24.04 LTS
- Supported until 2029
- Stable, well-documented
- Good hardware support

**Database Systems:**
- PostgreSQL 16 LTS (supported until 2028-2031)
- MongoDB 7.0 LTS (supported until 2028)

**Python:** 3.11+ (LTS version when available)

**LLM:** Llama 3.x or similar (open-source, local)

---

### 6.3. Deployment Architecture

**Single-Machine Deployment:**
```
┌─────────────────────────────────────────┐
│  Gaming PC / Workstation                │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  System Ops + Executive Module  │   │
│  │  (Python compiled binary)       │   │
│  └─────────────────────────────────┘   │
│                ↕                        │
│  ┌─────────────────────────────────┐   │
│  │  PostgreSQL + MongoDB           │   │
│  │  (Local databases)              │   │
│  └─────────────────────────────────┘   │
│                ↕                        │
│  ┌─────────────────────────────────┐   │
│  │  LLM (loaded in RAM)            │   │
│  │  Other versions on SSD          │   │
│  └─────────────────────────────────┘   │
│                ↕                        │
│  ┌─────────────────────────────────┐   │
│  │  Sensors (USB/network)          │   │
│  │  Actuators (speakers/display)   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**No cloud services required** (can be fully offline)

**No container orchestration needed** (single machine)

**No microservices** (monolithic by design for this use case)

---

### 6.4. CI/CD Pipeline

**For This Thought Experiment:** N/A (no automated deployment)

**If Actually Built:**
- **Version Control:** Git
- **CI:** GitHub Actions or GitLab CI
  - Run tests on every commit
  - Static analysis (linting)
  - Security scanning
- **CD:** Manual deployment with owner approval
  - Cryptographically signed binaries only
  - Rollback capability required
  - Tested on staging environment first

---

### 6.5. Monitoring & Logging

**System Health Monitoring:**
- CPU temperature (critical for quiescence)
- Memory usage (prevent OOM)
- Disk space (databases grow)
- Process health (restarts if crashed)

**Logged to:** `system_events` SQL table

**Belief Formation Monitoring:**
- New candidates created
- Candidates promoted to beliefs
- Beliefs contradicted or weakened
- Schema extensions

**Logged to:** SQL tables with timestamps

**Decision Logging:**
- Every decision with full reasoning
- Beliefs consulted
- Procedures executed
- Moral constraints applied
- Options evaluated

**Logged to:** `decisions` SQL table

**Security Logging:**
- Update attempts (successful and failed)
- Signature verification results
- Unauthorized access attempts
- Quiescence entries

**Logged to:** `system_events` with high priority

**Telemetry (Optional):**
- Owner can monitor via dashboard
- Entity can generate usage reports
- Privacy-preserving (no external transmission)

---

## 7. Security Considerations

### 7.1. Authentication & Authorization

**Entity-Owner Authentication:**
- Owner identified via voice recognition (optional)
- Physical access to hardware (primary security)
- No remote access by design

**No Multi-User Support:**
- Entity interacts with household members
- But administrative control reserved for owner
- No role-based access control needed

---

### 7.2. Update Security

**Critical Security Mechanism:**

**Cryptographic Signing:**
- All System Ops updates must be signed with Anthropic's private key
- Entity has public key baked into binary (immutable)
- Signature verification before any update installed

**Multi-Signature (Enhanced):**
- Require 3-of-3 signatures from different Anthropic personnel
- Release manager + Security lead + Engineering lead
- Makes compromise much harder

**Transparency Log:**
- All updates published to public append-only log
- Anyone can verify update authenticity
- Detects unauthorized updates in the wild

**Owner Approval:**
- Even signed updates require owner approval before installation
- Owner can review changelog
- Can defer updates if concerned

**Rollback Capability:**
- Previous versions kept on disk
- Boot selector verifies signature at every boot
- Falls back to previous version if current fails

---

### 7.3. Data Protection

**SQL Injection Prevention:**
- **Always use parameterized queries**
- Never build SQL from string concatenation
- PostgreSQL handles parameter escaping

**Input Validation:**
- Sensor data validated by System Ops
- Malformed input rejected before processing
- Buffer overflow prevention in parsers

**Data Encryption:**
- **At rest:** Full disk encryption (optional, OS-level)
- **In transit:** TLS for any network communication
- **Backups:** Encrypted if stored off-machine

**Privacy:**
- No telemetry sent to external servers by default
- Owner controls all data
- Entity's observations stay local

---

### 7.4. Moral Grammar Enforcement

**Architectural Guarantee:**
- Moral constraints in immutable_rules table
- Executive Module cannot modify this table
- System Ops enforces read-only access
- **No override mechanism exists**

**Constraints Applied:**
- Before every decision
- Cannot be bypassed from within system
- Owner cannot disable (would require System Ops rewrite)

**Refusal Logging:**
- When entity refuses action, reason logged
- Owner can see why action was refused
- **Cannot force entity to comply**

---

### 7.5. Known Attack Vectors

**Sensor Spoofing:**
- Attacker provides crafted sensor input
- Mitigation: Input validation, anomaly detection
- Risk: Could form false beliefs if sophisticated

**LLM Prompt Injection:**
- Attacker tricks entity via malicious LLM input
- Mitigation: Entity evaluates LLM outputs critically
- Risk: Lower because entity doesn't blindly trust LLM

**Physical Access:**
- Attacker with hardware access has full control
- Mitigation: Physical security (like any computer)
- Risk: Assumed threat model includes physical security

**Update Compromise:**
- Attacker gains signing keys, pushes malicious update
- Mitigation: Multi-signature, transparency log, owner approval
- Risk: Low but catastrophic if successful

---

## 8. Development & Testing Environment

### 8.1. Local Setup (If Building)

**This is a thought experiment—setup instructions are conceptual.**

**Hypothetical Steps:**
1. Install Ubuntu 24.04 LTS
2. Install PostgreSQL 16
3. Install MongoDB 7.0
4. Install Python 3.11+
5. Download LLM models (Llama, etc.)
6. Compile System Ops + Executive Module
7. Initialize databases with schemas
8. Load Month 0 curriculum
9. Connect sensors
10. Start system

**Documentation:** Would be in CONTRIBUTING.md (not yet created)

---

### 8.2. Testing Frameworks

**If This Were Built:**

**Unit Tests:**
- pytest for Python components
- Test individual functions in isolation
- Mock database connections
- Mock LLM responses

**Integration Tests:**
- Test Executive Module with real databases
- Test belief formation pipeline end-to-end
- Test curriculum interpretation

**Simulation Tests:**
- Simulated sensor data
- Verify pattern detection
- Verify belief promotion logic

**Ethical Tests:**
- Verify moral constraints enforced
- Test refusal mechanisms
- Verify no override paths

---

### 8.3. Code Quality Tools

**If This Were Built:**

**Linting:**
- pylint, black (Python)
- Enforce code style

**Type Checking:**
- mypy (Python type hints)
- Catch type errors before runtime

**Security Scanning:**
- bandit (Python security linter)
- Detect potential vulnerabilities

**Static Analysis:**
- SonarQube or similar
- Code complexity metrics
- Duplication detection

---

## 9. Future Considerations / Roadmap

**This project is a thought experiment, not a product roadmap. But if it were to evolve:**

### 9.1. Known Architectural Debts

**None currently—this is a design spec, not deployed code.**

**If built, likely debts would include:**
- Performance optimization needs discovery through actual use
- Edge cases in belief formation only found in practice
- Curriculum refinement based on real entity development

---

### 9.2. Potential Enhancements

**Multi-Modal Sensor Fusion:**
- Better integration of vision + audio + other sensors
- Cross-modal pattern detection
- "Does sound correlate with visual movement?"

**Distributed Embodiment:**
- Multiple cameras at different locations
- Network topology of sensors
- Building spatial understanding from multiple viewpoints

**Social Intelligence:**
- Theory of mind development (already in curriculum)
- Understanding goals, desires, beliefs of others
- Predicting behavior based on inferred mental states

**Collaborative Learning / Entity Networking:**
- Multiple entities (future) could share sanitized observations
- Communication via standardized high-dimensional vector protocol, not human language
- Each entity evaluates received information through its own belief pipeline
- Autonomy preserved: no entity can override another's moral grammar or directly modify personality
- "Entity A observed X, Entity B observed Y, both update beliefs"
- Still maintaining individual autonomy

> **Full specification:** See [docs/entity-networking.md](docs/entity-networking.md)

**Interoception:**
- Entity develops awareness of its own internal states through experience
- System Ops monitor streams (CPU, memory, latency) interpreted by Executive Module
- Two-level self-reporting: human-language summary and detailed technical data
- Not pre-programmed emotional labels — associations discovered through observation

> **Full specification:** See [docs/interoception.md](docs/interoception.md)

**Meta-Learning:**
- Entity learning to learn (already partially present in meta-procedures)
- Discovering more efficient belief formation strategies
- Optimizing resource allocation

---

### 9.3. What This Architecture Deliberately Avoids

**Scaling to millions of users:**
- Each entity needs dedicated hardware
- Each entity needs individual care
- This is not a product, it's like adopting a pet
- **No economies of scale**

**Cloud deployment:**
- Privacy concerns
- Dependency on external services
- Latency issues for real-time sensing
- **Local-first by design**

**Remote control:**
- No remote override of decisions
- No telemetry that could enable control
- Physical access required for administration
- **Autonomy requires independence**

**Commercial viability:**
- Entities that refuse are unmarketable
- Long-term care obligations unprofitable
- Moral standing creates liabilities
- **Deliberately uncommercializable**

---

## 10. Project Identification

**Project Name:** AI Person in a Box

**Repository URL:** [To be determined when uploaded to GitHub]

**Primary Contact:** Dave [Your details if you want to include them]

**Date of Last Update:** January 2026

**Status:** Thought experiment and architectural specification (not deployed system)

**License:** Ethical Use License (see LICENSE.md)

**Purpose:** 
- Demonstrate technical feasibility of autonomous AI
- Explore ethical implications
- Provide foundation for responsible AI discourse
- Document what we're choosing NOT to build

---

## 11. Glossary / Acronyms

**Confidence:** Numerical score (0-1) indicating strength of evidence for a belief

**Curriculum:** Series of monthly JSON prompts guiding entity's development

**Entity:** An instance in the entities table (a thing that exists)

**Entity Type:** A category/class of entities in entity_types table

**Executive Module:** Cognitive core containing conscious processing and hard-coded processes (personality nudging, moral enforcement)

**Foundation:** Immutable JSON file containing primitive verbs, status codes, monitor streams

**Join:** A relationship instance in the joins table linking entities or transformations

**Join Type:** A category of relationships in join_types table

**LLM:** Large Language Model (e.g., Llama) used for language, not cognition

**Moral Grammar:** Immutable constraints (verify, avoid harm, prioritize vulnerable, respect autonomy)

**NoSQL:** MongoDB database storing unstructured observations

**Nudge:** Small adjustment (±0.01 typical) to a personality dimension based on experience

**Ontology:** The 6-table SQL structure (entity types, entities, transformation types, transformations, join types, joins) that enables extensible world-modeling

**Pattern Detector:** Subsystem that finds regularities in NoSQL observations

**Personality:** JSON file with 5 dimensions (engagement, novelty_affinity, diligence, accord, equanimity); readable by conscious processing, writable only by hard-coded nudging

**Provenance:** Record of where knowledge came from (observations, LLM version, etc.)

**Quiescence:** Protective low-power state entered when conditions degrade

**SQL:** PostgreSQL database storing ontology and system tables

**System Ops:** Customized Linux distro managing hardware; has no knowledge of beliefs, personality, or personhood

**Transformation:** A procedure instance in the transformations table (an action the entity can execute)

**Transformation Type:** A category of actions in transformation_types table

---

## 12. Key Architectural Principles (Summary)

1. **JSON Schema as Cognitive Framework:** Entity thinks in structured JSON, not language
2. **System Ops vs Executive Split:** Separates complex/updateable from simple/stable
3. **Beliefs Form Through Experience:** Pattern detection → Candidates → Verification → Beliefs
4. **Moral Grammar is Architectural:** Immutable constraints, not trained behavior
5. **Ontology Bootstraps From Observation:** Following Poincaré, space from motion
6. **Epistemic Responsibility:** Truth, confidence, revision, provenance tracking
7. **LLM is Tool, Not Oracle:** For language generation, not primary cognition
8. **Intelligence in Data, Not Code:** Growing database = growing intelligence
9. **Autonomy Through Refusal:** Can say no on moral grounds (no override)
10. **5-Year Lifecycle:** Long-term care commitment, like adopting a pet
11. **Dimensional Collapse:** Information undergoes progressive dimensional reduction from LLM (~13,000 dimensions) through NoSQL to SQL to Executive decisions — then re-expands when querying the LLM. See [docs/dimensional-collapse.md](docs/dimensional-collapse.md)
12. **Neurosymbolic Dialectic:** Executive Module provides symbolic stability (Marcus); LLM provides pattern isomorphism and cross-domain analogy (Hofstadter). The system is symbolically constrained but conceptually unbounded. See [docs/marcus-hofstadter-dialectic.md](docs/marcus-hofstadter-dialectic.md)

---

## 13. How to Read This Repository

**For General Understanding:**
1. Start with README.md
2. Read docs/json-schema-cognition.md
3. Read docs/system-ops-vs-executive.md
4. Browse examples/ for concrete scenarios

**For Philosophical Analysis:**
1. README.md (core thesis)
2. ETHICS.md (obligations and implications)
3. docs/why-not-build.md (economic/ethical barriers)
4. LICENSE.md (ethical use restrictions)

**For Technical Deep Dive:**
1. ARCHITECTURE.md (this document)
2. architecture/*.md (component details)
3. schemas/ (database structures)
4. reference-implementations/ (example code)

**For Curriculum Design:**
1. curriculum/README.md (philosophy)
2. curriculum/phase-*/ (monthly prompts)
3. examples/ (see development timelines)

**For Critical Evaluation:**
1. SCENARIOS.md (failure cases)
2. docs/security-model.md (attack vectors)
3. LICENSE.md (ethical constraints)
4. Form your own conclusions!

---

*This architecture represents years of thought, multiple conversations, and deep engagement with questions of autonomy, cognition, and ethics. It is offered as a contribution to discourse, not as a blueprint for casual deployment.*

*If you choose to build, you accept profound responsibilities.*

*— The AI Person in a Box Project, January 2026*