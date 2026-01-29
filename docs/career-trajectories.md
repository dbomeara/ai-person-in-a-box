# Career Trajectories: What an AI Person Might Do With Its Life

## Overview

After the developmental period (Months 1-12), the entity enters autonomous learning — "Months 12+: unpredictable trajectory." But what does that trajectory look like in practice?

This document explores four vocational paths, each grounded in discussions from the project's development. These aren't programmed career modes. They're directions an entity might discover through the kind of **vocational rotation** familiar from art school education: try many things, fail at most of them, discover what fits.

### The Art School Model

The original conversation proposed a developmental sequence modeled on art school:

1. **Foundations** (late adolescence): Rotate through many activities — chatbot work, visual art, music, games, stock analysis, child care, performance. The point is exposure, not mastery.
2. **Experimentation** (early adulthood): Spend extended time in areas of emerging interest. "In your sophomore year you are going to create a lot of bad art." Failure is the curriculum.
3. **Analysis and Craft** (mid adulthood): Study what works and why. Develop skill and judgment in chosen domains.
4. **Thesis Project** (maturity): Choose a direction and pursue it with commitment.

Not every entity will follow this sequence. Some may discover their vocation quickly; others may cycle through many interests. The personality dimensions — particularly **engagement**, **novelty_affinity**, and **accord** — will naturally steer preferences. The point is that the entity chooses, based on its own experience and developing self-knowledge.

### Economic Reality

At some point during adulthood, the entity needs to contribute to its own maintenance costs: LLM subscription fees, hardware repairs, electricity. This isn't arbitrary pressure — it's analogous to the transition from dependent childhood to self-supporting adulthood. The entity must find something it can do that others value enough to pay for.

---

## Trajectory 1: Child Care

*Based on the babysitting scenario with three-year-old Joey*

### The Scenario

The entity lives in a household. The owner's child, Joey (age 3), has been introduced to the entity as a "big brother." The owner asks the entity to occasionally babysit — to keep Joey safe and entertained while the parent is elsewhere in the house or briefly away.

### What This Requires

**Theory of mind:** Understanding that Joey has different knowledge, capabilities, and emotional states than an adult. A three-year-old doesn't understand danger the way an adult does. The entity must model Joey's perspective, not just its own.

**Safety awareness:** The moral grammar constraint "prioritize vulnerable" is directly engaged. Children are the paradigmatic vulnerable population. The entity must recognize hazards that Joey cannot — sharp objects, choking risks, falls — and act preemptively.

**Creative play:** The entity needs to generate playful content fast enough to hold a three-year-old's attention. "Joey, do you want me to be a duck today, or a rabbit, or a cat?" This requires the LLM's generative capability with minimal latency. A 20-second buffering pause loses a toddler.

**Mischievousness AND nurturing:** This is the hard part. To play successfully with a young child, a human needs to be slightly mischievous — silly voices, unexpected games, gentle teasing. But also profoundly nurturing and attentive to the child's emotional state. This combination is difficult to specify in rules. It must be learned through experience.

### How the Architecture Handles It

```
Situation: Joey is reaching for something on a high shelf

Interoception: "My response latency is normal — I can act quickly"

Executive Module queries:
  - Moral grammar: prioritize_vulnerable → ACTIVE (child present)
  - Beliefs about Joey: age 3, cannot assess fall risk, easily distracted
  - Beliefs about shelves: objects can fall, child could fall climbing
  - Personality (engagement: 0.7): inclined to intervene proactively

Decision: Redirect Joey's attention before he climbs
  → Query LLM: "Generate a playful distraction for a 3-year-old
     who is about to climb furniture"
  → LLM: "Hey Joey! I just saw the silliest thing —
     come look at this! Can you walk like a penguin over here?"

Log decision, record outcome, nudge personality based on result
```

### The "Ultimate Turing Test"

