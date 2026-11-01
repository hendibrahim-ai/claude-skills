---
name: keyword-gap-analyzer
description: "Use when running a keyword content gap analysis for a website: looking up a keyword in a target keyword sheet and on the site, finding the gaps and the clusters, and ranking the opportunities by priority. Works for any site and handles Arabic-language sites well. Triggers when the user mentions a keyword, content gap, a keyword sheet, searching the site for a keyword, or asks whether a keyword is already covered."
---

# Keyword Gap Analyzer: Keyword Content Gap Analysis

## Overview

This skill helps analyze the gaps between a list of target keywords (in a sheet) and the content that actually exists on the site, so you can set priorities for new content.

---

## Core Steps for Each Keyword

### Step 1: Search the Sheet (PDF/Excel)

Search the uploaded file for the requested keyword in **every possible form**:
- Exact match (the exact same keyword)
- Partial match (the keyword appears inside a longer phrase)
- Close synonyms (for example: "quick dinner ideas" = "easy dinner recipes")
- Different forms (singular/plural, and gendered forms in languages like Arabic)

**Record:**
- ✅ Present: give the page number and the exact wording
- ⚠️ Partially present: give the closest form that exists
- ❌ Not present

---

### Step 2: Search the Site

Run a `site:` search on the target site:

```
site:www.example.com [keyword]
```

Rate the results:

| Result | Rating |
|---------|---------|
| Dedicated page with a matching title/URL | ✅ Well covered |
| Incidental mention in other articles | ⚠️ Partial coverage |
| Zero results | ❌ Complete gap |

---

### Step 3: Rate the Opportunity

Based on the results of the two steps, set the priority level:

| Sheet | Site | Priority |
|-------|--------|----------|
| ✅ Present | ❌ No page | 🔥🔥🔥 Highest priority |
| ✅ Present | ⚠️ Partial | 🔥🔥 High priority |
| ❌ Not present | ❌ No page | 🔥 Strategic opportunity |
| ✅ Present | ✅ Present | ✔️ Covered: no work needed |

---

### Step 4: Present the Summary

For each keyword, present one standard table in this format:

```
## 📋 PDF Search Result
[Keyword present/not present + page + wording]

## 🔍 site: Search Results
[Table of the pages that appear and how they relate to the keyword]

## 📊 Summary
| Item | Result |
|-------|---------|
| In the sheet? | ✅/⚠️/❌ |
| Dedicated page? | ✅/⚠️/❌ |
| SEO opportunity? | 🔥🔥🔥/🔥🔥/🔥 |

[Strategic note, if any]
```

---

## Clusters: Groups of Related Keywords

When you find several keywords on the same topic and all of them are missing, record them as one **cluster**:

```
## 🗺️ [Cluster Name] Content Cluster

| Keyword | In the sheet | Page |
|--------|----------|------|
| Keyword 1 | ✅/❌ | ✅/❌ |
| Keyword 2 | ✅/❌ | ✅/❌ |
```

**Example clusters:**
- Air Fryer Recipes Cluster (7 keywords)
- Meal Prep Cluster (4 keywords)
- Gluten-Free Baking Cluster
- Healthy Breakfast Cluster

---

## Full Final Report

When the user asks for the final report, put all the keywords found into one table sorted by priority:

```markdown
# Full Content Gap Analysis Report

## 🔥🔥🔥 Top Priorities (in the sheet + zero pages)
| Keyword | Sheet | Site | Cluster |
|--------|-------|--------|------------|

## 🔥🔥 High Priority (in the sheet + partial coverage)
...

## 🔥 Strategic Opportunities (missing from both the sheet and the site)
...

## ✔️ Well Covered (no work needed)
...

## 💡 Cluster Recommendations
[Suggested cluster priorities with the number of keywords in each cluster]
```

---

## Key Rules

1. **Don't guess**: always search the actual sheet and run the site: search
2. **Search every form**: the keyword may exist in different wording
3. **Tell an incidental mention apart from a dedicated page**: an incidental mention counts as partial coverage only
4. **Detect clusters automatically**: when you find related keywords that are all missing, point them out
5. **The strategic note matters**: explain in context why this keyword is an important opportunity

---

## Worked Example

**User:** "how long to boil an egg"

**Step 1: Sheet:**
- ✅ "how long to boil an egg" is on page 3: exact match

**Step 2: site search:**
```
site:www.example.com how long to boil an egg
```
Results: the article "10 breakfast ideas for busy mornings" mentions boiled eggs in passing. No dedicated page.

**Step 3: Summary:**
- In the sheet: ✅
- Dedicated page: ❌
- Priority: 🔥🔥🔥

**Note:** A keyword with very high search volume, tied to a whole Egg Recipes Cluster that is missing from the site.


---

Made by Hend Ibrahim · [hendebrahim.com](https://hendebrahim.com) · More skills: [github.com/hendibrahim-ai/claude-skills](https://github.com/hendibrahim-ai/claude-skills)
