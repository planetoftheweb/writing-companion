"""Shared styles and the PDF renderer for the video playbooks.

Run build.py to rebuild both PDFs. Requires Playwright with Chromium:
    pip install playwright && playwright install chromium
"""
import pathlib
from playwright.sync_api import sync_playwright

SRC = pathlib.Path(__file__).resolve().parent   # docs/playbooks/source
OUT = SRC.parent                                # docs/playbooks

FONT_LINKS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..800&display=swap">'

CSS = r"""
  @page { size: Letter; margin: 0; }
  :root {
    --ink: #16233b; --muted: #5b6472; --teal: #0f8f80; --teal-soft: #e6f6f3;
    --line: #d9e1e8; --paper: #ffffff; --chip: #f3f6f9;
    --s1: #7a6fd0; --s2: #0f8f80; --band: #eef8f6; --red: #e5322f;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: var(--paper); }
  body { font-family: "Inter", sans-serif; color: var(--ink); font-size: 8.5pt; line-height: 1.37; }
  .page { width: 8.5in; height: 11in; padding: 0.4in 0.5in 0.3in; display: flex; flex-direction: column;
    break-after: page; overflow: hidden; }
  .page:last-child { break-after: auto; }
  b { font-weight: 700; }
  .num { font-weight: 700; color: var(--teal); }

  header { display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 8pt; border-bottom: 2pt solid var(--ink); }
  .kicker { font-size: 7pt; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: var(--teal); margin-bottom: 3pt; }
  h1 { font-family: "Inter Display", "Inter", sans-serif; font-size: 22pt; font-weight: 800; letter-spacing: -0.015em; line-height: 1.05; }
  .sub { margin-top: 4pt; color: var(--muted); font-size: 9pt; max-width: 5in; }
  .byline { text-align: right; font-size: 7.6pt; color: var(--muted); line-height: 1.5; }
  .byline b { color: var(--ink); }
  .runhead { display: flex; justify-content: space-between; font-size: 7pt; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--muted); padding-bottom: 5pt; border-bottom: 1pt solid var(--line); margin-bottom: 9pt; }
  .runhead span:first-child { color: var(--teal); }

  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin: 9pt 0 10pt; }
  .stat { background: var(--teal-soft); border-radius: 5pt; padding: 6pt 8pt; }
  .stat .v { font-family: "Inter Display", "Inter", sans-serif; font-size: 17pt; font-weight: 800; color: var(--teal); line-height: 1; letter-spacing: -0.01em; }
  .stat .l { margin-top: 3pt; font-size: 7.3pt; line-height: 1.3; }

  h2 { font-family: "Inter Display", "Inter", sans-serif; font-size: 11.5pt; font-weight: 800; letter-spacing: -0.005em;
    padding-bottom: 3pt; margin-bottom: 6pt; border-bottom: 1pt solid var(--line); display: flex; align-items: baseline; gap: 6pt; }
  h2 .tag { font-family: "Inter", sans-serif; font-size: 6.8pt; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal); }
  h3 { font-family: "Inter Display", "Inter", sans-serif; font-size: 9.6pt; font-weight: 800; margin-bottom: 2pt; }
  .lead { color: var(--muted); font-size: 8.2pt; margin-bottom: 7pt; }
  section.block { margin-bottom: 9.5pt; }

  ol.rules { list-style: none; counter-reset: n; }
  ol.rules li { counter-increment: n; position: relative; padding-left: 17pt; margin-bottom: 5.5pt; }
  ol.rules li::before { content: counter(n); position: absolute; left: 0; top: 0.5pt; width: 11.5pt; height: 11.5pt; border-radius: 50%;
    background: var(--ink); color: #fff; font-size: 6.6pt; font-weight: 700; text-align: center; line-height: 11.5pt; }
  ol.rules.start5 { counter-reset: n 4; }
  ol.rules.start4 { counter-reset: n 3; }
  .two { display: grid; grid-template-columns: 1fr 1fr; gap: 0 18pt; }
  .three { display: grid; grid-template-columns: repeat(3, 1fr); gap: 9pt; }

  .card { border: 1pt solid var(--line); border-radius: 6pt; padding: 7pt 9pt; background: #fff; }
  .card.hi { border-color: var(--teal); background: var(--teal-soft); }
  .card .badge { display: inline-block; font-size: 6.4pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #fff;
    background: var(--teal); border-radius: 99pt; padding: 1pt 5pt; margin-bottom: 3pt; }
  .card p { font-size: 8pt; }
  .chips { display: flex; flex-wrap: wrap; gap: 3pt; margin-top: 5pt; }
  .chips span { font-size: 6.8pt; font-weight: 600; padding: 1.5pt 5pt; border-radius: 99pt; background: #fff; border: 0.75pt solid var(--teal); }
  .eg { font-size: 7.6pt; color: var(--muted); margin-top: 3pt; }
  .eg b { color: var(--ink); }

  .prompt { background: var(--chip); border-left: 2.5pt solid var(--teal); border-radius: 0 5pt 5pt 0; padding: 6pt 8pt; }
  .prompt .pl { font-size: 6.6pt; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal); margin-bottom: 2pt; }
  .prompt .pt { font-size: 7.9pt; line-height: 1.38; }

  .cap { font-size: 7pt; color: var(--muted); margin-top: 4pt; line-height: 1.35; }
  footer { margin-top: auto; padding-top: 5pt; border-top: 1pt solid var(--line); font-size: 6.6pt; color: var(--muted); line-height: 1.4; }

  /* files diagram */
  .files { position: relative; padding-right: 24pt; }
  .layer { display: grid; grid-template-columns: 62pt 1fr; gap: 7pt; align-items: stretch; }
  .layer .scope { font-size: 6.5pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
    display: flex; align-items: center; line-height: 1.3; border-right: 1pt solid var(--line); padding-right: 6pt; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 6pt; }
  .file .nm { font-family: "Inter Display", "Inter", sans-serif; font-size: 9.6pt; font-weight: 800; margin-bottom: 1pt; }
  .file p { font-size: 7.8pt; line-height: 1.34; }
  .down { height: 11pt; display: flex; justify-content: center; align-items: center; color: var(--muted); font-size: 8pt; padding-left: 69pt; }
  .piece { margin-left: 69pt; text-align: center; background: var(--ink); color: #fff; border-radius: 6pt; padding: 5pt; font-weight: 700; font-size: 8.4pt; }
  .piece span { font-weight: 400; opacity: 0.8; }
  .loopline { position: absolute; right: 8pt; top: 14pt; bottom: 10pt; width: 16pt; border: 1.25pt solid var(--teal); border-left: none; border-radius: 0 8pt 8pt 0; }
  .loopline::after { content: ""; position: absolute; top: -4pt; left: -2pt; border: 3.5pt solid transparent; border-right: 5pt solid var(--teal); border-left: none; }
  .looplabel { position: absolute; right: 4pt; top: 50%; transform: translateY(-50%); writing-mode: vertical-rl; font-size: 6.2pt; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; color: var(--teal); white-space: nowrap; background: #fff; padding: 4pt 0; line-height: 1; }


  .filerow { display: grid; grid-template-columns: 1fr 1fr 1.45fr 1fr; gap: 7pt; }
  .file .scope { font-size: 6.3pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--teal); margin-bottom: 2pt; }
  .arrows { display: grid; grid-template-columns: 1fr 1fr 1.45fr 1fr; gap: 7pt; text-align: center; color: var(--muted); font-size: 7pt; line-height: 1; margin: 4pt 0 3pt; }
  .flowbar { display: grid; grid-template-columns: 1fr auto; gap: 12pt; align-items: center; }
  .flowbar .piece { margin-left: 0; }
  .cycle { font-size: 7.8pt; font-weight: 700; color: var(--teal); }
  .opt { border: 1pt solid var(--line); border-radius: 6pt; padding: 6pt 9pt; margin-bottom: 6pt; }
  .opt.hi { border-color: var(--teal); background: var(--teal-soft); }
  .opt p { font-size: 8pt; }
  .opt .badge { display: inline-block; font-size: 6.4pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #fff; background: var(--teal); border-radius: 99pt; padding: 1pt 5pt; margin-bottom: 3pt; }


  .flow { display: grid; grid-template-columns: repeat(9, 1fr); gap: 4pt; }
  .flow div { background: var(--chip); border-radius: 5pt; padding: 5pt 5pt 6pt; font-size: 7.1pt; line-height: 1.3; }
  .flow div i { display: block; font-style: normal; width: 11pt; height: 11pt; border-radius: 50%; background: var(--teal); color: #fff;
    font-size: 6.4pt; font-weight: 700; text-align: center; line-height: 11pt; margin-bottom: 3pt; }
  .flow div b { display: block; }
  .checks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6pt 14pt; }
  .checks div { position: relative; padding-left: 15pt; font-size: 8pt; }
  .checks div::before { content: ""; position: absolute; left: 0; top: 1pt; width: 9pt; height: 9pt; border: 1.25pt solid var(--teal); border-radius: 2pt; }


  .grid4w { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0 12pt; font-size: 8pt; }
  .grid4w b { display: block; margin-bottom: 2pt; }
  a { color: var(--teal); font-weight: 700; text-decoration: none; }


  table.checks-t { width: 100%; border-collapse: collapse; font-size: 8pt; }
  table.checks-t th { text-align: left; font-size: 6.8pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); padding: 0 8pt 4pt 0; border-bottom: 1pt solid var(--ink); }
  table.checks-t td { padding: 4.5pt 8pt 4.5pt 0; border-bottom: 0.75pt solid var(--line); vertical-align: top; }
  table.checks-t td:first-child { width: 0.95in; }
  table.checks-t td:last-child { width: 1.25in; color: var(--teal); font-weight: 600; }
  table.checks-t tr.hi td { background: var(--teal-soft); }
  .scriptex { border: 1pt solid var(--line); border-radius: 6pt; padding: 6pt 10pt; }
  .scriptex .ln { display: grid; grid-template-columns: 0.95in 1fr; gap: 8pt; padding: 3pt 0; border-bottom: 0.75pt dashed var(--line); align-items: baseline; }
  .scriptex .ln:last-child { border-bottom: none; }
  .scriptex .lb { font-size: 6.6pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
  .scriptex .spoken .lb { color: var(--ink); }
  .scriptex .spoken p { font-size: 9.2pt; }
  .scriptex .visual .lb { color: var(--teal); }
  .scriptex .visual p { color: var(--teal); font-weight: 600; }
  .scriptex .note .lb { color: #b4531f; }
  .scriptex .note p { color: var(--muted); font-style: normal; background: #fbf3ec; border-radius: 4pt; padding: 2pt 5pt; }


  .three .card { padding: 6pt 8pt; }
  .three .card h3 { font-size: 9pt; margin-bottom: 1.5pt; }
  .three .card p { font-size: 7.8pt; line-height: 1.33; }
  table.checks-t td { padding: 3.4pt 8pt 3.4pt 0; }


  .polish { display: grid; grid-template-columns: 1.9in 1fr; gap: 12pt; align-items: center; background: var(--chip); border-radius: 7pt; padding: 8pt 10pt; }
  .polish h3 { font-size: 10.5pt; margin-bottom: 2pt; }
  .polish .pl2 { font-size: 7.9pt; color: var(--muted); line-height: 1.35; }
  .polish .steps { display: grid; grid-template-columns: 1fr 1fr 1fr 0.55fr; gap: 6pt; align-items: stretch; }
  .polish .st { background: #fff; border-radius: 5pt; padding: 5pt 7pt; font-size: 7.7pt; line-height: 1.33; position: relative; }
  .polish .st b { display: block; font-size: 8.6pt; color: var(--teal); margin-bottom: 1pt; }
  .polish .st.pub { background: var(--ink); color: #fff; display: flex; flex-direction: column; justify-content: center; }
  .polish .st.pub b { color: #fff; }
  .polish .st:not(.pub)::after { content: "\203A"; position: absolute; right: -6pt; top: 50%; transform: translateY(-50%); color: var(--muted); font-size: 11pt; font-weight: 700; }


  .ba { display: grid; grid-template-columns: 1fr 1fr 1.45in; gap: 9pt; }
  .ba .col { border: 1pt solid var(--line); border-radius: 6pt; padding: 6pt 8pt; }
  .ba .col p { font-size: 7.9pt; line-height: 1.36; }
  .ba .bl { font-size: 6.6pt; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin-bottom: 3pt; }
  .ba .said { border-color: var(--teal); background: var(--teal-soft); }
  .ba .said .bl { color: var(--teal); }
  .ba .why { background: var(--chip); border-color: var(--chip); }
  .ba ul.dots { list-style: none; }
  .ba ul.dots li { position: relative; padding-left: 10pt; margin-bottom: 4pt; font-size: 8pt; }
  .ba ul.dots li::before { content: ""; position: absolute; left: 0; top: 4.5pt; width: 5pt; height: 5pt; border-radius: 1.5pt; background: var(--teal); }

  /* chart */
  .band { display: grid; grid-template-columns: 2.1in 1fr; gap: 14pt; align-items: center; }
  .band p { font-size: 8pt; margin-bottom: 4pt; }
  .legend { display: flex; gap: 10pt; font-size: 7.2pt; color: var(--muted); }
  .legend i { display: inline-block; width: 8pt; height: 8pt; border-radius: 2pt; margin-right: 3pt; vertical-align: -1pt; }
  .chart svg { width: 100%; height: auto; display: block; font-family: "Inter", sans-serif; }
  .chart .grid { stroke: #e6ebf0; stroke-width: 0.75; }
  .chart .axis { stroke: #b9c3cd; stroke-width: 0.75; }
  .chart .t-tick { font-size: 7.5px; fill: var(--muted); }
  .chart .t-name { font-size: 8.5px; font-weight: 600; fill: var(--ink); }
  .chart .t-val { font-size: 7.5px; font-weight: 700; fill: var(--ink); }
  .chart .t-val2 { font-size: 7.5px; fill: var(--muted); }
  .chart .t-band { font-size: 7.5px; font-weight: 700; fill: var(--teal); }

  /* editing */
  .passes { display: grid; grid-template-columns: 2.55in 1fr; gap: 16pt; align-items: start; }
  .shot { border-radius: 6pt; overflow: hidden; border: 1pt solid #2a2f3a; }
  .shot img, .reel img { width: 100%; display: block; }
  .reel img { border-radius: 5pt; }
  ol.order { list-style: none; counter-reset: o; margin: 2pt 0 6pt; }
  ol.order li { counter-increment: o; position: relative; padding-left: 17pt; margin-bottom: 5pt; }
  ol.order li::before { content: counter(o); position: absolute; left: 0; top: 0.5pt; width: 11.5pt; height: 11.5pt; border-radius: 50%;
    background: var(--red); color: #fff; font-size: 6.6pt; font-weight: 700; text-align: center; line-height: 11.5pt; }
  .tip { background: var(--chip); border-radius: 5pt; padding: 6pt 8pt; font-size: 8pt; }
  .visuals { display: grid; grid-template-columns: 3.1in 1fr; gap: 16pt; align-items: start; }
  ul.vis { list-style: none; }
  ul.vis li { position: relative; padding-left: 10pt; margin-bottom: 5pt; }
  ul.vis li::before { content: ""; position: absolute; left: 0; top: 4.5pt; width: 5pt; height: 5pt; border-radius: 1.5pt; background: var(--teal); }
  .punch { font-weight: 700; font-size: 8.6pt; margin-top: 3pt; }
"""

BYLINE = '<div class="byline"><b>Ray Villalobos</b><br>Senior Staff Instructor<br>LinkedIn Learning<br>October 2026</div>'

def page(title, body, extra_css=""):
    """Wrap page sections in a full HTML document with the shared styles."""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'{FONT_LINKS}<style>{CSS}{extra_css}</style></head><body>{body}</body></html>')


def render(name, html):
    """Write the HTML next to the images, print overflow per page, and save the PDF to docs/playbooks."""
    html_path = SRC / f"_{name}.html"
    html_path.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        pg.goto(html_path.as_uri())
        pg.wait_for_timeout(800)
        over = pg.evaluate("[...document.querySelectorAll('.page')].map(p => p.scrollHeight - p.clientHeight)")
        print(f"{name}: pages={len(over)} overflow px per page={over} (anything over ~2 means text is cut off)")
        pg.pdf(path=str(OUT / f"{name}.pdf"), format="Letter", print_background=True, prefer_css_page_size=True)
        browser.close()
