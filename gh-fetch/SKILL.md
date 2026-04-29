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
npx degit {owner}/{repo}/{path} /tmp/{name}
```

## Whole repo

```bash
git clone --depth 1 https://github.com/{owner}/{repo}.git /tmp/{repo}
```
