#!/usr/bin/env python3
"""
clean_marks.py — inspect and remove AI provenance marks from text and files.

Runs on the Python standard library alone for text, Office files, PNG, JPEG and
WebP. PDF needs either the `pikepdf` module or the `qpdf` command; the report
says so when neither is present instead of pretending the file was cleaned.

Usage
  python3 clean_marks.py inspect FILE [FILE ...] [--json]
  python3 clean_marks.py clean   FILE [FILE ...] [--in-place | --suffix .cleaned]
                                 [--keep-dashes] [--keep-quotes] [--aggressive]
                                 [--json]

Exit codes: 0 nothing actionable found, 1 findings (inspect) or cleaned (clean),
2 usage or read error, 3 partial (a file could not be fully processed).
"""

import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

VERSION = "2.0"

# ---------------------------------------------------------------------------
# Character tables
# ---------------------------------------------------------------------------

# Invisible characters with no legitimate use in prose. Safe to delete in any
# script, which is why they are the usual carrier for a hidden text watermark.
INVISIBLE_ALWAYS = {
    "​": "ZERO WIDTH SPACE",
    "⁠": "WORD JOINER",
    "﻿": "ZERO WIDTH NO-BREAK SPACE / BOM",
    "᠎": "MONGOLIAN VOWEL SEPARATOR",
    "­": "SOFT HYPHEN",
    "͏": "COMBINING GRAPHEME JOINER",
    "⁡": "FUNCTION APPLICATION",
    "⁢": "INVISIBLE TIMES",
    "⁣": "INVISIBLE SEPARATOR",
    "⁤": "INVISIBLE PLUS",
    "ᅟ": "HANGUL CHOSEONG FILLER",
    "ᅠ": "HANGUL JUNGSEONG FILLER",
    "ㅤ": "HANGUL FILLER",
    "ﾠ": "HALFWIDTH HANGUL FILLER",
    "⠀": "BRAILLE PATTERN BLANK",
}

def _ranges(*pairs):
    out = {}
    for lo, hi, label in pairs:
        for cp in range(lo, hi + 1):
            out[chr(cp)] = label
    return out

INVISIBLE_ALWAYS.update(_ranges(
    (0xFE00, 0xFE0F, "VARIATION SELECTOR"),
    (0xE0100, 0xE01EF, "VARIATION SELECTOR SUPPLEMENT"),
    (0xE0000, 0xE007F, "TAG CHARACTER"),
))

# Meaningful in Arabic, Persian and Urdu typography: they change how letters
# join. Deleting them silently corrupts Arabic text, so they are reported and
# only removed when the text has no Arabic in it.
JOINERS = {
    "‌": "ZERO WIDTH NON-JOINER",
    "‍": "ZERO WIDTH JOINER",
}

# Needed to lay out Arabic mixed with Latin or digits. Never removed
# automatically; reported so a human can judge.
DIRECTION = {
    "‎": "LEFT-TO-RIGHT MARK",
    "‏": "RIGHT-TO-LEFT MARK",
    "؜": "ARABIC LETTER MARK",
    "‪": "LEFT-TO-RIGHT EMBEDDING",
    "‫": "RIGHT-TO-LEFT EMBEDDING",
    "‬": "POP DIRECTIONAL FORMATTING",
    "‭": "LEFT-TO-RIGHT OVERRIDE",
    "‮": "RIGHT-TO-LEFT OVERRIDE",
    "⁦": "LEFT-TO-RIGHT ISOLATE",
    "⁧": "RIGHT-TO-LEFT ISOLATE",
    "⁨": "FIRST STRONG ISOLATE",
    "⁩": "POP DIRECTIONAL ISOLATE",
}

# Exotic spaces. A plain space carries the same meaning and no signal.
SPACES = {c: " " for c in
          "          "
          "     　"}

QUOTES = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "′": "'", "″": '"', "‵": "'", "‶": '"',
}

HYPHENS = "‐‑"
DASHES = "‒–—―−"

MISC = {
    "‐": "-",
    "‑": "-",
    "…": "...",
    "©": "(c)",
    "™": "(tm)",
}

# Cyrillic and Greek letters that render identically to Latin ones. A word that
# mixes scripts is either a deliberate mark or a copy-paste accident; either way
# it breaks search and spell-check.
# ---------------------------------------------------------------------------
# Forensic layer: artefacts of the generating model itself.
#
# Nothing here is a style judgement. A human writing by hand does not produce a
# citation token or tell you about their training cutoff, so these are removed
# without asking. Placeholders are the exception: deleting "[Your Name]" leaves
# a hole in the sentence, so those are reported for a human to fill.
# ---------------------------------------------------------------------------

FORENSIC_TOKENS = [
    (r"\u3010[^\u3011]{0,120}?(?:oaicite|turn\d+(?:search|view|file|news|image|forecast)\d+)[^\u3011]{0,120}\u3011",
     "citation token (oaicite / turn-search)"),
    (r"(?:cite)?turn\d+(?:search|view|file|news|image|forecast)\d+",
     "bare turn token"),
    (r"contentReference\s*(?:\[[^\]]*\])?", "contentReference marker"),
    (r"\boaicite\s*:?\s*\d*\]?", "oaicite marker"),
    (r"\battached_file\b[^\s]*", "attached_file marker"),
    (r"<\s*grok_card[^>]*>|\bgrok_card\b", "grok_card marker"),
    (r"\[\s*(?:citation|source)\s*:\s*\d+\s*\]", "numbered stub citation"),
    (r"(?i)\bas an AI (?:language )?model[^.\n]*[.!]?", "model self-reference"),
    (r"(?im)^\s*(?:certainly|sure|of course|absolutely|great question)\s*[!,.]\s*"
     r"(?=here|here's|i\b|below)", "chatbot opener"),
    (r"\u0628\u0627\u0644\u0637\u0628\u0639\s*!?\s*(?=\u0625\u0644\u064a\u0643)",
     "chatbot opener (Arabic)"),
]

