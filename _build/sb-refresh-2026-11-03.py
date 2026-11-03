"""Small business page refresh (2026-11-03): light hero with cut-out photo + ZIP,
nationwide copy instead of Florida-only, photo industry tiles."""
import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def R(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)

# ---------------------------------------------------------------- CSS
CSS = r'''<style id="sb-refresh-css">
/* Small business page refresh (2026-11-03). Remove this block + the sb- markup to undo. */
.sb-hero{background:#faf8f5;padding:52px 0 0;overflow:hidden;position:relative}
.sb-hero .hero-grid{display:grid;grid-template-columns:1fr;gap:12px;align-items:center}
.sb-hero h1{color:#0b2346;font-size:clamp(2.1rem,4.6vw,3.2rem);line-height:1.06;margin-bottom:14px}
.sb-hero h1 span{background:linear-gradient(90deg,#16447f,#0db5a6);-webkit-background-clip:text;background-clip:text;color:transparent}
.sb-hero .eyebrow{background:#fff;border:1px solid #dbe7f7}
.sb-sub{font-size:1.15rem;line-height:1.6;color:#334155;max-width:520px;margin:0 0 20px}
.sbz{max-width:470px;margin:0 0 16px}
.sbz label{display:block;font-weight:700;font-size:.92rem;color:#0b2346;margin:0 0 8px}
.sbz-row{display:flex;gap:8px;background:#fff;border:1.5px solid #e2e8f0;border-radius:14px;padding:6px;box-shadow:0 10px 28px rgba(13,27,42,.08);transition:border-color .2s,box-shadow .2s}
.sbz-row:focus-within{border-color:#0db5a6;box-shadow:0 10px 28px rgba(13,181,166,.18)}
.sbz-row input{flex:1 1 0;width:0;min-width:0;border:0;outline:0;font:inherit;font-size:1.1rem;font-weight:600;letter-spacing:.06em;padding:10px 12px;color:#0b2346;background:transparent}
.sbz-row button{flex-shrink:0;border:0;border-radius:10px;background:#1f6fe5;color:#fff;font:inherit;font-weight:700;font-size:1rem;padding:12px 20px;cursor:pointer;white-space:nowrap;box-shadow:0 10px 24px -10px rgba(31,111,229,.65)}
.sbz-row button:hover{background:#1559c2}
.sbz-err{color:#b42318;font-size:.86rem;margin:8px 0 0}
.sb-rating{display:inline-flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:.92rem;color:#475569;text-decoration:none}
.sb-rating .st{color:#f5a400;letter-spacing:1px}
.sb-rating svg{background:#fff;border-radius:50%;padding:3px;width:24px;height:24px;flex-shrink:0;box-shadow:0 1px 4px rgba(13,27,42,.15)}
.sb-img{position:relative;width:min(420px,100%);margin:20px auto 0;align-self:end}
.sb-img img{position:relative;z-index:1;display:block;width:100%;height:auto}
.sb-ribbon{position:absolute;z-index:0;left:-38%;top:-4%;width:176%;height:auto;pointer-events:none;overflow:visible}
.sb-chip{position:absolute;z-index:2;background:#fff;border-radius:14px;padding:10px 14px;box-shadow:0 14px 30px -12px rgba(11,35,70,.35);font-size:.82rem;font-weight:700;color:#0b2346;line-height:1.25;display:flex;align-items:center;gap:10px}
.sb-chip b{display:block;font-size:1.1rem;color:#0b7f74}
.sb-chip i{font-style:normal;width:34px;height:34px;border-radius:10px;background:#e6f7f5;color:#0b7f74;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sb-chip.c1{left:-8%;top:38%}.sb-chip.c2{right:-6%;top:12%}
@media(min-width:900px){
 .sb-hero{padding-top:64px}
 .sb-hero .hero-grid{grid-template-columns:1.1fr .9fr;gap:24px}
 .sb-hero .hero-grid>div:first-child{padding-bottom:72px}
 .sb-img{width:min(440px,100%);margin:0 auto}
 .sb-ribbon{left:-6%;width:140%;top:-8%}
}
@media(max-width:899px){.sb-img{overflow:hidden;padding-top:10px}.sb-ribbon{left:-30%;width:160%;top:0}.sb-chip.c1{left:2%}.sb-chip.c2{right:2%}}
@media(max-width:480px){.sbz-row button{padding:12px 14px;font-size:.95rem}.sb-rating{display:flex;justify-content:center;font-size:.85rem}.sb-rating .fr{display:none}.sb-chip{font-size:.74rem;padding:8px 10px}.sb-chip b{font-size:.98rem}.sb-chip i{width:28px;height:28px}}
/* industry photo tiles */
.sb-ind{display:grid;grid-template-columns:1fr;gap:18px}
@media(min-width:640px){.sb-ind{grid-template-columns:1fr 1fr}}
@media(min-width:960px){.sb-ind{grid-template-columns:repeat(3,1fr)}}
.sb-tile{position:relative;display:block;border-radius:18px;overflow:hidden;aspect-ratio:4/3;background:#e8eef7;text-decoration:none!important;box-shadow:0 16px 36px -18px rgba(13,27,42,.45);isolation:isolate}
.sb-tile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.sb-tile:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,35,70,0) 30%,rgba(11,35,70,.85) 100%);z-index:1}
.sb-tile-b{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:20px;color:#fff}
.sb-tile-b small{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(6px);border-radius:999px;padding:4px 11px;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.sb-tile-b h3{color:#fff;font-size:1.25rem;margin:10px 0 4px;line-height:1.25}
.sb-tile-b p{color:rgba(255,255,255,.88);font-size:.9rem;margin:0;line-height:1.45}
.sb-tile-b span{display:inline-flex;align-items:center;gap:6px;margin-top:10px;font-weight:700;font-size:.88rem;color:#5eead4;transition:gap .2s}
.sb-tile:hover img{transform:scale(1.05)}.sb-tile:hover .sb-tile-b span{gap:10px}
@media(prefers-reduced-motion:reduce){.sb-tile img{transition:none}.sb-tile:hover img{transform:none}}
/* rules cards + stats polish */
.sb-rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.sb-rule{text-align:left;background:#fff;border:1px solid var(--line,#e4e9f2);border-radius:16px;padding:22px;box-shadow:0 8px 24px -16px rgba(13,27,42,.25)}
.sb-rule i{font-style:normal;width:44px;height:44px;border-radius:12px;background:#eaf2fd;color:#16447f;display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.sb-rule h3{margin:0 0 6px;font-size:1.08rem}.sb-rule p{margin:0;color:var(--ink-2,#334155);font-size:.95rem;line-height:1.55}
.sb-why{display:grid;grid-template-columns:1fr;gap:28px;align-items:center;margin-top:44px}
@media(min-width:900px){.sb-why{grid-template-columns:.9fr 1.1fr}}
.sb-why img{width:100%;border-radius:20px;aspect-ratio:4/3;object-fit:cover;box-shadow:0 20px 44px -22px rgba(13,27,42,.5)}
.sb-why .stats{margin-top:18px}
</style>
'''
R('</head>', CSS + '</head>')

