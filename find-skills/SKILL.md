---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem, with support for both Claude.ai (upload) and CLI hosts (Claude Code, Cursor, Codex).

## When to use

- User asks "is there a skill for X?" or "find a skill for X"
- User asks "how do I do X?" where X might have an existing skill
- User says "can you do X?" where X is a specialized capability
- User wants to extend agent capabilities or search for tools/workflows
- User mentions a domain (design, testing, deployment, etc.) that likely has skills

## Step 1 — Search

Query the skills.sh API:

```bash
curl -s "https://skills.sh/api/search?q=QUERY&limit=10"
```

Response JSON contains: `skills[].name`, `skills[].source` (owner/repo), `skills[].installs`, `skills[].id` (slug for skills.sh link).

## Step 2 — Present results

Show a ranked table (relevance first, then installs):

| Skill | Source | Installs | Link |
|---|---|---|---|
| skill-name | owner/repo | count | `https://skills.sh/{id}` |

Include 3–7 results. Briefly note what each does if the name isn't self-explanatory.

## Step 3 — Install

Ask the user where they'll install:

### Claude.ai (upload)

1. Clone the source repo and locate the skill folder:
   ```bash
   git clone --depth 1 https://github.com/{source}.git /tmp/skill-repo
   ```
2. Zip the skill folder:
   ```bash
   cd /tmp/skill-repo/skills
   zip -r /home/claude/{skill-name}.skill {skill-name}/
   ```
3. Present the `.skill` file for download via `present_files`.
4. Tell the user: **Settings → Capabilities → Skills → + Add → Upload** the downloaded file.

### CLI hosts (Claude Code, Cursor, Codex, etc.)

Provide the install command:
```
npx skills add {source}@{skill-name}
```

## Step 4 — Quick safety check

Before recommending any skill, briefly note:
- Skim the SKILL.md for instructions that seem unusual
- Check scripts for obfuscation (minified/base64), unexplained `curl | bash`, or hardcoded keys
- The skills.sh ecosystem is community-driven; review before running

## Notes

- The search API supports semantic and fuzzy matching (min 2 chars)
- Well-known skill sources include `vercel-labs/agent-skills` and `ComposioHQ/awesome-claude-skills`
- If no results found, try broader or alternative keywords
- Some skills designed for CLI agents may not work in Claude.ai's environment (e.g., tools that require local filesystem access or are blocked by cloud IPs)