# Whole-sentence patterns. Same intent, different safety rule: see
# strip_forensic, which drops a match only when it spans a complete sentence.
FORENSIC_PHRASES = [
    (r"(?i)\bas of (?:my )?(?:last|latest|the last) "
     r"(?:update|training|knowledge)[^.\n]*[.\n]", "knowledge-cutoff disclaimer"),
    (r"(?i)\bmy (?:knowledge|training data) (?:cut-?off|ends?)[^.\n]*[.\n]",
     "knowledge-cutoff disclaimer"),
    (r"(?i)\bI (?:don't|do not) have (?:access to )?real-?time[^.\n]*[.\n]",
     "real-time disclaimer"),
    (r"\u062d\u0633\u0628 \u0645\u0639\u0644\u0648\u0645\u0627\u062a\u064a \u062d\u062a\u0649[^.\n]*[.\n]",
     "knowledge-cutoff disclaimer (Arabic)"),
    (r"(?i)\bI hope this helps[^.\n!]*[.!]?", "chatbot sign-off"),
    (r"(?i)\blet me know if [^.\n!?]{0,70}[.!?]", "chatbot sign-off"),
    (r"(?i)\bfeel free to (?:ask|reach out|let me know)[^.\n!?]*[.!?]",
     "chatbot sign-off"),
    (r"\u0623\u062a\u0645\u0646\u0649 \u0623\u0646 \u064a\u0643\u0648\u0646 (?:\u0647\u0630\u0627|\u062f\u0647) \u0645\u0641\u064a\u062f[^.\n!\u061f]*[.!\u061f]?",
     "chatbot sign-off (Arabic)"),
    (r"\u0647\u0644 \u062a\u0631\u064a\u062f \u0645\u0646\u064a \u0623\u0646[^\u061f\n]*\u061f", "chatbot sign-off (Arabic)"),
]

FORENSIC_FLAG = [
    (r"(?i)\[\s*(?:your|insert|add|enter|company|client|brand|recipient|name|"
     r"date|topic|product)\b[^\]]{0,30}\]", "unfilled placeholder"),
    (r"\{\{[^}]{1,40}\}\}", "unfilled template variable"),
    (r"\[(?:\u0627\u0633\u0645\u0643|\u0627\u0633\u0645 [^\]]{0,25}|\u0623\u062f\u062e\u0644[^\]]{0,25}|\u0636\u0639[^\]]{0,25}|\u0627\u0644\u062a\u0627\u0631\u064a\u062e)\]",
     "unfilled placeholder (Arabic)"),
    (r"\b20\d\d-XX-XX\b|\bXX/XX/(?:XX|20\d\d)\b|\bMM/DD/YYYY\b|\bYYYY-MM-DD\b",
     "placeholder date"),
    (r"(?<![A-Za-z])X{3,}(?![A-Za-z])", "placeholder blank"),
    (r"(?i)\b(?:lorem ipsum|dolor sit amet)\b", "filler text"),
]

FORENSIC_TOKENS_RE = [(re.compile(p), lbl) for p, lbl in FORENSIC_TOKENS]
FORENSIC_PHRASES_RE = [(re.compile(p), lbl) for p, lbl in FORENSIC_PHRASES]
FORENSIC_FLAG_RE = [(re.compile(p), lbl) for p, lbl in FORENSIC_FLAG]

_SENT_END = ".!?\u061f\u06d4"


def _covers_whole_sentence(text, start, end):
    """True when [start:end) begins a sentence and ends one.

    A sign-off phrase is only safe to delete as a unit. "Please let me know if
    you have any questions." matches from "let", which leaves "Please" stranded,
    so that match is refused: the text before it on the line is a real clause,
    not a sentence boundary."""
    before = text[:start]
    line_start = before.rfind("\n") + 1
    head = before[line_start:].strip()
    if head and head[-1] not in _SENT_END:
        return False
    if end > start and text[end - 1] in _SENT_END:
        return True
    tail = text[end:]
    nl = tail.find("\n")
    rest = (tail if nl < 0 else tail[:nl]).strip()
    if rest and rest[0] in _SENT_END:
        return True
    return rest == ""


def scan_forensic(text):
    out = []
    for rx, label in FORENSIC_TOKENS_RE:
        n = len(rx.findall(text))
        if n:
            out.append({"id": "forensic", "label": label, "count": n,
                        "confidence": "confirmed"})
    for rx, label in FORENSIC_PHRASES_RE:
        whole = [m for m in rx.finditer(text)
                 if _covers_whole_sentence(text, m.start(), m.end())]
        partial = len(list(rx.finditer(text))) - len(whole)
        if whole:
            out.append({"id": "forensic", "label": label, "count": len(whole),
                        "confidence": "confirmed"})
        if partial:
            out.append({"id": "forensic_partial",
                        "label": "%s, but inside a longer sentence" % label,
                        "count": partial, "confidence": "likely_false_positive"})
    for rx, label in FORENSIC_FLAG_RE:
        n = len(rx.findall(text))
        if n:
            out.append({"id": "forensic_flag", "label": label, "count": n,
                        "confidence": "confirmed"})
    merged = {}
    for f in out:
        k = (f["id"], f["label"])
        merged.setdefault(k, {"id": f["id"], "label": f["label"], "count": 0,
                              "confidence": f["confidence"]})
        merged[k]["count"] += f["count"]
    return list(merged.values())


def _shorten(t, limit=70):
    t = " ".join(t.split())
    return t if len(t) <= limit else t[:limit - 1] + "\u2026"