# ---------------------------------------------------------------- HERO
G = '<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
RIB = '<svg class="sb-ribbon" viewBox="0 0 600 700" aria-hidden="true" focusable="false"><defs><linearGradient id="sbg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#16447f"/><stop offset=".55" stop-color="#1f6fe5"/><stop offset="1" stop-color="#0db5a6"/></linearGradient></defs><path d="M120 -120 C 40 120, 80 300, 300 330 C 500 358, 640 420, 560 820" fill="none" stroke="url(#sbg1)" stroke-width="84" stroke-linecap="round"/><path d="M50 -120 C -30 160, 20 360, 270 400" fill="none" stroke="#0db5a6" stroke-opacity=".35" stroke-width="14" stroke-linecap="round"/></svg>'
ICO_USERS = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="7" r="3"/><path d="M3 21v-1a6 6 0 0 1 12 0v1"/><circle cx="17.5" cy="9.5" r="2.5"/><path d="M16 21v-.5a4.5 4.5 0 0 1 6-4.2"/></svg>'
ICO_CHECK = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'
HERO = f'''<section class="hero sb-hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Group Health Insurance &middot; 40+ States</span>
        <h1>Small Business Health Insurance for <span>2 to 50 Employees</span></h1>
        <p class="sb-sub">Group plans from top A-rated carriers, compared and set up for you, free. No HR department needed.</p>
        <form class="sbz" action="/small-business-health-quote" method="get" novalidate onsubmit="var z=this.zip.value.replace(/\\D/g,'');var e=this.querySelector('.sbz-err');if(z.length!==5){{e.hidden=false;this.zip.focus();return false}}e.hidden=true;this.zip.value=z;">
          <input type="hidden" name="type" value="business" /><input type="hidden" name="from" value="small-business-health-insurance_zip" />
          <label for="sbz-zip">Enter your business ZIP code</label>
          <div class="sbz-row"><input id="sbz-zip" name="zip" type="text" inputmode="numeric" pattern="[0-9]{{5}}" maxlength="5" placeholder="ZIP code" autocomplete="postal-code" required /><button type="submit">Find Affordable Plans</button></div>
          <p class="sbz-err" role="alert" hidden>Please enter a valid 5-digit ZIP code.</p>
        </form>
        <a class="sb-rating" href="/#reviews-anchor" aria-label="Rated 5.0 out of 5 from 53 Google reviews">{G}<span class="st" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5.0 from 53 Google reviews<span class="fr"> &middot; Free, no obligation</span></a>
      </div>
      <div class="sb-img">
        {RIB}
        <img decoding="async" fetchpriority="high" srcset="/compressed/sb-owner-cutout-400.webp 400w, /compressed/sb-owner-cutout.webp 522w" sizes="(max-width: 900px) 400px, 440px" src="/compressed/sb-owner-cutout.webp" width="522" height="908" alt="Smiling small business owner" loading="eager" />
        <div class="sb-chip c1"><i>{ICO_USERS}</i><span><b>2 to 50</b>employees</span></div>
        <div class="sb-chip c2"><i>{ICO_CHECK}</i><span><b>$0</b>to set up</span></div>
      </div>
    </div>
  </div>
</section>'''
m = re.search(r'<section class="hero">\n.*?</section>', s, re.S)
assert m and 'Small Business Health Insurance for 2 to 50 Employees' in m.group(0)
s = s[:m.start()] + HERO + s[m.end():]

