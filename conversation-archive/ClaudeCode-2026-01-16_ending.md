
I"m thinking, but I'm not sure, that the Entities and Transformations table should be empty at Day 0 bootup. I suspect, and I'm also not sure about this, that the other 4 of the ontology tables may need to be prepopulated with simple entity types, simple transformation types, simple joins and simple join types.
That's a thoughtful distinction. Let me reason through it with you.

The Intuition
Entities and Transformations are instances - specific things and specific actions. At Day 0, the system hasn't encountered anything yet, so there's nothing to record. Empty makes sense.

The Type tables (EntityTypes, TransformationTypes, JoinTypes) and Joins are different. They define what kinds of things can exist and how things can relate. Without some minimal structure here, the system has no vocabulary to even begin categorizing its first observations.

The Question
How minimal can the prepopulated types be while still enabling the system to bootstrap?

A Possible Minimal Seed
EntityTypes (3 rows):

id	parent_type_id	name	description
1	null	thing	Base type for all entities
2	1	pattern	A recurring observable regularity
3	1	event	Something that happens
TransformationTypes (2 rows):

id	parent_type_id	name	description
1	null	action	Base type for all transformations
2	1	observation	Recording something perceived
JoinTypes (3 rows):

id	name	is_ordered	is_symmetric	description
1	related_to	false	true	Generic relationship
2	instance_of	false	false	Entity is instance of type
3	follows	true	false	Temporal/causal sequence
Joins: Empty (no relationships exist yet between things that don't exist)

The Alternative View
Maybe even this is too much. Perhaps:

Only one EntityType: thing
Only one TransformationType: action
Only one JoinType: related_to
And the system discovers finer distinctions (pattern vs. event, follows vs. related_to) through experience?

The Tension
More prepopulated	Less prepopulated
Faster bootstrap	Purer emergence
Risk: imposing structure	Risk: can't start at all
Like giving a child words	Like expecting language invention
My Uncertainty
I'm not sure either. The question might be: what's the minimum the Executive needs to make its first observation useful?

If the system perceives something, it needs to be able to:

Create an Entity (needs at least one EntityType)
Record that it observed it (needs at least one TransformationType)
Maybe link them (needs at least one JoinType)
So perhaps the absolute minimum is one of each type table - just enough grammar to form the first sentence.

What's your instinct? Do you lean toward minimal (1 each) or slightly richer (3-5 each)?