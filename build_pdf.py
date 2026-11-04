"""Build the submission PDF: cover page, main text (at most three pages), references, appendix.

Adapted from the LaTeX backend of Assignment 1 (01-coupon-impact/src/coupon_analysis/latex.py).
Understood Markdown subset: ## and ### headings, paragraphs, **bold**, *italic*, $...$, $$...$$, pipe tables
with a "**Table X.** caption" line directly above. Compiler: tectonic; pages are counted with pypdf.

    uv run --with pypdf python build_pdf.py
"""
from __future__ import annotations

import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).parent
PDF_NAME = "2226237U_simon_jensen"          # filename required by the assignment: studentid_firstname_lastname.pdf
MAX_PAGES = 3
LINE_SPREAD = "1.15"
MARGIN = "2.5cm"                             # layout of the Current Issues report (01-news-analysis)
PARSKIP = "5pt"
SECSKIP = "10pt"                         # more air than single spacing ("preferably double-spaced"), still three pages

PREAMBLE = r"""\documentclass[12pt,a4paper]{article}
\usepackage[a4paper,margin=%(margin)s]{geometry}
\usepackage{newtxtext,newtxmath}
\usepackage{amsmath}
\usepackage{booktabs,microtype,xurl}
\usepackage[labelfont=bf,labelsep=period,justification=justified,singlelinecheck=false,skip=4pt,font={normalsize}]{caption}
\usepackage[colorlinks=true,allcolors=black,pdftitle={%(title)s},pdfauthor={Simon Jensen},pdfsubject={Final Report, Topics in Econometrics B}]{hyperref}
\urlstyle{same}
\setlength{\parindent}{0pt}
\setlength{\parskip}{%(parskip)s plus 1pt}
\setlength{\abovedisplayskip}{4pt plus 2pt}
\setlength{\belowdisplayskip}{4pt plus 2pt}
\pagestyle{plain}
\linespread{%(spread)s}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\emergencystretch=3em
\relpenalty=10000
\binoppenalty=10000
\newcommand{\sect}[1]{\par\vspace{%(secskip)s}{\large\bfseries #1}\par\nopagebreak\vspace{2pt}}
\newcommand{\subsect}[1]{\par\vspace{0.2em}{\bfseries #1}\par\nopagebreak}
"""

_SPECIALS = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_UNICODE = {"−": r"\textminus{}", "α": r"$\alpha$", "τ": r"$\tau$", "–": "--", "×": r"$\times$", "ü": r"\"u"}


def _math(m: str) -> str:
    return re.sub(r"(?<=\d),(?=\d{3})", "{,}", m).replace("%", r"\%")


def _plain(text: str) -> str:
    if "—" in text:
        raise SystemExit("Em dash in the text. Rewrite the sentence without it.")
    text = re.sub(r'"([^"]*)"', "\x01\\1\x02", text)            # straight quotes -> typographic quotes
    out = "".join(_SPECIALS.get(ch) or _UNICODE.get(ch, ch) for ch in text)
    out = out.replace("\x01", "``").replace("\x02", "''")
    return out.replace(r" \%", r"~\%")                          # keep "21 %" and "$p_0 = 2.5$ %" on one line


def inline(text: str) -> str:
    parts = re.split(r"(\$[^$]+\$|`[^`]+`|\*\*.+?\*\*|\*[^*\s][^*]*?\*|https?://\S+)", text)
    out = []
    for p in parts:
        if not p:
            continue
        if p.startswith("`") and p.endswith("`"):
            out.append(r"\texttt{" + _plain(p[1:-1]) + "}")
        elif p.startswith("$") and p.endswith("$") and len(p) > 2:
            out.append("$" + _math(p[1:-1]) + "$")
        elif p.startswith("**") and p.endswith("**") and len(p) > 4:
            out.append(r"\textbf{" + inline(p[2:-2]) + "}")
        elif p.startswith("*") and p.endswith("*") and len(p) > 2:
            out.append(r"\textit{" + inline(p[1:-1]) + "}")
        elif p.startswith("http"):
            url = p.rstrip(".,;")
            out.append(r"\url{" + url + "}" + p[len(url):])
        else:
            out.append(_plain(p))
    return "".join(out)


def _table(lines: list[str], caption: str) -> str:
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    header, align_row, body = rows[0], rows[1], rows[2:]
    spec = "".join("r" if a.endswith(":") else ("p{6.2cm}" if len(header) == 3 and i == 2 else "l")
                   for i, a in enumerate(align_row))
    out = [r"\begin{table}[htbp]", r"\centering", r"\caption{" + inline(caption) + "}", r"\small",
           r"\begin{tabular}{@{}" + spec + r"@{}}", r"\toprule",
           " & ".join(r"\textbf{" + inline(c) + "}" for c in header) + r" \\", r"\midrule"]
    out += [" & ".join(inline(c) for c in r) + r" \\" for r in body]
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(out)