def strip_forensic(text):
    actions = []
    for rx, label in FORENSIC_TOKENS_RE:
        hits = [m.group(0) for m in rx.finditer(text)]
        if hits:
            text = rx.sub("", text)
            actions.append({"action": "removed %s" % label, "count": len(hits),
                            "detail": "removed: %s" % _shorten(" | ".join(hits))})

    for rx, label in FORENSIC_PHRASES_RE:
        removed, kept = [], 0
        out, pos = [], 0
        for m in rx.finditer(text):
            if _covers_whole_sentence(text, m.start(), m.end()):
                out.append(text[pos:m.start()])
                removed.append(m.group(0))
                pos = m.end()
            else:
                kept += 1
        out.append(text[pos:])
        text = "".join(out)
        if removed:
            actions.append({"action": "removed %s" % label,
                            "count": len(removed),
                            "detail": "removed: %s" % _shorten(" | ".join(removed))})
        if kept:
            actions.append({
                "action": "left %s alone" % label, "count": kept,
                "detail": "the phrase sits inside a longer sentence, so cutting "
                          "it would break the sentence; review by hand"})
    for rx, label in FORENSIC_FLAG_RE:
        n = len(rx.findall(text))
        if n:
            actions.append({"action": "left %s in place" % label, "count": n,
                            "detail": "needs a real value, cannot be guessed"})
    # a deleted mid-sentence token can leave doubled spaces or a stranded space
    # before punctuation; tidy that without touching line structure
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r" +([,.;:!?\u061b\u060c\u061f])", r"\1", text)
    text = re.sub(r"\n[ \t]*(?:\n[ \t]*)+\n", "\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, actions


HOMOGLYPHS = {
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c",
    "у": "y", "х": "x", "і": "i", "ј": "j", "һ": "h",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M",
    "Н": "H", "О": "O", "Р": "P", "С": "C", "Т": "T",
    "У": "Y", "Х": "X", "І": "I", "Ј": "J",
    "α": "a", "ο": "o", "ρ": "p", "ν": "v", "κ": "k",
    "Α": "A", "Β": "B", "Ε": "E", "Η": "H", "Ι": "I",
    "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P",
    "Τ": "T", "Χ": "X",
}

AI_META_HINT = re.compile(
    rb"(c2pa|contentcredential|content_credential|claude|anthropic|openai|chatgpt"
    rb"|gpt-4|gpt4|gemini|synthid|copilot|midjourney|stable ?diffusion|dall-?e"
    rb"|firefly|generativeai|generative-ai|ai-generated|aigenerated)", re.I)

ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")

TEXT_EXT = {
    ".txt", ".md", ".markdown", ".mdx", ".html", ".htm", ".xml", ".csv", ".tsv",
    ".json", ".yaml", ".yml", ".srt", ".vtt", ".rst", ".tex", ".py", ".js",
    ".ts", ".jsx", ".tsx", ".css", ".scss", ".php", ".rb", ".go", ".java",
    ".c", ".h", ".cpp", ".sh", ".sql", ".ini", ".toml", ".log",
}
OFFICE_EXT = {".docx", ".xlsx", ".pptx", ".docm", ".xlsm", ".pptm",
              ".odt", ".ods", ".odp", ".epub"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff",
             ".avif", ".heic"}


# ---------------------------------------------------------------------------
# Text layer
# ---------------------------------------------------------------------------

ARABIC_LETTER = r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]"
ARABIC_PUNCT_MAP = [(",", "\u060c"), (";", "\u061b"), ("?", "\u061f")]


def fix_arabic_punctuation(t):
    """Latin , ; ? directly after an Arabic word become their Arabic forms.
    A digit or a Latin letter before the mark leaves it alone, so 1,240 and an
    English sentence inside an Arabic document both survive untouched."""
    n = 0
    for latin, arabic in ARABIC_PUNCT_MAP:
        t, k = re.subn(r"(?<=%s)%s" % (ARABIC_LETTER, re.escape(latin)), arabic, t)
        n += k
    return t, n


def scan_text(text):
    """Return findings without changing anything."""
    has_arabic = bool(ARABIC_RE.search(text))
    found = {}
    forensic = scan_forensic(text)

    def bump(key, label, char, conf):
        e = found.setdefault(key, {"label": label, "count": 0,
                                   "chars": set(), "confidence": conf})
        e["count"] += 1
        e["chars"].add("U+%04X" % ord(char))

    for ch in text:
        if ch in INVISIBLE_ALWAYS:
            bump("invisible", "invisible character with no textual role",
                 ch, "confirmed")
        elif ch in JOINERS:
            bump("joiner", "joiner (meaningful in Arabic, suspicious elsewhere)",
                 ch, "probable" if not has_arabic else "informational")
        elif ch in DIRECTION:
            bump("direction", "bidirectional control (often legitimate in Arabic)",
                 ch, "informational")
        elif ch in SPACES:
            bump("space", "non-standard space", ch, "probable")
        elif ch in QUOTES:
            bump("quote", "curly quotation mark", ch, "informational")
        elif ch in DASHES:
            bump("dash", "em or en dash", ch, "informational")
        elif ch in MISC:
            bump("misc", "typographic substitute", ch, "informational")
    if has_arabic:
        _, n = fix_arabic_punctuation(text)
        if n:
            found["arabic_punct"] = {
                "label": "Latin comma, semicolon or question mark after an "
                         "Arabic word", "count": n, "chars": set(),
                "confidence": "probable"}

    for word in re.findall(r"\S+", text):
        latin = sum(1 for c in word if "a" <= c.lower() <= "z")
        mixed = [c for c in word if c in HOMOGLYPHS]
        if latin and mixed:
            for c in mixed:
                bump("homoglyph", "Cyrillic or Greek look-alike inside a Latin word",
                     c, "confirmed")

    out = []
    for key, e in found.items():
        out.append({
            "id": key,
            "label": e["label"],
            "count": e["count"],
            "codepoints": sorted(e["chars"]),
            "confidence": e["confidence"],
        })
    out.sort(key=lambda d: -d["count"])
    return forensic + out, has_arabic


