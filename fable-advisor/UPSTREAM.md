# Upstream and divergence

**Upstream:** [czlonkowski/fables](https://github.com/czlonkowski/fables) → `plugins/fable-advisor/` (MIT, © 2026 Romuald Członkowski).

**Synced to:** upstream commit `4cb1e26` (v0.6.3, "Record Fable 5.2 CLI smoke test", Nov 2026). This folder's first commit holds the upstream skill folder verbatim plus the Claude Code agent definition (`agents/fable-advisor.md`), so `git diff <first commit> -- fable-advisor/` shows exactly what this fork changed.

Prior art outside upstream: a friend's (Sira, ThepExcel) unpublished `/fable-advisor` with the same shape — Opus main, a skill that prepares the brief and gates what needs Fable, Fable as a fresh subagent for plans and stuck points; he reported many projects for about 10% of his Fable allowance.

## How to update from upstream

Diff upstream's `plugins/fable-advisor/` between the "synced to" commit and its HEAD. Apply changes to the gate, triggers, budget, brief template, advice handling and the agent's system prompt (which lives here as the preamble in SKILL.md). Skip the Codex route. Bump "Synced to" when done.

## Divergence (and why)

1. **Upstream's CLI route becomes the default for Claude too; the Codex specifics are dropped** (`references/codex-cli.md`, `agents/openai.yaml` removed). Upstream uses `claude -p` only from Codex hosts and the native agent from Claude Code. Measured 11 Nov 2026 on the same 319-word brief from cloud Claude Code (Opus 5.5 main, Fable 5.2, effort high): headless read about 2.5k input tokens ($0.11, 21 s, mostly thinking and answer output); an Agent-tool subagent took about 63.5k tokens (36 s), carrying the session's memory instructions, about 60 skill descriptions and the tool list, and the memory file even told it to read three more files. From Chat the Agent spawn was about 90k (korakot/claude `wiki/advisor.md`). Both Fable runs recommended headless by default. `scripts/consult.py` wraps upstream's flags (`--safe-mode --tools '' --no-session-persistence --max-turns 1 --max-budget-usd 1.00`, JSON output, `modelUsage` check) and adds the preamble as `--system-prompt`. The Agent tool stays as a fallback when the CLI is missing or not logged in.
2. **No separate agent definition; its system prompt becomes `preamble.txt`.** Profile skills carry no agent files. The preamble keeps the agent file's rules (commit, may reject the menu, weigh the orchestrator's evidence, no deliverables, the four-part answer under 300 words); "read named files narrowly" became "name the gap", since the default route has no tools.
3. **Effort `high`, not `xhigh`; model alias `fable`, not a pinned ID**, so the skill follows new Fable releases (the script checks the output came from a Fable model). Anthropic's Fable 5.2 guidance: start at high; gains above it are uneven. The scarce resource is the Fable allowance.
4. **Framed by the scarce allowance, not price.** On premium subscription seats Fable draws from the shared weekly limit and may use at most half of it (support article "Claude Fable models on your plan", read 11 Nov 2026; corrected from "its own smaller weekly cap"), while the main model rarely runs out, so the parent spends its own tokens freely on evidence. Also names the built-in `/advisor fable` (whole transcript, uncached) as what this replaces.
5. **Gate step 0: skip automatic consults when the main model is already Fable**, and **never fork** (a fork copies the whole conversation). Both are explicit because a cloud default like `CLAUDE_CODE_SUBAGENT_MODEL` or a fork would quietly undo the point.
6. **Trigger 1 widened** beyond software (adds data-pipeline or dataset design and research method; drops n8n specifics), since Kora's Claude Code work includes data and research jobs.
7. **Shorter.** Pricing figures and upstream-specific notes (named spawns inside subagents, plugin-installed agent names) removed; reporting back trimmed to one or two lines.
