# -*- coding: utf-8 -*-
"""Wire the Sep-16 small-business trade pages and posts into the site."""
import json, io, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s):
    io.open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)

# ---------------------------------------------------------------- 1. hub cards
HUB = "group-health-insurance-by-industry.html"
h = rd(HUB)
anchor = '''        <a class="vs-ih-card" href="/health-insurance-for-hvac-companies">
          <strong>HVAC companies</strong>
          <span>Roughly $350 to $650 per employee per month. Certified techs are the hardest hires in the trades to keep.</span>
          <em>See plans and costs &rarr;</em>
        </a>
'''
assert anchor in h, "hub anchor card not found"
new_cards = '''        <a class="vs-ih-card" href="/health-insurance-for-roofing-companies">
          <strong>Roofing companies</strong>
          <span>Rated on your crew, not your loss runs. Comp pays for the fall off the roof and nothing else.</span>
          <em>See plans and costs &rarr;</em>
        </a>
        <a class="vs-ih-card" href="/health-insurance-for-daycare-centers">
          <strong>Daycare and childcare centers</strong>
          <span>Thin margins, high turnover, mostly female staff. Four ways to offer coverage without breaking tuition.</span>
          <em>See plans and costs &rarr;</em>
        </a>
'''
if '/health-insurance-for-roofing-companies' not in h:
    h = h.replace(anchor, anchor + new_cards, 1)
    wr(HUB, h)
    print("hub: 2 cards added")
else:
    print("hub: already wired")

# ---------------------------------------------------------- 2. blog index cards
BLOG = "blog.html"
b = rd(BLOG)
POSTS = [
    ("/blog/skilled-trades-health-insurance",
     "/compressed/electrician-lineman-utility-pole.jpg",
     "Electrician working on a utility pole, illustrating group health insurance costs for skilled trades businesses",
     "Small Business | 9 min read",
     "Health Insurance for the Skilled Trades: What It Really Costs",
     "Roughly $350 to $700 per employee per month in 2027, and four ways to structure it. Plus the participation rule that blocks most trade applications before a carrier ever quotes."),
    ("/blog/workers-comp-vs-health-insurance",
     "/compressed/construction-site-safety-briefing.jpg",
     "Construction crew in a site safety briefing, illustrating the difference between workers compensation and health insurance",
     "Small Business | 7 min read",
     "Workers&rsquo; Comp Is Not Health Insurance &mdash; Here Is the Gap",
     "&ldquo;We carry comp&rdquo; is the most expensive sentence in the trades. A seven-row breakdown of what comp pays for, what it never touches, and the owner-exemption trap."),
    ("/blog/1099-crew-vs-w2-health-insurance",
     "/compressed/10-99working.jpg",
     "Tradesman reviewing paperwork on a job site, illustrating 1099 contractor versus W-2 employee classification for health insurance",
     "Small Business | 8 min read",
     "1099 Crew or W-2 Employees? What It Does to Your Health Plan",
     "Contractors cannot go on your group plan and do not count toward 50 employees. Where the classification line actually sits, and what getting it wrong costs."),
    ("/blog/seasonal-part-time-crew-health-insurance",
     "/compressed/construction-crew-rebar-column.jpg",
     "Construction crew working on a rebar column, illustrating how part-time and seasonal workers count toward health insurance requirements",
     "Small Business | 8 min read",
     "Do Part-Time and Seasonal Crews Count for Health Insurance?",
     "Part-time hours count toward the 50-employee rule but do not have to be offered coverage. The full-time-equivalent math, and the 120-day seasonal exception the trades need."),
]
MARK = "      <!-- Newest posts -->\n"
assert MARK in b, "blog post-grid marker not found"
block = ""
for href, img, alt, meta, title, dek in POSTS:
    if href + '"' in b:
        continue
    block += (
        '      <a class="post-card" href="%s">\n'
        '        <div class="cover"><img src="%s" alt="%s" loading="lazy" /></div>\n'
        '        <div class="body">\n'
        '          <div class="meta">%s</div>\n'
        '          <h3>%s</h3>\n'
        '          <p>%s</p>\n'
        '          <span class="read-more">Read article &rarr;</span>\n'
        '        </div>\n'
        '      </a>\n\n' % (href, img, alt, meta, title, dek)
    )
if block:
    b = b.replace(MARK, MARK + block, 1)
    wr(BLOG, b)
    print("blog.html: %d cards added" % block.count("post-card"))
else:
    print("blog.html: already wired")

# ------------------------------------------------------------- 3. vercel.json
V = "vercel.json"
d = json.loads(rd(V))
srcs = set(x.get("source", "") for x in d["redirects"])
new_paths = [
    "/health-insurance-for-roofing-companies",
    "/health-insurance-for-daycare-centers",
    "/blog/skilled-trades-health-insurance",
    "/blog/workers-comp-vs-health-insurance",
    "/blog/1099-crew-vs-w2-health-insurance",
    "/blog/seasonal-part-time-crew-health-insurance",
]
added = 0
for p in new_paths:
    s = p + ".html"
    if s in srcs:
        continue
    d["redirects"].append({"source": s, "destination": p, "permanent": True})
    added += 1
if added:
    wr(V, json.dumps(d, indent=2) + "\n")
print("vercel.json: %d redirects added (%d total)" % (added, len(d["redirects"])))
