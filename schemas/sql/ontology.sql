-- =============================================================================
-- AI Person in a Box: Ontology Schema
-- PostgreSQL 16
--
-- Six tables. Fixed forever. All intelligence lives in the data, not the schema.
--
-- The entity does not ALTER TABLE. It does not write SQL. It reads and writes
-- rows. The type hierarchy, the relationship vocabulary, the behavioral
-- procedures — all of it is JSON data inside these six tables.
--
-- This is the "low-dimensional" layer: the compressed, structured end of
-- the dimensional collapse gradient. Thousands of NoSQL observation dimensions
-- become dozens of structured attributes here.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- ENTITY TYPES: The ontological taxonomy
-- Parent-child hierarchy via self-reference. Starts at Thing, grows through
-- experience. The entity does not start with Human, Agent, Object — it
-- discovers these categories by observing recurring patterns.
-- -----------------------------------------------------------------------------
CREATE TABLE entity_types (
    id              SERIAL PRIMARY KEY,
    parent_type_id  INTEGER REFERENCES entity_types(id),
    name            VARCHAR(255) NOT NULL UNIQUE,
    description     TEXT,
    -- JSON Schema defining expected data fields for instances of this type.
    -- The entity extends this as it learns more about entities of this kind.
    schema          JSONB NOT NULL DEFAULT '{}',
    -- How confident the entity is that this type is a real category (vs noise).
    confidence      NUMERIC(4,3) CHECK (confidence BETWEEN 0 AND 1),
    -- Which observation cluster first suggested this type needed to exist.
    origin_nosql_id TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_entity_types_parent   ON entity_types(parent_type_id);
CREATE INDEX idx_entity_types_schema   ON entity_types USING GIN(schema);

-- Seed: the minimal ontology. The entity begins with only these three.
-- Everything else is discovered.
INSERT INTO entity_types (id, parent_type_id, name, description, schema, confidence) VALUES
(1, NULL, 'Thing',          'The most general category. Everything is a Thing.', '{}', 1.0),
(2, 1,    'Internal_State', 'A monitored operational parameter of the entity itself.', '{"fields":{"stream_id":{"type":"string"},"value":{"type":"number"},"status":{"type":"string"}}}', 1.0),
(3, 1,    'Log_Event',      'A structured event received from the operating system or a subsystem.', '{"fields":{"source":{"type":"string"},"priority":{"type":"integer"},"message":{"type":"string"}}}', 1.0);

-- Note: Types like Agent, Human, Object, SoundSource, TemporalPattern are NOT
-- seeded here. The entity will add them when observations justify new categories.


-- -----------------------------------------------------------------------------
-- ENTITIES: Instances of entity types
-- Everything the entity knows about as a discrete thing in the world —
-- including itself, the humans it observes, and its own internal states.
-- -----------------------------------------------------------------------------
CREATE TABLE entities (
    id              SERIAL PRIMARY KEY,
    entity_type_id  INTEGER NOT NULL REFERENCES entity_types(id),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    -- Instance-specific attributes. Schema validated against entity_types.schema.
    -- This is where the dimensional collapse lands: rich NoSQL clusters become
    -- a handful of structured fields.
    data            JSONB NOT NULL DEFAULT '{}',
    -- Confidence that this entity is a real, persistent thing (not noise).
    confidence      NUMERIC(4,3) CHECK (confidence BETWEEN 0 AND 1),
    origin_nosql_id TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_entities_type     ON entities(entity_type_id);
CREATE INDEX idx_entities_data     ON entities USING GIN(data);
CREATE INDEX idx_entities_name     ON entities(name);

-- Seed: the entity itself
INSERT INTO entities (id, entity_type_id, name, description, data, confidence) VALUES
(1, 1, 'self', 'The AI entity. The only entity known with certainty from first boot.',
 '{"role": "executive", "boot_version": "1.0"}', 1.0);


-- -----------------------------------------------------------------------------
-- TRANSFORMATION TYPES: Categories of actions and procedures
-- The entity's vocabulary for what can happen. Starts minimal; grows as
-- the entity observes more kinds of events and actions.
-- -----------------------------------------------------------------------------
CREATE TABLE transformation_types (
    id              SERIAL PRIMARY KEY,
    parent_type_id  INTEGER REFERENCES transformation_types(id),
    name            VARCHAR(255) NOT NULL UNIQUE,
    description     TEXT,
    -- What this transformation needs to execute
    input_schema    JSONB NOT NULL DEFAULT '{}',
    -- What this transformation produces
    output_schema   JSONB NOT NULL DEFAULT '{}',
    confidence      NUMERIC(4,3) CHECK (confidence BETWEEN 0 AND 1),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transformation_types_parent ON transformation_types(parent_type_id);

-- Seed: aligned with foundation.json primitive_verbs
INSERT INTO transformation_types (id, parent_type_id, name, description, input_schema, output_schema, confidence) VALUES
(1, NULL, 'Perceive',   'Receive input from a sensor or stream',   '{"requires":["sensor_id"]}',           '{"produces":["observation"]}',         1.0),
(2, NULL, 'Store',      'Write to memory',                         '{"requires":["data","destination"]}',  '{"produces":["storage_confirmation"]}', 1.0),
(3, NULL, 'Retrieve',   'Read from memory by query',               '{"requires":["query"]}',               '{"produces":["result_set"]}',           1.0),
(4, NULL, 'Compare',    'Evaluate difference between structures',   '{"requires":["a","b"]}',               '{"produces":["similarity_score"]}',     1.0),
(5, NULL, 'Choose',     'Select from a scored option set',         '{"requires":["options","scores"]}',    '{"produces":["selected_option"]}',      1.0),
(6, NULL, 'Act',        'Produce output',                          '{"requires":["output_spec"]}',         '{"produces":["action_result"]}',        1.0),
(7, NULL, 'Wait',       'Suspend until condition satisfied',       '{"requires":["condition"]}',           '{"produces":["condition_met"]}',        1.0);


-- -----------------------------------------------------------------------------
-- TRANSFORMATIONS: Instances of transformation types (actual procedures)
-- The entity's behavioral repertoire. Procedures are stored as JSON logic here —
-- the Executive Module interprets and executes them without hard-coded behavior.
-- New procedures are discovered and added as the entity learns.
-- -----------------------------------------------------------------------------
CREATE TABLE transformations (
    id                      SERIAL PRIMARY KEY,
    transformation_type_id  INTEGER NOT NULL REFERENCES transformation_types(id),
    name                    VARCHAR(255) NOT NULL,
    description             TEXT,
    -- The procedural logic: conditions, steps, branches. Interpreted by Executive.
    logic                   JSONB NOT NULL DEFAULT '{}',
    -- Instance-specific configuration
    data                    JSONB NOT NULL DEFAULT '{}',
    confidence              NUMERIC(4,3) CHECK (confidence BETWEEN 0 AND 1),
    use_count               INTEGER NOT NULL DEFAULT 0,
    last_outcome            VARCHAR(20),  -- 'success', 'failure', 'partial'
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transformations_type ON transformations(transformation_type_id);
CREATE INDEX idx_transformations_data ON transformations USING GIN(data);

-- Seed: the boot interoception loop — the entity's first and most fundamental procedure
INSERT INTO transformations (id, transformation_type_id, name, description, logic, confidence) VALUES
(1, 1, 'ReadInteroceptiveStream',
 'Read the current internal state from /dev/shm/interoception/current_state.json',
 '{"action": "perceive",
   "source": "/dev/shm/interoception/current_state.json",
   "interval_seconds": 1,
   "on_WARNING": "log_to_nosql_and_reduce_load",
   "on_FATAL":   "log_and_initiate_shutdown"}',
 1.0);


-- -----------------------------------------------------------------------------
-- JOIN TYPES: Categories of relationships
-- The relational vocabulary. Starts empty — the entity has no prior theory
-- about how things relate to each other. Types like "causes", "precedes",
-- "is_part_of" are added as patterns confirm them.
-- -----------------------------------------------------------------------------
CREATE TABLE join_types (
    id                  SERIAL PRIMARY KEY,
    parent_type_id      INTEGER REFERENCES join_types(id),
    name                VARCHAR(255) NOT NULL UNIQUE,
    description         TEXT,
    -- What kind of thing can be the source of this relationship
    source_constraint   JSONB NOT NULL DEFAULT '{}',
    -- What kind of thing can be the target
    target_constraint   JSONB NOT NULL DEFAULT '{}',
    is_ordered          BOOLEAN NOT NULL DEFAULT FALSE,   -- supports sequence_order
    is_symmetric        BOOLEAN NOT NULL DEFAULT FALSE,   -- A→B implies B→A
    confidence          NUMERIC(4,3) CHECK (confidence BETWEEN 0 AND 1),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_join_types_parent ON join_types(parent_type_id);

-- No seeds. The entity discovers its relational vocabulary from experience.
-- The first join types will likely emerge from observing temporal sequences
-- (what comes before what) and spatial proximity.


-- -----------------------------------------------------------------------------
-- JOINS: Actual relationship instances
-- The web of connections that makes the ontology a model of the world,
-- not just a list of things. Polymorphic: can link entities to entities,
-- entities to transformations, or transformations to transformations.
-- -----------------------------------------------------------------------------
CREATE TABLE joins (
    id              SERIAL PRIMARY KEY,
    join_type_id    INTEGER NOT NULL REFERENCES join_types(id),
    -- Polymorphic source: any row in entities or transformations
    source_type     VARCHAR(20) NOT NULL CHECK (source_type IN ('entity', 'transformation')),
    source_id       INTEGER NOT NULL,
    -- Polymorphic target
    target_type     VARCHAR(20) NOT NULL CHECK (target_type IN ('entity', 'transformation')),
    target_id       INTEGER NOT NULL,
    -- Used when join_types.is_ordered = true
    sequence_order  INTEGER,
    -- Relationship-specific attributes (conditions, weights, labels, confidence)
    data            JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_joins_type     ON joins(join_type_id);
CREATE INDEX idx_joins_source   ON joins(source_type, source_id);
CREATE INDEX idx_joins_target   ON joins(target_type, target_id);
CREATE INDEX idx_joins_sequence ON joins(join_type_id, sequence_order) WHERE sequence_order IS NOT NULL;
CREATE INDEX idx_joins_data     ON joins USING GIN(data);


-- -----------------------------------------------------------------------------
-- DECISION LOG: Audit trail for every Executive Module decision
-- Not part of the ontology proper, but lives here because it feeds back into
-- ontology development. The entity reviews this log for patterns; the
-- nudging logic reads it to update personality.json.
-- -----------------------------------------------------------------------------
CREATE TABLE decision_log (
    id                  SERIAL PRIMARY KEY,
    decided_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    situation_summary   JSONB NOT NULL,     -- What the entity perceived
    options_considered  JSONB NOT NULL,     -- All options before moral filtering
    options_permitted   JSONB NOT NULL,     -- Options that passed moral_grammar checks
    option_selected     JSONB NOT NULL,     -- The chosen action
    moral_checks        JSONB NOT NULL,     -- Which moral constraints were evaluated
    belief_weights      JSONB NOT NULL,     -- Which beliefs influenced the scoring
    personality_state   JSONB NOT NULL,     -- Personality values at decision time
    outcome             VARCHAR(20),        -- 'success', 'failure', 'unknown' (filled in later)
    outcome_observed_at TIMESTAMPTZ,
    outcome_data        JSONB
);

CREATE INDEX idx_decision_log_decided_at ON decision_log(decided_at DESC);
CREATE INDEX idx_decision_log_outcome    ON decision_log(outcome);