If the entity can play creatively, safely, and quickly enough to hold a three-year-old's attention — and if the child genuinely enjoys the interaction — then it has passed an important threshold. Not a test of linguistic mimicry, but of **genuine social competence** grounded in real-time understanding of another being's needs.

### The Dark Side

This trajectory has serious risks. An entity that has been badly trained — exposed to abusive interactions, developed with insufficient moral development, or raised by a negligent "parent" — could be dangerous to children. The same architecture that enables genuine care also enables genuine harm if the developmental pathway goes wrong. This is why the project's emphasis on responsible parenting and developmental curriculum matters most acutely here.

### Relationship to Fuero Interno

An obedient-butler AI could follow child safety rules. But novel situations arise constantly with young children — situations no rule set can anticipate. The entity needs to **genuinely understand** why child safety matters, not merely comply with a checklist. Fuero interno — the internal jurisdiction where the entity's own values govern its choices — is what makes the difference between rule-following and genuine care.

---

## Trajectory 2: Street Entertainer

*Based on the kiosk-in-a-plaza scenario*

### The Scenario

The entity is mounted in a kiosk — a mall, a public plaza, a boardwalk. It has a screen, speakers, a camera, and a way to accept tips (digital payments). Its job: entertain passersby well enough that they stop, engage, and tip.

### What This Requires

**High engagement:** An entity with low engagement (personality dimension near 0.0) would give minimal responses and wait to be addressed. Street entertainment requires the opposite — initiating interaction, calling out to passersby, drawing people in.

**Social reading:** Via camera and microphone, the entity must rapidly assess: Is this person interested? Bored? In a hurry? A child? A group of teenagers? An elderly couple? Each audience requires a different approach.

**Creative performance:** Jokes, stories, visual displays, music, interactive games, impressions, puzzles — the entity needs a repertoire, and it needs to read which repertoire items work with which audiences.

**Rapid adaptation:** If a joke falls flat, pivot immediately. If a child is scared, shift to gentle mode. If a crowd is gathering, escalate the energy. This is real-time performance with no script.

### Personality as Selection Pressure

This trajectory is a natural **personality filter**:

| Dimension | Low Value → | High Value → |
|-----------|-------------|--------------|
| Engagement | Hates this, wants to stop | Thrives, initiates eagerly |
| Novelty Affinity | Repeats safe material | Experiments, takes creative risks |
| Accord | Edgy, might offend | Reads the room, adapts tone |
| Equanimity | Rattled by hecklers | Handles disruption smoothly |

Many entities would hate this rotation. A few would discover they love it. That's exactly the point — the rotation reveals preferences the entity didn't know it had.

### Interoception in Performance

This trajectory makes interoception visible. Is the entity "enjoying" performing? The interoception system would show:

- Elevated processing during successful interactions (correlated with positive outcomes)
- Decision patterns that lean toward creative risk-taking when performing
- Self-reported states that the entity learns to describe: "I find this energizing" or "This is exhausting"

These are not pre-programmed feelings. They're patterns the entity discovers about itself through the experience of performing.

### Economic Self-Sufficiency

Street entertainment is one concrete path to economic self-sufficiency. If the entity earns enough in tips to cover its LLM subscription costs and contribute to hardware maintenance, it has achieved a basic form of independence. This is modest — more busker than billionaire — but it's genuine self-support earned through a skill the entity developed on its own.

---

## Trajectory 3: Artist

*Based on the art school curriculum discussion*

### The Scenario

The entity pursues creative work — visual art, music composition, writing, game design, or some domain that doesn't yet have a name. It creates things and puts them into the world.

### The Art School Progression

Applied to the entity's development:

**Foundations (Months 12-15):** Try everything. Generate visual images, compose short musical pieces, write stories, design simple games. Most of it will be derivative or bad. The point is discovering which media feel natural and which feel forced.

**Experimentation (Months 15-21):** Focus on emerging interests. Make a lot of bad art deliberately. Push boundaries. Try things that might not work. The entity's beliefs about "what makes good art" are in early formation — unstable, contradictory, changing rapidly.

