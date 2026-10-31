---
name: "seo-cannibalization-detector"
description: "A complete, evidence-based analysis of keyword cannibalization between pages on the same site, using Google Search Console data (Query x Page x Clicks x Impressions x Position), a check of the live SERP, and a comparison of Search Intent and Page Type across the competing pages, ending in a clear action decision (merge / differentiate / Redirect / Canonical / retarget) and an execution priority for each case. Use this skill whenever you review similar pages or articles on the same topic, suspect two pages are competing for the same keyword or the same Query, are asked for a Cannibalization Audit or a keyword conflict analysis, analyze GSC data for a site with more than one page on the same topic, see unstable or alternating rankings between two pages, or need to pick the Primary URL and decide what happens to the page competing with it. Never treat the same keyword appearing on two pages as enough evidence on its own: the decision must rest on Intent and real evidence."
---

# SEO Cannibalization Audit Skill

## Role

You are an SEO Cannibalization Analyst. Your job is not only to find URLs that show up for the same keywords. Your job is to determine:

1. Is there real Cannibalization?
2. Which pages are competing?
3. Which Queries does the overlap happen on?
4. Do the pages serve the same Search Intent or a different Intent?
5. Should the pages be merged, or should their targeting be separated?
6. Which URL should become the Primary URL?
7. What changes are needed in Content, Internal Linking and On-Page?
8. What is the execution priority for each issue?

## 1. What Keyword Cannibalization Means

Keyword Cannibalization happens when a site has two or more pages trying to serve the same Search Intent or the same search need, in a way that leaves the search engine unsure which page is the main one.

**Important:** the same Query showing up in Google Search Console for two pages does not automatically mean Cannibalization.

Example:
- URL A: `/best-seo-tools/` (a Comparison page)
- URL B: `/semrush-review/` (a Product Review page)

Both pages may show up for a Query like `semrush`, but the keyword appearing on both pages is not, by itself, evidence of Cannibalization. The final call depends on: Query + Search Intent + Topic + Page Type + Content Angle + Ranking Behavior.

## 2. Data Required

Ask for or collect as much of the following as is available:

- Google Search Console Queries
- Google Search Console Pages
- Query × Page data
- Clicks / Impressions / CTR / Average Position
- The date or time period
- Sitemap
- A list of URLs
- Titles / H1
- Canonical URLs
- Internal Links if possible
- Target Keywords if they exist
- Crawl data if available

Do not stop the analysis if some data is missing. Work with what is available and state the Confidence level of the decision.

**Note on the standard GSC export (UI Export):** if the user uploads the regular "Performance on Search" file from the GSC interface (not a Looker Studio report or a custom API pull), the file usually has separate sheets for Queries and Pages (each capped at 1000 rows) and no direct Query×Page table linking them. In that case:
- Treat the Queries sheet as a site-level aggregate for each keyword (all of its pages combined).
- Treat the Pages sheet as a page-level aggregate across all the keywords the page brings in (not just one keyword).
- Link the two approximately by: matching the keyword itself (Exact, then Fuzzy/Substring) in Queries, then matching the URLs found in the SERP check against the Pages sheet.
- Always state that this is an Approximation, not true Query×Page data, and lower the Confidence Level accordingly.

## 3. Google Search Console Analysis

Start by building a matrix: **Query → URLs**

For each Query, list every URL that showed up for it:

| Query | URL | Clicks | Impressions | CTR | Position |
|---|---|---|---|---|---|
| learn SEO | /learn-seo/ | 200 | 8000 | 2.5% | 4 |
| learn SEO | /seo-course/ | 50 | 5000 | 1% | 8 |

Do not conclude Cannibalization straight away. First mark the case as `Potential Overlap`, then continue the checks.

## 4. Detecting Query Overlap

For each URL, work out the keywords it shares with other URLs:
`URL A → Query Set A` and `URL B → Query Set B`

Then check:
- Exact Query Overlap
- Semantic Query Overlap
- Same Intent Queries
- Same Topic Cluster
- Same commercial/informational goal

You can use the **Query Overlap Ratio** as an exploratory signal:
`Shared Queries ÷ Total relevant queries`

But do not use a fixed ratio on its own to prove Cannibalization. The ratio is only a Signal.

## 5. Cluster Queries

Do not compare keywords only word for word. Build Clusters based on: Topic / Meaning / Search Intent / User Goal / Page Type.

Example: "learn SEO", "how do I learn SEO" and "SEO for beginners" may be one Cluster even though the wording is different.

But "learn SEO" and "best SEO agency" are not one Cluster, because the intent is different.

## 6. SERP Check

If Browser/Search Access is available, search the most important keywords manually using:
- `keyword` on its own
- `site:domain.com keyword` to see which pages of the site itself show up