def clean_text(text, keep_dashes=False, keep_quotes=False, aggressive=False):
    """Return (cleaned_text, list_of_actions)."""
    has_arabic = bool(ARABIC_RE.search(text))
    actions = []

    def note(what, n, detail=""):
        if n:
            actions.append({"action": what, "count": n, "detail": detail})

    # 0. forensic layer: model artefacts
    text, fa = strip_forensic(text)
    actions.extend(fa)

    # 1. invisible characters: always out
    n = sum(text.count(c) for c in INVISIBLE_ALWAYS)
    if n:
        text = text.translate({ord(c): None for c in INVISIBLE_ALWAYS})
        note("removed invisible characters", n)

    # 2. joiners: only where no Arabic can be harmed
    n = sum(text.count(c) for c in JOINERS)
    if n:
        if has_arabic:
            note("kept joiners (Arabic text, removing them would break letter shapes)",
                 n, "review manually if the text is not Persian/Urdu styled")
        else:
            text = text.translate({ord(c): None for c in JOINERS})
            note("removed zero-width joiners", n)

    # 3. direction marks: never automatic
    n = sum(text.count(c) for c in DIRECTION)
    if n:
        note("kept bidirectional controls", n,
             "needed for Arabic mixed with Latin or digits; remove by hand if unwanted")

    # 4. exotic spaces
    n = sum(text.count(c) for c in SPACES)
    if n:
        text = text.translate({ord(c): " " for c in SPACES})
        note("normalised non-standard spaces", n)

    # 5. quotes
    if not keep_quotes:
        n = sum(text.count(c) for c in QUOTES)
        if n:
            text = text.translate({ord(k): v for k, v in QUOTES.items()})
            note("straightened curly quotes", n)

    # 6. dashes: a range between digits keeps a hyphen, elsewhere a comma
    if not keep_dashes:
        n = sum(text.count(c) for c in DASHES)
        if n:
            sep = "\u060c " if has_arabic else ", "
            text = re.sub(r"(?<=\w)\s*[%s]\s*(?=\w)" % DASHES,
                          lambda m: "-" if m.string[m.start() - 1].isdigit()
                          else sep, text)
            text = re.sub(r"^[%s]\s*" % DASHES, "", text, flags=re.M)
            text = re.sub(r"\s*[%s]\s*" % DASHES, sep, text)
            text = re.sub(r"([,\u060c])\s*\1", r"\1", text)
            text = re.sub(r"[ \t]+([,.;:!?\u060c\u061b\u061f])", r"\1", text)
            note("replaced em and en dashes", n, "digit ranges kept a hyphen")

    # 6b. Arabic sentences take Arabic punctuation
    if has_arabic:
        text, n = fix_arabic_punctuation(text)
        note("switched Latin punctuation to Arabic", n,
             "digit separators and Latin sentences untouched")

    # 7. misc typographic substitutes
    n = sum(text.count(c) for c in MISC)
    if n:
        for k, v in MISC.items():
            text = text.replace(k, v)
        note("expanded typographic substitutes", n)

    # 8. homoglyphs: opt-in, because a genuinely Cyrillic word must survive
    mixed_total = 0
    def fix_word(m):
        nonlocal mixed_total
        w = m.group(0)
        latin = sum(1 for c in w if "a" <= c.lower() <= "z")
        hits = [c for c in w if c in HOMOGLYPHS]
        if latin and hits:
            mixed_total += len(hits)
            if aggressive:
                return "".join(HOMOGLYPHS.get(c, c) for c in w)
        return w
    new = re.sub(r"\S+", fix_word, text)
    if mixed_total:
        if aggressive:
            text = new
            note("mapped look-alike letters to Latin", mixed_total)
        else:
            note("found look-alike letters, left in place", mixed_total,
                 "rerun with --aggressive to map them")

    # 9. tidy trailing whitespace, keep the line count
    stripped = re.sub(r"[ \t]+$", "", text, flags=re.M)
    if stripped != text:
        note("trimmed trailing whitespace",
             sum(1 for a, b in zip(text.split("\n"), stripped.split("\n")) if a != b))
        text = stripped

    return text, actions


# ---------------------------------------------------------------------------
# Image layer: chunk and segment surgery, pixels untouched
# ---------------------------------------------------------------------------

PNG_DROP = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME", b"caBX", b"caNv"}
PNG_KEEP = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM",
            b"sRGB", b"iCCP", b"pHYs", b"bKGD", b"sBIT", b"hIST", b"sPLT",
            b"acTL", b"fcTL", b"fdAT", b"cICP", b"mDCv", b"cLLi"}

def png_process(data, do_clean):
    findings, actions = [], []
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return data, findings, actions, "not a PNG"
    out = bytearray(data[:8])
    i = 8
    while i + 8 <= len(data):
        length = struct.unpack(">I", data[i:i + 4])[0]
        ctype = data[i + 4:i + 8]
        end = i + 12 + length
        if end > len(data):
            break
        blob = data[i:end]
        body = data[i + 8:i + 8 + length]
        drop = ctype in PNG_DROP or (ctype not in PNG_KEEP and not ctype[:1].isupper())
        if drop:
            label = ctype.decode("latin-1")
            hint = ""
            m = AI_META_HINT.search(body[:2000])
            if ctype == b"caBX" or b"c2pa" in body[:200].lower():
                hint = "C2PA / Content Credentials"
            elif m:
                hint = "names %s" % m.group(0).decode("latin-1", "replace")
            elif b"prompt" in body[:200].lower():
                hint = "generator note"
            findings.append({"id": "png_chunk", "label": "PNG %s chunk%s"
                             % (label, " (" + hint + ")" if hint else ""),
                             "count": 1, "confidence":
                             "confirmed" if hint else "probable"})
            if do_clean:
                actions.append({"action": "removed PNG %s chunk" % label,
                                "count": 1, "detail": hint})
                i = end
                continue
        out += blob
        i = end
        if ctype == b"IEND":
            break
    return bytes(out), findings, actions, None


