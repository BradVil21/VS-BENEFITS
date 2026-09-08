# -*- coding: utf-8 -*-
"""Wire the September trucking work into the existing site.

1. A "Tools and guides" block on every trucking page pointing at the five new
   pages, so they start life with real internal links instead of none.
2. The sticky mobile call bar on trucking pages. Drivers search from the cab;
   on a phone the call is the conversion and the form is not.
3. hreflang pairs between the Spanish trucking pages and their English
   equivalents, plus a visible language link so the Spanish set stops being
   orphaned. Those pages carry the highest CTR on the site (20% and 33%) off
   almost no impressions - they are worth making findable.
"""
import glob, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_lib as P

NEW_BLOCK = """
<section class="vs-related-guides" data-block="vs-trucking-tools">
  <div class="vs-rg-inner">
    <h2>Driver tools and coverage guides</h2>
    <p class="vs-rg-sub">Work out the number first, then choose where to buy. Ready to talk to somebody? <a href="/quote?type=individual" style="color:#16447f;font-weight:700">Get my quote &rarr;</a></p>
    <div class="vs-rg-grid">
        <a class="vs-rg-card" href="/truck-driver-health-insurance-cost-calculator">
          <strong>Cost Calculator for Drivers</strong>
          <span>Your 2027 premium after credits in about a minute, plus what your Schedule C deductions are actually worth.</span>
          <em>Run the numbers &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/truck-driver-open-enrollment-2027">
          <strong>Open Enrollment 2027 for Drivers</strong>
          <span>Nov 1 to Jan 15. The three dates that matter, what changed with the subsidy cliff, and how to enroll from the road.</span>
          <em>See the dates &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/ooida-health-insurance-vs-aca">
          <strong>OOIDA vs the Marketplace</strong>
          <span>What an association benefits package actually covers, and where a subsidized Marketplace plan wins.</span>
          <em>Compare them &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/blue-cross-blue-shield-truck-drivers">
          <strong>Blue Cross Blue Shield for Drivers</strong>
          <span>Which Blue plans travel and which do not. The two questions to ask before you enroll.</span>
          <em>Read the guide &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/best-trucking-company-health-benefits">
          <strong>Judging a Fleet's Benefits</strong>
          <span>The five things that decide whether a company plan is good, and the questions to take to orientation.</span>
          <em>Read the guide &rarr;</em>
        </a>
        <a class="vs-rg-card" href="/dot-physical-requirements">
          <strong>DOT Physical Requirements</strong>
          <span>Blood pressure thresholds, sleep apnea and CPAP, diabetes, vision - and what decides your card length.</span>
          <em>Read the guide &rarr;</em>
        </a>
    </div>
  </div>
</section>
"""

NEW_PAGES = {"truck-driver-health-insurance-cost-calculator","truck-driver-open-enrollment-2027",
             "ooida-health-insurance-vs-aca","blue-cross-blue-shield-truck-drivers",
             "best-trucking-company-health-benefits"}

TRUCK_RE = re.compile(r'truck|trucker|cdl|otr|owner-operator|owner_operator|camioner|fleet|freight|dot-physical|occupational-accident', re.I)

# Spanish <-> English pairs
PAIRS = [
 ("seguro-medico-camioneros",         "truck-driver-health-insurance"),
 ("seguro-medico-camioneros-florida", "truck-driver-health-insurance-florida"),
 ("seguro-medico-owner-operators",    "best-health-insurance-owner-operators"),
 ("costo-seguro-medico-camioneros",   "truck-driver-health-insurance-cost"),
]
ES_TO_EN = dict(PAIRS)
EN_TO_ES = {e: s for s, e in PAIRS}

def trucking_pages():
    out = []
    for f in sorted(glob.glob("*.html") + glob.glob("blog/*.html")):
        slug = f[:-5]
        base = os.path.basename(slug)
        if base in NEW_PAGES:
            continue
        c = open(f, encoding="utf-8").read()
        is_truck = TRUCK_RE.search(base) or 'data-block="truck-cluster"' in c or 'data-block="vs-truck-verticals"' in c
        if is_truck:
            out.append(f)
    return out

def main():
    ch = P.Chrome()
    stats = {"block": 0, "sticky": 0, "hreflang": 0, "langlink": 0}
    for f in trucking_pages():
        c = open(f, encoding="utf-8").read()
        orig = c
        slug = os.path.basename(f)[:-5]

        # 1. tools block, before the footer
        if 'data-block="vs-trucking-tools"' not in c and "<footer>" in c:
            c = c.replace("<footer>", NEW_BLOCK + "\n<footer>", 1)
            stats["block"] += 1

        # 2. sticky call bar
        if 'id="vs-callbar"' not in c and "</head>" in c and "</body>" in c:
            c = c.replace("</head>", P.STICKY_CSS + "\n</head>", 1)
            c = c.replace("</body>", P.STICKY_HTML + "\n</body>", 1)
            stats["sticky"] += 1

        # 3. hreflang on both sides of each pair
        other, lang_self, lang_other = None, None, None
        if slug in ES_TO_EN:
            other, lang_self, lang_other = ES_TO_EN[slug], "es", "en"
        elif slug in EN_TO_ES:
            other, lang_self, lang_other = EN_TO_ES[slug], "en", "es"
        if other and 'hreflang="%s"' % lang_other not in c:
            tags = ('<link rel="alternate" hreflang="%s" href="%s/%s" />\n'
                    '<link rel="alternate" hreflang="%s" href="%s/%s" />\n'
                    '<link rel="alternate" hreflang="x-default" href="%s/%s" />\n'
                    % (lang_self, P.SITE, slug, lang_other, P.SITE, other,
                       P.SITE, other if lang_other == "en" else slug))
            c = re.sub(r'(<link rel="canonical"[^>]*/>\s*)', r'\1' + tags, c, count=1)
            stats["hreflang"] += 1

        # 4. visible language link, so the Spanish pages are reachable by crawl
        if other and 'data-lang-switch' not in c:
            label = ("Read this page in English" if lang_self == "es" else "Lea esta p&aacute;gina en espa&ntilde;ol")
            link = ('<div data-lang-switch style="background:var(--blue-50);border-bottom:1px solid var(--blue-100);'
                    'text-align:center;padding:8px 16px;font-size:.9rem">'
                    '<a href="/%s" hreflang="%s" style="color:var(--blue-700);font-weight:700">%s &rarr;</a></div>'
                    % (other, lang_other, label))
            m = re.search(r'</header>', c)
            if m:
                c = c[:m.end()] + "\n" + link + c[m.end():]
                stats["langlink"] += 1

        if c != orig:
            open(f, "w", encoding="utf-8").write(c)

    print("trucking pages touched: %d" % len(trucking_pages()))
    for k, v in stats.items():
        print("  %-9s %d" % (k, v))

if __name__ == "__main__":
    main()
