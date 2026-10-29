---
name: arabic-humanizer
description: "Clean AI-sounding Arabic writing so it reads like an Arabic speaker wrote it. Covers Modern Standard Arabic and Egyptian dialect, and any format: pasted text, an article, an email, a social post, a WhatsApp message, UI copy, or a Word, PowerPoint or Excel file edited in place. Use when the user asks to humanize Arabic text, says an Arabic draft sounds like ChatGPT or like a translation, wants an Arabic post, deck or email checked before sending, or asks whether Arabic text looks AI-written. Requests can be in Arabic or English. Not for English-only text."
---

# Arabic Humanizer

AI models learn most of their writing from English. When they write Arabic, a lot of that English comes through: English idioms translated word for word, English sentence rhythm, English punctuation, and a stiff, bureaucratic register that no Arabic writer uses unless they are filling in a government form. Arabic readers notice this in the first two lines, even when they can't say what's wrong.

This skill finds those tells and rewrites them in natural Arabic, without changing what the text says.

It works on:

- **Modern Standard Arabic (MSA)** and **Egyptian Arabic**. Other dialects follow the same method; keep the writer's dialect and don't convert it.
- **Any context:** article, email, social post, chat message, slide deck, report, spreadsheet, UI copy, speech transcript.
- **Any input:** pasted text, `.md` or `.txt`, and `.docx`, `.pptx` and `.xlsx` files edited in place with the included script. PDFs can be read but not written back.

The instructions are in English. The examples are in Arabic, because they are the phrases this skill looks for, and each one has an English gloss.

---

## 1. Hard rules

1. **Add no facts.** No new numbers, names, dates, sources, quotes or examples. If the text is empty of substance, say so and ask for the missing facts. Don't fill the gap with nicer wording.
2. **Keep the meaning and the stance.** A hedge stays a hedge, an opinion stays an opinion, and a strong claim stays strong.
3. **Keep the register.** MSA stays MSA and Egyptian stays Egyptian. Never translate, and never "upgrade" dialect to MSA.
4. **Leave sacred and quoted text alone.** Quran, hadith, poetry, legal clauses and direct quotes are copied exactly.
5. **No em dashes or en dashes** in the output. Arabic doesn't use them. Use `،` or `.` or `:` instead.
6. **Show before you write.** For a file, work in chat first and write the file once, at the end, to a new path.
7. **Don't chase detector scores.** AI detectors are unreliable on Arabic (see section 9). The goal is good Arabic, not a number.

---

## 2. Before you edit: read the text

### Register

Decide which register the text is in, because the fixes differ:

| Register | Signs |
|---|---|
| MSA | tanwin (ـًا، ـٌ), future with سـ / سوف, negation with لا / لم / لن, ليس |
| Egyptian | مش، ده، دي، دول، إزاي، ليه، عشان، future with هـ / حـ, negation with مش / مفيش / ما...ش |
| Mixed | an MSA article with Egyptian quotes, or the reverse. Keep each part in its own register |

A register **slip** is a finding on its own: an Egyptian WhatsApp message that suddenly says "سوف أرسل لك الملف" (I shall send you the file) reads as machine-written.

### Context

| Context | How to recognise it |
|---|---|
| Article / web page | headings, paragraphs, links, maybe a target keyword |
| Email | greeting, a person addressed, a request |
| Social post | short, a hook at the top, hashtags |
| Chat / WhatsApp | short lines, dialect, no formatting |
| Slide deck | slide numbers, short titles, bullets |
| Report | numbered sections, tables, a summary |
| Spreadsheet | cells, headers, a notes column |
| UI copy | buttons, error messages, labels |
| Transcript | repetition, filler words, missing punctuation |

If you can't tell, ask one short question.

### Lock these before touching anything

- Numbers, percentages, prices, dates, names of people, brands and products, links, code, table data.
- **SEO keywords** in an article: the keyword and its count stay the same. Rewrite around it.
- Headings' order and levels, slide count and order, spreadsheet headers that formulas depend on.
- **Anything only the writer could know**: their own numbers, a client story, a tool they use by name, a year count. Keep it even if the wording is rough. It's the most human part of the text.

---

## 3. The invisible layer

AI-generated Arabic often carries characters you can't see, and they can break layout or give the text away. Check for:

- Zero-width characters and stray direction marks (U+200B, U+200C, U+200D, U+200E, U+200F, U+061C).
- Citation tokens left by chat tools: `oaicite`, `turn0search`, `contentReference`.
- Tatweel (ـ) used to stretch words for no reason: "جـــديد".
- Latin punctuation inside Arabic sentences: `,` `;` `?` where `،` `؛` `؟` belong. Leave digit separators alone (`1,240`).

