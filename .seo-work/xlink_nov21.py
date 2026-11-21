# -*- coding: utf-8 -*-
"""Internal links to page-2 pages (2026-11-21). One small box above the footer,
only listing targets the page doesn't already link to. Idempotent (id marker)."""
import glob, re
CO = ("/blog/company-truck-driver-health-insurance", "Company driver with no health insurance? Your options")
COST = ("/truck-driver-health-insurance-cost", "How much truck driver health insurance costs in 2027")
MIA = ("/seguro-de-salud-miami", "Seguros médicos en Miami: precios 2027")
SKIP = {"trucking-health-quote.html", "trucking-partners.html"}
truck = [f for f in glob.glob("*.html") if re.search(r"truck|owner-operator|cdl|otr|lease-operator|trucker|dot-physical", f) and f not in SKIP and "lp/" not in f]
spanish = ["seguro-medico-camioneros.html", "seguro-medico-camioneros-florida.html", "costo-seguro-medico-camioneros.html", "seguro-medico-owner-operators.html", "examen-medico-dot.html", "blog/inscripcion-abierta-2027.html", "blog/mejores-seguros-medicos-miami-2027.html"]
def box(f, targets, label):
    s = open(f, encoding="utf-8").read()
    if 'id="vs-xl"' in s or "<footer" not in s: return 0
    t = [x for x in targets if 'href="%s"' % x[0] not in s and f[:-5] != x[0].lstrip("/")]
    if not t: return 0
    links = " &middot; ".join('<a href="%s">%s</a>' % x for x in t)
    html = ('<section id="vs-xl" style="padding:22px 0;border-top:1px solid #e4e9f2;background:#fff"><div class="container" style="max-width:820px">'
            '<p style="margin:0;font-size:.98rem;line-height:1.7"><strong>%s</strong> %s</p></div></section>\n' % (label, links))
    i = s.index("<footer")
    open(f, "w", encoding="utf-8").write(s[:i] + html + s[i:]); return len(t)
n = 0
for f in truck:
    if f in spanish: continue
    n += bool(box(f, [COST, CO], "Popular driver guides:"))
for f in spanish:
    n += bool(box(f, [MIA, ("/costo-seguro-medico-camioneros", "Costo del seguro médico para camioneros")], "Guías en español:"))
print("pages updated", n)
