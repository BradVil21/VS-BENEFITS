# -*- coding: utf-8 -*-
"""Add trade-specific sections to existing industry pages so they match the
"group health insurance for [trade]" queries we already rank 19-41 for,
instead of spinning up new thin pages.

Facts used:
 - ACA small-group (1-50 in FL) premiums may vary ONLY by age, geographic rating
   area, family size, tobacco and plan. Industry/hazard/claims experience rating
   is prohibited. (Unlike workers' comp.)
 - Davis-Bacon: bona fide health contributions count toward the fringe obligation,
   subject to annualization across DBRA and non-DBRA hours.
   Source: DOL WHD Fact Sheet 66E.
"""
import re, json

STYLE_ID='vs-trade-style'
STYLE='''<style id="vs-trade-style">
.vs-trade{padding:44px 0;border-top:1px solid #e4e9f2}
.vs-trade .vs-tr-inner{width:100%;max-width:1160px;margin:0 auto;padding:0 18px}
.vs-trade h2{font-family:'Poppins','Inter',system-ui,sans-serif;color:#0b2346;font-size:1.5rem;margin:0 0 8px;line-height:1.25}
.vs-trade .vs-tr-lede{color:#3d4c5f;font-size:1rem;line-height:1.65;margin:0 0 22px;max-width:760px}
.vs-trade .vs-tr-key{background:#f2f7fd;border:1px solid #d6e6f7;border-left:4px solid #16447f;border-radius:12px;padding:18px 20px;margin:0 0 24px}
.vs-trade .vs-tr-key strong{display:block;color:#0b2346;font-size:1rem;margin-bottom:5px}
.vs-trade .vs-tr-key p{margin:0;color:#3d4c5f;font-size:.95rem;line-height:1.65}
.vs-tr-grid{display:grid;grid-template-columns:1fr;gap:14px;margin-bottom:22px}
.vs-tr-item{background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:18px 20px}
.vs-tr-item h3{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.02rem;line-height:1.35;margin:0 0 7px}
.vs-tr-item p{margin:0;color:#5a6b80;font-size:.92rem;line-height:1.6}
.vs-tr-cta{display:inline-block;background:#16447f;color:#fff;font-weight:700;font-size:.95rem;padding:13px 26px;border-radius:999px;text-decoration:none}
.vs-tr-cta:hover{background:#0e3266;text-decoration:none;color:#fff}
@media(min-width:760px){.vs-tr-grid{grid-template-columns:1fr 1fr}}
</style>'''

RATING_NOTE = ('<div class="vs-tr-key"><strong>Your trade does not raise your health premium.</strong>'
 '<p>This surprises most owners in a high-hazard trade. Workers&rsquo; compensation is priced on your '
 'class code and claims history. Small-group health insurance is not. Under the ACA, a plan for a group '
 'of 1 to 50 in Florida can only be priced on five things: employee age, the geographic rating area, '
 'family size, tobacco use, and the plan you pick. Industry, injury rate and prior claims are not '
 'permitted rating factors. A roofing crew and an accounting office of the same ages in the same county '
 'pay the same rate for the same plan.</p></div>')

DAVIS_BACON = ('<div class="vs-tr-key"><strong>On public work, benefits can offset your fringe obligation.</strong>'
 '<p>If you bid federally funded jobs, Davis-Bacon requires a prevailing wage plus a fringe rate. Bona fide '
 'health insurance contributions count toward that fringe obligation rather than being paid out as cash. '
 'The catch is annualization: your credit is based on the effective annual rate of contributions across '
 '<em>all</em> hours worked, DBRA and non-DBRA alike, so you cannot fund a full year of benefits out of '
 'prevailing-wage hours alone. Worth modelling before you bid, not after. '
 '(<a href="https://www.dol.gov/agencies/whd/fact-sheets/66E-DBRA-compliance-fringe-benefit-requirements" '
 'rel="nofollow noopener" target="_blank">DOL Fact Sheet 66E</a>.)</p></div>')

