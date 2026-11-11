# fable-advisor

Consult Claude Fable from an Opus (or lower) session with a curated brief, as a one-shot headless `claude -p` call (`scripts/consult.py`), instead of `/advisor fable`, which sends Fable the whole transcript on every call. About 2.5k input tokens per consult in cloud Claude Code, against about 63k for an Agent-tool subagent (the fallback). Fork of [czlonkowski/fables](https://github.com/czlonkowski/fables) `fable-advisor`; divergences in [UPSTREAM.md](UPSTREAM.md).

**Install:** save `fable-advisor.skill` (a zip of this folder's `SKILL.md`) to the claude.ai profile with the Save skill button on its file card, in Chat or in a Claude Code session (done 11 Nov 2026 from cloud Claude Code). It then syncs into cloud Claude Code as `/anthropic-skills:fable-advisor`.

**Use:** say "ask Fable" at a decision point, or let it fire on its triggers (costly-to-revert decision, stuck after two different attempts, plan or pre-completion review, unattended automation). Budget: one consult per task by default, three at most.
