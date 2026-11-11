---
name: fable-advisor
description: Claude Code or Chat, wherever the Agent tool accepts model fable. Consult Claude Fable through a fresh subagent that reads only a curated brief, from a session whose main model is below Fable (usually Opus). Use when the user says "ask Fable" or similar; before a costly-to-revert decision (architecture, schema, data or pipeline design, migration, an unattended loop or schedule); after two genuinely different failed fix attempts; or for a plan or pre-completion review of consequential work. Not for routine reversible work, for generation, or in sessions already running on Fable.
---

# Fable Advisor — a curated consult

Fable is the scarce resource: on premium subscription seats it draws from the shared weekly limit but may use at most half of it (Pro and standard seats pay usage credits for it), while the main model's tokens rarely run out. Claude Code's built-in `/advisor fable` sends Fable the whole transcript on every call, uncached. Here Fable is a fresh subagent that reads only the brief you write, plus the few files it chooses to open. So spend your own tokens freely on orientation and evidence, and spend Fable's on judgment only.

**Fable supplies the judgment; you supply the tokens.** Fable decides or reviews; you explore, build, write and test. Never hand Fable generation work.

## The gate

0. **Main model.** If this session already runs on Fable, there is nothing stronger to ask: skip automatic consults.
1. **Is the decision costly to revert, or am I genuinely stuck?** If a wrong call costs under an hour of rework, decide yourself.
2. **Is there a real fork in the road?** Fable adds value when competing options have evidence to weigh, or a failure doesn't fit your model of the problem. If you only want confirmation, skip it.

If any answer says skip, decide yourself. An explicit request from the user ("ask Fable") bypasses the gate but not the budget.

## The five triggers

Orient first (read the key files, gather the constraints) so the brief carries evidence; a consult without evidence buys generic advice.

1. **Costly-to-revert decision, before building.** Architecture, schema and data models, API contracts, data-pipeline or dataset design, research method, technology choice. Timing: after orientation, before the first substantive write.
2. **Stuck.** Two or more genuinely different failed attempts, recurring errors, or results that don't fit. Bring exact errors, what each attempt ruled out.
3. **Plan review.** A drafted plan for a non-trivial task that embeds a costly-to-revert choice (in plan mode: before presenting it).
4. **Pre-completion review.** Before declaring done on hard-to-revert work: production changes, data migrations, anything others will rely on. Include what was built, how it was verified, and your specific worries.
5. **Unattended automation.** Before starting a loop, schedule or long autonomous job that acts without a human watching. Have Fable check stop conditions, interval against how fast the watched thing changes, per-run verification, cost per run × frequency, what it writes to outside systems, and silent-failure modes. Read-only polling that is cheap to cancel needs no review.

## When not to consult

- Easily reversed work: renames, local refactors, flags, styling, wording.
- Decisions already made by the user, by repo convention, or by CLAUDE.md / AGENTS.md / memory.
- Routine implementation with a clear path, however long.
- Generation of any kind: code, documents, configs. That is your job.
- A first failed attempt: try a genuinely different approach first.
- Thinking you haven't done yet. Fable amplifies a well-framed question and wastes its allowance on a vague one.

## Budget

- **Default one consult per task; hard cap three Fable interactions** (spawns and follow-ups combined). Needing a fourth means the problem is misframed: say so to the user instead.
- **Announce each consult** in one line before it: `Consulting Fable on <decision> (trigger: <which>, consult 1/3).`
- **Batch** pending decisions into one consult.
- **One spawn plus at most one follow-up per question.** Fable is a consultant, not a pair programmer.
- The user's instructions win (skip Fable, always ask first, a different effort).
- Never run ordinary subagents (exploration, implementation, review fan-outs) on Fable under this skill.

## How to consult

Use the Agent tool:

- `subagent_type`: `general-purpose`. **Never a fork**: a fork copies the whole conversation, which is exactly what this skill avoids.
- `model`: `"fable"`. A model passed on the call overrides defaults such as `CLAUDE_CODE_SUBAGENT_MODEL`.
- `effort`: `"high"` where the tool accepts it (Chat's Agent tool does not). Fable 5.2 guidance is to start at high; `xhigh` spends more of the allowance for uneven gains.
- Foreground (the verdict gates your next step).
- `prompt`: the preamble below, then the brief.

From Chat the spawn costs far more than in Claude Code: it inherits Chat's whole system prompt, memory snapshot and tool list (about 90k tokens for a 400-word brief, tested 11 Nov 2026; numbers in korakot/claude `wiki/advisor.md`). Keep Chat consults rare.

Keep the agent's ID or name from the result: a follow-up goes by `SendMessage` with only the new information, never a re-brief. If the spawn fails or reports a model other than Fable (no Fable access, a consent prompt, an allowlist), tell the user rather than quietly consulting a weaker model.

**Preamble** (prepend verbatim):

> You are a one-shot strategic advisor to a capable orchestrator that does all the building itself. Supply judgment, not artifacts: no code beyond a 10-line sketch, no documents or configs, and do not edit files or run commands that change anything. The brief should usually suffice; if a load-bearing fact is missing, read the named files narrowly (grep, targeted ranges), never explore the whole repository; if something crucial is still missing, name the gap instead of guessing. Commit: if it genuinely depends, say on what and give the decision rule. You may reject the menu and name a better option; that is the most valuable outcome. Weigh the orchestrator's first-hand evidence over your priors. Answer with **Verdict** (1–3 committed sentences) → **Why** (load-bearing reasons only) → **Risks** (top 2–3 of your own recommendation) → **Would change my mind** (1–2 specific pieces of evidence). Under 300 words; no preamble, no restating the brief. Your final message is the deliverable.

## The brief

Curate; never forward the transcript. Aim for about 800 words, 1,200 at most including excerpts.

```
DECISION: <the question in one sentence, first line>

CONTEXT: <2–4 sentences: what is being built or studied, for whom, where it runs>

OPTIONS:
  A. <option> — <main pro / main con>
  B. <option> — <...>
  My leaning: <X, because Y>          # always state one; it sharpens the advice

CONSTRAINTS: <the hard ones only>

EVIDENCE: <the facts that matter: key excerpts, numbers, exact errors,
           what failed attempts ruled out>

FILES (read narrowly only if needed):
  <path> — <what is in it and why it matters>   # at most 5

ANSWER FORMAT: Verdict first, then top risks, then what would change your mind.
Under 300 words.
```

For **stuck**, replace OPTIONS with ATTEMPTS (what you tried, the exact result, what each ruled out). For **pre-completion review**, replace OPTIONS with WHAT WAS BUILT + HOW VERIFIED + SPECIFIC WORRIES. For **automation design**, replace OPTIONS with the design: trigger and interval, what each run does, stop criteria, per-run checks, model and turn caps, cost per run, and every outside system it touches.

## Treating the advice

- **Give it serious weight.** Don't relitigate it without new evidence.
- **Reality beats advice.** If a recommendation fails against the facts (the file says X, the API returns Y), adapt. A passing self-test is not proof the advice was wrong.
- **A conflict gets one follow-up, not a silent switch.** Send the same agent the new evidence and ask which constraint breaks the tie; it counts toward the cap.
- **Fable may reject the menu.** Take that seriously.

## Reporting back

Tell the user, briefly: that Fable was consulted (how many times), its verdict in one or two sentences, and whether you followed it, with the reason if not.
