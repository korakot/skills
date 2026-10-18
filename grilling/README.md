# grilling

Interview the user about a plan or decision in rounds: each round asks every question whose prerequisites are settled, each with a recommended answer worded so "yes" accepts it, until the design tree is fully visited.

A fork of Matt Pocock's [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) (MIT). One change: a round of three or more questions is shown as a [point-review](../point-review) widget (Accept = yes, Reject or a note = your own answer). Details: [`UPSTREAM.md`](UPSTREAM.md).

[wayfinder](../wayfinder) calls it alongside [domain-modeling](../domain-modeling).

## Install

Claude.ai: upload `grilling.skill` in **Settings → Customize → Skills**. Claude Code: copy the folder into `.claude/skills/`.