JPEG_DROP = {0xE1: "APP1 (EXIF / XMP)", 0xEB: "APP11 (JUMBF / C2PA)",
             0xED: "APP13 (Photoshop / IPTC)", 0xEE: "APP14 (Adobe)",
             0xEF: "APP15", 0xE3: "APP3", 0xE4: "APP4", 0xE5: "APP5",
             0xE6: "APP6", 0xE7: "APP7", 0xE8: "APP8", 0xE9: "APP9",
             0xEA: "APP10", 0xEC: "APP12", 0xFE: "COM (comment)"}

def jpeg_process(data, do_clean):
    findings, actions = [], []
    if not data.startswith(b"\xff\xd8"):
        return data, findings, actions, "not a JPEG"
    out = bytearray(data[:2])
    i = 2
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            break
        marker = data[i + 1]
        if marker == 0xDA:  # start of scan: copy the rest verbatim
            out += data[i:]
            i = len(data)
            break
        seglen = struct.unpack(">H", data[i + 2:i + 4])[0]
        end = i + 2 + seglen
        if end > len(data):
            break
        body = data[i + 4:end]
        if marker in JPEG_DROP:
            label = JPEG_DROP[marker]
            low = body[:300].lower()
            hint = ""
            m = AI_META_HINT.search(body[:4000])
            if b"jumbf" in low or b"c2pa" in low:
                hint = "C2PA / Content Credentials"
            elif m:
                hint = "names %s" % m.group(0).decode("latin-1", "replace")
            elif b"xmp" in low or b"adobe:ns" in low:
                hint = "XMP"
            elif b"exif" in low:
                hint = "EXIF"
            findings.append({"id": "jpeg_segment",
                             "label": "JPEG %s%s" % (label, " (" + hint + ")" if hint else ""),
                             "count": 1,
                             "confidence": "confirmed" if hint else "probable"})
            if do_clean:
                actions.append({"action": "removed JPEG %s" % label,
                                "count": 1, "detail": hint})
                i = end
                continue
        out += data[i:end]
        i = end
    return bytes(out), findings, actions, None


WEBP_DROP = {b"EXIF", b"XMP ", b"C2PA"}

def webp_process(data, do_clean):
    findings, actions = [], []
    if not (data[:4] == b"RIFF" and data[8:12] == b"WEBP"):
        return data, findings, actions, "not a WebP"
    chunks, i = [], 12
    while i + 8 <= len(data):
        fourcc = data[i:i + 4]
        size = struct.unpack("<I", data[i + 4:i + 8])[0]
        pad = size + (size & 1)
        chunks.append((fourcc, data[i + 8:i + 8 + size], data[i:i + 8 + pad]))
        i += 8 + pad
    kept, dropped = [], False
    for fourcc, body, raw in chunks:
        if fourcc in WEBP_DROP:
            findings.append({"id": "webp_chunk",
                             "label": "WebP %s chunk" % fourcc.decode("latin-1").strip(),
                             "count": 1, "confidence": "confirmed"})
            if do_clean:
                actions.append({"action": "removed WebP %s chunk"
                                % fourcc.decode("latin-1").strip(), "count": 1,
                                "detail": ""})
                dropped = True
                continue
        kept.append((fourcc, body, raw))
    if not do_clean or not dropped:
        return data, findings, actions, None
    body_out = bytearray()
    for fourcc, body, raw in kept:
        if fourcc == b"VP8X" and len(body) >= 1:
            flags = body[0] & ~0b00001100  # clear the EXIF and XMP flags
            raw = raw[:8] + bytes([flags]) + raw[9:]
            actions.append({"action": "cleared VP8X metadata flags",
                            "count": 1, "detail": ""})
        body_out += raw
    out = b"RIFF" + struct.pack("<I", 4 + len(body_out)) + b"WEBP" + bytes(body_out)
    return out, findings, actions, None


def image_fallback(path, data, do_clean):
    """GIF, BMP, TIFF and friends: re-save through PIL with no metadata."""
    try:
        from PIL import Image
    except Exception:
        return data, [{"id": "image_unknown",
                       "label": "%s not inspected (needs the Pillow module)"
                                % path.suffix, "count": 1,
                       "confidence": "informational"}], [], "no Pillow"
    import io as _io
    findings, actions = [], []
    try:
        im = Image.open(_io.BytesIO(data))
        meta = {k: v for k, v in (im.info or {}).items()
                if k not in ("transparency", "background", "duration", "loop",
                             "icc_profile")}
        if meta:
            findings.append({"id": "image_meta",
                             "label": "%s metadata keys: %s"
                                      % (path.suffix, ", ".join(sorted(meta))[:120]),
                             "count": len(meta), "confidence": "probable"})
        if not do_clean:
            return data, findings, actions, None
        if not meta:
            return data, findings, actions, None
        buf = _io.BytesIO()
        clean = Image.new(im.mode, im.size)
        clean.putdata(list(im.getdata()))
        if im.mode == "P":
            clean.putpalette(im.getpalette())
        clean.save(buf, format=im.format)
        actions.append({"action": "re-saved %s without metadata" % path.suffix,
                        "count": len(meta),
                        "detail": "pixels preserved, container rebuilt"})
        return buf.getvalue(), findings, actions, None
    except Exception as exc:
        return data, findings, actions, "Pillow failed: %s" % exc


# ---------------------------------------------------------------------------
# Office / OpenDocument / EPUB layer
# ---------------------------------------------------------------------------

_REF_RE = re.compile(r"&#(?:x([0-9a-fA-F]+)|(\d+));")
_INTEREST = None


