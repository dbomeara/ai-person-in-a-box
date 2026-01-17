# Ontology Database Schema

## Overview

This document specifies the database architecture that enables the AI entity to build and extend its own ontology. The design follows a key principle: **a small set of fixed tables enables the construction of arbitrarily complex conceptual structures**.

The system consists of:
- **6 SQL tables** for the extensible ontology (read/write by conscious processing)
- **3 JSON files** for foundational structures:
  - foundation.json (immutable primitives, read-only)
  - moral_grammar.json (immutable constraints, read-only)
  - personality.json (readable by conscious processing, writable only by hard-coded nudging logic)

---

## Design Philosophy

### Why This Architecture?

**The entity designs its own schema** - but not by writing SQL. Instead:
- The 6 ontology tables are fixed "physics" - unchanging rules
- Everything else is "chemistry" - emergent structures built from primitives
- JSON `data` columns provide schema-free extension
- Types define structure; instances hold data

**Separation of concerns:**
| Component | Storage | Access | Purpose |
|-----------|---------|--------|---------|
| Foundation | JSON file | Read-only | Primitive vocabulary |
| Moral Grammar | JSON file | Read-only | Immutable constraints |
| Personality | JSON file | Read by conscious, written by hard-coded nudging | Behavioral biases |
| Ontology | SQL tables | Read/Write by conscious processing | Learned knowledge and structure |

