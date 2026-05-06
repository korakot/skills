---
name: writing-skills
description: Use when creating new skills, editing existing skills, or reviewing a SKILL.md
---

<!-- Adapted from obra/superpowers (v5.1.0). Workflow concerns (test, eval, iterate, package) are deferred to skill-creator; this skill focuses on writing the SKILL.md text itself. -->

# Writing Skills

Complements `skill-creator`. While skill-creator runs the workflow (capture intent → draft → eval → iterate → package), this skill is about the principles for writing the SKILL.md text well: what makes a description trigger reliably, how to structure the body, what patterns to avoid.

## What Is a Skill?

A skill is a reusable reference for a technique, pattern, or tool that future Claude needs to find and apply. It is not a narrative about how a problem was once solved.

- **Skills are:** reusable techniques, patterns, mental models, reference material
- **Skills are not:** session logs, project-specific conventions (those go in CLAUDE.md or project docs), one-off solutions

## When to Create a Skill

Create when:
- The technique wasn't intuitively obvious
- It will apply across projects, not just this one
- A future you would want to find this again

Don't create for:
- One-off solutions
- Standard practices already well-documented elsewhere
- Project-specific conventions
- Mechanical constraints enforceable in code

## Skill Types

| Type | Purpose |
|---|---|
| **Technique** | Concrete how-to with steps |
| **Pattern** | Way of thinking about a problem |
| **Reference** | Lookup material — API, syntax, conventions |

The type informs the structure: techniques need steps, patterns need a mental model, references need scannability.

## The Description Field

This is where most skill quality lives — Claude reads the description to decide whether to load the body. Get this wrong and the skill never fires, no matter how good the body is.

**Two rules that override everything else:**

1. **Description = WHEN to use, not WHAT it does.** Never summarize the workflow. Testing has shown that when a description summarizes the steps, Claude follows the description and skips the body — the skill becomes documentation Claude never reads.
2. **Two sentences, third person, "Use when..." opener.** Keep it tight.

```yaml
# ❌ BAD — workflow summary
description: Use when fixing tests — write failing test first, watch fail, then minimal code

# ❌ BAD — body content leaking into trigger surface
description: Use when authoring SKILL.md — covers description writing (CSO), structure, anti-patterns

# ❌ BAD — first person
description: I can help when async tests are flaky

# ❌ BAD — too vague
description: For async testing

# ✅ GOOD — trigger conditions only
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently

# ✅ GOOD — narrow scope, action verbs
description: Use when creating new skills, editing existing skills, or reviewing a SKILL.md
```

**Keyword coverage:** Include words a future Claude would search for — error messages, symptoms, tool names. Trigger on the *problem* ("race conditions"), not the *language-specific symptom* ("setTimeout").

**Naming:** verb-first, gerund (-ing) for processes. `creating-skills` not `skill-creation`. `condition-based-waiting` not `async-helpers`.

## SKILL.md Structure

YAML frontmatter (required):

- `name`: letters, numbers, hyphens only — no parentheses or special chars
- `description`: as above

See [agentskills.io/specification](https://agentskills.io/specification) for additional supported fields.

Body template — scale sections to skill size; small skills can collapse to overview + core pattern:

```markdown
# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
Symptoms and use cases. When NOT to use.

## Core Pattern (for techniques/patterns)
The actual approach — steps, mental model, before/after.

## Quick Reference (for references)
Table or bullets for scanning.

## Common Mistakes
What goes wrong, how to recognize it, how to fix.
```

## File Organization

Three patterns, in order of frequency:

**Self-contained** — most skills:
```
skill-name/
  SKILL.md
```

**With reusable example or tool:**
```
skill-name/
  SKILL.md
  example.py     # Working code to adapt
```

**With heavy reference:**
```
skill-name/
  SKILL.md           # Overview + workflows
  api-reference.md   # 600 lines of API docs
```

The SKILL.md links to reference files; Claude follows the link only when needed. Heavy reference inline burns context on every load.

## Token Efficiency

Frequently-loaded skills compete with everything else for context. Be ruthless:

- Don't document every flag — reference `--help`
- Don't repeat content from cross-referenced skills — link to them
- One excellent example beats three mediocre ones
- If a skill grows past ~500 lines, the body should mostly be navigation; details belong in reference files

## Cross-Referencing Other Skills

In Claude.ai, just mention the skill by name in prose: "For the eval workflow, use the `skill-creator` skill." Claude follows the reference when relevant. No special syntax needed.

(`@`-style force-loading is CC-specific and burns context on every load — don't port that pattern.)

## Visual Flow (optional)

If a skill has a non-trivial decision flow, sketch it as a mermaid block or ask Claude to render via `show_widget` during authoring. Most skills are clearer as a numbered checklist — don't add visual machinery for its own sake.

## Anti-Patterns

- **Narrative example** — "In session 2025-10-03, we found empty projectDir caused..." Too specific, not reusable.
- **Multi-language dilution** — `example-js.js`, `example-py.py`, `example-go.go`. Mediocre everywhere, maintenance burden. Pick one.
- **Description leakage** — putting body content (topic words, internal acronyms, "covers X, Y, Z") into the description as decoration. Descriptions are triggers, not summaries.
- **Generic labels** — `helper1`, `step3`, `pattern4`. Labels should carry semantic meaning.
- **Code in flowcharts** — flowcharts show flow. Code goes in the body.

## Testing and Iteration

For evaluating a skill — test cases, grading, description optimization, iteration loop — use the `skill-creator` skill. It has the full workflow, including Claude.ai-specific adaptations for environments without subagents.

## See Also

- `anthropic-best-practices.md` — Anthropic's official skill-authoring guide (companion reference, lives next to this SKILL.md when installed)
- `skill-creator` skill — for the create → test → iterate → package workflow