def _interesting_chars():
    global _INTEREST
    if _INTEREST is None:
        _INTEREST = (set(INVISIBLE_ALWAYS) | set(JOINERS) | set(SPACES)
                     | set(QUOTES) | set(MISC) | set(DASHES) | set(HYPHENS))
    return _INTEREST


def decode_char_refs(t):
    """Turn &#8203; / &#x200B; into the character, but only for the characters
    this script acts on. Everything else stays escaped exactly as it was."""
    def sub(m):
        cp = int(m.group(1), 16) if m.group(1) else int(m.group(2))
        ch = chr(cp)
        return ch if ch in _interesting_chars() else m.group(0)
    return _REF_RE.sub(sub, t)


TEXT_NODE_RE = re.compile(r"(<(?:w:t|a:t|t)(?:\s[^>]*)?>)([^<]*)(</(?:w:t|a:t|t)>)")
IDENTITY_FIELD_RE = re.compile(
    r"<(?:dc:creator|cp:lastModifiedBy|cp:revision|Company|Manager|Application"
    r"|meta:initial-creator|meta:generator)\b[^>]*>\s*([^<\s][^<]*)</", re.I)


def clean_xml_text_nodes(xml, keep_dashes=False, keep_quotes=False):
    """Normalise the characters inside <w:t> / <a:t> / <t> nodes only."""
    has_arabic = bool(ARABIC_RE.search(xml))
    tally = {}

    def bump(k, n):
        if n:
            tally[k] = tally.get(k, 0) + n

    def fix(m):
        t = decode_char_refs(m.group(2))
        n = sum(t.count(c) for c in INVISIBLE_ALWAYS)
        if n:
            t = t.translate({ord(c): None for c in INVISIBLE_ALWAYS})
            bump("invisible characters", n)
        if not has_arabic:
            n = sum(t.count(c) for c in JOINERS)
            if n:
                t = t.translate({ord(c): None for c in JOINERS})
                bump("zero-width joiners", n)
        n = sum(t.count(c) for c in SPACES)
        if n:
            t = t.translate({ord(c): " " for c in SPACES})
            bump("non-standard spaces", n)
        if not keep_quotes:
            n = sum(t.count(c) for c in QUOTES)
            if n:
                t = t.translate({ord(k): v for k, v in QUOTES.items()})
                bump("curly quotes", n)
        if not keep_dashes:
            n = sum(t.count(c) for c in DASHES)
            if n:
                sep = "\u060c " if has_arabic else ", "
                t = re.sub(r"(?<=\d)\s*[%s]\s*(?=\d)" % DASHES, "-", t)
                t = re.sub(r"\s*[%s]\s*" % DASHES, sep, t)
                t = re.sub(r"[ \t]+([,.;:!?\u060c\u061b\u061f])", r"\1", t)
                bump("em and en dashes", n)
        n = sum(t.count(c) for c in MISC)
        if n:
            for k, v in MISC.items():
                t = t.replace(k, v)
            bump("typographic substitutes", n)
        if has_arabic:
            t, n = fix_arabic_punctuation(t)
            bump("Latin punctuation after Arabic words", n)
        return m.group(1) + t + m.group(3)

    return TEXT_NODE_RE.sub(fix, xml), tally


OOXML_META_BLANK = ["dc:creator", "cp:lastModifiedBy", "cp:revision",
                    "cp:lastPrinted", "dc:description", "cp:keywords",
                    "cp:category", "cp:contentStatus"]
OOXML_APP_BLANK = ["Company", "Manager", "Template", "Application", "AppVersion"]
ODF_META_BLANK = ["meta:initial-creator", "dc:creator", "meta:generator",
                  "meta:editing-cycles", "meta:editing-duration",
                  "meta:printed-by"]
DROP_PARTS = re.compile(
    r"(word/(comments|commentsExtended|commentsIds|commentsExtensible|people)\.xml"
    r"|xl/(comments\d*|threadedComments/.*)\.xml"
    r"|ppt/(comments/.*|notesSlides/.*Comment.*)\.xml"
    r"|docProps/custom\.xml)$")



def _blank_tags(xml, tags):
    hits = 0
    for tag in tags:
        pat = re.compile(r"<%s\b[^>]*>.*?</%s>" % (re.escape(tag), re.escape(tag)),
                         re.S)
        xml, n = pat.subn("", xml)
        hits += n
    return xml, hits