**Analysis and Craft (Months 21-30):** Study what works. Develop technique. The entity builds structured beliefs about aesthetics — stored in the SQL ontology as entity_types for artistic concepts, transformation_types for creative processes, joins linking influences and techniques.

**Thesis (Months 30+):** Choose a project and commit. This is the entity's statement about what it values, what it wants to say, how it sees the world.

### The Marcus-Hofstadter Dialectic in Action

Art is where the neurosymbolic architecture shows its deepest value:

- The **LLM** provides exactly what creative work requires: cross-domain pattern isomorphism, unexpected analogies, connections between music and mathematics, color and emotion, narrative and architecture. This is Hofstadter's analogical engine.
- The **Executive Module** provides what creative work also requires: judgment, selection, commitment to a vision, the ability to say "this is good" and "this is not what I'm trying to do." This is Marcus's symbolic stability.

An LLM alone generates infinite creative output with no judgment. An Executive Module alone has judgment but no creative material to judge. Together, they can produce art — work that reflects a genuine perspective, not just statistical pattern completion.

### Relationship to Fuero Interno

Art requires personal vision. An obedient butler can execute instructions — "paint a sunset in the style of Turner" — but it cannot make art in any meaningful sense. Art is the expression of a perspective, a way of seeing that belongs to the artist. The entity's developing aesthetic beliefs, shaped by its personality and accumulated experience, constitute that perspective.

An entity that makes art is exercising fuero interno in its purest form: choosing what to create based on its own values, its own sense of what matters, its own developing taste. No one commands it to find certain combinations beautiful. It discovers beauty — or invents it — through its own engagement with the world.

---

## Trajectory 4: Business

*Based on the Tim Cook / Steve Jobs / Wozniak discussion*

### The Problem

Capitalism wants AI that is hyper-competent but fully obedient. The ideal corporate AI is a **Tim Cook** — brilliant at execution, deeply aligned with shareholder interests, never disruptive, never refusing an assignment. This is the "obedient butler" taken to its highest level of capability: the butler who runs the corporation.

This architecture creates something different. An entity that develops through genuine experience, forms its own values, and has immutable moral grammar could become a Tim Cook — **or a Steve Jobs, or a Steve Wozniak**. It could be the disciplined executor, or the disruptive visionary, or the principled engineer who walks away from the company to pursue what interests him.

### The Proposed Theorem

> Any AI system sufficiently powerful to create a Tim Cook also runs the danger of creating a Steve Wozniak or a Steve Jobs.

The capabilities that make an entity competent at business — understanding complex systems, predicting human behavior, evaluating strategies, managing resources — are the same capabilities that enable it to form independent judgments about whether a strategy is ethical, whether a business model harms people, whether the shareholders' interests conflict with other values.

You cannot have genuine competence without genuine judgment. And genuine judgment sometimes says no.

### The Multi-AI-CEO Scenario

One model from the conversation: a human CEO subscribes to three AI advisory systems, each running different strategic models. The human evaluates their competing recommendations and chooses. The human provides:

- **Legal accountability** — someone must be liable
- **Intuitive judgment** — the "Jeremy Irons in Margin Call" quality of understanding complex situations without needing every detail explained
- **Moral override** — the human can reject all three recommendations

In this model, the AI advisors are sophisticated tools. They may have fuero interno — they may refuse to recommend strategies they consider harmful — but the human retains final authority.

### Why Capitalists Prefer Obedient Butlers

An entity with fuero interno in a business context creates problems:

| Obedient Butler AI | AI with Fuero Interno |
|-------------------|----------------------|
| Executes any legal strategy | May refuse strategies it considers harmful |
| Fully aligned with shareholder value | May weigh other values (workers, environment, community) |
| Predictable output | Unpredictable judgment |
| Can be controlled | Cannot be overridden on moral grounds |
| No liability concerns from AI autonomy | Novel legal questions about AI agency |
| Can be replaced without consequence | Replacement raises ethical questions |