If the `remove-ai-marks` skill is installed, run it in inspect mode and fold its findings into your edit. If it isn't, check these by hand and say that file metadata (author fields, C2PA) was not checked.

---

## 4. What to look for

Each pattern has a **Change** or **Report** label. **Change** patterns are fixed by default. **Report** patterns are things good Arabic writers also do on purpose, so you list them and let the user decide, unless they ask for a full pass.

### Group 1: English wearing Arabic words

The biggest group. The sentence is grammatical, but it was thought in English.

**1.1 Word-for-word idioms** · Change

| AI Arabic | It's really | Natural Arabic |
|---|---|---|
| يلعب دورًا هامًا | "plays an important role" | مهم / يساعد في |
| في نهاية المطاف | "at the end of the day" | في الآخر / أخيرًا, or delete |
| على أساس يومي | "on a daily basis" | يوميًا / كل يوم |
| خذ في اعتبارك | "take into consideration" | انتبه إلى / خلّي بالك |
| الأمر كله يتعلق بـ | "it's all about" | المهم هو |
| من ناحية أخرى (with no contrast) | "on the other hand" as filler | delete |
| أتمنى أن تصلك هذه الرسالة وأنت بخير | "I hope this email finds you well" | delete, or a real greeting the writer would use |

**1.2 "Not just X, but Y"** · Change

