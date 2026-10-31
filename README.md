# Claude Skills for Arabic Writing, SEO and Ads

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Works with Claude, Codex, Cursor and Gemini CLI](https://img.shields.io/badge/works%20with-Claude%20%7C%20Codex%20%7C%20Cursor%20%7C%20Gemini%20CLI-8A63D2)
![New skill most days](https://img.shields.io/badge/new%20skill-most%20days-2ea44f)

Ready-to-install skills that teach your AI assistant how to do real work properly:

1. **Clean up AI-sounding writing**, especially in Arabic, where most tools fall short.
2. **Do real SEO work**: diagnose a site before touching it, find cannibalization and keyword gaps, read Search Console, and report what changed.
3. **Run and diagnose ad accounts** on Meta and Google Ads, with numbers checked before any change.
4. **Create content and grow on LinkedIn**: repurposing, captions in Arabic dialects, profile reviews and weekly plans.
5. **Run a freelance business**: proposals, onboarding, call notes and monthly client reports.
6. **Edit talking-head videos** with effects rendered on your own computer.

I use these skills every day on client work. Before publishing each one, I rewrite it in English, swap client details for everyday examples, and remove anything private. One new skill goes up most days.

---

## Contents

- [Who this is for](#who-this-is-for)
- [The skills](#the-skills)
- [Coming next](#coming-next)
- [Spotlight: arabic-humanizer](#spotlight-arabic-humanizer)
- [Install](#install)
- [How to use a skill](#how-to-use-a-skill)
- [How these skills are built](#how-these-skills-are-built)
- [About me](#about-me)
- [Feedback](#feedback)

---

## Who this is for

- **Writers, marketers and agencies working in Arabic** whose drafts come out of ChatGPT or Claude sounding translated, stiff or obviously machine-made.
- **SEO specialists and freelancers** who want Claude to follow a real method: diagnose first, then act, with numbers to back every recommendation.
- **Anyone sending files to clients** who needs Word, PowerPoint and Excel files without hidden AI traces.

You don't need to write code. If you can copy a folder or upload a zip file, you can use these.

---

## The skills

| Skill | What it does | Works on |
|---|---|---|
| [arabic-humanizer](skills/arabic-humanizer) | Cleans AI-sounding Arabic so it reads like an Arabic speaker wrote it: English idioms translated word for word, `يتم` constructions, empty openings, Latin punctuation, and MSA slipping into Egyptian. Works on pasted text and on Word, PowerPoint and Excel files edited in place. | Arabic text (MSA and Egyptian) |
| [remove-ai-marks](skills/remove-ai-marks) | Removes the mechanical traces a model leaves in a file, such as hidden Unicode characters, `oaicite` tokens, chatbot sign-offs, unfilled `[Your Name]` placeholders, and C2PA/EXIF/author metadata in docx, xlsx, pptx, pdf, png, jpg and webp. It changes no wording. Pairs with `arabic-humanizer`: that one fixes the writing, this one cleans the file. Image cleaning uses Pillow and PDF cleaning uses pikepdf or qpdf. | English and Arabic files |
| [seo-cannibalization-detector](skills/seo-cannibalization-detector) | Finds pages on the same site competing for the same queries, using Search Console data, the live results page and search intent, and ends with a decision for each case: merge, split, redirect, canonical or retarget. | Any site |

---

## Coming next

The release order for the coming weeks. Each one is checked off when it goes live.

- [x] [arabic-humanizer](skills/arabic-humanizer): clean AI-sounding Arabic
- [x] [remove-ai-marks](skills/remove-ai-marks): strip hidden characters, AI tokens and metadata from files
- [ ] seo-diagnosis: the thinking step before any SEO task (stage, bottleneck, hypothesis, priority)
- [x] [seo-cannibalization-detector](skills/seo-cannibalization-detector): pages competing for the same queries, and what to do with each
- [ ] keyword-gap-analyzer: target keywords with no page on the site, grouped and ranked
- [ ] gsc-audit: Search Console audit, period comparison and quick wins
- [ ] weekly-seo-report: what changed this week, whether it matters, and what to do first
- [ ] daily-search-console-check: a 5-minute morning check of Search Console, with three lines on what to do today
- [ ] gsc-indexing-check: check indexing for a list of URLs and log the result
- [ ] prospect-site-diagnostic: a measured site diagnosis to send a prospect before the first call
- [ ] rank-tracking-check: read a rank tracker and flag drops and lost keywords
- [ ] backlink-prospect-check: score backlink prospects with Semrush and Ahrefs metrics
- [ ] seo-case-study-evidence: collect and check the SEO evidence behind a case study
- [ ] seo-tool-evaluation: research an SEO tool end to end before you pay for it

**Then, ads:**

- [ ] meta-ads-campaign-playbook: plan, build and fix Meta campaigns, symptom by symptom
- [ ] google-ads-account-diagnostics: a full Google Ads diagnosis that checks tracking before anything else
- [ ] ads-complaint-reply: answer "the campaign isn't working" with the real numbers
- [ ] meta-lead-reconciliation: Meta says 3 leads, your CRM says 11; find out why
- [ ] meta-ads-placement-review: see which placements waste budget
- [ ] ads-account-operating-file: one living file per ad account, so nothing gets forgotten
- [ ] ads-case-study-evidence: the paid-media evidence behind a case study

**Then, content and LinkedIn:**

- [ ] business-context-file: one file with your offer, audience and voice that every other skill reads first
- [ ] content-repurposer: one article, video or podcast becomes a LinkedIn post, an X thread, an email and a carousel
- [ ] youtube-to-content: a YouTube video becomes a blog post, a post and three short-video scripts
- [ ] arabic-caption-writer: Instagram, Facebook and TikTok captions in Egyptian, Gulf or Modern Standard Arabic
- [ ] linkedin-profile-audit: review a LinkedIn profile and rewrite the headline, About and Featured
- [ ] linkedin-content-plan: a weekly LinkedIn plan built from your offer and your proof
- [ ] linkedin-post-mortem: which posts worked, why, and what to stop doing

**Then, running a freelance business:**

- [ ] call-notes-to-actions: a call transcript becomes a summary, decisions, tasks and a follow-up email
- [ ] monthly-client-report: your SEO or ads numbers become a short monthly client report
- [ ] client-onboarding-pack: welcome message, intake questions, access checklist and first-week plan
- [ ] freelance-proposal-writer: a proposal built on the client's own words in the job post
- [ ] freelancer-profile-audit: audit an Upwork or freelance profile, from title to portfolio

**Then, more SEO:**

- [ ] ai-search-visibility-check: can ChatGPT, Perplexity and AI Overviews find, read and cite your site?
- [ ] google-business-profile-audit: audit a Google Business Profile against the competitors around it
- [ ] salla-zid-store-seo: SEO for stores built on Salla and Zid
- [ ] content-refresh-planner: find old pages losing traffic and decide what to update first

**Then, video effects for talking-head clips:**

- [ ] head-pop-out: your head pops out over the top of a card
- [ ] grid-dive: a wall of video tiles, then the camera dives into yours
- [ ] title-orbit: your title spins in a 3D ring around your head
- [ ] magnifying-lens: a glass lens slides over your face and follows you

Star or watch the repo to see each one when it lands.

---

## Spotlight: arabic-humanizer

AI models learn most of their writing from English. When they write Arabic, the English shows: idioms translated word for word, English sentence rhythm, Latin commas, and a stiff, bureaucratic tone nobody uses in real life. Arabic readers notice it within two lines.

`arabic-humanizer` finds those tells and rewrites them in natural Arabic, without adding facts or changing what the text says.

### Before and after

**Before** (typical AI Arabic):

> في عالم يتسم بالتطور المتسارع، لا يقتصر الأمر على تقديم وجبات لذيذة، بل يمتد ليشمل تجربة متكاملة. يتم تحضير جميع الأطباق يوميًا بشكل كبير من المكونات الطازجة، مما يسهم في تعزيز رضا العملاء.
>
> *(In a world of rapid change, it's not limited to serving delicious meals, it extends to a complete experience. The preparing of all dishes is done daily to a great extent from fresh ingredients, which contributes to enhancing customer satisfaction.)*

**After:**

> نحضّر جميع الأطباق يوميًا من مكونات طازجة.
>
> *(We prepare all the dishes daily from fresh ingredients.)*

The empty opening, the "not just X, but Y" construction, the `يتم` passive, the intensifier and the "which contributes to enhancing" rider are all gone. What the text actually said stays, and so does the register: it was MSA, so it stays MSA. The skill would also ask for one real detail, such as which dish or what time the food is prepared, because that's what makes a text sound like its writer.

### What it catches

| Group | Examples it looks for |
|---|---|
| English wearing Arabic words | يلعب دورًا هامًا · في نهاية المطاف · لا يقتصر الأمر على... بل · في عالم يتسم بـ · تجدر الإشارة إلى أن |
| Bureaucratic grammar | يتم + verbal noun · stacked verbal nouns · sentences chained with و · the same opener in every paragraph |
| Weight with nothing inside | بشكل كبير · الحل الأمثل · نقلة نوعية · مما يسهم في تعزيز · "major companies use this" with no names |
| Shape and punctuation | Latin `,` instead of `،` · em dashes · every paragraph the same length · bold and emoji everywhere |
| Wrong register | سوف and tanwin inside Egyptian chat · بالتأكيد! · يسعدني أن أساعدك |
| Chatbot leftovers | بالطبع! إليك... · أتمنى أن يكون هذا مفيدًا · حسب معلوماتي حتى |

It also has rules for each kind of text (article, email, social post, WhatsApp, slide deck, spreadsheet, UI copy, speech transcript) and edits `.docx`, `.pptx` and `.xlsx` files without breaking their layout.

---

## Install

### Claude Code

Install every skill in the repo:

```bash
git clone https://github.com/hendibrahim-ai/claude-skills.git
cp -r claude-skills/skills/* ~/.claude/skills/
```

Or just one:

```bash
cp -r claude-skills/skills/arabic-humanizer ~/.claude/skills/
```

On Windows, the skills folder is `C:\Users\<you>\.claude\skills\`.

### Claude.ai (web and desktop app)

1. Download the repo: **Code → Download ZIP** at the top of this page.
2. Open the `skills` folder and zip the one skill folder you want (for example `arabic-humanizer`).
3. In Claude, go to **Settings → Capabilities → Skills**, click **Upload skill**, and choose that zip.

### OpenAI Codex, Cursor, Gemini CLI and other tools

These skills follow the open [Agent Skills](https://agentskills.io) format, so any tool that reads `SKILL.md` folders can use them. Copy the skill's folder into that tool's skills folder:

| Tool | Skills folder |
|---|---|
| OpenAI Codex CLI | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Cursor | `.cursor/skills/` in your project (Cursor also reads the Claude and Codex folders) |

Folder locations can change between versions, so check your tool's docs if a skill doesn't load.

### Requirements

Skills with a `scripts` folder need Python 3. Each skill's own `SKILL.md` lists anything else it needs.

---

## How to use a skill

You don't have to call a skill by name. Your AI assistant reads each skill's description and uses it when your request matches. For example:

- "Humanize this Arabic email before I send it to the client."
- "Check this PowerPoint deck. The Arabic sounds translated."
- In Arabic, too: "نقّي النص ده، شكله مكتوب بـ ChatGPT" (clean this text, it looks like ChatGPT wrote it)

To be sure a specific skill runs, name it: "Use arabic-humanizer on this post."

---

## How these skills are built

Every skill here follows the same rules:

- **No invented facts.** A skill never adds numbers, names, sources or examples that weren't in your input. If something is missing, it asks.
- **Your meaning stays.** Wording changes. The message, the stance and the level of certainty don't.
- **It shows before it writes.** For files, you see every change in chat first, and the original file is never overwritten.
- **Plain English instructions.** Every skill is written in English so anyone can read and adapt it, even the ones built for Arabic.
- **Real work, generalised.** Each one comes from client work. Client names, domains and private data are removed before publishing, and the examples are everyday ones: restaurants, bakeries, travel sites.

---

## About me

I'm Hend Ibrahim. I trained as a doctor, and I still use the rule I learned there: diagnose before you treat. Today I work as an SEO manager and a Top Rated freelancer, and I build Claude skills and automations that let me do SEO, Arabic content and reporting work faster without cutting corners.

🌐 [hendebrahim.com](https://hendebrahim.com) · 💼 [LinkedIn](https://www.linkedin.com/in/hendebrahim) · 🐙 [GitHub](https://github.com/hendibrahim-ai)

---

## Feedback

If a skill gets something wrong, [open an issue](https://github.com/hendibrahim-ai/claude-skills/issues) with the input you gave it and what you expected. I read every one.

## License

[MIT](LICENSE). Use, change and share these skills freely. Just keep the license file with them.
