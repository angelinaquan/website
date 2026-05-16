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
        "blurb": (
            "Newton's spinning bucket is supposed to show that absolute space is real. I argue, "
            "with Dasgupta (2015), that relationalism can explain the water's curvature without it."
        ),
    },
    {
        "slug": "against-instantaneous-velocity",
        "title": "Against Instantaneous Velocity",
        "category": "Metaphysics",
        "source": "essay7.txt",
        "math": True,
        "blurb": (
            "Velocity is usually treated as a property at an instant. I argue it is really a "
            "relation over time—and the limit definition does not change that metaphysically."
        ),
    },
    {
        "slug": "predication-without-existence",
        "title": "Against the Principle that Predication Requires Existence",
        "category": "Metaphysics",
        "source": "essay8.txt",
        "math": True,
        "blurb": (
            "If $Fx$, must $x$ exist? Fictional and modal discourse suggest we can predicate "
            "properties of things that do not exist in the actual world."
        ),
    },
    {
        "slug": "special-relativity-against-presentism",
        "title": "Special Relativity Against Presentism",
        "category": "Metaphysics",
        "source": "essay9.txt",
        "math": True,
        "blurb": (
            "Presentism needs an objective present. Special relativity's relativity of simultaneity "
            "makes that hard to defend."
        ),
    },
    {
        "slug": "against-principle-alternative-possibilities",
        "title": "Against the Principle of Alternative Possibilities",
        "category": "Metaphysics",
        "source": "essay10.txt",
        "blurb": (
            "Frankfurt cases show you can act freely even when you could not have done otherwise—"
            "what matters is the source of the action."
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
    {
        "slug": "sleeping-beauty-self-locating-probability",
        "title": "Sleeping Beauty and Self-Locating Probability",
        "category": "Paradox and Infinity",
        "source": "essay5.txt",
        "math": True,
        "blurb": (
            "When Beauty wakes up, should her credence in Heads be 1/2 or 1/3? I argue the Thirder "
            "view better fits her self-locating evidence."
        ),
    },
    {
        "slug": "cantor-theorem-listing-infinity",
        "title": "Cantor's Theorem and the Failure of Listing Infinity",
        "category": "Paradox and Infinity",
        "source": "essay6.txt",
        "math": True,
        "blurb": (
            "Cantor's theorem is not just about larger infinities—it shows why no list can exhaust "
            "all subsets of a set."
        ),
    },
]

MATH_PATTERN = re.compile(
    r"\\\[(?:.|\n)*?\\\]|" r"\$\$(?:.|\n)*?\$\$|" r"\$(?:\\.|[^$])+\$",
    re.DOTALL,
)


def parse_sections(text: str):
    """Split body and references by References/Bibliography heading."""
    for heading in ("\nReferences\n", "\nBibliography:\n", "\nBibliography\n"):
        if heading in text:
            body, refs = text.split(heading, 1)
            return body.strip(), refs.strip()
    return text.strip(), ""


def escape_with_math(text: str) -> str:
    parts = []
    last = 0
    for match in MATH_PATTERN.finditer(text):
        if match.start() > last:
            parts.append(html.escape(text[last : match.start()]))
        parts.append(match.group(0))
        last = match.end()
    if last < len(text):
        parts.append(html.escape(text[last:]))
    return "".join(parts)


def paragraphs_to_html(text: str, allow_math: bool = False) -> str:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(blocks) == 1 and "\n" in blocks[0]:
        blocks = [ln.strip() for ln in blocks[0].splitlines() if ln.strip()]
    out = []
    for block in blocks:
        content = escape_with_math(block) if allow_math else html.escape(block)
        out.append(f"<p>{content}</p>")
    return "\n".join(out)


def refs_to_html(refs: str) -> str:
    if not refs:
        return ""
    lines = [ln.strip() for ln in refs.splitlines() if ln.strip()]
    items = "\n".join(f"<p style=\"margin:0 0 8px 0;\">{html.escape(ln)}</p>" for ln in lines)
    return f'<p style="margin-top:24px;"><strong>References</strong></p>\n{items}'


MATHJAX_HEAD = """<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$']],
    displayMath: [['\\\\[', '\\\\]']]
  }
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>"""


def page_html(meta: dict, body_html: str, refs_html: str, thesis: str | None = None) -> str:
    title = html.escape(meta["title"])
    category = html.escape(meta["category"])
    mathjax_head = MATHJAX_HEAD if meta.get("math") else ""
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
    {mathjax_head}
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
        body_html = paragraphs_to_html(body, allow_math=meta.get("math", False))
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
