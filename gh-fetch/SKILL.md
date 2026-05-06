---
name: gh-fetch
description: Read files from a GitHub repo via bash. web_fetch on GitHub will fail.
---

# Fetch GitHub content via bash

URLs may be user-provided, found via web search, or inferred from a project name.

## Single file

```bash
# github.com/{owner}/{repo}/blob/{branch}/{path}
#   → cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/{path}
curl -s "https://cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/{path}"
```

## Subfolder

```bash
# Call 1 — fetch (npx download + clone can be slow; split for visibility)
npx degit {owner}/{repo}/{path} /tmp/{name} --force

# Call 2 — verify
find /tmp/{name} -type f | sort
```

## Whole repo

```bash
git clone --depth 1 https://github.com/{owner}/{repo}.git /tmp/{repo}
```