# ---------------------------------------------------------------- WHO WE SERVE
R('<p>We work with small employers across Florida and 40+ states who want to offer real benefits without a full HR team. From a two-person trade shop in Tampa to a 20-person dental practice in Miami -- if you have between 2 and 25 employees, we have a plan for you.</p>',
  '<p>We work with small employers in 40+ states who want to offer real benefits without a full HR team. From a two-person trade shop to a 20-person dental practice, if you have between 2 and 50 employees, we have a plan for you.</p>')

# ---------------------------------------------------------------- RULES (nationwide)
I_USERS = '<i>' + ICO_USERS.replace('18','22',2) + '</i>'
I_SHIELD = '<i>' + ICO_CHECK.replace('18','22',2) + '</i>'
I_MAP = '<i><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l-6 3V6l6-3 6 3 6-3v15l-6 3-6-3zM9 3v15M15 6v15"/></svg></i>'
I_TAX = '<i><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></i>'
m = re.search(r'<span class="eyebrow">Florida Employers</span>.*?</div>\n  </div>\n</section>', s, re.S)
assert m
RULES = f'''<span class="eyebrow">Rules to Know</span>
      <h2>Small Business Health Insurance Rules and Participation</h2>
      <p style="max-width:700px;margin:0 auto;color:var(--ink-2)">A few rules shape how small group health insurance works in every state. Here is what employers should know before shopping for a plan.</p>
    </div>
    <div class="sb-rules">
      <div class="sb-rule">{I_USERS}<h3>Minimum Participation</h3><p>Most carriers require 50% to 75% of eligible employees to enroll. Employees covered through a spouse can usually waive without counting against you.</p></div>
      <div class="sb-rule">{I_SHIELD}<h3>Guaranteed Issue</h3><p>Small group plans for 1 to 50 employees are guaranteed issue under federal law. Carriers cannot deny coverage or charge more because of anyone&rsquo;s health.</p></div>
      <div class="sb-rule">{I_MAP}<h3>Carriers Vary by State</h3><p>Which carriers and networks you can pick from depends on your state and county. We compare Blue Cross Blue Shield, UnitedHealthcare, Aetna, Cigna and regional carriers for your ZIP code.</p></div>
      <div class="sb-rule">{I_TAX}<h3>Small Business Tax Credit</h3><p>Businesses with fewer than 25 full-time equivalent employees and average wages under $56,000 may qualify for a federal Small Business Health Care Tax Credit worth up to 50% of your premium contribution. We check this for every client.</p></div>
    </div>
  </div>
</section>'''
s = s[:m.start()] + RULES + s[m.end():]

