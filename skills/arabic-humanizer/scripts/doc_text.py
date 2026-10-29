#!/usr/bin/env python3
"""
doc_text.py: pull the prose out of a document, and put an edited version back.

Cleaning marks is mechanical and safe to do in place. Rewriting prose is a
judgement call the user has to see first, so this script never rewrites anything
by itself: it hands you numbered units, then writes a new file once you hand the
edited units back.

  python3 doc_text.py extract FILE [--json] [--out DUMP]
  python3 doc_text.py apply   FILE --edits EDITS [--out NEWFILE]

EDITS is either a JSON object mapping unit id to new text, or the marker format
`extract` prints, which you can edit and feed straight back:

    [[s1p1]]  slide 1  (body)
    the new text for that unit

A unit left out of EDITS is copied through untouched, byte for byte. To remove a
unit's line entirely, give it the single word [[delete]] as its new text.

Unit ids come from the unit's position in the file, not from a running count, so
they stay the same between rounds of edits. A deletion is the one thing that
shifts them; the script says so when it happens.

Formatting survives everywhere except inside a paragraph you changed, where the
new text takes the formatting of that paragraph's first run: a rewritten sentence
has no way of knowing which half of it used to be bold. Every affected unit is
named in the report.

Supported: .docx .pptx .xlsx (extract + apply), .pdf .txt .md (extract only).
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

VERSION = "2.0"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
SS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
DELETE = "[[delete]]"


def _register():
    ET.register_namespace(
        "w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    ET.register_namespace(
        "a", "http://schemas.openxmlformats.org/drawingml/2006/main")
    ET.register_namespace(
        "", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")


# ---------------------------------------------------------------------------
# element helpers
# ---------------------------------------------------------------------------

def node_text(el, t_tag):
    return "".join(t.text or "" for t in el.iter(t_tag))


def set_node_text(el, t_tag, new):
    """Write `new` into the first text node and drop the runs that held the rest.

    Blanking the other runs instead of removing them leaves empty formatting
    marks that Word and PowerPoint still carry, so the run element goes. Returns
    True when more than one run was involved, the case where inline formatting
    could not be preserved."""
    parents = {c: p for p in el.iter() for c in p}
    nodes = list(el.iter(t_tag))
    if not nodes:
        return False
    nodes[0].text = new
    nodes[0].set(XML_SPACE, "preserve")
    for n in nodes[1:]:
        run = parents.get(n)
        grand = parents.get(run)
        if run is not None and grand is not None:
            grand.remove(run)
        else:
            n.text = ""
    return len(nodes) > 1


def drop_element(root, el):
    for parent in root.iter():
        for child in list(parent):
            if child is el:
                parent.remove(child)
                return True
    return False


# ---------------------------------------------------------------------------
# per-format walkers: each yields (unit_id, label, element, text)
# ---------------------------------------------------------------------------

def docx_walk(z, names):
    def code(part):
        if part.endswith("word/document.xml"):
            return "p", "body"
        m = re.search(r"(header|footer)(\d*)", part)
        return (m.group(1)[0] + (m.group(2) or "1") + "p", m.group(1))
    parts = ([n for n in names if n == "word/document.xml"]
             + sorted(n for n in names
                      if re.match(r"word/(header|footer)\d*\.xml$", n)))
    for part in parts:
        root = ET.fromstring(z.read(part))
        prefix, where = code(part)
        for i, el in enumerate(root.iter(W + "p")):
            yield part, root, "%s%d" % (prefix, i), \
                "%s (%s)" % (where, docx_kind(el)), el, node_text(el, W + "t"), \
                W + "t"


def docx_kind(para):
    for st in para.iter(W + "pStyle"):
        v = st.get(W + "val", "")
        if v.lower().startswith("heading"):
            return "heading " + v[-1] if v[-1].isdigit() else "heading"
        if "title" in v.lower():
            return "title"
    for _ in para.iter(W + "numPr"):
        return "list item"
    return "paragraph"


def pptx_walk(z, names):
    def num(n):
        m = re.search(r"slide(\d+)\.xml$", n)
        return int(m.group(1)) if m else 0
    slides = sorted((n for n in names
                     if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=num)
    for part in slides:
        root = ET.fromstring(z.read(part))
        sn = re.search(r"slide(\d+)", part).group(1)
        for i, el in enumerate(root.iter(A_NS + "p")):
            yield part, root, "s%sp%d" % (sn, i), "slide %s" % sn, el, \
                node_text(el, A_NS + "t"), A_NS + "t"
    notes = sorted((n for n in names
                    if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)),
                   key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)))
    for part in notes:
        root = ET.fromstring(z.read(part))
        sn = re.search(r"notesSlide(\d+)", part).group(1)
        for i, el in enumerate(root.iter(A_NS + "p")):
            yield part, root, "n%sp%d" % (sn, i), "notes %s" % sn, el, \
                node_text(el, A_NS + "t"), A_NS + "t"


def xlsx_walk(z, names):
    parts = ([n for n in names if n == "xl/sharedStrings.xml"]
             + sorted(n for n in names
                      if re.match(r"xl/worksheets/sheet\d+\.xml$", n)))
    for part in parts:
        root = ET.fromstring(z.read(part))
        shared = part.endswith("sharedStrings.xml")
        tag = SS + ("si" if shared else "is")
        prefix = "c" if shared else "w%sc" % re.search(r"sheet(\d+)", part).group(1)
        for i, el in enumerate(root.iter(tag)):
            yield part, root, "%s%d" % (prefix, i), \
                "cell text" if shared else "sheet cell", el, \
                node_text(el, SS + "t"), SS + "t"


WALKERS = {".docx": docx_walk, ".docm": docx_walk,
           ".pptx": pptx_walk, ".pptm": pptx_walk,
           ".xlsx": xlsx_walk, ".xlsm": xlsx_walk}


# ---------------------------------------------------------------------------
# zip-backed extract and apply
# ---------------------------------------------------------------------------

def zip_extract(path, walker):
    z = zipfile.ZipFile(str(path))
    units = []
    for part, root, uid, label, el, text, t_tag in walker(z, z.namelist()):
        if text.strip():
            units.append({"id": uid, "loc": label, "text": text})
    z.close()
    return units


def zip_apply(path, walker, edits, out_path):
    _register()
    z = zipfile.ZipFile(str(path))
    names = z.namelist()
    roots, touched, collapsed, deleted, unknown = {}, [], [], [], set(edits)
    for part, root, uid, label, el, text, t_tag in walker(z, names):
        roots.setdefault(part, root)
        root = roots[part]
        if uid not in edits:
            continue
        unknown.discard(uid)
        new = edits[uid]
        if not text.strip():
            continue
        if new.strip().lower() == DELETE:
            if drop_element(root, el):
                deleted.append(uid)
            continue
        if new != text:
            if set_node_text(el, t_tag, new):
                collapsed.append(uid)
            touched.append(uid)
    repl = {}
    for part, root in roots.items():
        if any(u.startswith(tuple()) for u in []):
            pass
        repl[part] = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
    with zipfile.ZipFile(str(out_path), "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zipfile.ZipFile(str(path)).infolist():
            data = repl.get(item.filename) or z.read(item.filename)
            zout.writestr(item, data)
    z.close()
    return touched, collapsed, deleted, sorted(unknown)


# ---------------------------------------------------------------------------
# pdf and plain text: extract only
# ---------------------------------------------------------------------------

def blocks(text, prefix="b"):
    units = []
    for i, block in enumerate(re.split(r"\n\s*\n", text)):
        if block.strip():
            units.append({"id": "%s%d" % (prefix, i),
                          "loc": "heading" if block.lstrip().startswith("#")
                                 else "block",
                          "text": block.strip("\n")})
    return units


def pdf_extract(path):
    if not shutil.which("pdftotext"):
        raise SystemExit("PDF extraction needs the pdftotext command "
                         "(poppler-utils); it is not installed")
    out = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                         capture_output=True)
    if out.returncode != 0:
        raise SystemExit("pdftotext failed: %s"
                         % out.stderr.decode("utf-8", "replace")[:300])
    text = out.stdout.decode("utf-8", "replace")
    return [{"id": u["id"], "loc": "page text",
             "text": " ".join(u["text"].split())} for u in blocks(text)]


def plain_extract(path):
    return blocks(path.read_text(encoding="utf-8", errors="replace"))


# ---------------------------------------------------------------------------
# edits parsing and reporting
# ---------------------------------------------------------------------------

MARKER = re.compile(r"^\s*\[\[([A-Za-z]+\d+(?:[A-Za-z]+\d+)*)\]\].*$")


def parse_edits(path):
    raw = Path(path).read_text(encoding="utf-8")
    if raw.lstrip().startswith("{"):
        return json.loads(raw)
    edits, current, buf = {}, None, []
    for line in raw.splitlines():
        m = MARKER.match(line)
        if m:
            if current:
                edits[current] = "\n".join(buf).strip("\n")
            current, buf = m.group(1), []
        elif current is not None:
            buf.append(line)
    if current:
        edits[current] = "\n".join(buf).strip("\n")
    return edits


def dump(units):
    out = []
    for u in units:
        out.append("[[%s]]  %s" % (u["id"], u["loc"]))
        out.append(u["text"])
        out.append("")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["extract", "apply"])
    p.add_argument("file")
    p.add_argument("--edits")
    p.add_argument("--out")
    p.add_argument("--json", action="store_true")
    p.add_argument("--version", action="version", version=VERSION)
    a = p.parse_args(argv)

    path = Path(a.file).expanduser()
    if not path.is_file():
        raise SystemExit("not a file: %s" % path)
    ext = path.suffix.lower()
    walker = WALKERS.get(ext)

    if a.mode == "extract":
        if walker:
            units = zip_extract(path, walker)
        elif ext == ".pdf":
            units = pdf_extract(path)
        else:
            units = plain_extract(path)
        payload = (json.dumps({"version": VERSION, "file": str(path),
                               "units": units}, ensure_ascii=False, indent=2)
                   if a.json else dump(units))
        if a.out:
            Path(a.out).write_text(payload, encoding="utf-8")
            print("%d unit(s) written to %s" % (len(units), a.out))
        else:
            print(payload)
        return 0

    if not a.edits:
        raise SystemExit("apply needs --edits")
    if not walker:
        raise SystemExit("apply is not supported for %s; for plain text and PDF "
                         "write the new file directly" % ext)
    edits = parse_edits(a.edits)
    if not edits:
        raise SystemExit("no units found in %s; each unit starts with a line "
                         "like [[s1p1]]" % a.edits)
    out_path = Path(a.out) if a.out else path.with_name(
        path.stem + ".humanized" + path.suffix)
    touched, collapsed, deleted, unknown = zip_apply(path, walker, edits,
                                                     out_path)
    print("wrote: %s" % out_path)
    print("units changed: %d%s" % (len(touched),
          (", deleted: %d" % len(deleted)) if deleted else ""))
    if collapsed:
        print("inline formatting collapsed to the first run in: %s"
              % ", ".join(collapsed))
    if deleted:
        print("DELETED units: %s" % ", ".join(deleted))
        print("ids after a deleted unit shift by one. Re-run extract on the "
              "new file before another round of edits.")
    if unknown:
        print("ids in the edits file that matched no unit: %s"
              % ", ".join(unknown))
    print("the original file was not modified")
    print("REMINDER: metadata lives outside the text. Run clean_marks.py clean "
          "on %s to clear the author fields the new file inherited." % out_path)
    return 0 if (touched or deleted) else 1


if __name__ == "__main__":
    sys.exit(main())
