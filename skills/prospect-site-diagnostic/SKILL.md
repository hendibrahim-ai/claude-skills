---
name: "prospect-site-diagnostic"
description: "Use when a prospect sends their website link and asks for a call, or replies to a proposal asking for a meeting. Turns that reply into a pre-meeting diagnostic document built on real measurements, plus a short message that books the call. Triggers: the prospect sent their site, prepare a file before the call, audit a prospect's website, reply to a client who asked for a meeting."
---

# Prospect Site Diagnostic Before the Meeting

When a prospect replies to a proposal, sends their website link and asks for a meeting, the output is two things: **a short message** that locks in the time, and **a diagnostic document** built on real measurements, not on impressions.

The goal is not a full report. The goal is three or four specific observations the prospect can check for themselves in a minute. That is what sets you apart from everyone else who applied to the same job.

---

## Governing Rules

1. **Every number in the document is measured from the site or from a tool. No numbers from memory.**
2. **Anything you can't prove goes in the "What we need data to determine" section at the end of the document**, instead of being stated as fact.
3. **The message is short and the document carries the details.** The message is not the place for the report.
4. **Never mention developers or the site's technical stack** in the document. If the recommendations need new pages, say "requires technical support on your side" and leave it there.
5. **No personal names and no agency name** in the document.
6. **No em dashes or en dashes.**

---

## Step 0: Summary of Understanding

Before any checks, come back to the user with a summary of the prospect's reply: what exactly they said, what they asked for, and where the conversation stands (proposal sent, waiting for a proposal, meeting requested). Get the user's confirmation before you start.

---

## Step 1: Scan the Site Structure

Pull directly from the site with fetch or from the browser:

- **sitemap.xml**: total number of URLs, and how they break down (core pages, articles, products, language versions)
- **robots.txt**: clean, or is something blocked
- **Homepage**: H1, H2 and H3 headings, menu links, hreflang, schema, word count
- **Service or product types announced in the copy**: these reveal page gaps
- **Search the whole homepage copy for any mention of price or cost**

The key question here: **does every announced service have its own page?** A missing page for an existing service is the strongest gap you will find, and the easiest one for the prospect to verify.

## Step 2: Measure a Sample of Pages

Open 12 to 16 pages that cover the full range, and measure for each one:

- Word count
- Number of H2 and H3 headings
- Whether there is video or images
- Title, meta description and URL

This table is the hard evidence nobody can argue with. Sort it by word count, ascending, so the gap shows.

**What to look for:** a repeated template, pages that are just a wrapper for a video, zero H3 headings, a title or URL that doesn't carry a query.

## Step 3: Demand Numbers

Pull a list of 25 to 40 keywords from a keyword tool (WriterZen Keyword Planner or whatever is available) covering:

- The main commercial query and its variants
- Every service type announced on the site
- Price, cost and booking
- The informational cluster the site already writes about

Take **the clusters and the volume of each**, not individual keywords.

**Two warnings:**

- **Don't add up two variants of the same query** ("best pizza cairo" and "best pizza in cairo"). Google serves them with the same ranking, so adding them is double counting, not extra demand.
- **Qualify difficulty with its scale.** KD on an ads scale says bidding is cheap, not that organic ranking is easy. Don't say "low competition" without looking at page one.

## Step 4: Search Results from the Prospect's Country (Mandatory)

**This is the most important step. Don't skip it.**

The search results you see from your location are completely different from what the prospect sees. Use **Nightwatch Search Simulator** (a browser extension) with Country = the prospect's country and Language = their language.

From page one, extract:

| Item | Why it matters |
|---|---|
| Every result and its type | Government, nonprofit, commercial platform, app store, social content |
| **Any price shown inside a search result** | If competitors show their prices and the prospect doesn't, that is the strongest observation in the document |
| **Any feature a competitor announces in its result snippet** | If it announces the prospect's own feature, that is a hit |
| "People also ask" (PAA) questions | Evidence from Google of the gaps |
| Related searches at the bottom of the page | Same thing |
| Whether there is an AI Overview and what its sources are | If a competitor is the source, that is a strong point |
| **Whether the prospect's site shows up at all** | |