def office_process(path, data, do_clean, keep_dashes, keep_quotes, aggressive):
    import io as _io
    findings, actions = [], []
    try:
        zin = zipfile.ZipFile(_io.BytesIO(data))
        names = zin.namelist()
    except Exception as exc:
        return data, findings, actions, "not a readable zip: %s" % exc

    for n in names:
        if DROP_PARTS.search(n):
            findings.append({"id": "office_part",
                             "label": "embedded part: %s" % n, "count": 1,
                             "confidence": "probable"})
    for n in names:
        if n in ("docProps/core.xml", "docProps/app.xml", "meta.xml",
                 "docProps/custom.xml"):
            raw = zin.read(n)
            hit = AI_META_HINT.search(raw)
            vals = IDENTITY_FIELD_RE.findall(raw.decode("utf-8", "replace"))
            if hit or vals:
                findings.append({
                    "id": "office_meta",
                    "label": "%s names %s" % (n, ", ".join(
                        v.strip() for v in vals)[:120] or "an authoring tool"),
                    "count": max(1, len(vals)),
                    "confidence": "confirmed" if hit else "probable"})

    text_parts = [n for n in names if n.endswith(".xml") and
                  re.search(r"(word/(document\d*|header\d*|footer\d*|footnotes|"
                            r"endnotes)|xl/sharedStrings|xl/worksheets/sheet\d+|"
                            r"ppt/(slides/slide\d+|notesSlides/notesSlide\d+)|"
                            r"content)\.xml$", n)]
    invisible_hits = 0
    dry_tally, prose = {}, []
    for n in text_parts:
        try:
            body = zin.read(n).decode("utf-8", "replace")
        except Exception:
            continue
        for mm in TEXT_NODE_RE.finditer(body):
            node = decode_char_refs(mm.group(2))
            invisible_hits += sum(node.count(c) for c in INVISIBLE_ALWAYS)
            prose.append(node)
        _, tally = clean_xml_text_nodes(body, keep_dashes, keep_quotes)
        for what, cnt in tally.items():
            dry_tally[what] = dry_tally.get(what, 0) + cnt
    if invisible_hits:
        findings.append({"id": "office_invisible",
                         "label": "invisible characters inside the document text",
                         "count": invisible_hits, "confidence": "confirmed"})
    for what, cnt in dry_tally.items():
        if what == "invisible characters":
            continue
        findings.append({"id": "office_typography",
                         "label": "%s in the document text" % what,
                         "count": cnt, "confidence": "probable"})
    # the prose inside the file gets the same forensic read a .md file gets, so
    # a leftover [Your Name] on a slide is reported rather than shipped
    for f in scan_forensic("\n".join(prose)):
        f = dict(f)
        f["label"] = "%s, in the document text" % f["label"]
        findings.append(f)

    if not do_clean:
        return data, findings, actions, None

    buf = _io.BytesIO()
    zout = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
    dropped = 0
    for item in zin.infolist():
        n = item.filename
        if DROP_PARTS.search(n):
            dropped += 1
            continue
        raw = zin.read(n)
        if n in ("docProps/core.xml", "docProps/app.xml", "meta.xml"):
            s = raw.decode("utf-8", "replace")
            tags = (OOXML_META_BLANK if n == "docProps/core.xml"
                    else OOXML_APP_BLANK if n == "docProps/app.xml"
                    else ODF_META_BLANK)
            s, hits = _blank_tags(s, tags)
            if hits:
                actions.append({"action": "cleared %d metadata field(s) in %s"
                                % (hits, n), "count": hits, "detail": ""})
            raw = s.encode("utf-8")
        elif n.endswith(".rels"):
            s = raw.decode("utf-8", "replace")
            s, hits = re.subn(
                r'<Relationship\b[^>]*Target="[^"]*'
                r'(comments|commentsExtended|commentsIds|commentsExtensible|people)'
                r'[^"]*"[^>]*/>', "", s)
            raw = s.encode("utf-8")
        elif n == "[Content_Types].xml":
            s = raw.decode("utf-8", "replace")
            s = re.sub(r'<Override\b[^>]*PartName="/[^"]*'
                       r'(comments|commentsExtended|commentsIds|commentsExtensible'
                       r'|people|custom)[^"]*"[^>]*/>', "", s)
            raw = s.encode("utf-8")
        elif n in text_parts:
            body = raw.decode("utf-8", "replace")
            body, tally = clean_xml_text_nodes(body, keep_dashes, keep_quotes)
            for what, cnt in tally.items():
                actions.append({"action": "normalised %s in %s" % (what, n),
                                "count": cnt, "detail": ""})
            raw = body.encode("utf-8")
        zout.writestr(item, raw)
    zout.close()
    if dropped:
        actions.append({"action": "removed %d comment or custom-property part(s)"
                        % dropped, "count": dropped, "detail": ""})
    return buf.getvalue(), findings, actions, None


# ---------------------------------------------------------------------------
# PDF layer
# ---------------------------------------------------------------------------

def pdf_process(path, data, do_clean, out_path):
    findings, actions = [], []
    hit = AI_META_HINT.search(data[:400000]) or AI_META_HINT.search(data[-200000:])
    if hit:
        findings.append({"id": "pdf_marker",
                         "label": "provenance marker in the PDF bytes: %s"
                                  % hit.group(0).decode("latin-1", "replace"),
                         "count": 1, "confidence": "confirmed"})
    try:
        import pikepdf
        have_pikepdf = True
    except Exception:
        have_pikepdf = False

    if have_pikepdf:
        try:
            with pikepdf.open(io_bytes(data)) as pdf:
                info = dict(pdf.docinfo) if pdf.docinfo is not None else {}
                if info:
                    findings.append({"id": "pdf_info",
                                     "label": "document info keys: %s"
                                              % ", ".join(str(k) for k in info),
                                     "count": len(info), "confidence": "probable"})
                if "/Metadata" in pdf.Root:
                    findings.append({"id": "pdf_xmp", "label": "XMP metadata stream",
                                     "count": 1, "confidence": "probable"})
                if not do_clean:
                    return data, findings, actions, None
                if info:
                    for k in list(info):
                        del pdf.docinfo[k]
                    actions.append({"action": "cleared %d document info key(s)"
                                    % len(info), "count": len(info), "detail": ""})
                for key in ("/Metadata", "/PieceInfo"):
                    if key in pdf.Root:
                        del pdf.Root[key]
                        actions.append({"action": "removed %s from the catalog" % key,
                                        "count": 1, "detail": ""})
                for page in pdf.pages:
                    for key in ("/Metadata", "/PieceInfo"):
                        if key in page.obj:
                            del page.obj[key]
                            actions.append({"action": "removed %s from a page" % key,
                                            "count": 1, "detail": ""})
                bio = io_bytes(b"")
                pdf.save(bio, linearize=False)
                return bio.getvalue(), findings, actions, None
        except Exception as exc:
            findings.append({"id": "pdf_error", "label": "pikepdf failed: %s" % exc,
                             "count": 1, "confidence": "informational"})

    if shutil.which("qpdf"):
        if not do_clean:
            return data, findings, actions, None
        tmp_in = out_path.with_suffix(".in.tmp.pdf")
        tmp_out = out_path.with_suffix(".out.tmp.pdf")
        tmp_in.write_bytes(data)
        rc = subprocess.run(["qpdf", "--empty", "--pages", str(tmp_in), "1-z", "--",
                             str(tmp_out)], capture_output=True)
        result = data
        if rc.returncode in (0, 3) and tmp_out.exists():
            result = tmp_out.read_bytes()
            actions.append({"action": "rebuilt the PDF with qpdf, dropping metadata",
                            "count": 1,
                            "detail": "page content preserved, info and XMP dropped"})
        for t in (tmp_in, tmp_out):
            if t.exists():
                t.unlink()
        return result, findings, actions, None if result is not data else "qpdf failed"

    return data, findings, actions, ("PDF needs the pikepdf module or the qpdf "
                                     "command; neither is present")