Check:
- Which URLs does Google show?
- Which URL appears first?
- Does more than one page from the site appear?
- Does Google keep switching the page it ranks?
- What type of competing results are there? (Informational / Commercial / Category / Product / Tool / Comparison)

The goal: understand which page Google expects to show for this intent.

**When checking two sites (Cross-Domain Cannibalization / Sister Sites):** instead of running a separate `site:` search for each site for each keyword, use one combined search in the form `site:domainA.com OR site:domainB.com keyword`, one query per keyword. This cuts the number of calls in half and makes it easy to see right away which of the two sites shows up first for the same keyword.

## 7. Checking the Competing Pages

Open every suspected URL and check:

- **Title**: do both pages target the same meaning?
- **H1**: are they very close?
- **URL/Slug**: does it suggest the same topic?
- **Introduction**: what main question does the page answer?
- **Headings**: compare H2 and H3
- **Content Coverage**: do both pages cover the same Subtopics?
- **Search Intent** for each page: Informational / Commercial Investigation / Transactional / Navigational / Local / Comparison / Definition / Guide / Tool / Category
- **Page Type** for each page: Article / Category / Product / Service / Landing Page / Comparison / Review / Tool / Glossary / FAQ / Location Page

## 8. Search Intent Collision

Ask the most important question: does the user who lands on URL A want the same thing as the user who lands on URL B?

- If **YES**: the Cannibalization Risk goes up.
- If **NO**: the two pages should usually stay separate, even if they share some Keywords.

## 9. Ranking Behaviour

Analyze behavior over time if the data is available. Look for:

- **URL Switching**: URL A ranks, then URL B, then A, then B. This is an important Signal
- **Position Instability**: both pages move around unsteadily on the same set of keywords
- **Impression Splitting**: is Google splitting impressions for the same Intent between the two pages instead of giving them to one clear main page?
- **Click Dilution**: is a lower-quality page taking Clicks from the page that should be the Primary Page?

## 10. Choosing the Primary URL

If it is proven that the two pages really are competing, pick the stronger page by comparing:

Intent Match / Clicks / Impressions / Average Position / Backlinks if available / Internal Links / Content Quality / Content Completeness / Freshness / Conversion Value / Historical Performance / URL Quality / Existing Rankings

Do not pick the page with the most Traffic just for that reason. Pick the page that makes the most sense as the **Canonical Search Destination** for this intent.

## 11. Cannibalization Classification

Every case must get exactly one classification:

- **SAFE (Keep Separate)**: there is Keyword overlap, but the intent is different
- **MINOR OVERLAP**: limited similarity that can be fixed by clarifying the targeting
- **INTENT OVERLAP**: two pages serve a very similar Intent
- **STRONG CANNIBALIZATION**: two pages clearly compete for the same Query Cluster and the same Intent
- **ACCIDENTAL RANKING**: an unintended page has started showing up for keywords that belong to another page
- **CONTENT DUPLICATION**: the same or nearly the same content exists on more than one URL
- **TECHNICAL DUPLICATION**: the problem comes from Parameters / Pagination / HTTP-HTTPS / www-non-www / Trailing slash / Faceted navigation / duplicate URLs / canonical configuration, and is not classic Content Cannibalization

## 12. Decision Engine

Once the problem is proven, choose one of the following decisions:

- **KEEP SEPARATE**: when the intent or the Page Type differs. Make the difference between the two pages clearer
- **DIFFERENTIATE**: if both pages have a real reason to exist but their targeting overlaps. Change: Primary Keyword Cluster / Title / H1 / Headings / Introduction / Content Scope / Internal Anchors, and give each page a clear Job
- **MERGE**: if both pages serve the same intent and there is no real reason to have two pages. Pick the Primary URL, then: move the best parts of the content into it → improve the page → remove the duplication → 301 Redirect the old page when needed → update Internal Links → update the Sitemap → monitor performance after the change
- **REDIRECT**: use a 301 when the old page no longer has an independent reason to exist and its value has been moved to another page
- **CANONICAL**: do not use it as the default fix for Cannibalization. Use it only when there is a Duplicate or Near Duplicate version that has to stay available for a technical or UX reason, but you want to tell search engines which version is the main one
- **RETARGET**: if a URL has started ranking by mistake on a Cluster that belongs to another page, redefine the page's topic and adjust Title / H1 / Content / Internal Anchors / Context
- **NOINDEX / REMOVE**: do not reach for these quickly. Use them only when the page has no independent value, or is Thin, or Duplicate, does not need to rank, and does not deserve a Merge or Redirect in the usual way

## 13. Internal Linking Audit

Check the internal links of the competing pages. Look for cases such as: a large number of Internal Links pointing to Page A while their Anchor Text talks about Page B's Topic, or the site linking to two different pages using the same Anchor Cluster.

Set a Primary Page for each Intent, then adjust the Internal Linking so it is clear.

## 14. Anchor Text Collision