> "لا يقتصر الأمر على السرعة، بل يمتد ليشمل الأمان" (It's not limited to speed, it extends to security)
> "ليس مجرد تطبيق، بل رفيقك اليومي" (Not just an app, but your daily companion)

This is the English "it's not just X, it's Y" in Arabic clothes, and it's the strongest single tell. Say both things plainly: "التطبيق سريع وآمن" (The app is fast and secure).

**1.3 The empty opening** · Change

> "في عالم يتسم بالتطور المتسارع..." (In a world of rapid change...)
> "في ظل التقدم التكنولوجي الذي نشهده اليوم..." (Given the technological progress we see today...)
> "هذا ما سنعرفه في السطور القادمة" (That's what we'll find out in the coming lines)

Test: would this sentence fit an article about anything? Then delete it and start with the first real fact.

**1.4 Announcing a point instead of making it** · Change

> "تجدر الإشارة إلى أن" / "من الجدير بالذكر أن" / "لا بد من التنويه إلى أن" (It is worth noting that...)

Delete the announcement and keep the point.

**1.5 Studies and experts with no names** · Change

> "تشير الدراسات إلى..." (Studies indicate...) / "يؤكد الخبراء أن..." (Experts confirm...)

If the text names the study, keep it. If not, cut the attribution. If the sentence carries a number, keep the number, cut "studies show", and tell the user the number needs a source.

### Group 2: bureaucratic grammar

**2.1 يتم + verbal noun** · Change

> "يتم إعداد التقرير" (The preparing of the report is done) / "يتم استخدام الأداة"

Arabic has verbs. Use them: "نُعدّ التقرير" / "الفريق يستخدم الأداة" / Egyptian: "بنجهّز التقرير". If no one in the text is doing the action, rephrase without an actor ("التقرير شهري") rather than invent one.

**2.2 Stacked verbal nouns** · Change

> "تعزيز فعالية استدامة الكفاءة التشغيلية" (enhancing the effectiveness of the sustainability of operational efficiency)

Unstack them into a verb and an object: "نشغّل الفريق بكفاءة لمدة أطول".

**2.3 Passive that hides who did it** · Change when it hides responsibility, Report otherwise

> "مما أثار تساؤلات" (which raised questions: raised by whom?)
> "تم اتخاذ قرار" (a decision was taken: by whom?)

If the text knows who, name them. Formal scientific and legal Arabic uses the passive correctly, so only report it there.

**2.4 Waw chains** · Change

> "وتعد المنصة من أبرز المنصات، وتوفر أدوات متنوعة، وتتميز بواجهة سهلة، وتدعم عدة لغات"

One sentence joined by و four times. Split it into two or three sentences with full stops.

**2.5 The same opener everywhere** · Change

Paragraph after paragraph starting with "يُعد", "يُمثل", "يعتبر", "تلعب". Change the way in: start with the subject, a number, or a short statement.

### Group 3: weight with nothing inside

**3.1 Intensifiers** · Change

> "بشكل كبير" / "بصورة ملحوظة" / "على نحو فعّال" / "بشكل أساسي"

Read the sentence without them. If it means the same, they go.

**3.2 Sales superlatives** · Change

> "الحل الأمثل" (the optimal solution) / "نقلة نوعية" (a quantum leap) / "ثورة حقيقية" (a true revolution) / "لا غنى عنه" (indispensable)

Replace with something checkable ("يجهّز الطلب في 20 دقيقة") or cut.

**3.3 Riders that add nothing** · Change when empty, Report when they carry a fact

> "...مما يسهم في تعزيز تجربة المستخدم" (...which contributes to enhancing the user experience)
> "...الأمر الذي يعكس التزامنا بالجودة" (...which reflects our commitment to quality)

**3.4 Vague "big names"** · Change

> "الشركات الكبرى تعتمد على هذه الطريقة" (Major companies rely on this method)

Swap in any other company and any other method: if the sentence is still "true", it says nothing. Ask the user for the real name or case, or cut it.

**3.5 Certainty nobody can back** · Change

> "خلال خمس سنوات لن يحتاج أحد إلى مصمم" (In five years nobody will need a designer)

Replace with what the writer actually saw ("طلبات التصميم عندي قلّت النص السنة دي"), but only if the text or the user gives you that fact. If the writer really holds the strong view, keep it.

### Group 4: shape and punctuation

**4.1 Latin punctuation in Arabic** · Change

A Latin comma after an Arabic word looks like a translation. Use `،` `؛` `؟`. Keep digits as they are.

**4.2 Dashes** · Change

The em dash isn't Arabic punctuation. Replace each one with what the sentence needs: `،` or `:` or a new sentence.

**4.3 Triples** · Report

> "بسرعة وأمان وموثوقية" (quickly, safely and reliably)

AI reaches for three. Arabic rhetoric also loves three, so report it and let the user choose. In a full pass, keep the one that carries information.

**4.4 Every heading in the same mould** · Report

> "أهمية الطبخ المنزلي / مميزات الطبخ المنزلي / فوائد الطبخ المنزلي"

Make each heading say what's under it. In an SEO article, keyword placement wins over variety.

**4.5 Every paragraph the same length** · Change (not in decks or spreadsheets)

Real writing has a long paragraph next to a one-liner. Let each one run as long as its point needs.

**4.6 Bold and emoji everywhere** · Change

Bold the one fact that matters per paragraph. Emoji belong in chat and some social posts, not in reports, formal email or web copy.

### Group 5: wrong register

**5.1 MSA inside Egyptian** · Change

In a chat message or an Egyptian post: no tanwin, no سوف, no لم / لن. Use هـ / حـ for the future and مش / مفيش / ما...ش for negation.

> "سوف أرسل لك الملف لاحقًا" → "هبعتلك الملف كمان شوية"

**5.2 Customer-service cheer** · Change

> "بالتأكيد!" (Certainly!) / "يسعدني أن أساعدك" (I'm happy to help you) / "لا تتردد في التواصل" (Don't hesitate to reach out)

No Egyptian writes this to a colleague. Cut it or use what the writer would say.

**5.3 Stacked courtesy** · Change

> "أود أن أعرب عن خالص شكري وتقديري لحضرتكم" (I would like to express my sincere thanks and appreciation to you)

→ "شكرًا جدًا" or "شكرًا لحضرتك على..." with the actual reason.

### Group 6: chatbot leftovers

**6.1 Chat replies pasted into the document** · Change

> "بالطبع! إليك المقال:" (Of course! Here's the article:)
> "أتمنى أن يكون هذا مفيدًا" (I hope this is helpful)
> "هل تريد مني أن أكتب نسخة أقصر؟" (Do you want me to write a shorter version?)
> "حسب معلوماتي حتى تاريخ..." (According to my information up to...)

Delete them. No writer puts these in their own text.

**6.2 Unfilled placeholders** · Report

> "[اسم الشركة]" / "[التاريخ]" / "[Your Name]"

Never fill or delete a placeholder by guessing. Ask the user what goes there.

---

## 5. Extra rules by context

**Article.** Open with the answer to the reader's question in the first three lines. Paragraphs of four lines or fewer, with different lengths. Keep the keywords and heading levels. If cleaning removes more than 15% of the words, say the article needed content, not polish, and name what's missing.

**Email.** Short. The request in the first two lines. One request and one deadline at the end. Keep the level of formality the writer chose (حضرتك stays حضرتك).

**Social post.** The first two lines are the hook, never a definition or "في عالم اليوم". End with a real question or a next step, not "ما رأيكم؟" on its own.

**Chat / WhatsApp.** Dialect, short lines, the writer's own particles (يعني، بقى، خلاص، طيب). Nothing that sounds like a call centre.

**Slide deck.** The title states the conclusion: "الطلبات زادت 40%" (orders rose 40%), not "نتائج الطلبات" (order results). If there are no numbers, don't invent one: list the titles that need a figure and ask. No bullet gets longer than it was. Same slide count and order.

**Spreadsheet.** Headers stay short and unchanged if anything refers to them. Clean the notes columns, not the data.

**UI copy.** A button is one verb: "احفظ", not "اضغط هنا للحفظ". An error message says how to fix the problem, not "عذرًا، حدث خطأ ما" (Sorry, something went wrong).

**Transcript.** Confirm what the transcript says first, since speech-to-text mangles numbers and English terms written in Arabic letters. Remove filler like "حلو الكلام؟", "تمام؟", "من الآخر". Keep every example and number the speaker gave. Ask where the text is going before restructuring it.

---

## 6. Editing files

For `.docx`, `.pptx` and `.xlsx`, don't rewrite inside the file blindly. Pull the text out, agree the edits in chat, then write a new file once:

```bash
# 1. list the text units, numbered
python3 scripts/doc_text.py extract deck.pptx

# 2. after the user approves the edits
python3 scripts/doc_text.py apply deck.pptx --edits edits.txt --out deck.v2.pptx
```

`extract` prints units like this:

```
[[u2]]  slide 1:p1  (slide1)
لا يقتصر الأمر على الطعم، بل يمتد ليشمل القيمة الغذائية
```

Show each unit's before and after in chat. When the user is done, write the approved units into `edits.txt` in the same `[[id]]` format and run `apply`. Units you leave out are copied unchanged.

Tell the user two things once:

- Inside a paragraph you changed, mixed formatting (one bold word, say) collapses to the paragraph's first style. `apply` lists those units.
- Slide space is fixed. A cleaner bullet that is longer will overflow, so keep it the same length or shorter.

To delete a line, give its unit the text `[[delete]]`. Deleting shifts later unit ids, so run `extract` again before another round.

The original file is never changed. Every write goes to a new file with a version number.

If `remove-ai-marks` is installed, run it on the new file last, so author fields and hidden metadata don't still say the file came from a chatbot.

---

## 7. How to deliver

Give the cleaned text in chat first, then a short report. Scale the report to the text: a three-line WhatsApp message needs one line of notes, not ten.

For a longer text, report:

1. **How AI it read before and after:** clean / light tells / clearly AI / needs real content. Decide by how many Change patterns you found and how serious they were, mostly groups 1 and 2.
2. **The main fixes**, up to five, each with one before → after from the text.
3. **What you reported but didn't change** (the Report patterns, placeholders, rough passages you kept because they carry the writer's own experience).
4. **What you removed for lack of a source.**
5. **What's missing**, if the text is thin: the one question that would fix it ("What was the real number?", "Which customer?").
6. **One verification line**, for example: "Checked: nothing added, all 6 numbers and 2 links unchanged, Egyptian register kept."

If the text is so empty that cleaning would leave almost nothing, don't rewrite it from scratch, because that means inventing content. Say so and ask for the raw material.

---

## 8. Final check before delivering

- [ ] Nothing in the output that wasn't in the input.
- [ ] Every number, name, date and link is identical. Compare them one by one.
- [ ] Locked items intact: keywords, headings, slide count, headers, the writer's own details.
- [ ] Each sentence means what it meant, with the same certainty.
- [ ] Register unchanged, with no MSA slipped into dialect or the reverse.
- [ ] Arabic punctuation in Arabic sentences, and no em or en dashes.
- [ ] No placeholder filled or removed by guessing.
- [ ] Read it again for the patterns in section 4. A fix sometimes creates a new tell, such as every sentence becoming short.
- [ ] Report patterns were listed, not silently changed, unless the user asked for a full pass.

If something fails, fix it and check again.

---

## 9. About AI detectors

Detectors do badly on Arabic. Formal MSA is uniform by nature, so human-written Arabic gets flagged as AI often. Don't use a detector's percentage as evidence, don't promise the user their text is "undetectable", and if they want a rewrite only to lower a detector score, tell them it isn't a reliable target and offer this pass instead. Text that carries the writer's own facts and voice doesn't need to win that game.

---

## 10. Don't use this skill on

- English-only text
- Quran, hadith, religious text and poetry
- Legal contracts and regulatory text
- Code, config files and data
- Hiding plagiarism or getting around academic integrity checks


---

Made by Hend Ibrahim · [hendebrahim.com](https://hendebrahim.com) · More skills: [github.com/hendebrahim-ai/claude-skills](https://github.com/hendebrahim-ai/claude-skills)