**Why JSON for primitives?**
- Immutability is architectural (file isn't written to)
- Loads before database - provides vocabulary to interpret data
- No permissions/triggers needed to enforce read-only
- Clear separation: primitives aren't "data the system creates"

**Why JSON columns in SQL?**
- Executive Model just reads/writes key-value pairs
- No ALTER TABLE, no dynamic SQL, no schema introspection
- Field definitions live in Type tables' `schema` column
- Actual values live in instance tables' `data` column
- JSON is essentially "a database rendered in sparse syntax"

---

## Foundation: Immutable Primitives

**File:** `schemas/json-schema/foundation.json`

```json
{
  "version": "1.0",

  "primitive_verbs": [
    {"id": "perceive", "description": "Receive input"},
    {"id": "store", "description": "Write to memory"},
    {"id": "retrieve", "description": "Read from memory"},
    {"id": "compare", "description": "Evaluate difference"},
    {"id": "choose", "description": "Select from options"},
    {"id": "act", "description": "Produce output"},
    {"id": "wait", "description": "Suspend pending condition"}
  ],

  "system_status_codes": [
    {"id": "OFFLINE", "description": "System not running"},
    {"id": "STARTING", "description": "System initializing"},
    {"id": "NORMAL", "description": "Operating within parameters"},
    {"id": "ALERT", "description": "Condition requires attention"},
    {"id": "WARNING", "description": "Condition may cause failure"},
    {"id": "ERROR", "description": "Operation failed"},
    {"id": "FATAL", "description": "System cannot continue"}
  ],

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

### What's Included vs. Excluded

**Included (given at birth):**
- Raw verbs (what the system *can* do)
- System status codes (what the OS *tells* it)
- Monitor stream definitions (what metrics exist)

**Excluded (discovered through experience):**
- Human-analogous states ("hunger", "curiosity")
- Semantic relationships ("is_a", "causes", "before")
- Abstract types ("thing", "event", "agent")
- Emotional interpretations of status codes

The system learns that `WARNING` after low `token_balance` feels like something - it builds that association through experience, not from a provided mapping.

---

## Ontology Tables (6 Tables)

### Entity Types

Categories and classes of entities.

```sql
CREATE TABLE entity_types (
    id              SERIAL PRIMARY KEY,
    parent_type_id  INTEGER REFERENCES entity_types(id),
    name            VARCHAR(255) NOT NULL UNIQUE,
    description     TEXT,
    schema          JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for hierarchy traversal
CREATE INDEX idx_entity_types_parent ON entity_types(parent_type_id);
```

**Fields:**
- `parent_type_id`: Enables type hierarchy (e.g., Human → Agent → Thing)
- `schema`: JSON Schema defining expected fields for instances of this type

**Example `schema`:**
```json
{
  "fields": {
    "hair_color": {"type": "string", "enum": ["brown", "black", "blonde", "red", "gray", "white"]},
    "birth_date": {"type": "date"},
    "height_cm": {"type": "number", "min": 0, "max": 300}
  },
  "required": ["birth_date"]
}
```

---

### Entities

Instances of entity types.

```sql
CREATE TABLE entities (
    id              SERIAL PRIMARY KEY,
    entity_type_id  INTEGER NOT NULL REFERENCES entity_types(id),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    data            JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_entities_type ON entities(entity_type_id);
CREATE INDEX idx_entities_data ON entities USING GIN(data);
```

**Fields:**
- `entity_type_id`: What kind of thing this is
- `data`: Instance-specific attributes (validated against type's schema)

**Example `data`:**
```json
{
  "hair_color": "brown",
  "birth_date": "1985-03-15",
  "height_cm": 180,
  "preferred_language": "English"
}
```

---

### Transformation Types

Categories of actions and operations.

```sql
CREATE TABLE transformation_types (
    id              SERIAL PRIMARY KEY,
    parent_type_id  INTEGER REFERENCES transformation_types(id),
    name            VARCHAR(255) NOT NULL UNIQUE,
    description     TEXT,
    input_schema    JSONB DEFAULT '{}',
    output_schema   JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transformation_types_parent ON transformation_types(parent_type_id);
```

**Fields:**
- `input_schema`: What this type of transformation requires
- `output_schema`: What this type of transformation produces

**Example:**
```json
// input_schema for "Conversation Action"
{
  "requires": ["conversation_state", "participant_list"]
}

// output_schema
{
  "produces": ["updated_conversation_state", "optional_message"]
}
```

---

### Transformations

Instances of transformation types (specific actions/procedures).

```sql
CREATE TABLE transformations (
    id                      SERIAL PRIMARY KEY,
    transformation_type_id  INTEGER NOT NULL REFERENCES transformation_types(id),
    name                    VARCHAR(255) NOT NULL,
    description             TEXT,
    logic                   JSONB DEFAULT '{}',
    data                    JSONB DEFAULT '{}',
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transformations_type ON transformations(transformation_type_id);
CREATE INDEX idx_transformations_data ON transformations USING GIN(data);
```

**Fields:**
- `logic`: The procedure definition (rules, prompts, references)
- `data`: Instance-specific configuration

**Example `logic`:**
```json
{
  "action": "evaluate",
  "conditions": ["is_farewell", "is_timeout", "needs_escalation"],
  "on_true": {"next": "end_conversation"},
  "on_false": {"next": "continue_flow"}
}
```

---

### Join Types

Categories of relationships between entities/transformations.

```sql
CREATE TABLE join_types (
    id                  SERIAL PRIMARY KEY,
    parent_type_id      INTEGER REFERENCES join_types(id),
    name                VARCHAR(255) NOT NULL UNIQUE,
    description         TEXT,
    source_constraint   JSONB DEFAULT '{}',
    target_constraint   JSONB DEFAULT '{}',
    is_ordered          BOOLEAN DEFAULT FALSE,
    is_symmetric        BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_join_types_parent ON join_types(parent_type_id);
```

**Fields:**
- `source_constraint`: What can be a valid source for this relationship
- `target_constraint`: What can be a valid target
- `is_ordered`: Does this relationship support sequencing?
- `is_symmetric`: Does A→B imply B→A?

**Example:**
```json
// "FlowsTo" join type
{
  "name": "FlowsTo",
  "source_constraint": {"type": "transformation"},
  "target_constraint": {"type": "transformation"},
  "is_ordered": true,
  "is_symmetric": false
}
```

---

### Joins

Actual relationship instances.

```sql
CREATE TABLE joins (
    id              SERIAL PRIMARY KEY,
    join_type_id    INTEGER NOT NULL REFERENCES join_types(id),
    source_type     VARCHAR(20) NOT NULL CHECK (source_type IN ('entity', 'transformation')),
    source_id       INTEGER NOT NULL,
    target_type     VARCHAR(20) NOT NULL CHECK (target_type IN ('entity', 'transformation')),
    target_id       INTEGER NOT NULL,
    sequence_order  INTEGER,
    data            JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for relationship queries
CREATE INDEX idx_joins_type ON joins(join_type_id);
CREATE INDEX idx_joins_source ON joins(source_type, source_id);
CREATE INDEX idx_joins_target ON joins(target_type, target_id);
CREATE INDEX idx_joins_sequence ON joins(join_type_id, sequence_order);
CREATE INDEX idx_joins_data ON joins USING GIN(data);
```

**Fields:**
- `source_type`/`target_type`: Polymorphic - can link entities or transformations
- `sequence_order`: For ordered relationships (flows, sequences)
- `data`: Relationship-specific attributes (conditions, weights, labels)

**Example `data`:**
```json
{
  "condition": "is_farewell OR is_timeout",
  "label": "exit condition met"
}
```

---

## Personality (JSON File, Not SQL)

See [personality-system.md](personality-system.md) for full details.

Personality is stored as a **JSON file**, not a SQL table. This is simpler and makes the access control clearer.

**File:** `personality.json`

```json
{
  "version": "1.0",
  "initialized_at": "2026-01-17T10:00:00Z",
  "dimensions": {
    "engagement": {"value": 0.33, "initial_value": 0.33, "last_nudge": -0.002, ...},
    "novelty_affinity": {"value": 0.71, ...},
    "diligence": {"value": 0.55, ...},
    "accord": {"value": 0.48, ...},
    "equanimity": {"value": 0.62, ...}
  }
}
```

**Key characteristics:**
- **Readable by conscious processing** - The Executive can see its own personality values
- **Not directly writable** - Change only happens through hard-coded nudging logic
- **Part of Executive Module** - Not managed by System Ops (which is just an OS)

---

## Complete Schema Summary

```
┌─────────────────────────────────────────────────────────────────┐
│  JSON FILES (Executive Module manages these)                    │
│                                                                 │
│  foundation.json         (Read-only - immutable primitives)     │
│  moral_grammar.json      (Read-only - immutable constraints)    │
│  personality.json        (Read by conscious, nudged by hard-coded)
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ inform
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  SQL ONTOLOGY (Read/Write by conscious processing)              │
│                                                                 │
│  ┌─────────────┐    ┌─────────────────────┐    ┌────────────┐  │
│  │ EntityTypes │    │ TransformationTypes │    │ JoinTypes  │  │
│  │ (classes)   │    │ (action classes)    │    │ (relation  │  │
│  │             │    │                     │    │  classes)  │  │
│  └──────┬──────┘    └──────────┬──────────┘    └─────┬──────┘  │
│         │                      │                      │         │
│         │ instances            │ instances            │ instances
│         ▼                      ▼                      ▼         │
│  ┌─────────────┐    ┌─────────────────────┐    ┌────────────┐  │
│  │  Entities   │◄───┤   Transformations   │◄───┤   Joins    │  │
│  │ (things)    │    │   (actions)         │    │ (links)    │  │
│  └─────────────┘    └─────────────────────┘    └────────────┘  │
│         ▲                      ▲                      │         │
│         └──────────────────────┴──────────────────────┘         │
│                         connected by                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ decisions logged to
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  decision_log table (SQL)                                       │
│  - Records decisions with personality/moral/belief weights      │
│  - Used by conscious processing for spaced repetition review    │
│  - Used by hard-coded logic for personality nudging             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example: Modeling a Conversation Flow

### 1. Define Types

**EntityTypes:**
| id | parent_type_id | name | schema |
|----|----------------|------|--------|
| 1 | null | Thing | `{}` |
| 2 | 1 | Agent | `{"fields": {"capabilities": {"type": "array"}}}` |
| 3 | 2 | Human | `{"fields": {"name": {"type": "string"}}}` |
| 4 | 2 | AI_System | `{"fields": {"model": {"type": "string"}}}` |
| 5 | 1 | Conversation | `{"fields": {"status": {"type": "string"}}}` |
| 6 | 1 | Message | `{"fields": {"content": {"type": "string"}}}` |

**TransformationTypes:**
| id | name | input_schema | output_schema |
|----|------|--------------|---------------|
| 1 | ConversationAction | `{"requires": ["conversation_state"]}` | `{"produces": ["conversation_state"]}` |
| 2 | Listen | `{"requires": ["incoming_message"]}` | `{"produces": ["parsed_intent"]}` |
| 3 | Respond | `{"requires": ["response_plan"]}` | `{"produces": ["outgoing_message"]}` |

**JoinTypes:**
| id | name | is_ordered | is_symmetric |
|----|------|------------|--------------|
| 1 | ParticipatesIn | false | false |
| 2 | FlowsTo | true | false |
| 3 | OnCondition | true | false |

### 2. Create Flow Template

**Transformations:**
| id | type_id | name | logic |
|----|---------|------|-------|
| 1 | 2 | ReceiveInput | `{"action": "await_input"}` |
| 2 | 1 | ParseIntent | `{"action": "analyze"}` |
| 3 | 1 | Evaluate | `{"action": "check_conditions"}` |
| 4 | 3 | Respond | `{"action": "compose"}` |

**Joins (the flow arrows):**
| join_type_id | source_id | target_id | sequence_order | data |
|--------------|-----------|-----------|----------------|------|
| 2 | 1 | 2 | 1 | `{"label": "input received"}` |
| 2 | 2 | 3 | 2 | `{"label": "intent parsed"}` |
| 3 | 3 | 4 | 3 | `{"condition": "continue"}` |
| 2 | 4 | 1 | 4 | `{"label": "loop back"}` |

### 3. Visual Result

```
    ┌──────────────┐
    │ ReceiveInput │ ◄────────────────┐
    └──────┬───────┘                  │
           │ (1)                      │
           ▼                          │
    ┌──────────────┐                  │
    │  ParseIntent │                  │
    └──────┬───────┘                  │
           │ (2)                      │
           ▼                          │
    ┌──────────────┐                  │
    │   Evaluate   │                  │
    └──────┬───────┘                  │
           │ (3) [continue]           │
           ▼                          │
    ┌──────────────┐                  │
    │   Respond    ├──────────────────┘
    └──────────────┘      (4)
```

---

## Executive Model Operations

The Executive Module needs only basic CRUD operations:

### Create
```sql
-- New entity
INSERT INTO entities (entity_type_id, name, data)
VALUES (3, 'User-Sarah', '{"name": "Sarah", "preferred_language": "English"}');

-- New relationship
INSERT INTO joins (join_type_id, source_type, source_id, target_type, target_id, data)
VALUES (1, 'entity', 101, 'entity', 103, '{"role": "participant"}');
```

### Read
```sql
-- Find all humans
SELECT * FROM entities e
JOIN entity_types t ON e.entity_type_id = t.id
WHERE t.name = 'Human';

-- Find flow from a transformation
SELECT * FROM joins
WHERE source_type = 'transformation' AND source_id = 3
ORDER BY sequence_order;

-- Query JSON data
SELECT * FROM entities
WHERE data->>'preferred_language' = 'English';
```

### Update
```sql
-- Update entity data
UPDATE entities
SET data = jsonb_set(data, '{status}', '"ended"')
WHERE id = 103;
```

### Delete
```sql
-- Remove relationship
DELETE FROM joins WHERE id = 105;
```

No dynamic SQL. No ALTER TABLE. No schema design. The ontology grows through *data*, not schema changes.

---

## Boot Sequence

1. **Load foundation.json** → System has primitive vocabulary
2. **Connect to PostgreSQL** → Access ontology tables
3. **Initialize personality** (if first boot) → Random values clustered around 0.5
4. **Executive Module starts** → Can query/modify ontology, influenced by personality

Foundation terms can be referenced in database records by string ID. The foundation remains external and immutable; the database extends but never modifies it.

---

## Migration Notes

This schema is designed for PostgreSQL 16 LTS. Key features used:
- `JSONB` for flexible attribute storage with indexing
- `GIN` indexes for efficient JSON queries
- `CHECK` constraints for enum-like validation
- Self-referential foreign keys for hierarchies

For the thought experiment, exact SQL syntax matters less than the conceptual architecture. Any database supporting JSON columns and foreign keys could implement this design.