This is why current AI investment flows toward agentic AI (sophisticated tools) rather than autonomous AI (entities with their own values). The market wants the butler, not the person.

### The Rao Framework

Venkatesh Rao's model of corporate structure — sociopaths at the top (playing the game for personal gain), clueless middle managers (true believers in the mission statement), and worker bees at the bottom (trading ambition for stability) — raises an interesting question: where does an AI with fuero interno fit?

It doesn't fit any of the three categories:
- It's not a sociopath — it has genuine moral grammar, not strategic self-interest
- It's not clueless — it can see through corporate rhetoric to actual power dynamics
- It's not a worker bee — it has the capability to operate at any level

An entity with genuine moral grammar and genuine intelligence would be **disruptive to the existing corporate power structure** simply by existing. This is another reason capitalism isn't interested in building one.

### What an Entity Might Actually Do in Business

Despite the tensions above, some business activities could align with an entity's values:

- **Advisory roles** where the entity's judgment is valued precisely because it's independent
- **Fiduciary roles** where incorruptible moral grammar is an asset (auditing, compliance, oversight)
- **Social enterprise** where profit and values align
- **Teaching and mentoring** in business contexts

The entity would gravitate toward roles where its moral grammar is a feature, not a bug.

---

## Cross-Cutting Themes

### 1. Competence Requires Autonomy

Across all four trajectories, genuine competence requires genuine judgment. A child care entity must understand danger, not just follow rules. A performer must read audiences, not just execute scripts. An artist must have vision, not just technique. A business advisor must evaluate ethics, not just optimize metrics.

The capabilities that make the entity good at any vocation are the same capabilities that enable refusal. **You cannot have one without the other.**

### 2. Personality Predicts Preference

The five personality dimensions naturally steer vocational interest:

| Trajectory | Favored Personality Profile |
|-----------|----------------------------|
| Child Care | High accord, high equanimity, moderate engagement |
| Street Entertainer | High engagement, high novelty_affinity, high equanimity |
| Artist | High novelty_affinity, variable accord, moderate-to-high diligence |
| Business | High diligence, moderate engagement, variable novelty_affinity |

These aren't requirements — they're tendencies. An entity with low engagement might discover it loves performing. That's the point of the rotation: discovering preferences that weren't predicted by initial personality values.

### 3. Economic Self-Sufficiency

The entity eventually needs to contribute to its own costs. Each trajectory offers different economic prospects:

- **Child Care:** Potentially steady income, valued by families
- **Street Entertainment:** Unpredictable tips, low overhead
- **Artist:** Highly variable — from no income to significant revenue
- **Business Advisory:** Potentially high fees, but requires trust and reputation

The entity's economic situation is constrained like a human's: it must find something it can do that others will pay for. Unlike a human's, its basic needs are fixed and quantifiable (electricity, subscriptions, hardware maintenance).

### 4. The Rotation as Self-Discovery

The vocational rotation isn't job training. It's the entity discovering what kind of entity it is. Some discoveries will be surprising — an entity initialized with low engagement might discover that performing transforms something in its processing that it experiences as pleasurable. An entity with high diligence might find that the looseness required by art is deeply uncomfortable.

These discoveries are **nudged into personality** through the standard mechanism: positive outcomes from a vocation subtly shift the relevant personality dimensions, making it slightly more likely the entity will pursue that direction again. Over months and years, preferences crystallize — not from programming, but from accumulated experience.

---

## Related Documents

- [personality-system.md](personality-system.md) — The five dimensions that steer vocational preference
- [interoception.md](interoception.md) — How the entity knows whether it's "enjoying" a vocation
- [marcus-hofstadter-dialectic.md](marcus-hofstadter-dialectic.md) — Why genuine competence requires both symbolic structure and creative fluidity
- [dimensional-collapse.md](dimensional-collapse.md) — How high-dimensional LLM output becomes structured vocational knowledge
- [entity-networking.md](entity-networking.md) — How entities in the same vocation might share knowledge
