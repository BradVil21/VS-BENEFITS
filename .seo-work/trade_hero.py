# -*- coding: utf-8 -*-
"""Simple trade-page hero, modelled on the homepage hero (2026-11-21).

Headline, one-line subhead, ZIP box that goes straight to the business quote,
Google rating line, photo on the right over the brand ribbon. Self-contained:
all classes are prefixed th- so it can drop into any page template.
"""

CSS = """<style id="vs-th-css">
.th-hero{background:#faf8f5;overflow:hidden;isolation:isolate;padding:56px 0 64px}
.th-in{max-width:1200px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:1.05fr 1fr;gap:48px;align-items:center}
.th-in>*{min-width:0}
.th-hero h1{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:clamp(2.1rem,4.4vw,3.2rem);line-height:1.08;font-weight:800;margin:0 0 18px;letter-spacing:-.01em}
.th-hero h1 span{display:block;background-image:linear-gradient(90deg,#16447f,#0db5a6);-webkit-background-clip:text;background-clip:text;color:transparent}
.th-sub{font-size:1.15rem;line-height:1.6;color:#334155;max-width:540px;margin:0 0 22px}
.th-zip label{display:block;font-weight:700;color:#0b2346;font-size:.98rem;margin:0 0 8px}
.th-row{display:flex;gap:8px;background:#fff;border:1px solid #dbe3ee;border-radius:14px;padding:6px;max-width:470px;box-shadow:0 12px 30px -18px rgba(11,35,70,.35)}
.th-row input{flex:1 1 auto;min-width:0;border:0;outline:0;font:inherit;font-size:1.1rem;padding:10px 12px;background:transparent;color:#0b2346}
.th-row button{flex:0 0 auto;border:0;cursor:pointer;background:#1f6fe5;color:#fff;font:inherit;font-weight:700;font-size:1rem;padding:12px 20px;border-radius:10px;box-shadow:0 10px 24px -10px rgba(31,111,229,.65)}
.th-row button:hover{background:#1559c2}
.th-zip input:invalid:not(:placeholder-shown){color:#b42318}
.th-rating{display:inline-flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:14px;font-size:.92rem;color:#475569!important;text-decoration:none!important}
.th-stars{color:#f5a623;letter-spacing:1px}
.th-media{position:relative}
.th-ribbon{position:absolute;z-index:0;pointer-events:none;left:-8%;top:-30%;width:120%;height:auto;overflow:visible}
.th-photo{position:relative;z-index:1;border-radius:22px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(11,35,70,.55);aspect-ratio:4/3;background:#e8eef6}
.th-photo img{display:block;width:100%;height:100%;object-fit:cover}
.th-card{position:relative;z-index:1;background:#fff;border-radius:22px;box-shadow:0 30px 60px -30px rgba(11,35,70,.45);padding:30px 30px 26px}
.th-card h2{font-family:'Poppins','Inter',sans-serif;font-size:1.25rem;color:#0b2346;margin:0 0 16px}
.th-card ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.th-card li{display:flex;gap:12px;align-items:baseline;color:#334155;font-size:1rem;line-height:1.45}
.th-card li b{font-family:'Poppins','Inter',sans-serif;color:#16447f;font-size:1.35rem;min-width:84px}
@media(max-width:900px){
 .th-hero{padding:32px 0 40px}
 .th-in{grid-template-columns:1fr;gap:28px}
 .th-copy{text-align:center}
 .th-sub{margin-left:auto;margin-right:auto}
 .th-row{margin:0 auto}
 .th-media{overflow:hidden;padding:26px 12px 12px;margin:0 -12px}
 .th-ribbon{top:-55%;left:-10%;width:120%}
}
@media(max-width:480px){
 .th-hero h1{font-size:1.95rem}
 .th-row button{padding:12px 14px;font-size:.95rem}
 .th-rating{font-size:.85rem;justify-content:center}
 .th-free{display:none}
}
</style>"""

RIBBON = ('<svg class="th-ribbon" viewBox="0 0 600 560" aria-hidden="true" focusable="false"><defs><linearGradient id="thg1" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#16447f"/><stop offset=".55" stop-color="#1f6fe5"/><stop offset="1" stop-color="#0db5a6"/></linearGradient></defs>'
          '<path d="M170 -340 C 40 -80, 30 210, 250 262 C 430 304, 620 330, 575 700" fill="none" stroke="url(#thg1)" stroke-width="78" stroke-linecap="round"/>'
          '<path d="M95 -340 C -30 -40, -10 290, 215 335" fill="none" stroke="#0db5a6" stroke-opacity=".35" stroke-width="14" stroke-linecap="round"/></svg>')

G = ('<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/>'
     '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
     '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
     '<path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>')

