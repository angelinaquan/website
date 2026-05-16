#!/usr/bin/env python3
"""Generate philosophy essay pages from sources/*.txt"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SOURCES = ROOT / "sources"

ESSAYS = [
    {
        "slug": "newtons-bucket-relationalism",
        "title": "Newton's Bucket and Relationalism",
        "category": "Metaphysics",
        "source": "essay1.txt",
        "thesis": (
            "Newton uses the spinning bucket to argue that only absolute space can explain why "
            "the water's surface curves and that this proves relationalism false, but I will argue, "
            "with help from Dasgupta (2015), that the bucket does not actually rule out relationalism "
            "because acceleration can be explained through relations between bodies, Newton's "
            "empty-universe example assumes what it tries to prove, and a simpler relational account "
            "makes better sense without positing absolute space."
        ),
        "blurb": (
            "Newton's spinning bucket is supposed to show that absolute space is real. I argue, "
            "with Dasgupta (2015), that relationalism can explain the water's curvature without it."
        ),
    },
    {
        "slug": "everett-measurement-problem",
        "title": "Everett and the Measurement Problem",
        "category": "Philosophy of Quantum Mechanics",
        "source": "essay2.txt",
        "blurb": (
            "Does the Everett interpretation solve the measurement problem? I argue it keeps the "
            "formalism clean but leaves definiteness of experience, probability, and evidence unclear."
        ),
    },
    {
        "slug": "bohm-everett-brown-wallace",
        "title": "Is Bohm Just Everett in Disguise?",
        "category": "Philosophy of Quantum Mechanics",
        "source": "essay3.txt",
        "blurb": (
            "Brown and Wallace claim Bohmian mechanics already contains Everettian worlds. I argue "
            "the particle configuration still does essential explanatory work."
        ),
    },
    {
        "slug": "configuration-space-quantum-state",
        "title": "Configuration Space and the Quantum State",
        "category": "Philosophy of Quantum Mechanics",
        "source": "essay4.txt",
        "blurb": (
            "Should the quantum state be read as a field in 3N-dimensional configuration space? "
            "I argue the view is coherent but fails to non-circularly recover three-dimensional space."
        ),
    },
]


def parse_sections(text: str):
    """Split body and references by References/Bibliography heading."""
    for heading in ("\nReferences\n", "\nBibliography:\n", "\nBibliography\n"):
        if heading in text:
            body, refs = text.split(heading, 1)
            return body.strip(), refs.strip()
    return text.strip(), ""


def paragraphs_to_html(text: str) -> str:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(blocks) == 1 and "\n" in blocks[0]:
        blocks = [ln.strip() for ln in blocks[0].splitlines() if ln.strip()]
    return "\n".join(f"<p>{html.escape(b)}</p>" for b in blocks)


def refs_to_html(refs: str) -> str:
    if not refs:
        return ""
    lines = [ln.strip() for ln in refs.splitlines() if ln.strip()]
    items = "\n".join(f"<p style=\"margin:0 0 8px 0;\">{html.escape(ln)}</p>" for ln in lines)
    return f'<p style="margin-top:24px;"><strong>References</strong></p>\n{items}'


def page_html(meta: dict, body_html: str, refs_html: str, thesis: str | None = None) -> str:
    title = html.escape(meta["title"])
    category = html.escape(meta["category"])
    thesis_block = ""
    if thesis:
        thesis_block = f'<p><strong>Thesis:</strong> {html.escape(thesis)}</p>\n<p></p>\n'
    return f"""<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title} — Angelina Quan</title>
    <meta name="author" content="Angelina Quan">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="../../images/angelina-quan.jpeg" type="image/jpeg">
    <link rel="shortcut icon" href="../../images/angelina-quan.jpeg" type="image/jpeg">
    <link rel="apple-touch-icon" href="../../images/angelina-quan.jpeg">
    <link rel="stylesheet" type="text/css" href="../../stylesheet.css">
  </head>
  <body>
    <table style="width:100%;max-width:800px;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
      <tr style="padding:0px">
        <td style="padding:0px">
          <table style="width:100%;border:0px;border-spacing:0px 0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>
            <tr>
              <td style="padding:16px;width:100%;vertical-align:middle">
                <p class="name" style="text-align:center;margin-bottom:0;">{title}</p>
                <p style="text-align:center;margin-top:8px;">
                  <a href="../">← Back to Philosophy Essays</a>
                </p>
              </td>
            </tr>
            <tr>
              <td style="padding:8px 16px 16px 16px;width:100%;vertical-align:middle">
                <strong>Angelina Quan</strong>
                <br>
                <em>{category}</em>
                <p></p>
                {thesis_block}{body_html}
                {refs_html}
              </td>
            </tr>
          </tbody></table>
        </td>
      </tr>
    </tbody></table>
  </body>
</html>
"""


def main():
    for meta in ESSAYS:
        raw = (SOURCES / meta["source"]).read_text(encoding="utf-8")
        # Drop leading author line if present
        raw = re.sub(r"^Angelina Quan\s*\n+", "", raw.strip())
        body, refs = parse_sections(raw)
        body_html = paragraphs_to_html(body)
        refs_html = refs_to_html(refs)
        thesis = meta.get("thesis")
        out_dir = ROOT / meta["slug"]
        out_dir.mkdir(exist_ok=True)
        (out_dir / "index.html").write_text(
            page_html(meta, body_html, refs_html, thesis), encoding="utf-8"
        )
        print("Wrote", out_dir / "index.html")


if __name__ == "__main__":
    main()
