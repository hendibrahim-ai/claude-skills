# Claude skills for SEO and clean writing

These are skills I use every day in Claude Code and Claude.ai, for SEO work and for writing that doesn't read like it came from a chatbot. All of them are written in English. Some are built for Arabic text, which few public skills handle well.

I built them for my own client work, then removed client names, domains and private links before publishing. I add a new skill here most days.

## The skills

| Skill | What it does | Works on |
|---|---|---|
| [arabic-humanizer](skills/arabic-humanizer) | Cleans AI-sounding Arabic so it reads like an Arabic speaker wrote it: English idioms translated word for word, `يتم` constructions, empty openings, Latin punctuation, and MSA slipping into Egyptian. Works on pasted text and on Word, PowerPoint and Excel files edited in place. | Arabic text (MSA and Egyptian) |

### arabic-humanizer: before and after

**Before** (typical AI Arabic):

> في عالم يتسم بالتطور المتسارع، لا يقتصر الأمر على تقديم وجبات لذيذة، بل يمتد ليشمل تجربة متكاملة. يتم تحضير جميع الأطباق يوميًا بشكل كبير من المكونات الطازجة، مما يسهم في تعزيز رضا العملاء.

**After:**

> نحضّر جميع الأطباق يوميًا من مكونات طازجة.

The empty opening, the "not just X, but Y" construction, the `يتم` passive, the intensifier and the "which contributes to enhancing" rider are all gone. What the text actually said stays, and so does the register: it was MSA, so it stays MSA. The skill would also ask for one real detail, such as which dish or what time the food is prepared, because that's what makes a text sound like its writer.

## Install

**Claude Code:** copy the skill's folder into `~/.claude/skills/`. For example:

```bash
cp -r skills/arabic-humanizer ~/.claude/skills/
```

**Claude.ai:** zip the skill's folder, then upload it in **Settings → Capabilities → Skills**.

Skills with a `scripts` folder need Python 3. Each skill's own file says if it needs anything else.

## Feedback

If a skill gets something wrong, open an issue with the input and what you expected. I read them.

More from me: [hendebrahim.com](https://hendebrahim.com) · [LinkedIn](https://www.linkedin.com/in/hendebrahim)

## License

[MIT](LICENSE)