STATS_CARD = ('<div class="th-card"><h2>Why trade owners use us</h2><ul>'
              '<li><b>1,000+</b><span>companies helped with employee benefits</span></li>'
              '<li><b>2&ndash;100+</b><span>employees, from two-truck shops to full crews</span></li>'
              '<li><b>40+</b><span>states where we&rsquo;re licensed</span></li>'
              '<li><b>$0</b><span>to use us. Carriers pay our commission</span></li></ul></div>')

def hero(slug, lead, span, sub, img=None, alt="", w=1600, h=900, qtype="business"):
    """img: base name in /compressed with .jpg/.webp and -900 variants (or None for the stats card)."""
    if img:
        media = ('<div class="th-photo"><picture>'
                 '<source type="image/webp" srcset="/compressed/{i}-900.webp 900w, /compressed/{i}.webp {w}w" sizes="(max-width:900px) 100vw, 560px">'
                 '<img src="/compressed/{i}-900.jpg" srcset="/compressed/{i}-900.jpg 900w, /compressed/{i}.jpg {w}w" sizes="(max-width:900px) 100vw, 560px" '
                 'width="{w}" height="{h}" alt="{a}" fetchpriority="high" decoding="async" /></picture></div>').format(i=img, w=w, h=h, a=alt)
    else:
        media = STATS_CARD
    return ('<section class="th-hero"><div class="th-in"><div class="th-copy">'
            '<h1>{lead} <span>{span}</span></h1>'
            '<p class="th-sub">{sub}</p>'
            '<form class="th-zip" action="/quote" method="get">'
            '<label for="th-zip-in">Enter your ZIP code</label>'
            '<div class="th-row"><input id="th-zip-in" name="zip" type="text" inputmode="numeric" pattern="[0-9]{{5}}" maxlength="5" placeholder="ZIP code" autocomplete="postal-code" required />'
            '<button type="submit">Find Affordable Plans</button></div>'
            '<input type="hidden" name="type" value="{qtype}" /><input type="hidden" name="from" value="{slug}_hero" /></form>'
            '<a class="th-rating" href="/#reviews-anchor" aria-label="Rated 5.0 out of 5 from 53 Google reviews">{g}<span class="th-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5.0 from 53 Google reviews<i class="th-free"> &middot; Free, no obligation</i></a>'
            '</div><div class="th-media">{rib}{media}</div></div></section>').format(lead=lead, span=span, sub=sub, slug=slug, g=G, rib=RIBBON, media=media, qtype=qtype)

PB_CSS = """<style id="vs-pb-css">
.pb{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:center;max-width:1100px;margin:0 auto}
.pb>*{min-width:0}
.pb-img{position:relative}
.pb-img img{display:block;width:100%;height:auto;border-radius:20px;box-shadow:0 30px 60px -30px rgba(11,35,70,.6)}
.pb-img::before{content:"";position:absolute;inset:18px -14px -14px 18px;border-radius:20px;background:linear-gradient(135deg,#16447f,#0db5a6);opacity:.18;z-index:-1}
.pb h2{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:clamp(1.5rem,3vw,2.05rem);line-height:1.2;margin:0 0 14px}
.pb p{color:#334155;line-height:1.65;margin:0 0 16px}
.pb ul{list-style:none;padding:0;margin:0 0 22px;display:grid;gap:10px}
.pb li{position:relative;padding-left:30px;color:#1e293b;line-height:1.5}
.pb li::before{content:"";position:absolute;left:0;top:3px;width:20px;height:20px;border-radius:50%;background:#0db5a6 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 13l4 4L19 7'/%3E%3C/svg%3E") center/12px no-repeat}
@media(max-width:860px){.pb{grid-template-columns:1fr;gap:26px}.pb-img::before{inset:12px -8px -8px 12px}}
</style>"""

def photo_band(img, alt, heading, text, bullets, href, btn="Get my free quote", w=1200, h=900):
    pic = ('<picture><source type="image/webp" srcset="/compressed/{i}-900.webp 900w, /compressed/{i}.webp {w}w" sizes="(max-width:860px) 100vw, 540px">'
           '<img src="/compressed/{i}-900.jpg" srcset="/compressed/{i}-900.jpg 900w, /compressed/{i}.jpg {w}w" sizes="(max-width:860px) 100vw, 540px" width="{w}" height="{h}" alt="{a}" loading="lazy" decoding="async" /></picture>').format(i=img, w=w, h=h, a=alt)
    return ('<section class="section"><div class="container"><div class="pb"><div class="pb-img">%s</div><div><h2>%s</h2><p>%s</p><ul>%s</ul>'
            '<a class="btn btn-primary" href="%s">%s</a></div></div></div></section>') % (pic, heading, text, "".join("<li>%s</li>" % b for b in bullets), href, btn)
