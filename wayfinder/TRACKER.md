# Tracker: GitHub issues

How this fork expresses the map's operations on GitHub. Adapted from upstream's `setup-matt-pocock-skills/issue-tracker-github.md` ("Wayfinding operations"), plus the parts upstream leaves to per-repo setup: which repo, the roster, and running from Claude Chat.

## Which repo holds a map

A map lives in the repo its subject belongs to, so its decisions sit next to the material they decide about. A map about a dissertation goes in the dissertation's repo; a map about a tool goes in that tool's repo. Visibility follows the repo: anything that must stay private goes in a private repo, and a map that collaborators should see goes in a repo they can read.

The user's own routing note (usually kept with the roster, below) says which repos exist and which are private. If no repo fits, ask rather than create one; a new repo is the user's call.

All of a map's tickets live in the same repo as the map. Sub-issues and dependencies work across repos on GitHub, but a frontier query stays simple only when everything is in one place.

## The roster

The user keeps one roster listing every map: a name wrapping its link, plus whether it's active or done. It is the only cross-repo index, so a session in any repo or any tool can find a map. Ask the user where it lives if you don't know (for example a memory file or a wiki page), and add one line when charting a map.

The roster is a pointer list, never a store: decisions live only in the tickets. As a backstop, the search `user:<owner> label:wayfinder:map` lists every map across the user's repos.

## Operations

Run `gh` inside a clone of the map's repo (it infers the repo from `git remote -v`). Where `gh` isn't available, as in Claude Chat, use the GitHub MCP tools named in brackets.

- **Labels**: the first map in a repo needs the labels created: `gh label create wayfinder:map`, and likewise `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task`. A label that doesn't exist fails the create call, so check `gh label list` once per new repo.
- **Map**: `gh issue create --label wayfinder:map` with the Destination / Notes / Decisions-so-far / Not-yet-specified / Out-of-scope body. [`issue_write`]
- **Child ticket**: `gh issue create --parent <map> --label wayfinder:<type>` (`gh` 2.94+), or `gh issue edit <map> --add-sub-issue <child>` afterwards. Older `gh`: `gh api --method POST repos/<owner>/<repo>/issues/<map>/sub_issues -F sub_issue_id=<child-db-id>`. [`issue_write`, then `sub_issue_write`]
- **Database id**: dependency and sub-issue API calls take the issue's numeric database id, not its `#number` or `node_id`: `gh api repos/<owner>/<repo>/issues/<n> --jq .id`. Passing the number is the usual silent mistake, because it is also a valid-looking integer.
- **Blocking**: GitHub's native issue dependencies, which show "Blocked by" in the issue UI so the frontier is visible without opening the map. `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`. The GitHub MCP has no dependency tool, so from Claude Chat either get a token for `gh` or fall back to a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open sub-issues (`gh api repos/<owner>/<repo>/issues/<map>/sub_issues`), and drop any with an assignee or an open blocker (`issue_dependencies_summary.blocked_by > 0`, or an open issue in a `Blocked by` line). First in map order wins. [`issue_read` with sub-issues]
- **Claim**: `gh issue edit <n> --add-assignee @me`, the session's first write. [`issue_write`]
- **Resolve**: `gh issue comment <n> --body "<self-contained answer>"`, then `gh issue close <n>`, then append the Decisions-so-far line to the map body (`gh issue edit <map> --body-file ...`, after re-reading the body, since another session may have edited it). [`add_issue_comment`, `issue_write`]
