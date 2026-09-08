# -*- coding: utf-8 -*-
"""/truck-driver-health-insurance-cost-calculator

Targets "truck driver health insurance cost" (pos 21), "owner operator health
insurance cost" (pos 13) and "how much does owner operator insurance cost" -
all of which had impressions and no clicks.

The differentiator over the generic subsidy calculator is that an
owner-operator's MAGI is a number they partly control. Settlement gross is not
what the Marketplace looks at; net after Schedule C deductions is. The
calculator makes that lever visible, which is the single most valuable thing a
broker can show a 1099 driver, and it is why this page should convert.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_lib as P

SLUG = "truck-driver-health-insurance-cost-calculator"
TITLE = "Truck Driver Health Insurance Cost Calculator (2027)"
DESC  = ("See what health insurance actually costs an owner-operator or company driver in 2027 "
         "after ACA credits, and how Schedule C deductions change the number. Free, no login.")
KEYS  = ("truck driver health insurance cost calculator, owner operator health insurance cost, "
         "how much does owner operator health insurance cost, truck driver health insurance cost, "
         "1099 truck driver health insurance cost, owner operator medical insurance cost")

FAQ = [
 ("How much does health insurance cost for an owner-operator?",
  "There is no single number, because the premium depends on your age, your ZIP code, how many "
  "people are on the plan and - the part most drivers miss - your net self-employment income "
  "after Schedule C deductions. A 45-year-old owner-operator netting $58,000 will usually see a "
  "very different figure from one netting $105,000, because the second is over the 400% federal "
  "poverty level cliff and gets no premium tax credit at all. The calculator on this page "
  "estimates both the full premium and what you would pay after credits."),
 ("Does the Marketplace look at my gross settlements or my net?",
  "Net. The figure that drives your subsidy is modified adjusted gross income, which for an "
  "owner-operator starts from Schedule C profit - gross settlements minus fuel, maintenance, "
  "insurance, tolls, depreciation, the per-diem meal allowance you are entitled to and your other "
  "legitimate business expenses. Drivers who report their settlement gross when they apply almost "
  "always overstate their income and quote themselves out of a credit they qualify for."),
 ("What is the 400% subsidy cliff and why does it matter so much in 2027?",
  "The enhanced ACA subsidies expired at the end of 2025. That restored a hard cutoff: at one "
  "dollar over 400% of the federal poverty level, the premium tax credit goes to zero rather than "
  "phasing out. For a single driver that line is roughly $62,600 of MAGI, and for a family of four "
  "roughly $128,600. Crossing it can cost several hundred dollars a month, which is why an accurate "
  "deduction picture is worth real money to a 1099 driver."),
 ("Can I deduct my health insurance premiums as an owner-operator?",
  "If you are self-employed, show a profit, and are not eligible for a subsidized plan through a "
  "spouse's employer, the self-employed health insurance deduction lets you deduct premiums for "
  "yourself, your spouse and your dependents. It is an above-the-line deduction, so you get it "
  "whether or not you itemise. It reduces income tax but not self-employment tax, and it interacts "
  "with the premium tax credit - worth having your tax preparer and your broker in the same "
  "conversation once, rather than guessing."),
 ("Is the estimate on this page a quote?",
  "No. It is an estimate built from the published 2027 premium tax credit formula and standard "
  "age rating, and it is deliberately conservative. Actual premiums vary by county and carrier. "
  "A licensed advisor can pull the real plans available at your ZIP code at no cost to you - "
  "carriers pay our commission, so comparing costs you nothing either way."),
 ("Do company drivers need this calculator?",
  "Sometimes. If your carrier offers a plan, compare its employee cost against what you see here "
  "before assuming the company plan wins. Many small carriers offer a plan with a high deductible "
  "and a narrow regional network, which is a poor fit for a driver running 48 states. If your "
  "carrier offers nothing, an ACA plan is your route and this estimate applies to you directly."),
]

CALC_CSS = """<style id="vs-calc-css">
.tc-wrap{max-width:760px;margin:0 auto}
.tc-card{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);padding:26px 22px}
.tc-prog{display:flex;align-items:center;gap:12px;margin-bottom:20px}
.tc-track{flex:1;height:7px;background:var(--blue-100);border-radius:999px;overflow:hidden}
.tc-fill{height:100%;width:20%;background:linear-gradient(90deg,var(--blue-600),var(--teal));border-radius:999px;transition:width .3s}
.tc-meta{font-size:.8rem;font-weight:700;color:var(--muted);white-space:nowrap}
.tc-panel{display:none}.tc-panel.active{display:block}
.tc-panel h3{margin-bottom:6px;font-size:1.18rem}
.tc-hint{font-size:.88rem;color:var(--muted);margin-bottom:16px}
.tc-field{margin-bottom:14px}
.tc-field label{display:block;font-weight:700;font-size:.9rem;margin-bottom:6px;color:var(--blue-900)}
.tc-field input,.tc-field select{width:100%;min-height:48px;padding:12px 14px;border:1.5px solid var(--line);border-radius:11px;font-size:1rem;font-family:inherit;color:var(--ink);background:#fff}
.tc-field input:focus,.tc-field select:focus{outline:none;border-color:var(--blue-500);box-shadow:0 0 0 3px rgba(47,125,224,.14)}
.tc-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:9px}
.tc-tile{border:1.5px solid var(--line);border-radius:12px;padding:13px 8px;text-align:center;cursor:pointer;font-weight:700;font-size:.92rem;background:#fff;transition:border-color .18s,background .18s;min-height:48px;display:flex;flex-direction:column;justify-content:center;gap:2px}
.tc-tile small{display:block;font-weight:500;font-size:.74rem;color:var(--muted)}
.tc-tile:hover{border-color:var(--blue-500)}
.tc-tile.sel{border-color:var(--blue-700);background:var(--blue-50);color:var(--blue-900)}
.tc-tile.sel small{color:var(--blue-700)}
.tc-row{display:flex;gap:10px;flex-wrap:wrap}.tc-row>*{flex:1;min-width:130px}
.tc-nav{display:flex;gap:10px;margin-top:18px}
.tc-err{color:#b91c1c;font-size:.88rem;font-weight:600;margin-top:10px;min-height:1.2em}
.tc-res{display:none;margin-top:26px}
.tc-res.show{display:block}
.tc-headline{background:linear-gradient(135deg,var(--blue-800),var(--blue-600));color:#fff;border-radius:16px;padding:26px 22px;text-align:center;margin-bottom:16px}
.tc-headline .big{font-family:'Poppins',sans-serif;font-size:clamp(2.1rem,9vw,3rem);font-weight:800;line-height:1.05;margin:6px 0}
.tc-headline .sub{color:rgba(255,255,255,.9);font-size:.92rem}
.tc-tiers{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:16px}
@media(min-width:560px){.tc-tiers{grid-template-columns:repeat(3,1fr)}}
.tc-tier{border:1px solid var(--line);border-radius:14px;padding:16px;text-align:center;background:#fff}
.tc-tier .nm{font-size:.76rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;color:var(--muted)}
.tc-tier .amt{font-family:'Poppins',sans-serif;font-size:1.5rem;font-weight:700;color:var(--blue-700);margin:4px 0 2px}
.tc-tier .per{font-size:.76rem;color:var(--muted)}
.tc-tier.best{border-color:var(--teal);box-shadow:0 0 0 2px rgba(13,181,166,.16)}
.tc-lever{background:var(--blue-50);border:1px solid var(--blue-100);border-radius:14px;padding:18px;margin-bottom:16px}
.tc-lever h4{margin-bottom:8px;font-size:1rem}
.tc-lever table{width:100%;border-collapse:collapse;font-size:.9rem;margin-top:10px}
.tc-lever th{text-align:left;font-size:.76rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding:6px 8px;border-bottom:1px solid var(--blue-100)}
.tc-lever td{padding:8px;border-bottom:1px solid rgba(30,90,176,.10);color:var(--ink-2)}
.tc-lever tr:last-child td{border-bottom:0}
.tc-lever td.hi{font-weight:700;color:var(--blue-800)}
.tc-lever tr.you td{background:rgba(13,181,166,.10)}
.tc-note{background:#fff7ed;border:1px solid #fed7aa;border-radius:12px;padding:14px 16px;font-size:.9rem;color:#7c2d12;margin-bottom:14px}
.tc-ok{background:#ecfdf5;border:1px solid #a7f3d0;border-radius:12px;padding:14px 16px;font-size:.92rem;color:#065f46;margin-top:12px}
.tc-disc{font-size:.8rem;color:var(--muted);line-height:1.55;margin-top:14px}
</style>"""

def hero():
    return """
<section class="hero">
  <div class="container">
    <div style="max-width:760px">
      <span class="eyebrow">Free &middot; No login &middot; 60 seconds</span>
      <h1>Truck Driver Health Insurance <span>Cost Calculator</span></h1>
      <p class="hero-sub">Health insurance for truck drivers is priced on your age, your ZIP code and your
      <strong>net</strong> self-employment income &mdash; not your settlement gross. This calculator estimates what an
      owner-operator or company driver actually pays for 2027 coverage after the premium tax credit, and shows you
      how your Schedule C deductions move that number.</p>
      <div class="hero-meta">
        <span><span class="dot"></span>Built on the published 2027 credit formula</span>
        <span><span class="dot"></span>Licensed advisor, 40+ states</span>
        <span><span class="dot"></span>Carriers pay our commission</span>
      </div>
    </div>
  </div>
</section>"""

def calculator():
    return """
<section class="section bg-soft">
  <div class="container tc-wrap">
    <div class="tc-card">
      <div class="tc-prog">
        <div class="tc-track"><div class="tc-fill" id="tc-fill"></div></div>
        <span class="tc-meta"><span id="tc-step">Step 1 of 5</span> &middot; <span id="tc-pct">20%</span></span>
      </div>

      <div class="tc-panel active" id="tc-p1">
        <h3>Where do you domicile?</h3>
        <p class="tc-hint">Plans and pricing are set by county, so we need the ZIP on your driver's license &mdash; not wherever the truck is tonight.</p>
        <div class="tc-field"><label for="tc-zip">Home ZIP code</label>
          <input id="tc-zip" type="text" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="33101" /></div>
      </div>

      <div class="tc-panel" id="tc-p2">
        <h3>Where should the advisor reach you?</h3>
        <p class="tc-hint">We do not sell your number and we do not robocall it. One licensed advisor, one call, at a time that works around your hours.</p>
        <div class="tc-field"><label for="tc-phone">Mobile number</label>
          <input id="tc-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(954) 825-1009" /></div>
      </div>

      <div class="tc-panel" id="tc-p3">
        <h3>Who is going on the plan?</h3>
        <div class="tc-field"><label for="tc-age">Your age</label>
          <input id="tc-age" type="number" inputmode="numeric" min="18" max="64" placeholder="45" /></div>
        <div class="tc-row">
          <div class="tc-field"><label for="tc-age2">Spouse age <small style="font-weight:400;color:var(--muted)">(optional)</small></label>
            <input id="tc-age2" type="number" inputmode="numeric" min="18" max="64" placeholder="&mdash;" /></div>
          <div class="tc-field"><label for="tc-kids">Children under 21</label>
            <select id="tc-kids"><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3 or more</option></select></div>
        </div>
      </div>

      <div class="tc-panel" id="tc-p4">
        <h3>How do you get paid?</h3>
        <div class="tc-field"><label>Driver type</label>
          <div class="tc-tiles" id="tc-type">
            <div class="tc-tile sel" data-val="oo">Owner-operator<small>1099 / own authority</small></div>
            <div class="tc-tile" data-val="lease">Lease operator<small>1099, leased on</small></div>
            <div class="tc-tile" data-val="w2">Company driver<small>W-2</small></div>
          </div></div>
        <div id="tc-1099-block">
          <div class="tc-field"><label for="tc-gross">Annual gross settlements</label>
            <input id="tc-gross" type="text" inputmode="numeric" placeholder="185,000" /></div>
          <div class="tc-field"><label for="tc-ded">Annual business deductions <small style="font-weight:400;color:var(--muted)">(fuel, maintenance, insurance, tolls, depreciation, per diem)</small></label>
            <input id="tc-ded" type="text" inputmode="numeric" placeholder="120,000" />
            <p class="tc-hint" style="margin:8px 0 0">Not sure? Most long-haul owner-operators run 60&ndash;70% of gross in expenses. Leave it blank and we will assume 65%.</p></div>
        </div>
        <div id="tc-w2-block" hidden>
          <div class="tc-field"><label for="tc-w2inc">Annual household income (W-2 wages, before tax)</label>
            <input id="tc-w2inc" type="text" inputmode="numeric" placeholder="72,000" /></div>
        </div>
      </div>

      <div class="tc-panel" id="tc-p5">
        <h3>Last step &mdash; who is this for?</h3>
        <p class="tc-hint">So the advisor knows who they are calling, and so we can email you the numbers.</p>
        <div class="tc-row">
          <div class="tc-field"><label for="tc-first">First name</label><input id="tc-first" type="text" autocomplete="given-name" /></div>
          <div class="tc-field"><label for="tc-last">Last name</label><input id="tc-last" type="text" autocomplete="family-name" /></div>
        </div>
        <div class="tc-field"><label for="tc-email">Email <small style="font-weight:400;color:var(--muted)">(optional)</small></label>
          <input id="tc-email" type="email" autocomplete="email" /></div>
      </div>

      <div class="tc-err" id="tc-error" role="alert" aria-live="polite"></div>
      <div class="tc-nav">
        <button type="button" class="btn btn-secondary" id="tc-back" hidden>Back</button>
        <button type="button" class="btn btn-primary full-w" id="tc-next">Continue</button>
        <button type="button" class="btn btn-primary full-w" id="tc-go" hidden>Show my estimate</button>
      </div>
      <p id="tc-success" class="tc-ok" hidden></p>
    </div>

    <div class="tc-res" id="tc-res">
      <div class="tc-headline">
        <div class="sub">Estimated premium tax credit</div>
        <div class="big" id="tc-subsidy">$0</div>
        <div class="sub" id="tc-fplline">&mdash;</div>
      </div>
      <div class="tc-tiers">
        <div class="tc-tier"><div class="nm">Bronze</div><div class="amt" id="tc-bronze">&mdash;</div><div class="per">per month, after credit</div></div>
        <div class="tc-tier best"><div class="nm">Silver</div><div class="amt" id="tc-silver">&mdash;</div><div class="per">per month, after credit</div></div>
        <div class="tc-tier"><div class="nm">Gold</div><div class="amt" id="tc-gold">&mdash;</div><div class="per">per month, after credit</div></div>
      </div>
      <div id="tc-cliffnote"></div>
      <div class="tc-lever" id="tc-lever">
        <h4>What your deductions are worth</h4>
        <p style="font-size:.9rem;margin:0;color:var(--ink-2)">The Marketplace prices you on net income, so every legitimate Schedule C
        deduction is doing two jobs: cutting your tax bill and moving you down this table. Your row is highlighted.</p>
        <table id="tc-levertbl"></table>
      </div>
      <div class="cta-strip" style="margin-top:18px">
        <h2 style="font-size:1.35rem">Want the real plans, not an estimate?</h2>
        <p>A licensed VS Health Benefits advisor will pull the actual 2027 plans available at your ZIP code, check the
        network against the lanes you run, and send you a side-by-side. Carriers pay our commission, so it costs you nothing.</p>
        <a class="btn" href="/quote?type=individual" style="background:#fff;color:var(--blue-700)">Get my plan comparison</a>
      </div>
      <p class="tc-disc" id="tc-disc"></p>
    </div>
  </div>
</section>"""

def body_copy():
    return """
<section class="section">
  <div class="container" style="max-width:820px">
    <h2>What decides an owner-operator's premium</h2>
    <p>Four things, and only one of them is about the truck.</p>
    <ul class="check-list">
      <li><strong>Your age.</strong> ACA plans are age-rated on a fixed federal curve. A 60-year-old pays almost exactly three times what a 21-year-old pays for the same plan. Nothing you do changes this one.</li>
      <li><strong>Your ZIP code.</strong> Rates are set per rating area, and neighbouring counties can differ by 20&ndash;30% for the same carrier. Your domicile ZIP is what counts, not where you happen to be parked.</li>
      <li><strong>Who is on the plan.</strong> Spouse and children each add premium, though children under 21 are rated well below an adult and only your first three are charged.</li>
      <li><strong>Your net self-employment income.</strong> This is the lever. It sets your premium tax credit, and for a 1099 driver it is the number most within your control.</li>
    </ul>

    <h2>Why settlement gross is the wrong number</h2>
    <p>The single most expensive mistake we see owner-operators make on a Marketplace application is entering their
    settlement gross. A driver grossing $190,000 who runs $125,000 in fuel, maintenance, insurance, tolls, depreciation
    and per diem does not have $190,000 of income in the eyes of the Marketplace. He has roughly $65,000 of Schedule C
    profit, and that is what modified adjusted gross income is built from.</p>
    <p>Entered as $190,000 he is far over the cliff and told he gets nothing. Entered correctly he is inside the credit
    range. Same driver, same truck, same year &mdash; and for a driver covering a family, commonly several hundred dollars
    a month apart, purely on which line he read off his settlement statement.</p>

    <h2>The 400% cliff is back, and it is a cliff</h2>
    <p>The enhanced subsidies that ran from 2021 through 2025 expired at the end of 2025. For 2026 and 2027 the original
    ACA rule is back: the premium tax credit ends abruptly at 400% of the federal poverty level rather than tapering.
    A single driver one dollar over roughly $62,600 of MAGI gets no credit at all, where a driver a dollar under gets a
    substantial one.</p>
    <p>How much that cliff is worth depends on your household. A single driver a little over the line may find the gap
    manageable; an owner-operator covering a spouse and children is usually looking at a materially larger number, because
    the credit is calculated against the cost of covering everyone. Either way it makes year-end planning worth doing: a
    deferred repair, equipment bought in December rather than January, or a per-diem allowance actually claimed can each be
    the difference between a credit and none. That is a conversation to have with your tax preparer before 31 December,
    not in April.</p>

    <h2>What about company drivers?</h2>
    <p>If your carrier offers a plan, compare it honestly rather than assuming it wins. Two things to check: what the
    plan costs you per week out of settlement, and whether the network actually covers the states you run. A regional
    HMO is cheap on paper and close to useless for a driver who is out three weeks at a time. If your carrier offers
    nothing &mdash; which is still common at small fleets &mdash; the Marketplace is your route and the estimate above applies
    to you directly. Our guide to
    <a href="/blog/company-truck-driver-health-insurance">company driver coverage when the carrier offers nothing</a>
    walks through it.</p>

    <h2>The deduction most owner-operators leave on the table</h2>
    <p>If you are self-employed, show a profit for the year, and are not eligible for subsidized coverage through a
    spouse's employer, the self-employed health insurance deduction lets you deduct premiums for yourself, your spouse
    and your dependents above the line &mdash; whether or not you itemise. It reduces income tax but not self-employment tax,
    and it interacts with the premium tax credit in a way that is worth getting right once.
    <a href="/blog/can-owner-operators-deduct-health-insurance">The full rules are here</a>.</p>
  </div>
</section>

<section class="section bg-soft">
  <div class="container" style="max-width:820px">
    <h2 class="center">Truck Driver Health Insurance Cost FAQ</h2>
    <div style="height:18px"></div>
    """ + P.faq_html(FAQ) + """
  </div>
</section>"""

RELATED = """
<section class="vs-related-guides" data-block="vs-trucking-calc">
  <div class="vs-rg-inner">
    <h2>Next steps for drivers</h2>
    <p class="vs-rg-sub">The estimate is the starting point. These are the decisions that come after it.
    Ready for real numbers? <a href="/quote" style="color:#16447f;font-weight:700">Get my quote &rarr;</a></p>
    <div class="vs-rg-grid">
      <a class="vs-rg-card" href="/best-health-insurance-owner-operators">
        <strong>Best Health Insurance for Owner-Operators</strong>
        <span>The four real options compared on price, network reach and deductibility.</span>
        <em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/truck-driver-health-insurance-cost">
        <strong>What Drivers Actually Pay</strong>
        <span>Cost ranges by age and household, and the four things that move the number.</span>
        <em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/ooida-health-insurance-vs-aca">
        <strong>OOIDA vs the Marketplace</strong>
        <span>What the association actually covers, and where a Marketplace plan wins.</span>
        <em>Compare them &rarr;</em></a>
      <a class="vs-rg-card" href="/truck-driver-open-enrollment-2027">
        <strong>Open Enrollment 2027 for Drivers</strong>
        <span>Nov 1 to Jan 15. Deadlines, and how to enroll from the road.</span>
        <em>See the dates &rarr;</em></a>
    </div>
  </div>
</section>"""

CALC_JS = """<script>
/* Truck driver cost calculator.
   Shares the subsidy engine with /aca-subsidy-calculator so the two pages can
   never disagree: 2026/2027 FPL, the post-enhanced-credit applicable-percentage
   table, and the federal age curve. What is new here is the 1099 path - gross
   settlements minus Schedule C deductions - and the lever table, which is the
   reason a driver has any reason to use this page over the generic one. */
(function(){
  "use strict";
  var FPL_BASE=15650, FPL_ADD=5500, BASE21=375, DEFAULT_EXPENSE_RATIO=0.65;
  function fpl(n){return FPL_BASE+(n-1)*FPL_ADD;}
  function lerp(x,x0,x1,y0,y1){return y0+(y1-y0)*(x-x0)/(x1-x0);}
  /* IRS Rev. Proc. 2025-25 sliding scale. null above 400% FPL = the cliff. */
  function applicablePct(p){if(p<133)return 2.10;if(p<150)return lerp(p,133,150,3.14,4.19);if(p<200)return lerp(p,150,200,4.19,6.60);if(p<250)return lerp(p,200,250,6.60,8.44);if(p<300)return lerp(p,250,300,8.44,9.96);if(p<=400)return 9.96;return null;}
  function ageFactor(a){if(a<21)return 0.765;if(a>=64)return 3.0;var p=[[21,1.0],[25,1.004],[30,1.135],[35,1.222],[40,1.278],[45,1.444],[50,1.786],[55,2.230],[60,2.714],[64,3.0]];for(var i=0;i<p.length-1;i++){if(a>=p[i][0]&&a<p[i+1][0])return lerp(a,p[i][0],p[i+1][0],p[i][1],p[i+1][1]);}return 1.0;}
  function prem(a){return BASE21*ageFactor(a);}
  function money(n){return "$"+Math.round(n).toLocaleString();}
  function $(id){return document.getElementById(id);}
  function val(id){var e=$(id);return e?(e.value||"").trim():"";}
  function num(id){return parseFloat(val(id).replace(/[^0-9.]/g,""))||0;}
  function err(m){$("tc-error").textContent=m||"";}
  function focusOn(id){var e=$(id);if(e)try{e.focus({preventScroll:false});}catch(_){e.focus();}}

  var TOTAL=5, step=1, driverType="oo", last={};

  function go(n){
    step=Math.min(Math.max(n,1),TOTAL);
    for(var i=1;i<=TOTAL;i++){var p=$("tc-p"+i);if(p)p.classList.toggle("active",i===step);}
    var pct=Math.round(step/TOTAL*100);
    $("tc-fill").style.width=pct+"%"; $("tc-pct").textContent=pct+"%";
    $("tc-step").textContent="Step "+step+" of "+TOTAL;
    $("tc-back").hidden=step===1; $("tc-next").hidden=step===TOTAL; $("tc-go").hidden=step!==TOTAL;
    err("");
  }
  function phoneDigits(){var d=val("tc-phone").replace(/\\D/g,"");if(d.length===11&&d.charAt(0)==="1")d=d.slice(1);return d;}

  /* MAGI from whichever path the driver is on. */
  function magi(){
    if(driverType==="w2") return num("tc-w2inc");
    var g=num("tc-gross"); if(!g) return 0;
    var d=num("tc-ded");
    if(!d) d=g*DEFAULT_EXPENSE_RATIO;
    return Math.max(0,g-d);
  }
  function household(){
    var n=1; if(parseInt(val("tc-age2"),10)>=18)n++;
    n+=Math.min(parseInt(val("tc-kids"),10)||0,3); return n;
  }
  function benchmark(){
    var a1=Math.min(Math.max(parseInt(val("tc-age"),10)||40,18),64);
    var a2=parseInt(val("tc-age2"),10);
    var kids=Math.min(parseInt(val("tc-kids"),10)||0,3);
    return prem(a1)+((a2>=18)?prem(Math.min(Math.max(a2,18),64)):0)+kids*(BASE21*0.765);
  }
  /* Net cost of the benchmark silver at a given MAGI. Used for both the result
     and every row of the lever table, so they cannot drift apart. */
  function priceAt(income,size,bench){
    var pctFpl=income/fpl(size)*100;
    var appl=applicablePct(pctFpl);
    if(appl===null) return {pctFpl:pctFpl,subsidy:0,silver:bench,cliff:true};
    var expected=(income*(appl/100))/12;
    var subsidy=Math.max(0,bench-expected);
    return {pctFpl:pctFpl,subsidy:subsidy,silver:Math.max(0,bench-subsidy),cliff:false};
  }

  function next(){
    if(step===1){ if(!/^\\d{5}$/.test(val("tc-zip"))){err("Please enter your 5-digit home ZIP code.");focusOn("tc-zip");return;} }
    else if(step===2){ if(phoneDigits().length!==10){err("Please enter a 10-digit mobile number so an advisor can reach you.");focusOn("tc-phone");return;} draft("Step 2 - phone"); }
    else if(step===3){ var a=parseInt(val("tc-age"),10);
      if(!a){err("Please enter your age.");focusOn("tc-age");return;}
      if(a<18||a>64){err("Enter an age between 18 and 64. Under 18 is usually covered as a child and 65+ is Medicare - an advisor can help with either.");focusOn("tc-age");return;} }
    else if(step===4){
      if(driverType==="w2"){ if(!num("tc-w2inc")){err("Please enter your household income.");focusOn("tc-w2inc");return;} }
      else { if(!num("tc-gross")){err("Please enter your annual gross settlements.");focusOn("tc-gross");return;} }
      draft("Step 4 - income"); }
    go(step+1);
  }

  function run(){
    if(!/^\\d{5}$/.test(val("tc-zip"))){go(1);err("Please enter your 5-digit home ZIP code.");focusOn("tc-zip");return;}
    if(phoneDigits().length!==10){go(2);err("Please enter a 10-digit mobile number.");focusOn("tc-phone");return;}
    if(!parseInt(val("tc-age"),10)){go(3);err("Please enter your age.");focusOn("tc-age");return;}
    if(!magi()&&driverType!=="w2"){go(4);err("Please enter your annual gross settlements.");focusOn("tc-gross");return;}
    if(!val("tc-first")){err("Please enter your first name.");focusOn("tc-first");return;}
    if(!val("tc-last")){err("Please enter your last name.");focusOn("tc-last");return;}
    var em=val("tc-email");
    if(em&&!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,}$/.test(em)){err("That email does not look right. Leave it blank if you would rather not share it.");focusOn("tc-email");return;}
    err("");

    var income=magi(), size=household(), bench=benchmark();
    var r=priceAt(income,size,bench);
    var bronze=Math.max(0,bench*0.78-r.subsidy), gold=Math.max(0,bench*1.22-r.subsidy);

    $("tc-subsidy").textContent=money(r.subsidy);
    $("tc-fplline").textContent=Math.round(r.pctFpl)+"% of the federal poverty level"+
      (driverType==="w2"?"":" \\u00b7 net income "+money(income));
    $("tc-bronze").textContent=money(bronze)+"/mo";
    $("tc-silver").textContent=money(r.silver)+"/mo";
    $("tc-gold").textContent=money(gold)+"/mo";

    var note="";
    if(r.pctFpl<100){
      note='<div class="tc-note"><strong>Your income may put you in Medicaid range</strong> rather than Marketplace subsidy range, '+
           'depending on your state. In states that did not expand Medicaid there is a coverage gap that catches a lot of drivers '+
           'in a slow year. An advisor can check your state at no cost.</div>';
    } else if(r.cliff){
      note='<div class="tc-note"><strong>You are above 400% of the federal poverty level, so no premium tax credit applies.</strong> '+
           'The enhanced subsidies expired at the end of 2025, so for 2027 this is a hard cliff rather than a taper. '+
           (driverType==="w2"?'':'If your deductions are higher than you entered - or if there is equipment or maintenance you were going to buy anyway - '+
           'look at the table below before year end. ')+
           'A private PPO or a spouse\\u2019s group plan may also beat an unsubsidized Marketplace plan; that is worth a conversation.</div>';
    }
    $("tc-cliffnote").innerHTML=note;

    /* Lever table: what the same driver pays at different net incomes. Only
       meaningful on the 1099 path, so it is hidden for W-2. */
    var lever=$("tc-lever");
    if(driverType==="w2"){ lever.style.display="none"; }
    else {
      lever.style.display="";
      /* Points either side of the driver's own figure, anchored on the cliff.
         The 97% row is the one that matters: the most income you can report and
         still hold the largest credit available to you. Only one row above the
         cliff, because every row above it is the same number. */
      /* Points either side of the driver's own figure, anchored on the cliff.
         The driver's own row uses their exact income, not a rounded one, so the
         table can never disagree with the headline above it. */
      var cliffLine=fpl(size)*4;
      var pts=[0.55,0.75,0.90,0.97].map(function(m){return Math.round(cliffLine*m/1000)*1000;});
      pts.push(Math.round(cliffLine/1000)*1000+1000);            // one row over the cliff
      pts=pts.filter(function(v){return v>0&&Math.abs(v-income)>1500;});  // no near-duplicate of the driver's row
      pts.push(income);
      pts=pts.filter(function(v,i,a){return a.indexOf(v)===i;}).sort(function(a,b){return a-b;});
      if(pts.length>6){
        var keep=pts.indexOf(income);
        pts=pts.filter(function(v,i){return i===keep||i<6;}).slice(0,6);
      }
      var rows='<tr><th>Net income (MAGI)</th><th>Credit / month</th><th>Silver / month</th></tr>';
      pts.forEach(function(v){
        var p=priceAt(v,size,bench);
        var isMine=(v===income);
        var label=money(v)+(isMine?' &larr; you':'');
        /* The row nearest the cliff that still has a credit is the actionable
           one - it is the most income you can report and stay eligible. It is
           not the biggest credit, so it must not be labelled as one. */
        if(!p.cliff&&p.subsidy>0&&v>cliffLine*0.94)
          label+=' <small style="color:#065f46;font-weight:700">last row still eligible</small>';
        rows+='<tr'+(isMine?' class="you"':'')+'><td class="hi">'+label+'</td><td>'+
              (p.cliff?'<span style="color:#b91c1c;font-weight:700">none &mdash; over the cliff</span>':money(p.subsidy))+
              '</td><td>'+money(p.silver)+'</td></tr>';
      });
      $("tc-levertbl").innerHTML=rows;
    }

    $("tc-disc").innerHTML="Estimate only, not a quote or an offer of coverage. Built from the 2027 premium tax credit formula "+
      "(IRS Rev. Proc. 2025-25) and the federal age-rating curve, using a national benchmark premium. Actual premiums are set by "+
      "county and carrier and will differ. Household of "+size+", benchmark "+money(bench)+"/mo before credits. "+
      "VS Health Benefits is a licensed insurance brokerage; we do not provide tax advice.";

    $("tc-res").classList.add("show");
    last={income:income,size:size,subsidy:r.subsidy,silver:r.silver,bronze:bronze,gold:gold,
          pctFpl:r.pctFpl,cliff:r.cliff,zip:val("tc-zip"),type:driverType,
          gross:num("tc-gross"),ded:num("tc-ded")||Math.round(num("tc-gross")*DEFAULT_EXPENSE_RATIO)};
    send();
    $("tc-res").scrollIntoView({behavior:"smooth",block:"start"});
  }

  var sent={};
  function send(){
    var first=val("tc-first"), digits=phoneDigits();
    var typeName={oo:"Owner-operator (1099)",lease:"Lease operator (1099)",w2:"Company driver (W-2)"}[last.type];
    var summary=typeName+". Est. credit "+money(last.subsidy)+"/mo (Bronze "+money(last.bronze)+", Silver "+
      money(last.silver)+", Gold "+money(last.gold)+"/mo). MAGI "+money(last.income)+", "+Math.round(last.pctFpl)+"% FPL"+
      (last.cliff?" - ABOVE THE 400% CLIFF, no credit":"")+". Household "+last.size+", age "+val("tc-age")+
      (val("tc-age2")?"/"+val("tc-age2"):"")+", ZIP "+last.zip+
      (last.type==="w2"?"":". Gross settlements "+money(last.gross)+", deductions "+money(last.ded)+".");
    var s=$("tc-success");
    if(s){s.hidden=false;s.textContent="Thanks "+first+" \\u2014 a licensed VS Health Benefits advisor will call with the actual plans available in "+last.zip+", at no cost to you.";}
    window.__tcSubmitted=true;
    if(sent[digits])return; sent[digits]=true;
    fetch("/api/lead-sync",{method:"POST",headers:{"Content-Type":"application/json"},keepalive:true,
      body:JSON.stringify({firstName:first,lastName:val("tc-last"),phone:val("tc-phone"),email:val("tc-email"),
        zip:last.zip,state:"",source:"trucker-cost-calculator",
        tags:["trucker-cost-calculator","trucking","website-lead",last.type==="w2"?"company-driver":"owner-operator"],
        notes:summary})}).catch(function(){});
    try{if(window.vsTrack)window.vsTrack("generate_lead",{currency:"USD",value:0,lead_type:"trucker_cost_calculator"});}catch(_){}
    try{if(typeof confetti==="function")confetti({particleCount:90,spread:70,origin:{y:.6},colors:["#1e5ab0","#0db5a6","#16a34a","#2f7de0","#ffc857"]});}catch(_){}
  }

  /* Progressive capture: a phone number typed and abandoned is still a lead. */
  var lastDraft="", lastAt=0;
  function draftPayload(s){
    if(phoneDigits().length!==10)return null;
    var em=val("tc-email"); if(em&&!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,}$/.test(em))em="";
    return {capture:"auto",type:"individual",step:s||("Step "+step),
      source:"Trucker cost calculator (in progress)",
      firstName:val("tc-first"),lastName:val("tc-last"),phone:val("tc-phone"),email:em,zip:val("tc-zip"),
      notes:"Started the truck driver health insurance cost calculator and has not pressed Show My Estimate yet.",
      attribution:(function(){try{return (window.vsAttribution&&window.vsAttribution())||null;}catch(e){return null;}})()};
  }
  function draft(s){
    if(window.__tcSubmitted)return;
    var p=draftPayload(s); if(!p)return;
    var h=JSON.stringify(p), now=Date.now();
    if(h===lastDraft&&now-lastAt<15000)return;
    lastDraft=h; lastAt=now;
    try{fetch("/api/lead-draft",{method:"POST",headers:{"Content-Type":"application/json"},keepalive:true,body:h}).catch(function(){});}catch(e){}
  }
  function beacon(){
    if(window.__tcSubmitted)return;
    var p=draftPayload("Left the page on step "+step); if(!p)return;
    var b=JSON.stringify(p);
    if(b===lastDraft&&Date.now()-lastAt<15000)return;
    lastDraft=b; lastAt=Date.now();
    try{ if(navigator.sendBeacon){navigator.sendBeacon("/api/lead-draft",new Blob([b],{type:"application/json"}));}
      else{fetch("/api/lead-draft",{method:"POST",headers:{"Content-Type":"application/json"},keepalive:true,body:b}).catch(function(){});} }catch(e){}
  }
  window.addEventListener("pagehide",beacon);
  document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden")beacon();});

  /* wiring */
  $("tc-type").addEventListener("click",function(e){
    var t=e.target.closest(".tc-tile"); if(!t)return;
    this.querySelectorAll(".tc-tile").forEach(function(x){x.classList.remove("sel");});
    t.classList.add("sel"); driverType=t.getAttribute("data-val");
    $("tc-1099-block").hidden=(driverType==="w2");
    $("tc-w2-block").hidden=(driverType!=="w2");
    err("");
  });
  ["tc-gross","tc-ded","tc-w2inc"].forEach(function(id){
    var e=$(id); if(!e)return;
    e.addEventListener("input",function(){var v=this.value.replace(/[^0-9]/g,"");this.value=v?parseInt(v,10).toLocaleString():"";});
  });
  $("tc-zip").addEventListener("input",function(){this.value=this.value.replace(/\\D/g,"").slice(0,5);});
  $("tc-next").addEventListener("click",next);
  $("tc-back").addEventListener("click",function(){go(step-1);});
  $("tc-go").addEventListener("click",run);
  ["tc-zip","tc-phone","tc-age","tc-gross","tc-w2inc"].forEach(function(id){
    var e=$(id); if(e)e.addEventListener("keydown",function(ev){if(ev.key==="Enter"){ev.preventDefault();step===TOTAL?run():next();}});
  });
  go(1);
})();
</script>"""

def main():
    ch = P.Chrome()
    schemas = [
        P.faq_schema(FAQ),
        P.breadcrumbs([("Home","/"),("Truck Driver Health Insurance","/truck-driver-health-insurance"),
                       ("Cost Calculator","/"+SLUG)]),
        {"@context":"https://schema.org","@type":"WebApplication",
         "name":"Truck Driver Health Insurance Cost Calculator",
         "applicationCategory":"FinanceApplication","operatingSystem":"Any",
         "url":P.SITE+"/"+SLUG,
         "description":"Estimates 2027 health insurance premiums and premium tax credits for owner-operators, "
                       "lease operators and company drivers, including the effect of Schedule C deductions on MAGI.",
         "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
         "provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":P.SITE+"/"}},
    ]
    main_html = "<main>" + hero() + calculator() + body_copy() + "</main>"
    html = ch.page(SLUG, TITLE, DESC, KEYS, main_html, schemas,
                   related_block=RELATED, body_extra=CALC_JS)
    # calculator CSS belongs in the head, after the chrome styles
    html = html.replace("</head>", CALC_CSS + "\n</head>", 1)
    p = P.write(SLUG, html)
    print("wrote", p, len(html), "bytes")

if __name__ == "__main__":
    main()
