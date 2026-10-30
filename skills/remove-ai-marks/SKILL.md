---
name: "remove-ai-marks"
description: "Strip the mechanical traces a model leaves in a file: invisible Unicode, oaicite and turn-search tokens, chatbot openers and sign-offs, knowledge-cutoff lines, unfilled [Your Name] placeholders, and provenance metadata (C2PA, EXIF, XMP, author fields) in docx, xlsx, pptx, pdf, png, jpg and webp. Use on: clean this file before I send it, strip AI metadata, remove hidden characters, remove C2PA, this file came from ChatGPT. Requests can be in Arabic or English. For the writing itself (phrasing, structure, AI-sounding style) use a humanizer skill (arabic-humanizer for Arabic text); this skill is the mechanical half and changes no wording."
---

# Remove AI marks

Two kinds of trace survive in a file that a model helped produce. One is
mechanical: characters and metadata a person never typed and cannot see. The
other is the writing itself. This skill handles the first kind only.

Most of it is genuinely invisible: a zero-width space or an `oaicite` token
changes nothing a reader would notice. One part is not, and it is worth being
straight about it. Chatbot residue ("Certainly! Here's...", "أتمنى أن يكون هذا
مفيدًا", "As of my last update...") is wording, and removing it is a small
editorial act. Two rules keep it safe: a phrase is only removed when it is a
**whole sentence** of its own, never a fragment of a longer one, and every
removal is reported with the exact text that came out. So a line like "Please
let me know if you have any questions" is left alone and flagged, because the
sentence belongs to the writer even though it shares words with a sign-off.

The writing is a humanizer skill's job (`arabic-humanizer` for Arabic text). Keep the two apart. Mixing them
produces the worst outcome, a file that was quietly reworded when the user only
asked to clean it.

## What it removes

| Layer | Content | Acts without asking |
| --- | --- | --- |
| Invisible | zero-width spaces, word joiners, soft hyphens, variation selectors, BOM, Hangul fillers | yes |
| Forensic tokens | `oaicite`, `turn0search3`, `contentReference`, `attached_file`, `grok_card`, "As an AI language model", the "Certainly!" opener | yes |
| Forensic sentences | "As of my last update...", "حسب معلوماتي حتى...", "I hope this helps", "Let me know if you'd like...", "أتمنى أن يكون هذا مفيدًا", "هل تريد مني أن..." | only when the phrase is a whole sentence; otherwise flagged |
| Typographic | odd spaces (NBSP, thin, narrow), curly quotes, em and en dashes, non-breaking hyphens, `…` | yes, and the em dash is a house rule here |
| Arabic punctuation | a Latin `,` `;` `?` sitting directly after an Arabic word becomes `،` `؛` `؟`. Digit separators (`1,240`) and Latin sentences inside an Arabic document are left alone | yes |
| Flagged | `[Your Name]`, `{{variable}}`, `2025-XX-XX`, `XXX`, Lorem ipsum, Cyrillic look-alikes inside Latin words | no, these need a real value |
| Metadata | author and last-modified-by fields, comments and revision parts, C2PA / Content Credentials, EXIF, XMP, PDF info and XMP streams | yes |

Two deliberate exceptions, both about Arabic:

- **Bidirectional marks** (RLM, LRM, isolates) are reported, never removed. In a
  line like `والـ ‏CTR‏ طلع 3.2%` they are what keeps the Latin and the digits
  in the right place. Stripping them scrambles the line in a way nobody notices
  until a client opens the file.
- **ZWNJ and ZWJ** are removed only when the text has no Arabic in it. In Arabic,
  Persian and Urdu they control how letters join, so they are legitimate
  typography, not a hidden mark.

## Running it

The work is done by `scripts/clean_marks.py`. It needs nothing but Python 3.7
and the standard library for text, Office files, PNG, JPEG and WebP. PDF uses
`pikepdf` if importable, otherwise the `qpdf` command; if neither is there, the
report says the PDF was not cleaned rather than implying it was.

```bash
python3 scripts/clean_marks.py inspect FILE [FILE ...]
python3 scripts/clean_marks.py clean   FILE [FILE ...] [--in-place]
```

**When another skill called this one, run `inspect` only.** A humanizer
skill delivers its result in chat and writes the file once at the end, so
producing a `.cleaned` file at that point hands the user a version they never
approved. Report the findings, and let the caller fold the fixes into the text
it is already showing.

When the user came here directly, inspect first and show what turned up, then clean. Two reasons this order is
worth the extra second: the user gets to see that a client deliverable carried
`Author: ChatGPT`, which is usually the thing they actually wanted to know; and
a file with nothing in it needs no new version.

Options worth knowing:

| Option | Effect |
| --- | --- |
| `--in-place` | overwrite the file. Without it, a sibling `name.cleaned.ext` is written |
| `--suffix .v2` | change that sibling suffix |
| `--keep-dashes` | leave em and en dashes alone, for a client whose style guide wants them |
| `--keep-quotes` | leave curly quotes alone, for typeset copy where they are correct |
| `--aggressive` | also map Cyrillic and Greek look-alikes to Latin. Off by default because a genuinely Russian word must survive |
| `--json` | machine-readable report, for processing many files |

Exit codes: `0` clean, `1` findings or changes, `3` something could not be fully
processed. A `3` is not a pass; say which file and why.

One false positive to expect, because it will happen: a file that *writes about*
these markers, a report, a log, a checklist, this skill's own text, gets flagged
for naming `oaicite` or "As of my last update". The script matches strings and
cannot tell a token from a mention of one. Read the finding before acting on it,
and never clean a document whose subject is AI provenance without checking what
the hits actually are.

**Inside an Office file, forensic sentences are reported, not removed.** A
leftover "I hope this helps!" on a slide or a `[Your Name]` in a Word paragraph
is named by `inspect` and left where it is by `clean`, which touches only
characters in that file: deleting a sentence from a slide changes the layout,
and a placeholder needs a real value. Those belong in the review loop a
humanizer skill runs, not in a silent script pass.

Several files at once is normal, and a whole folder is a glob:

```bash
python3 scripts/clean_marks.py clean ~/Deliverables/*.docx ~/Deliverables/*.png
```

## Reporting

State what was removed with counts, because a count is checkable and "cleaned
the file" is not. Then state what was left and why: a placeholder that needs a
value, a bidi mark that belongs there, a look-alike letter awaiting a decision.
Name the output file.

What not to say: that the file is now undetectable, or that it will pass any
particular checker. What this skill removes is real and verifiable. Whether some
tool still flags the file is a different question and not one to promise on.
A statistical watermark in the token choices, C2PA soft binding, and audio or
video watermarks are all out of scope; say so if the user asks about them.

## Then what

When the file holds prose the user is about to send, the mechanical pass is half
the job. Say so in one line and offer a humanizer skill (`arabic-humanizer` for Arabic), which covers the
writing: the staged openings, the "not X but Y" construction, the triads, the
flat sentence rhythm. Do not start rewriting here.

When the request was to humanize in the first place and you arrived through a
humanizer skill, run this pass, report the counts, and hand control back.

## Ethics

This is hygiene for the user's own work: their metadata, their client files.
Fine to clean a deliverable before it ships, or to keep an author field out of a
document going to a client.

Not fine, and worth saying plainly once rather than helping around it: passing
this off as proof a human wrote something, or defeating an academic integrity
process or a disclosure a user is obliged to make. Clean the file, and let the
claim about who wrote it be the user's own honest one.


---

Made by Hend Ibrahim · [hendebrahim.com](https://hendebrahim.com) · More skills: [github.com/hendibrahim-ai/claude-skills](https://github.com/hendibrahim-ai/claude-skills)