# why-choose: add a photo beside the stats
m = re.search(r'<h2>Why Small Business Owners Choose VS Health Benefits</h2></div>\n    <div class="stats">(.*?)</div>\n  </div>\n</section>', s, re.S)
assert m
s = s[:m.start()] + ('<h2>Why Small Business Owners Choose VS Health Benefits</h2></div>\n'
    '    <div class="sb-why"><img decoding="async" loading="lazy" src="/compressed/business-owner-office-640.webp" width="640" height="480" alt="Small business owner smiling in his office" />'
    '<div><p style="font-size:1.05rem;color:var(--ink-2);margin:0">One advisor handles your quotes, setup, employee enrollment and every renewal. You get real benefits for your team without adding HR work to your week.</p>'
    '<div class="stats">' + m.group(1) + '</div></div></div>\n  </div>\n</section>') + s[m.end():]

# ---------------------------------------------------------------- INDUSTRY PHOTO TILES
TILES = [
 ('/health-insurance-for-contractors', 'construction-workers-hard-hats-clipboard-640.webp', 'Construction workers in hard hats reviewing plans', 'Construction &amp; Trades', 'Contractors', 'Plans that help you win bids and keep your crew.'),
 ('/health-insurance-for-trucking-companies', 'trucker-red-semi-cab-640.webp', 'Truck driver next to his red semi', 'Fleets &amp; Carriers', 'Trucking Companies', 'National PPO networks that follow drivers on the road.'),
 ('/health-insurance-for-restaurants', 'restaurant-chef-plating-dish-640.webp', 'Chef plating food in a restaurant kitchen', 'Restaurants &amp; Hospitality', 'Restaurants', 'Keep great managers and staff on tight margins.'),
 ('/health-insurance-for-hvac-companies', 'hvac-rooftop-technician-wide-640.webp', 'HVAC technician on a rooftop', 'HVAC &amp; Mechanical', 'HVAC Companies', 'Keep certified techs on your trucks all year.'),
 ('/health-insurance-for-dental-offices', 'dentalimage-640.webp', 'Dental exam in progress', 'Dental Practices', 'Dental Offices', 'Recruit and keep hygienists and assistants.'),
 ('/health-insurance-for-salons-and-spas', 'salon2-640.webp', 'Stylist washing a client&rsquo;s hair in a salon', 'Salons &amp; Spas', 'Salons and Spas', 'Benefits that keep your best stylists in the chair.'),
]
tiles = ''.join(f'<a class="sb-tile" href="{h}"><img decoding="async" loading="lazy" src="/compressed/{img}" width="640" height="480" alt="{alt}" /><div class="sb-tile-b"><small>{tag}</small><h3>{t}</h3><p>{d}</p><span>Learn more <span aria-hidden="true">&rarr;</span></span></div></a>' for h, img, alt, tag, t, d in TILES)
m = re.search(r'(<span class="eyebrow">Industries We Serve</span>.*?</div>\n)    <div class="cards">.*?</div>\n  </div>\n</section>', s, re.S)
assert m
s = s[:m.start()] + m.group(1) + '    <div class="sb-ind">' + tiles + '</div>\n    <p class="center" style="margin-top:18px"><a href="/group-health-insurance-by-industry" style="font-weight:700;color:var(--blue-700)">See every industry we cover &rarr;</a></p>\n  </div>\n</section>' + s[m.end():]

