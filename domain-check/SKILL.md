---
name: domain-check
description: Brainstorm domain names and check which are unregistered, straight from the TLD registries (RDAP), then score a shortlist. Use when the user wants a domain for a site or project, asks whether a domain is available, or wants name ideas filtered to free ones.
---

# domain-check

The user wants a name, not a list of taken ones. So you brainstorm widely, check every candidate yourself, and show only free names with reasons. Checking is free and fast; the user's attention is not.

## 1. Gather the naming context

Before brainstorming, find out three things, from the conversation or by asking once:

- **Audience and purpose.** A site for Thai readers favours different names than a global one. In the case that shaped this skill, "mainly for Thai readers" moved the winner from bugsfound.com to nophai.com.
- **Preferred TLDs.** Default to `com,dev,app,net` unless told otherwise.
- **The user's own naming patterns.** If they keep a list of domains they own or considered (a notes page, a doc), read it. Names that last for a person tend to share a pattern, and matching it beats generic brainstorming. One user's list showed Thai–English double readings (promptam = พร้อมทำ), plain hyphenated descriptions (thai-nlp.com) and Latin words; generic English names like vulntide.com scored badly with him for being hard to say.

## 2. Brainstorm in batches

Generate 30–60 bases across several angles at once: the core idea in plain words, wordplay and double readings in the audience's language, a Latin or classical word, descriptive hyphenated forms, and the user's own suggestions. Short .com names in most tech spaces are taken, so breadth matters more than polish.

## 3. Check them all

```bash
python3 SKILL_DIR/scripts/check.py name1 name2 name3 -t com,dev,app,net
python3 SKILL_DIR/scripts/check.py -f names.txt          # one name per line
```

Bare names get every TLD; full domains are checked as given. Output is a grid, `✓` free and `✗` taken. The script reads registry endpoints from IANA's bootstrap file, retries rate limits, and accepts IDNs (โนภัย.com is sent as `xn--q3cog3d5d.com`). A `?noRDAP` TLD (e.g. .io) has to be checked at a registrar.

When a short, obvious name comes back free, re-check it before celebrating: query it alone with `--raw`, and if DNS lookups work in your environment, confirm the name has no nameservers. bugsfound.com looked too good to be true; it was real, while its neighbours bugfound.com and foundbugs.com were taken.

## 4. Look for traps and clashes on the shortlist

A free name can still be a bad one. For each finalist, check:

- **Typing traps.** How will people mistype it? Check those variants too, because a taken variant sends visitors elsewhere. Examples: singular vs plural (bugfound.com taken), the hyphen dropped (thaisec.com taken while thai-sec.com was free), romanisation variants (ปลอด as plod or plot).
- **Clashes.** Search the name. thai-sec reads as the Thai SEC (ก.ล.ต.); plodphai turned out to be a meme-coin name; pongkan is a common given name.
- **Meaning in the audience's language.** aphai carries Pāli *abhaya* (fearlessness), but Thais first read ขออภัย ("sorry").

## 5. Score and recommend

Score each finalist 1–5 on scope fit, say-and-type (heard once, typed right), distinctness, room to grow, and joy (how much the user likes it; estimate from their reactions and say so). Price rarely separates names in the same TLD, so leave it out unless it does. Present a small table, then name the winner and the single flaw that sank each runner-up. If the name has a natural backronym or tagline, offer one.

## What RDAP can't tell you

RDAP answers "is it registered". It does not show the price, flag premium names, or see names the registry has reserved, so the registrar's checkout is the final word. For registration length, a few years is usually right for an exploratory project: price locks save little, and many such names get dropped.

Internationalised names: .com allows one script per label, so a Thai name works (โนภัย.com) but a mixed one (Noภัย) does not. Many apps and email clients show IDNs as `xn--…`, which looks like phishing, so an IDN is at best a redirect, not the main address.