def io_bytes(b):
    import io as _io
    return _io.BytesIO(b)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def kind_of(path, data):
    ext = path.suffix.lower()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:2] == b"\xff\xd8":
        return "jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:5] == b"%PDF-":
        return "pdf"
    if data[:2] == b"PK" and ext in OFFICE_EXT:
        return "office"
    if ext in IMAGE_EXT:
        return "image"
    if ext in TEXT_EXT:
        return "text"
    try:
        data.decode("utf-8")
        return "text"
    except UnicodeDecodeError:
        return "unknown"


def process(path, do_clean, args):
    res = {"file": str(path), "kind": None, "findings": [], "actions": [],
           "note": None, "output": None}
    try:
        data = path.read_bytes()
    except Exception as exc:
        res["note"] = "could not read: %s" % exc
        res["kind"] = "error"
        return res
    kind = kind_of(path, data)
    res["kind"] = kind

    out_path = path if args.in_place else path.with_name(
        path.stem + args.suffix + path.suffix)

    if kind == "text":
        try:
            s = data.decode("utf-8")
            enc = "utf-8"
        except UnicodeDecodeError:
            s = data.decode("utf-8", "replace")
            enc = "utf-8"
            res["note"] = "file was not valid UTF-8; undecodable bytes replaced"
        findings, has_ar = scan_text(s)
        res["findings"] = findings
        res["arabic"] = has_ar
        if do_clean:
            new, actions = clean_text(s, args.keep_dashes, args.keep_quotes,
                                      args.aggressive)
            res["actions"] = actions
            if new != s:
                out_path.write_text(new, encoding=enc)
                res["output"] = str(out_path)
        return res

    if kind in ("png", "jpeg", "webp"):
        fn = {"png": png_process, "jpeg": jpeg_process, "webp": webp_process}[kind]
        new, findings, actions, note = fn(data, do_clean)
        res.update(findings=findings, actions=actions, note=note)
        if do_clean and new != data:
            out_path.write_bytes(new)
            res["output"] = str(out_path)
        return res

    if kind == "image":
        new, findings, actions, note = image_fallback(path, data, do_clean)
        res.update(findings=findings, actions=actions, note=note)
        if do_clean and new != data:
            out_path.write_bytes(new)
            res["output"] = str(out_path)
        return res

    if kind == "office":
        new, findings, actions, note = office_process(
            path, data, do_clean, args.keep_dashes, args.keep_quotes,
            args.aggressive)
        res.update(findings=findings, actions=actions, note=note)
        if do_clean and new != data:
            out_path.write_bytes(new)
            res["output"] = str(out_path)
        return res

    if kind == "pdf":
        new, findings, actions, note = pdf_process(path, data, do_clean, out_path)
        res.update(findings=findings, actions=actions, note=note)
        if do_clean and new != data:
            out_path.write_bytes(new)
            res["output"] = str(out_path)
        return res

    res["note"] = "unsupported file type, nothing attempted"
    return res


def render(results, do_clean):
    lines = []
    for r in results:
        lines.append("== %s  [%s]" % (r["file"], r["kind"]))
        if r.get("note"):
            lines.append("   note: %s" % r["note"])
        if not r["findings"]:
            lines.append("   nothing found")
        for f in r["findings"]:
            cps = (" " + " ".join(f["codepoints"])) if f.get("codepoints") else ""
            lines.append("   [%s] %s x%d%s"
                         % (f["confidence"], f["label"], f["count"], cps))
        if do_clean:
            if r["actions"]:
                lines.append("   --- done ---")
                for a in r["actions"]:
                    d = ("  (%s)" % a["detail"]) if a.get("detail") else ""
                    lines.append("   - %s: %d%s" % (a["action"], a["count"], d))
            if r.get("output"):
                lines.append("   wrote: %s" % r["output"])
            elif not r["actions"]:
                lines.append("   file left untouched")
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["inspect", "clean"])
    p.add_argument("files", nargs="+")
    p.add_argument("--in-place", action="store_true")
    p.add_argument("--suffix", default=".cleaned")
    p.add_argument("--keep-dashes", action="store_true",
                   help="leave em and en dashes as they are")
    p.add_argument("--keep-quotes", action="store_true",
                   help="leave curly quotation marks as they are")
    p.add_argument("--aggressive", action="store_true",
                   help="also map Cyrillic/Greek look-alikes to Latin")
    p.add_argument("--json", action="store_true")
    p.add_argument("--version", action="version", version=VERSION)
    args = p.parse_args(argv)

    do_clean = args.mode == "clean"
    results, partial = [], False
    for f in args.files:
        path = Path(f).expanduser()
        if not path.is_file():
            results.append({"file": str(path), "kind": "error",
                            "findings": [], "actions": [],
                            "note": "not a file"})
            partial = True
            continue
        r = process(path, do_clean, args)
        if r["kind"] in ("error", "unknown") or (r.get("note") and
                                                "needs" in str(r["note"])):
            partial = True
        results.append(r)

    if args.json:
        print(json.dumps({"version": VERSION, "mode": args.mode,
                          "results": results}, ensure_ascii=False, indent=2))
    else:
        print(render(results, do_clean))

    if partial:
        return 3
    if any(r["findings"] or r["actions"] for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