# ---------------------------------------------------------------- FAQ (nationwide)
R('<h2>Small Business Health Insurance Florida FAQ</h2>', '<h2>Small Business Health Insurance FAQ</h2>')
FAQ = [
 ('How many employees do I need for group health insurance in Florida?', 'How many employees do I need for group health insurance?',
  'In Florida, you need as few as 2 employees to qualify for a small group health plan.', 'In most states you need as few as 2 employees to qualify for a small group health plan.'),
 ('How much does small business health insurance cost in Florida?', 'How much does small business health insurance cost?',
  'Florida employers typically contribute $300 to $600 per employee per month for a solid group plan. The employee share depends on the employer contribution -- most Florida employers cover 50% to 75% of the employee-only premium.',
  'Employers typically contribute $300 to $600 per employee per month for a solid group plan, depending on the state, ages and plan design. Most employers cover 50% to 75% of the employee-only premium.'),
 ('When can I enroll in a small business health plan in Florida?', 'When can I enroll in a small business health plan?',
  'Unlike individual ACA plans, small group health insurance in Florida has no fixed open enrollment window.', 'Unlike individual plans, small group health insurance has no fixed open enrollment window.'),
 ('What is the best health insurance for a small business in Florida?', 'What is the best health insurance for a small business?',
  'Florida Blue has the broadest local network for Florida-based employees. UnitedHealthcare and Aetna are strong options if employees travel or work across multiple states.',
  'Your state&rsquo;s Blue Cross Blue Shield plan often has the broadest local network. UnitedHealthcare and Aetna are strong options if employees travel or work across multiple states.'),
 ('Do I have to offer health insurance to employees in Florida?', 'Do I have to offer health insurance to my employees?',
  'Florida employers with fewer than 50 full-time equivalent employees are not legally required to offer health insurance.', 'Employers with fewer than 50 full-time equivalent employees are not required by federal law to offer health insurance.'),
 ('Can I get group health insurance in Tampa or Miami for a small business?', 'Do you work with small businesses in my state?',
  'Yes. VS Health Benefits works with small businesses throughout Florida including Miami, Tampa, Fort Lauderdale, Orlando, Jacksonville, and St. Petersburg. Plan availability and carrier networks vary by county, which is why working with a local advisor matters. We know which carriers have the strongest networks in each Florida market.',
  'Yes. VS Health Benefits is licensed in 40+ states and works with small businesses from coast to coast. Plan availability and carrier networks vary by state and county, so we quote your exact ZIP code and show you which carriers have the strongest networks where your team lives and works.'),
]
for q_old, q_new, a_old, a_new in FAQ:
    R(q_old, q_new); R(a_old, a_new)

R('<div class="stat-num">2-25</div><div class="stat-label">Employee sweet spot</div>','<div class="stat-num">2-50</div><div class="stat-label">Employees per group</div>')
# head keywords: drop the Florida-only keyword
s = s.replace(', group plan Florida,', ', group plan,')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
