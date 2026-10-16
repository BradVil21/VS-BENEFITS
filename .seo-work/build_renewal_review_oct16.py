#!/usr/bin/env python3
"""Build /small-business-renewal-review (Oct 16 2026). Idempotent: re-run to rebuild.
Chrome (head styles, header, footer, scripts) is copied from an existing post so it
stays identical to the rest of the site; only meta, schema and <main> are replaced."""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "blog/small-business-health-insurance-cost-2027.html")
OUT = os.path.join(ROOT, "small-business-renewal-review.html")
URL = "https://www.vshealthbenefits.com/small-business-renewal-review"
TITLE = "2027 Group Health Renewal Went Up? Free Renewal Review"
DESC = ("Small group health renewals are coming in 8% to 15%+ higher for 2027. Send us your renewal and a licensed "
        "advisor will shop it against other carriers, level-funded and ICHRA options before you sign. Free.")
IMG = "https://www.vshealthbenefits.com/compressed/health-insurance-cost-2026-woman.jpg"

s = open(TPL, encoding="utf-8").read()

# ---- head meta ----
def sub1(pat, rep):
    global s
    s, n = re.subn(pat, rep, s, count=1, flags=re.S)
    assert n == 1, pat
sub1(r"<title>.*?</title>", f"<title>{TITLE}</title>")
sub1(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{DESC}" />')
sub1(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{URL}" />')
sub1(r'<meta property="og:type" content="[^"]*" />', '<meta property="og:type" content="website" />')
sub1(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{TITLE}" />')
sub1(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{DESC}" />')
sub1(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{URL}" />')
sub1(r'<meta name="twitter:title" content="[^"]*" />', f'<meta name="twitter:title" content="{TITLE}" />')
sub1(r'<meta name="twitter:description" content="[^"]*" />', f'<meta name="twitter:description" content="{DESC}" />')
s = re.sub(r'<meta property="article:[^>]*/>\n?', "", s)
# drop the post's JSON-LD; ours goes in below
s = re.sub(r'<script type="application/ld+json">.*?</script>\n?'.replace("+", r"\+"), "", s, flags=re.S)

FAQ = [
 ("Is a double-digit 2027 renewal increase normal?",
  "Unfortunately, yes. KFF's review of 2027 small-group rate filings found a median requested increase of 14%, driven by hospital and drug prices, specialty drugs and GLP-1 use. In Florida, small-group filings ranged from about 8% to 15.5%. Your own renewal also moves with your group's age and claims, so it can land above or below those figures."),
 ("Can I switch group health carriers at renewal?",
  "Yes. Small group plans can start on the first of any month, so your renewal date is the natural time to move. You can switch carriers, change plan designs, or move to a level-funded plan or an ICHRA, as long as the new plan is in place before the old one ends."),
 ("What if we can't meet the carrier's participation or contribution rules?",
  "Federal rules give small employers a window from November 15 to December 15 each year when carriers must accept a group even if it can't meet their minimum participation or employer-contribution requirements. Coverage bought in that window starts January 1."),
 ("Does a renewal review cost anything?",
  "No. Carriers pay us when a plan is placed, so the review, the comparison and the paperwork cost your business nothing. If your current renewal turns out to be the best option, we'll tell you."),
 ("What do you need from me?",
  "Your renewal letter, or just the current and new monthly premium, plus your headcount and ZIP code. To get firm quotes from other carriers we'll then need a short employee census (ages, ZIP codes and who is covered), which we send as a simple online form."),
 ("Will my employees lose their doctors if we switch?",
  "Not if we check first. We compare provider networks before recommending a change, and flag any doctors or hospitals your team uses that a new plan would not cover."),
]

schema = [
 {"@context":"https://schema.org","@type":"WebPage","name":TITLE,"url":URL,"description":DESC,
  "dateModified":"2026-10-16","inLanguage":"en-US",
  "author":{"@type":"Person","name":"Bradley Vilsaint","jobTitle":"Licensed Health Insurance Advisor","identifier":"NPN 22116298","url":"https://www.vshealthbenefits.com/bradley-vilsaint"},
  "publisher":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":"https://www.vshealthbenefits.com","telephone":"+1-954-825-1009"}},
 {"@context":"https://schema.org","@type":"Service","name":"Small business group health renewal review",
  "serviceType":"Group health insurance renewal review","areaServed":"US",
  "provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","telephone":"+1-954-825-1009"},
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD","description":"Free renewal review and carrier comparison for employers with 2-50 employees"}},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://www.vshealthbenefits.com/"},
  {"@type":"ListItem","position":2,"name":"Small Business Health Insurance","item":"https://www.vshealthbenefits.com/small-business-health-insurance"},
  {"@type":"ListItem","position":3,"name":"Renewal Review","item":URL}]},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
]
ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in schema)

CSS = r"""<style id="rr-css">
.rr-hero{display:grid;grid-template-columns:1.15fr 1fr;gap:40px;align-items:start;padding:28px 0 36px}
.rr-eyebrow{display:inline-block;background:#fff4e5;color:#9a4b00;font-weight:700;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;padding:6px 12px;border-radius:999px;margin-bottom:14px}
.rr-hero h1{font-family:Poppins,Inter,sans-serif;font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.15;color:var(--ink);margin:0 0 14px}
.rr-lede{font-size:1.08rem;color:var(--ink-2);line-height:1.6;margin:0 0 18px}
.rr-checks{list-style:none;padding:0;margin:0 0 20px}
.rr-checks li{position:relative;padding-left:28px;margin:9px 0;color:var(--ink-2);line-height:1.5}
.rr-checks li:before{content:"";position:absolute;left:0;top:4px;width:18px;height:18px;border-radius:50%;background:var(--teal) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fff' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E") center/11px no-repeat}
.rr-by{font-size:.86rem;color:var(--muted)}
.rr-jump{display:none}
.rr-by a{color:var(--blue-700);font-weight:600}
.rr-card{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);padding:24px}
.rr-card h2{font-family:Poppins,Inter,sans-serif;font-size:1.25rem;margin:0 0 4px;color:var(--ink)}
.rr-card .rr-sub{font-size:.9rem;color:var(--muted);margin:0 0 16px}
.rr-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.rr-f{margin-bottom:12px}
.rr-f label{display:block;font-size:.82rem;font-weight:600;color:var(--ink-2);margin-bottom:5px}
.rr-f input,.rr-f select{width:100%;min-height:var(--tap);padding:10px 12px;border:1.5px solid var(--line);border-radius:10px;font:inherit;font-size:16px;background:#fff;color:var(--ink)}
.rr-f input:focus,.rr-f select:focus{outline:none;border-color:var(--blue-500);box-shadow:0 0 0 3px rgba(47,125,224,.15)}
.rr-f.err input,.rr-f.err select{border-color:#dc2626}
.rr-consent{display:flex;gap:10px;align-items:flex-start;font-size:.74rem;line-height:1.5;color:var(--muted);margin:6px 0 14px}
.rr-consent input{margin-top:3px;width:18px;height:18px;flex:0 0 auto}
.rr-consent a{color:var(--blue-700)}
.rr-btn{width:100%;min-height:52px;border:0;border-radius:12px;background:linear-gradient(135deg,var(--blue-700),var(--teal));color:#fff;font-weight:800;font-size:1.02rem;cursor:pointer;font-family:inherit}
.rr-btn[disabled]{opacity:.7;cursor:wait}
.rr-msg{font-size:.85rem;color:#dc2626;margin:8px 0 0;min-height:1em}
.rr-fine{font-size:.78rem;color:var(--muted);text-align:center;margin:10px 0 0}
.rr-ok{display:none;text-align:center;padding:10px 0}
.rr-ok h3{font-family:Poppins,Inter,sans-serif;color:var(--ink);margin:8px 0}
.rr-ok p{color:var(--ink-2);font-size:.95rem;line-height:1.55}
.rr-ok a.rr-btn{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;margin-top:8px}
.rr-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:8px 0 40px}
.rr-stat{background:var(--blue-50);border:1px solid var(--blue-100);border-radius:14px;padding:18px}
.rr-stat b{display:block;font-family:Poppins,Inter,sans-serif;font-size:1.9rem;color:var(--blue-700);line-height:1.1}
.rr-stat span{display:block;font-size:.9rem;color:var(--ink-2);margin-top:6px;line-height:1.45}
.rr-sec{margin:0 0 44px}
.rr-sec h2{font-family:Poppins,Inter,sans-serif;font-size:clamp(1.35rem,3vw,1.8rem);color:var(--ink);margin:0 0 12px}
.rr-sec>p{color:var(--ink-2);line-height:1.65;max-width:820px}
.rr-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;counter-reset:rr}
.rr-step{border:1px solid var(--line);border-radius:14px;padding:20px;background:#fff}
.rr-step:before{counter-increment:rr;content:counter(rr);display:inline-flex;width:34px;height:34px;border-radius:50%;background:var(--blue-700);color:#fff;font-weight:800;align-items:center;justify-content:center;margin-bottom:10px}
.rr-step h3{font-size:1.05rem;margin:0 0 6px;color:var(--ink)}
.rr-step p{font-size:.93rem;color:var(--ink-2);line-height:1.55;margin:0}
.rr-levers{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.rr-lever{border-left:4px solid var(--teal);background:var(--bg-soft);border-radius:0 12px 12px 0;padding:14px 16px}
.rr-lever h3{font-size:1rem;margin:0 0 4px;color:var(--ink)}
.rr-lever p{font-size:.92rem;color:var(--ink-2);line-height:1.55;margin:0}
.rr-lever a{color:var(--blue-700);font-weight:600}
.rr-tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.rr-t{width:100%;border-collapse:collapse;font-size:.93rem;min-width:520px}
.rr-t th{text-align:left;background:var(--blue-50);color:var(--blue-700);padding:11px 13px;border-bottom:2px solid var(--blue-100);font-size:.86rem}
.rr-t td{padding:11px 13px;border-bottom:1px solid #eceff4;vertical-align:top;line-height:1.5;color:var(--ink-2)}
.rr-ind{display:flex;flex-wrap:wrap;gap:8px}
.rr-ind a{border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:.9rem;color:var(--blue-700);text-decoration:none;font-weight:600;background:#fff}
.rr-ind a:hover{border-color:var(--blue-500)}
.rr-faq details{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:10px;background:#fff}
.rr-faq summary{font-weight:700;cursor:pointer;color:var(--ink)}
.rr-faq details p{color:var(--ink-2);line-height:1.6;margin:10px 0 0}
.rr-cta{background:linear-gradient(135deg,var(--blue-800),var(--teal-dark));color:#fff;border-radius:18px;padding:30px;text-align:center;margin:0 0 40px}
.rr-cta h2{color:#fff;font-family:Poppins,Inter,sans-serif;margin:0 0 8px}
.rr-cta p{color:rgba(255,255,255,.9);margin:0 0 16px}
.rr-cta a{display:inline-block;background:#fff;color:var(--blue-700);font-weight:800;border-radius:999px;padding:12px 22px;text-decoration:none;margin:4px}
.rr-src{font-size:.8rem;color:var(--muted);line-height:1.6}
.rr-src a{color:var(--muted)}
@media (max-width:900px){.rr-jump{display:flex;align-items:center;justify-content:center;min-height:50px;border-radius:12px;background:var(--blue-700);color:#fff;font-weight:800;text-decoration:none;margin:0 0 16px}.rr-hero{grid-template-columns:1fr;gap:22px}.rr-stats,.rr-steps{grid-template-columns:1fr}.rr-levers{grid-template-columns:1fr}}
@media (max-width:420px){.rr-row{grid-template-columns:1fr;gap:0}.rr-card{padding:18px}}
</style>
"""
s = s.replace("</head>", ld + CSS + "</head>", 1)

# ---- breadcrumb ----
sub1(r'<nav class="breadcrumb" aria-label="Breadcrumb">.*?</nav>',
     '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">›</span>'
     '<a href="/small-business-health-insurance">Small Business</a><span class="sep">›</span><span>Renewal Review</span></nav>')
sub1(r'<a href="/blog" aria-current="page">Blog</a>', '<a href="/blog">Blog</a>')

EMP = "".join(f'<option value="{v}">{v}</option>' for v in ["2-5","6-10","11-25","26-50","51-100","100+"])
MONTHS = ["January 1, 2027","February 1, 2027","March 1, 2027","April 1, 2027","Later in 2027","Not sure"]
RD = "".join(f'<option value="{m}">{m}</option>' for m in MONTHS)
INC = ["Under 5%","5% to 10%","10% to 15%","15% to 20%","More than 20%","Haven't received it yet","No group plan yet"]
INCO = "".join(f'<option value="{v}">{v}</option>' for v in INC)

faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)

MAIN = f"""<main class="container" id="main">
  <section class="rr-hero">
    <div>
      <span class="rr-eyebrow">2027 group renewals are landing now</span>
      <h1>Your group health renewal went up. Get a second opinion before you sign.</h1>
      <p class="rr-lede">Small-group carriers asked for a median 14% increase for 2027. Send us your renewal and a licensed advisor will shop it against other carriers, level-funded plans and ICHRA, then show you the options side by side before your deadline.</p>
      <ul class="rr-checks">
        <li><strong>Free, no obligation.</strong> Carriers pay us, not you. If your renewal is the best deal, we'll say so.</li>
        <li><strong>Built for 2 to 50 employees</strong>, including trucking companies, contractors, restaurants and offices.</li>
        <li><strong>We check your team's doctors</strong> before recommending any change.</li>
        <li><strong>English y Español.</strong></li>
      </ul>
      <a class="rr-jump" href="#review">Start my free review &darr;</a>
      <p class="rr-by">Reviewed by <a href="/bradley-vilsaint">Bradley Vilsaint</a>, licensed health insurance advisor (NPN 22116298). Updated October 16, 2026. Prefer to talk? <a href="tel:+19548251009">(954) 825-1009</a></p>
    </div>

    <div class="rr-card" id="review">
      <form id="rr-form" novalidate>
        <h2>Request a free renewal review</h2>
        <p class="rr-sub">About 60 seconds. No census needed to start.</p>
        <div class="rr-row">
          <div class="rr-f"><label for="rr-first">First name</label><input id="rr-first" autocomplete="given-name" required></div>
          <div class="rr-f"><label for="rr-last">Last name</label><input id="rr-last" autocomplete="family-name" required></div>
        </div>
        <div class="rr-f"><label for="rr-biz">Business name</label><input id="rr-biz" autocomplete="organization" required></div>
        <div class="rr-row">
          <div class="rr-f"><label for="rr-emp">Employees</label><select id="rr-emp" required><option value="">Select</option>{EMP}</select></div>
          <div class="rr-f"><label for="rr-zip">Business ZIP</label><input id="rr-zip" inputmode="numeric" maxlength="5" autocomplete="postal-code" required></div>
        </div>
        <div class="rr-row">
          <div class="rr-f"><label for="rr-inc">Renewal increase</label><select id="rr-inc" required><option value="">Select</option>{INCO}</select></div>
          <div class="rr-f"><label for="rr-date">Renewal date</label><select id="rr-date" required><option value="">Select</option>{RD}</select></div>
        </div>
        <div class="rr-f"><label for="rr-phone">Mobile phone</label><input id="rr-phone" type="tel" inputmode="tel" autocomplete="tel" required></div>
        <div class="rr-f"><label for="rr-email">Work email</label><input id="rr-email" type="email" autocomplete="email" required></div>
        <label class="rr-consent"><input type="checkbox" id="rr-consent"><span>I agree to receive calls and SMS text messages from <strong>VS BENEFITS LLC</strong> (d/b/a VS Health Benefits) at the number provided about my quote, including by automated technology. Message &amp; data rates may apply. Message frequency varies. Reply <strong>STOP</strong> to opt out or <strong>HELP</strong> for help. Consent is not a condition of purchase. <a href="/privacy#sms" target="_blank" rel="noopener">Privacy Policy</a> &amp; <a href="/terms#sms-terms" target="_blank" rel="noopener">Terms</a>.</span></label>
        <button class="rr-btn" type="submit" id="rr-submit">Review my renewal &rarr;</button>
        <p class="rr-msg" id="rr-msg" role="alert"></p>
        <p class="rr-fine">Estimates and comparisons are not a guarantee of price or approval.</p>
      </form>
      <div class="rr-ok" id="rr-ok" aria-live="polite">
        <svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>
        <h3>Got it. Your review is started.</h3>
        <p>An advisor will reach out today during business hours. To speed things up, reply to our email with a copy of your renewal letter, or send it to <a href="mailto:info@vshealthbenefits.com?subject=Renewal%20review">info@vshealthbenefits.com</a>.</p>
        <p>The fastest way to get firm quotes is the employee census. It takes about five minutes.</p>
        <a class="rr-btn" id="rr-census" href="/census">Fill out the census &rarr;</a>
      </div>
    </div>
  </section>

  <section class="rr-stats" aria-label="2027 renewal numbers">
    <div class="rr-stat"><b>14%</b><span>Median increase small-group insurers requested for 2027 across 295 insurers in all 50 states (KFF).</span></div>
    <div class="rr-stat"><b>8&ndash;15.5%</b><span>Range of proposed 2027 small-group increases filed by Florida carriers (federal rate review filings).</span></div>
    <div class="rr-stat"><b>10.8%</b><span>Underlying medical cost trend insurers projected for 2027, driven by hospital prices, specialty drugs and GLP-1s.</span></div>
  </section>

  <section class="rr-sec">
    <h2>How the renewal review works</h2>
    <div class="rr-steps">
      <div class="rr-step"><h3>Send us the renewal</h3><p>The carrier's renewal letter, or just your current and new monthly premium. Add your headcount and ZIP.</p></div>
      <div class="rr-step"><h3>We shop it</h3><p>We price the same benefits with other carriers and model level-funded, ICHRA and plan-design alternatives using a short employee census.</p></div>
      <div class="rr-step"><h3>You pick, before the deadline</h3><p>You get a side-by-side of cost, deductibles and networks. Keep your renewal, adjust it, or switch. We handle the paperwork.</p></div>
    </div>
  </section>

  <section class="rr-sec">
    <h2>Six ways small employers cut a renewal increase</h2>
    <p>No single move fits every group. These are the levers we test against your renewal, in roughly the order they tend to matter.</p>
    <div class="rr-levers">
      <div class="rr-lever"><h3>1. Shop the same plan with other carriers</h3><p>Carriers price the same group very differently. A like-for-like comparison is the baseline for every review.</p></div>
      <div class="rr-lever"><h3>2. Move to a level-funded plan</h3><p>Healthier groups can pay a fixed monthly cost and may get money back in a low-claims year. <a href="/level-funded-health-insurance-florida">How level funding works</a>.</p></div>
      <div class="rr-lever"><h3>3. Switch to an ICHRA</h3><p>You set a fixed monthly allowance and employees buy their own plan. Your cost stops moving with the group's renewal. <a href="/ichra-florida-small-business">ICHRA for small businesses</a>.</p></div>
      <div class="rr-lever"><h3>4. Change the plan design</h3><p>A higher deductible, an HSA-eligible plan, or a narrower network can cut premiums while keeping the doctors your team uses.</p></div>
      <div class="rr-lever"><h3>5. Rework your contribution</h3><p>Pay a fixed share of a base plan and let employees buy up. You keep the benefit while capping what you spend.</p></div>
      <div class="rr-lever"><h3>6. Claim the small business tax credit</h3><p>Employers with fewer than 25 lower-wage employees may qualify for a federal credit. <a href="/blog/small-business-health-care-tax-credit-2026">Check eligibility</a>.</p></div>
    </div>
  </section>

  <section class="rr-sec">
    <h2>Key dates for a January 1 renewal</h2>
    <div class="rr-tw"><table class="rr-t">
      <thead><tr><th>When</th><th>What happens</th><th>What to do</th></tr></thead>
      <tbody>
        <tr><td>October &ndash; November</td><td>Most carriers send January 1 renewal letters 30 to 60 days ahead.</td><td>Send us the renewal as soon as it arrives. More time means more options.</td></tr>
        <tr><td>November 1</td><td>Individual open enrollment opens on HealthCare.gov.</td><td>Matters if you are weighing an ICHRA, since employees then buy individual plans.</td></tr>
        <tr><td>November 15 &ndash; December 15</td><td>Federal small-group window: carriers must accept groups that can't meet participation or contribution minimums.</td><td>Groups with low enrollment or a small employer contribution should apply in this window.</td></tr>
        <tr><td>Early to mid December</td><td>Carriers typically want new-group applications one to three weeks before the effective date.</td><td>Have your decision made and the census in by early December.</td></tr>
        <tr><td>January 1, 2027</td><td>New or renewed coverage starts.</td><td>We confirm ID cards and enrollment for every employee.</td></tr>
      </tbody>
    </table></div>
  </section>

  <section class="rr-sec">
    <h2>Renewal reviews by industry</h2>
    <p>Industries with high turnover, field crews or drivers spread across states have their own renewal problems. Start with yours:</p>
    <div class="rr-ind">
      <a href="/health-insurance-for-trucking-companies">Trucking companies</a>
      <a href="/group-health-insurance-for-delivery-fleets">Delivery fleets</a>
      <a href="/health-insurance-for-construction-companies">Construction</a>
      <a href="/health-insurance-for-contractors">Contractors</a>
      <a href="/health-insurance-for-restaurants">Restaurants</a>
      <a href="/health-insurance-for-hvac-companies">HVAC</a>
      <a href="/health-insurance-for-auto-repair-shops">Auto repair</a>
      <a href="/health-insurance-for-dental-offices">Dental offices</a>
      <a href="/health-insurance-for-salons-and-spas">Salons &amp; spas</a>
      <a href="/health-insurance-for-retail-businesses">Retail</a>
      <a href="/group-health-insurance-by-industry">All industries</a>
    </div>
  </section>

  <section class="rr-sec rr-faq">
    <h2>Renewal questions</h2>
    {faq_html}
  </section>

  <section class="rr-cta">
    <h2>Don't auto-renew a 15% increase.</h2>
    <p>A review costs nothing and usually takes a day once we have your census.</p>
    <a href="#review">Start my renewal review</a>
    <a href="tel:+19548251009">Call (954) 825-1009</a>
  </section>

  <p class="rr-src">Sources: <a href="https://www.healthcarefinancenews.com/news/small-business-health-insurers-seek-14-premium-increase-2027" rel="noopener" target="_blank">KFF analysis of 2027 small-group rate filings, via Healthcare Finance News (Aug 11, 2026)</a>; <a href="https://acasignups.net/node/9952" rel="noopener" target="_blank">Florida 2027 preliminary rate filings, ACASignups (updated Sept 24, 2026)</a>; small-group participation and contribution window: 45 CFR 147.104(b)(1). Florida figures are proposed rates and unweighted averages; final approved rates may differ. VS Health Benefits is a licensed independent agency and is not affiliated with HealthCare.gov, CMS or any government agency. This page is general information, not tax or legal advice.</p>
</main>"""
sub1(r'<main class="container">.*?</main>', MAIN.replace("\\", "\\\\"))

JS = r"""<script id="rr-js">
(function(){
  var f=document.getElementById('rr-form'); if(!f) return;
  var $=function(id){return document.getElementById(id);};
  var started=false;
  f.addEventListener('focusin',function(){ if(started) return; started=true;
    try{ window.vsTrack && window.vsTrack('quote_start',{type:'business',form:'renewal-review'}); }catch(e){} });
  try{ var q=new URLSearchParams(location.search); if(q.get('inc')){ $('rr-inc').value=q.get('inc'); } }catch(e){}
  function bad(id,on){ var el=$(id); if(el&&el.parentNode) el.parentNode.classList.toggle('err',!!on); }
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var v=function(id){return ($(id).value||'').trim();};
    var phone=v('rr-phone').replace(/\D/g,''); if(phone.length===11&&phone[0]==='1') phone=phone.slice(1);
    var email=v('rr-email'), zip=v('rr-zip');
    var checks=[['rr-first',v('rr-first')],['rr-last',v('rr-last')],['rr-biz',v('rr-biz')],['rr-emp',v('rr-emp')],
      ['rr-zip',/^\d{5}$/.test(zip)],['rr-inc',v('rr-inc')],['rr-date',v('rr-date')],['rr-phone',phone.length===10],
      ['rr-email',/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)]];
    var ok=true; checks.forEach(function(c){ bad(c[0],!c[1]); if(!c[1]) ok=false; });
    var msg=$('rr-msg');
    if(!ok){ msg.textContent='Please fill in the highlighted fields.'; return; }
    if(!$('rr-consent').checked){ msg.textContent='Please check the box so we can contact you about your review.'; return; }
    msg.textContent='';
    var btn=$('rr-submit'); btn.disabled=true; btn.textContent='Sending...';
    var data={type:'business',formName:'Renewal review',ownerFirstName:v('rr-first'),ownerLastName:v('rr-last'),
      businessName:v('rr-biz'),employees:v('rr-emp'),businessZip:zip,contactPhone:phone,contactEmail:email,
      renewalIncrease:v('rr-inc'),renewalDate:v('rr-date'),coverageStart:v('rr-date'),
      currentlyInsured:/No group plan/.test(v('rr-inc'))?'No':'Yes, renewing',
      requestedCoverage:'Group health renewal review',situations:['2027 renewal review'],
      smsConsent:true,consentText:'Renewal review form TCPA consent v2026-10-16',page:location.pathname};
    fetch('/api/business-quote',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return {};});})
      .then(function(j){
        try{ window.vsTrack && window.vsTrack('generate_lead',{lead_type:'business',form:'renewal-review',renewal_increase:data.renewalIncrease}); }catch(e){}
        if(j&&j.censusUrl){ $('rr-census').href=j.censusUrl.replace(/^https?:\/\/[^/]+/,''); }
        f.style.display='none'; $('rr-ok').style.display='block';
        $('review').scrollIntoView({behavior:'smooth',block:'start'});
      })
      .catch(function(){ btn.disabled=false; btn.textContent='Review my renewal →';
        msg.innerHTML='Something went wrong. Please call <a href="tel:+19548251009">(954) 825-1009</a> or try again.'; });
  });
})();
</script>
"""
s = s.replace('  <script src="/vs-attribution.js" defer></script>', JS + '  <script src="/vs-attribution.js" defer></script>', 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT, len(s))