SECTIONS = {
 'health-insurance-for-construction-companies.html': dict(
   anchor='construction-trades',
   h2='Group Health Insurance by Construction Trade',
   lede=('General contractor, excavation outfit, heavy civil crew &mdash; the plan design is similar, but the '
         'eligibility and compliance problems are not. Here is what changes by trade.'),
   keys=[RATING_NOTE, DAVIS_BACON],
   items=[
    ('Group health insurance for general contractors',
     'Your crew is usually part W-2, part 1099 subs. Only W-2 employees count toward group eligibility and '
     'participation, and only they can be covered on the group plan. Subs buy individually &mdash; we point them '
     'to the marketplace and they still get a premium deduction on net income. Mixing the two up is the single '
     'most common reason a group application gets kicked back.'),
    ('Group health insurance for excavation contractors',
     'Excavation runs seasonal headcount and a high workers&rsquo; comp mod, which leads a lot of owners to assume '
     'health coverage is priced out of reach. It is not, for the reason above. What actually matters is how you '
     'define eligibility so your headcount swings do not break participation minimums mid-year.'),
    ('Group health insurance for bridge construction contractors',
     'Heavy civil and bridge work is disproportionately public work, which puts you under prevailing wage. That '
     'makes the fringe credit the central design question: structure contributions right and benefits cost you '
     'materially less than paying the fringe in cash.'),
    ('Group health insurance for tunneling contractors',
     'Long-duration jobs, travelling crews and prevailing wage together. Crews working away from home need a plan '
     'with a genuine national network, not a county HMO &mdash; the same problem long-haul carriers have.'),
    ('Mixed W-2 and 1099 crews',
     'You can run a group plan for W-2 staff and separately help 1099 subs onto individual coverage. Some '
     'contractors use an ICHRA to reimburse individual premiums tax-free instead of running a group plan at all.'),
    ('Seasonal and project-based headcount',
     'Waiting periods of up to 90 days, and a measurement period for variable-hour employees, let you staff up '
     'for a job without every short-term hire triggering coverage.'),
   ]),

 'health-insurance-for-cleaning-companies.html': dict(
   anchor='cleaning-trades',
   h2='Group Health Insurance for Janitorial and Cleaning Contractors',
   lede=('Cleaning is the hardest small-group case in the trades: high turnover, part-time hours and thin margins '
         'on contract bids. It is still very doable &mdash; the design just has to account for all three.'),
   keys=[],
   items=[
    ('Group health insurance for janitorial companies',
     'Turnover is the problem, not price. A 90-day waiting period plus a measurement period for variable-hour '
     'staff means you are not enrolling and terminating people every month, which is what makes janitorial '
     'groups expensive to administer.'),
    ('Group health insurance for industrial cleaning contractors',
     'Industrial and post-construction cleaning crews are usually variable-hour and often work across several '
     'counties. Employee ZIP drives the rating area, so a crew spread across Miami-Dade and Broward can price '
     'differently than you expect. We model it before you commit.'),
    ('Building services and facilities contractors',
     'If you bid facility contracts, benefits are increasingly a scoring criterion, not just a cost. Showing a '
     'real benefits package can be the difference on a bid against a low-cost competitor.'),
    ('Part-time and variable-hour crews',
     'Employees averaging under 30 hours generally do not have to be offered coverage. The ACA lookback lets you '
     'measure over a period rather than guessing month to month.'),
   ]),

 'health-insurance-for-retail-businesses.html': dict(
   anchor='retail-trades',
   h2='Group Health Insurance for Retail Stores and Multi-Location Chains',
   lede=('One store and six stores are different problems. Participation, rating areas and seasonal staffing all '
         'behave differently once you have more than one location.'),
   keys=[],
   items=[
    ('Group health insurance for retail stores',
     'A single store with a handful of full-time staff is a straightforward small-group case. The decision is '
     'usually how much you contribute &mdash; carriers typically want at least 50% of the employee-only premium.'),
    ('Group health insurance for multi-location retailers',
     'Premiums are set by each employee&rsquo;s home ZIP, so the same plan costs different amounts across your '
     'locations. Participation is measured across the whole group, not per store, which usually works in your '
     'favour: a strong-participation flagship can carry a weaker location.'),
    ('Retail chains and franchise groups',
     'Common ownership across entities can make you a single employer for ACA purposes even when each store is '
     'its own LLC. Worth confirming before you assume you are under the 50 full-time-equivalent threshold.'),
    ('Seasonal and holiday staff',
     'Genuine seasonal workers can be excluded from the full-time count under the seasonal worker exception. '
     'Getting the definition right matters if your headcount doubles in Q4.'),
   ]),

 'health-insurance-for-trucking-companies.html': dict(
   anchor='carrier-types',
   h2='Group Health Insurance by Carrier Type',
   lede=('What changes between fleets is not the plan type &mdash; it is the network. A driver 1,400 miles from '
         'home needs coverage that works where the truck is.'),
   keys=[],
   items=[
    ('Group health insurance for refrigerated trucking companies',
     'Reefer runs are long-haul and often cross a dozen states. A regional HMO is close to useless for a driver '
     'in the middle of one; you want a genuine national PPO network. This is the single most important design '
     'decision for a reefer fleet, ahead of price.'),
    ('Group health insurance for trucking companies and fleets',
     'Flatbed, dump, oilfield and drayage each run different route profiles. Short-haul and drayage fleets whose '
     'drivers sleep at home can use a regional network and save real money; long-haul cannot.'),
    ('Owner-operators and leased drivers',
     'Leased owner-operators are 1099 and cannot go on your group plan. Many carriers use an ICHRA to reimburse '
     'their individual premiums tax-free instead, which is a legitimate way to offer something without '
     'reclassifying anyone.'),
    ('Driver retention',
     'Benefits are consistently one of the top reasons drivers stay or leave. For a small fleet, the cost of '
     'covering a driver is usually far less than the cost of recruiting and onboarding a replacement.'),
   ]),
}

def build(cfg, page_slug):
    items=''.join('\n        <div class="vs-tr-item"><h3>%s</h3><p>%s</p></div>'%(t,b) for t,b in cfg['items'])
    keys=''.join('\n      '+k for k in cfg['keys'])
    return ('<section class="vs-trade" id="%s">\n  <div class="vs-tr-inner">\n'
            '    <h2>%s</h2>\n    <p class="vs-tr-lede">%s</p>%s\n'
            '    <div class="vs-tr-grid">%s\n    </div>\n'
            '    <p style="margin:0"><a class="vs-tr-cta" href="/quote?type=business">'
            'Get group quotes for your crew &rarr;</a></p>\n'
            '  </div>\n</section>\n\n'
            % (cfg['anchor'], cfg['h2'], cfg['lede'], keys, items))

n=0
for f,cfg in SECTIONS.items():
    s=open(f,encoding='utf-8').read(); o=s
    s=re.sub(r'<section class="vs-trade" id="%s">.*?</section>\s*'%cfg['anchor'],'',s,flags=re.S)
    if STYLE_ID not in s:
        s=s.replace('</head>', STYLE+'\n</head>',1)
    i=s.rfind('<footer')
    if i<0: i=s.rfind('</body>')
    s=s[:i]+build(cfg,f)+s[i:]
    if s!=o: open(f,'w',encoding='utf-8').write(s); n+=1; print('  +',f,'(%d items)'%len(cfg['items']))
print('trade sections added:',n)