**If the SERP data from the tool differs from live Google, go with Google and write that caveat in the document header.**

## Step 5: Check Ads

Open the **Google Ads Transparency Centre** and search **By domain** for the prospect's domain and for every commercial competitor on page one, with the region set to the prospect's country:

`https://adstransparency.google.com/search?region=<CC>&query=<domain>`

This answers: is the prospect advertising? Are competitors advertising? And if the space is empty, that is an opportunity to put forward as a parallel track.

**And state the other possibility honestly:** an empty ad space may mean nobody has found it, or it may mean people tried and the conversions didn't work. Suggest a limited test campaign before any scaling.

## Step 6: Quick Indexing Check

**One `site:domain` search and paging through the result pages**, not a separate search for every URL (that gets you blocked after about 30 searches).

Extract: the URLs that show up, whether there are subdomains or language versions, and the "we have omitted some entries very similar" message if it appears.

**That "very similar entries" message is gold-standard evidence of a repeated template, and it comes from Google itself.**

**Mandatory caveat:** the number of `site:` results is not the real indexing figure. Write the pattern, not the number, and put the exact number in the missing data section.

## Step 7: Prioritise

Rank by Impact × Confidence ÷ Effort, and order items by how close they are to a sale, not by search volume.

**A gap with proven demand, an existing feature and a missing page is always number one.**

---

## Building the Document

This order is tested:

1. **Header**: audit date, what was checked, source of the demand numbers, source of the search results data with caveats
2. **Summary**: the findings in four paragraphs, not the methodology
3. **Demand table**: the clusters and their volumes
4. **Observations** (3 to 5), each with a heading that states its finding
5. **What I found working well**: builds credibility before the criticism
6. **The opportunity**: the page one table with prices, and seasonality
7. **Where the work starts**: numbered items, and one line about the technical support needed
8. **Parallel track** if there is one (ads), with "What I can't promise"
9. **What we need data to determine**: a table of each item against what it would settle

### Writing Rules

- **Observation headings state the finding**, not "Observation one". Compare: "Observation three: page structure" versus "One template repeated across forty-one pages"
- **When you criticise existing work, state its value first.** "This does not mean the content was misplaced" turns the message from "your work was wasted" into "it is missing a layer"
- **Numbers come with real examples**: a specific URL or query, not abstract statistics

---

## Before Delivery

**Run a humanizer skill on the document and on the message** (`arabic-humanizer` in this repo when they are in Arabic).

Patterns that show up in this kind of document in particular:

- **Negative contrast (X, not Y)**: it repeats easily as a rhythm. Count it, and if it appears more than twice, clean it up
- **Headings that all follow the same template**
- **Superlatives**: "the clearest opportunity", "the most important point", "the biggest opportunity"
- **Bold as decoration** on every label

**Target: both read as clean, with no tells left from the patterns above.**

---

## Delivery

**The document:** a Google Doc built from HTML (add `dir="rtl"` when the document is in Arabic or another right-to-left language), with headings and tables that have a coloured header row. The available Drive tool only creates new files. It can't edit the content of an existing file, so any revised version = a new doc.

**Remind the user to open up sharing** (Anyone with the link, Viewer) before sending the link, or to download it as a PDF and upload that directly. With a new client, the PDF is safer.

**The message:**

- Under 180 words
- Opens with the strongest observation, not the methodology
- Each observation on its own line, with varied lengths
- The free offer with a specific deadline
- Suggested times in the prospect's time zone, outside their country's weekend
- Closes with a real diagnostic question that opens a discussion in the meeting

---

## Questions for the Meeting, Not the Document

Some things can't go on paper, and they are what decide the size of the offer:

- **The value of a single booking and the conversion rate** (they turn search numbers into revenue numbers)
- Have they tried ads before
- If the site has a supply side (service provider sign-up, agent accreditation): **which is harder for them, attracting customers or attracting service providers?** The answer to that can change the whole shape of the offer
- Access to Search Console


---

Made by Hend Ibrahim · [hendebrahim.com](https://hendebrahim.com) · More skills: [github.com/hendibrahim-ai/claude-skills](https://github.com/hendibrahim-ai/claude-skills)
