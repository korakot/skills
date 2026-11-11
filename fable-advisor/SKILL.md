---
name: fable-advisor
description: Consult Claude Fable through a one-shot headless call that reads only a curated brief, from a session whose main model is below Fable (usually Opus). Works wherever the claude CLI is logged in (cloud Claude Code, the Chat sandbox), with an Agent-tool subagent as the fallback. Use when the user says "ask Fable" or similar; before a costly-to-revert decision (architecture, schema, data or pipeline design, migration, an unattended loop or schedule); after two genuinely different failed fix attempts; or for a plan or pre-completion review of consequential work. Not for routine reversible work, for generation, or in sessions already running on Fable.
---

# Fable Advisor — a curated consult

Fable is the scarce resource: on premium subscription seats it draws from the shared weekly limit but may use at most half of it (Pro and standard seats pay usage credits for it), while the main model's tokens rarely run out. Claude Code's built-in `/advisor fable` sends Fable the whole transcript on every call, uncached. Here Fable runs as a separate one-shot `claude -p` process that reads only the preamble and the brief you write: about 2.5k input tokens in cloud Claude Code, against about 63k for an Agent-tool subagent there and about 90k in Chat, because a subagent carries the session's memory, skill list and tools (measured 11 Nov 2026). So spend your own tokens freely on orientation and evidence, and spend Fable's on judgment only.

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

**Default: headless.** Write the brief to a file (scratchpad), then run the bundled script with a Bash timeout of about 6 minutes:

```bash
python3 <this skill's folder>/scripts/consult.py <brief-file>
```

It calls `claude -p --model fable --effort high --safe-mode --tools '' --system-prompt <preamble.txt>` with the brief on stdin, no session persistence, one turn and a $1 cap, then checks that the JSON result is a success and that the output came from a Fable model. It prints the verdict and one usage line (model, input, output, cost, time).

- **Exit 0:** the verdict. **Exit 2:** failed or not Fable: report it to the user, do not retry, do not swap models. **Exit 3:** the CLI is missing or not logged in: use the fallback below.
- Fable has **no tools** on this route, so the brief must carry the evidence: paste **verbatim excerpts** of load-bearing facts, not paraphrase; file paths are citations only.
- **Follow-up:** there is no session to resume. Make one fresh call with a short recap, Fable's previous verdict, and only the new evidence; it counts toward the cap.
- The user may ask for another effort or model (`--effort xhigh`, `--model claude-fable-5-1`).

**Fallback: Agent tool** (only on exit 3; announce it, since it costs roughly 25× the input, more in Chat). `subagent_type: general-purpose`, `model: "fable"` (a per-call model overrides defaults such as `CLAUDE_CODE_SUBAGENT_MODEL`), `effort: "high"` where the tool takes it (Chat's does not), foreground, prompt = the contents of `preamble.txt` + the brief. **Never a fork**: a fork copies the whole conversation. Follow-ups go to the same agent by `SendMessage`, new information only. If it reports a model other than Fable, tell the user.

## The brief

Curate; never forward the transcript. Aim for about 800 words, 1,200 at most including excerpts. Your own tokens are cheap: spend them on finding the right excerpts.

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

FILES (citations; Fable cannot open them on the default route):
  <path> — <what is in it and why it matters>   # at most 5

ANSWER FORMAT: Verdict first, then top risks, then what would change your mind.
Under 300 words.
```

For **stuck**, replace OPTIONS with ATTEMPTS (what you tried, the exact result, what each ruled out). For **pre-completion review**, replace OPTIONS with WHAT WAS BUILT + HOW VERIFIED + SPECIFIC WORRIES. For **automation design**, replace OPTIONS with the design: trigger and interval, what each run does, stop criteria, per-run checks, model and turn caps, cost per run, and every outside system it touches.

## Treating the advice

- **Give it serious weight.** Don't relitigate it without new evidence.
- **Reality beats advice.** If a recommendation fails against the facts (the file says X, the API returns Y), adapt. A passing self-test is not proof the advice was wrong.
- **A conflict gets one follow-up, not a silent switch.** One fresh call with the recap, the verdict and the new evidence; ask which constraint breaks the tie. It counts toward the cap.
- **Fable may reject the menu.** Take that seriously.

## Reporting back

Tell the user, briefly: that Fable was consulted (how many times), its verdict in one or two sentences, and whether you followed it, with the reason if not.
