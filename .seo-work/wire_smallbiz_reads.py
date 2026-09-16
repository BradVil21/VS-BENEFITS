# -*- coding: utf-8 -*-
"""Add a 'Reads for trade and small business owners' block to the trade pages."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCK = '''<section class="vs-related-guides" data-block="smallbiz-reads">
  <div class="vs-rg-inner">
    <h2>Reads for trade and small business owners</h2>
    <p class="vs-rg-sub">The four questions owners ask us most, answered in full with the rules and the numbers behind them.</p>
    <div class="vs-rg-grid">
        <a class="vs-rg-card" href="/blog/skilled-trades-health-insurance">
          <strong>What coverage actually costs a trade business</strong>
          <span>The 2027 per-employee range, what moves your rate, and the participation rule that blocks most applications before a carrier quotes.</span>
          <em>Read the guide &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/blog/workers-comp-vs-health-insurance">
          <strong>Workers&rsquo; comp is not health insurance</strong>
          <span>Seven rows showing exactly what comp pays for, what it never touches, and why the owner exemption leaves you with nothing.</span>
          <em>Read the guide &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/blog/1099-crew-vs-w2-health-insurance">
          <strong>1099 crew or W-2 employees?</strong>
          <span>Contractors cannot join your group plan and do not count toward 50. Where the line sits and what getting it wrong costs.</span>
          <em>Read the guide &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/blog/seasonal-part-time-crew-health-insurance">
          <strong>Do part-time and seasonal crews count?</strong>
          <span>Part-time hours count toward the 50-employee rule but do not have to be offered coverage. The math, plus the 120-day seasonal exception.</span>
          <em>Read the guide &rarr;</em>
        </a>
    </div>
  </div>
</section>'''

PAGES = [
    "health-insurance-for-hvac-companies.html",
    "health-insurance-for-construction-companies.html",
    "health-insurance-for-contractors.html",
    "group-health-insurance-for-general-contractors.html",
]

def close_of(s, start):
    """Index just past the </section> that closes the tag opening at `start`."""
    depth = 0
    i = start
    for m in re.finditer(r"</?section\b", s[start:]):
        tag = m.group(0)
        depth += 1 if tag == "<section" else -1
        if depth == 0:
            end = start + m.end()
            return s.index(">", end - 1) + 1
    raise ValueError("unbalanced section")

for p in PAGES:
    fp = os.path.join(ROOT, p)
    s = io.open(fp, encoding="utf-8").read()
    if 'data-block="smallbiz-reads"' in s:
        print("%-52s already wired" % p); continue
    m = re.search(r'<section class="vs-related-guides" data-block="sb-states">', s)
    if not m:
        print("%-52s NO sb-states anchor" % p); continue
    end = close_of(s, m.start())
    s = s[:end] + BLOCK + s[end:]
    io.open(fp, "w", encoding="utf-8").write(s)
    print("%-52s block added" % p)
