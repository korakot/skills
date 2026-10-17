# GLOSSARY.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account

**Anchor**:
The source paragraph an index entry points into. See [alignment](./alignment.md).
_Also_: จุดยึด
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General concepts of the field (in code: timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general one? Only the former belongs.
- **Link, don't restate.** When a wiki page explains the concept, end the definition with a link to it. The page holds the detail; the glossary holds the one-line meaning.
- **Other-language forms go under `_Also_`, not `_Avoid_`.** In a project that works across languages (Thai and English, say), the same concept's established term in the other language is a sanctioned equivalent, not a rejected synonym. `_Avoid_` stays for words that blur the concept.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

**Single context (most repos):** One `GLOSSARY.md` beside the repo's entry point: `wiki/GLOSSARY.md` next to `wiki/index.md` in a wiki repo, the repo root otherwise.

**Multiple contexts:** A `GLOSSARY-MAP.md` in that same place lists the contexts, where they live, and how they relate to each other:

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The skill infers which structure applies:

- If `GLOSSARY-MAP.md` exists, read it to find contexts
- If only a single `GLOSSARY.md` exists, single context
- If neither exists, create `GLOSSARY.md` beside the entry point lazily when the first term is settled

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.