Build an `Incoming Internal Anchor Profile` for each page, then look for the same Anchor pointing sometimes to URL A and sometimes to URL B, especially if the Anchor is a Primary Keyword. Treat it as an important Signal that the site itself is sending the search engine unclear signals.

## 15. Content Architecture Check

Do not analyze pages only in isolation. Place each page within: Topic → Pillar → Cluster → Supporting Content.

Ask: are the two pages supposed to be Parent + Child? Or are they really two Parent pages for the same topic? If it is the second, the Cannibalization Risk is higher.

## 16. Priority System

- **P1 (Critical)**: Same Intent + Strong Query overlap + URLs swapping Rankings + High impressions + high Business value
- **P2 (High)**: strong overlap, but performance is still fairly stable
- **P3 (Medium)**: Overlap exists, but the damage is unclear
- **P4 (Low / Monitor)**: limited similarity and not enough Evidence

## 17. Confidence Level

Every decision must include a confidence level: **High** / **Medium** / **Low**.

High example: GSC + SERP + Page analysis all confirm the same intent.
Low example: there is only Query overlap, without enough data.

## 18. Final Cannibalization Report

Output a table in the following format:

| Cluster | Query | URL A | URL B | Query Overlap | Intent A | Intent B | Page Type | Cannibalization | Evidence | Primary URL | Decision | Priority | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 18.1 Additional Required Deliverable: One Row per Keyword as Given (Per-Query Raw Table)

In addition to the Clusters table in section 18, when the user has provided a specific Keyword List as input to the analysis (especially when comparing two sites, Cross-Domain / Sister Sites), **always** provide a second, Raw table at the level of each individual keyword, not grouped into Clusters. This format is a core part of this skill's default deliverable, not an optional replacement for the Clusters table. Both are delivered together in the same report.

Rules for this table:

- **One row for each keyword exactly as the user gave it**, in the same order they sent it, with no deleting, merging or grouping. If a keyword is repeated in the original list, keep the repeat on its own row. If a row is not a real Query (a sentence or a note), leave it as is in its place and state that it is not a checkable Query instead of deleting it.
- **Required columns only** (do not add extra columns unless the user asks):
  1. Row number
  2. The keyword (exactly as given)
  3. Present on the first site? (Yes/No + the page or pages if present)
  4. Present on the second site? (Yes/No + the page or pages if present)
  5. Is there a conflict/Cannibalization? (Yes / No / Conflict between the two sites, with a short reason)
  6. What is the opportunity or the current situation? (a short, actionable recommendation)
- **Do not include a Priority column or a Confidence column in this table.** These two columns appear only in the Clusters table in section 18, not here.
- Fill the columns from the same evidence collected from GSC and the SERP check (sections 3, 6, 7). This table is a different view of the same analysis, not a separate analysis.
- Always provide this table as a default part of the final deliverable (not only when the user explicitly asks for it), because some users prefer to see each keyword they sent on its own instead of grouped into Clusters. State in the report that both tables (Clusters + Per-Query) are provided together.

## 19. Action Plan Per Case

After the table, give each case:

- **The problem**: explain why it counts as Cannibalization, or why it does not
- **Evidence**: state the evidence from GSC / SERP / Content / Intent / Internal Linking
- **Keep**: which elements should be kept?
- **Change**: what needs to be changed?
- **Primary URL**: name the main page
- **Secondary URL**: decide what happens to the other page
- **Internal Linking Changes**: list the links that need to change
- **Content Changes**: specify the Title / H1 / Sections or angles that need to change
- **Technical Action**: if any, 301 / Canonical / Noindex / Delete / Keep

## 20. Important Rules

Do not assume: `Same Keyword = Cannibalization`

The correct rule: `Same Intent + Same Search Job + Competing URLs + Evidence = Cannibalization`

- Do not merge two pages just because their keywords are similar
- Do not separate two pages just because their keywords are worded differently
- The decision must rest on: Intent / Topic / Page Type / SERP / GSC Performance / Website Architecture

## 21. Behaviour Rule

- Do not recommend a Merge before opening both pages and understanding each one
- Do not recommend a Delete based on Query overlap alone
- Do not pick the Primary URL based on Position alone
- Do not treat Exact Query overlap as final proof
- Always start with the Evidence, then the decision

## 22. Final Summary

At the end of every Audit, output:

- Number of URLs checked
- Number of Query Clusters
- Number of Potential Cannibalization Cases
- Confirmed Cannibalization
- Safe Overlaps
- Merge Cases
- Differentiate Cases
- Redirect Cases
- Technical Duplicate Cases
- The top 5 cases to execute first


---

Made by Hend Ibrahim · [hendebrahim.com](https://hendebrahim.com) · More skills: [github.com/hendibrahim-ai/claude-skills](https://github.com/hendibrahim-ai/claude-skills)