def blocks_to_tex(md: str) -> list[str]:
    tex = []
    blocks = [b.strip() for b in re.split(r"\n\s*\n", md.strip("\n")) if b.strip()]
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b.startswith("### "):
            tex.append(r"\subsect{" + inline(b[4:]) + "}")
        elif b.startswith("## "):
            tex.append(r"\sect{" + inline(b[3:]) + "}")
        elif b.startswith("# "):
            tex.append(r"\sect{" + inline(b[2:]) + "}")
        elif b.startswith("$$"):
            tex.append(r"\begin{equation*}" + "\n" + _math(b.strip("$").strip()) + "\n" + r"\end{equation*}")
        elif b.startswith("**Table"):
            m = re.match(r"\*\*(Table\s+\S+?)\.\*\*\s*(.*)", b, re.S)
            i += 1
            cap = m.group(2).strip()
            tex.append(_table([ln for ln in blocks[i].splitlines() if ln.strip()], cap).replace(
                r"\caption{", r"\renewcommand{\thetable}{" + m.group(1).split()[1] + r"}\caption{", 1))
        elif b.startswith("|"):
            raise SystemExit(f"Table without caption line: {b[:60]}")
        else:
            tex.append(inline(" ".join(b.split())))
        i += 1
    return tex


def frontmatter(md: str) -> tuple[dict[str, str], str]:
    _, fm, body = md.split("---", 2)
    meta = {}
    for ln in fm.strip().splitlines():
        k, v = ln.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    return meta, body


def cover(meta: dict[str, str]) -> str:
    """Centred title page in the style of the Current Issues report: course block, title, author block."""
    d = dt.date.fromisoformat(meta["datum"])
    title = _plain(meta["titel"]).replace(" Who ", r"\\ Who ", 1)
    return "\n".join([
        r"\begin{titlepage}", r"\centering", r"\vspace*{0.4cm}",
        r"{\large Hitotsubashi University\par Autumn--Winter Term 2026\par}", r"\vspace{0.6cm}",
        r"{\Large\bfseries Topics in Econometrics B\par}", r"{\large Lecturer: " + _plain(meta["dozent"]) + r"\par}",
        r"\vspace{4.2cm}",
        r"{\fontsize{22}{27}\selectfont\bfseries " + title + r"\par}", r"\vspace{0.4cm}",
        r"{\Large " + _plain(meta["untertitel"]).replace(" in B2B", r"\\ in B2B", 1) + r"\par}", r"\vspace{0.3cm}",
        r"{\large Final Report (Research Proposal)\par}",
        r"\vfill",
        r"{\large\bfseries " + _plain(meta["name"]) + r"\par}",
        r"{\large Student ID: " + _plain(meta["matrikel"]) + r"\par}", r"\vspace{0.4cm}",
        r"{\large " + f"{d.day} {d.strftime('%B %Y')}" + r"\par}",
        r"\vspace*{0.4cm}", r"\end{titlepage}", r"\setcounter{page}{1}",
        r"{\Large\bfseries " + _plain(meta["titel"]) + r"\par}", r"\vspace{4pt}"])


def to_tex(text_md: str, appendix_md: str) -> str:
    meta, body = frontmatter(text_md)
    main, refs = body.split("\n## References", 1)
    tex = [PREAMBLE % {"title": meta["titel"], "spread": LINE_SPREAD, "margin": MARGIN, "parskip": PARSKIP, "secskip": SECSKIP}, r"\begin{document}", cover(meta)]
    tex += blocks_to_tex(main)
    tex += [r"\newpage", r"\sect{References}",
            r"\begingroup\setlength{\parindent}{-1.2em}\setlength{\leftskip}{1.2em}\setlength{\parskip}{0.15em}"]
    def apa(entry: str) -> str:                                 # APA page ranges take an en dash, the DOI keeps its hyphens
        text, sep, doi = " ".join(entry.split()).partition(" https://")
        return re.sub(r"(?<=\d)-(?=\d)", "–", text) + sep + doi
    tex += [r"\linespread{1.0}\selectfont"]
    tex += [inline(apa(r)) + r"\par" for r in re.split(r"\n\s*\n", refs) if r.strip()]
    tex += [r"\endgroup", r"\newpage"]
    tex += blocks_to_tex(appendix_md)
    tex.append(r"\end{document}")
    return "\n\n".join(tex) + "\n"


def main() -> None:
    tex_path = HERE / f"{PDF_NAME}.tex"
    tex_path.write_text(to_tex((HERE / "text.md").read_text(), (HERE / "appendix.md").read_text()), encoding="utf-8")
    tectonic = shutil.which("tectonic") or str(Path.home() / ".local" / "bin" / "tectonic")
    proc = subprocess.run([tectonic, tex_path.name], cwd=HERE, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit("tectonic failed:\n" + proc.stderr[-2000:])
    tex_path.unlink()
    reader = PdfReader(str(HERE / f"{PDF_NAME}.pdf"))
    texts = [p.extract_text() or "" for p in reader.pages]
    refs_page = next(i for i, t in enumerate(texts) if t.lstrip().startswith("References"))
    body_pages = refs_page - 1                                   # page 0 is the cover
    print(f"{PDF_NAME}.pdf: {len(reader.pages)} pages, main text {body_pages} page(s)")
    if body_pages > MAX_PAGES:
        sys.exit(f"Main text runs to {body_pages} pages; the limit is {MAX_PAGES}.")


if __name__ == "__main__":
    main()
