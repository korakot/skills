# Upstream and divergence

**Upstream:** [czlonkowski/fables](https://github.com/czlonkowski/fables) → `plugins/fable-advisor/` (MIT, © 2026 Romuald Członkowski).

**Synced to:** upstream commit `4cb1e26` (v0.6.3, "Record Fable 5.2 CLI smoke test", Nov 2026). This folder's first commit holds the upstream skill folder verbatim plus the Claude Code agent definition (`agents/fable-advisor.md`), so `git diff <first commit> -- fable-advisor/` shows exactly what this fork changed.

Prior art outside upstream: a friend's (Sira, ThepExcel) unpublished `/fable-advisor` with the same shape — Opus main, a skill that prepares the brief and gates what needs Fable, Fable as a fresh subagent for plans and stuck points; he reported many projects for about 10% of his Fable allowance.

## How to update from upstream

Diff upstream's `plugins/fable-advisor/` between the "synced to" commit and its HEAD. Apply changes to the gate, triggers, budget, brief template, advice handling and the agent's system prompt (which lives here as the preamble in SKILL.md). Skip the Codex route. Bump "Synced to" when done.

## Divergence (and why)

1. **Claude only; the Codex route is dropped** (`references/codex-cli.md`, `agents/openai.yaml` removed). Kora consults Fable from Claude Code; a Chat test on 11 Nov 2026 showed the same Agent-tool route also works from Chat, at a much higher context cost (korakot/claude `wiki/advisor.md`).
2. **No separate agent definition; its system prompt becomes the preamble.** The skill is installed as a claude.ai profile skill, which syncs into cloud Claude Code sessions but carries no agent files, so upstream's fallback route (`general-purpose` + `model: "fable"` + preamble) is the only route. The preamble keeps the agent file's rules: read narrowly, commit, may reject the menu, weigh the orchestrator's evidence, no deliverables, the four-part answer under 300 words.
3. **Effort `high`, not `xhigh`.** Anthropic's Fable 5.2 guidance: start at high; gains above it are uneven. The scarce resource is the Fable allowance.
4. **Framed by the scarce allowance, not price.** On premium subscription seats Fable draws from the shared weekly limit and may use at most half of it (support article "Claude Fable models on your plan", read 11 Nov 2026; corrected from "its own smaller weekly cap"), while the main model rarely runs out, so the parent spends its own tokens freely on evidence. Also names the built-in `/advisor fable` (whole transcript, uncached) as what this replaces.
5. **Gate step 0: skip automatic consults when the main model is already Fable**, and **never fork** (a fork copies the whole conversation). Both are explicit because a cloud default like `CLAUDE_CODE_SUBAGENT_MODEL` or a fork would quietly undo the point.
6. **Trigger 1 widened** beyond software (adds data-pipeline or dataset design and research method; drops n8n specifics), since Kora's Claude Code work includes data and research jobs.
7. **Shorter.** Pricing figures and upstream-specific notes (named spawns inside subagents, plugin-installed agent names) removed; reporting back trimmed to one or two lines.
