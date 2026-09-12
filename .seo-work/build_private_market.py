# -*- coding: utf-8 -*-
"""/private-health-insurance - the private (non-Marketplace) market.

House rule: the plans are medically underwritten, so every claim here is about
product-category behaviour, not about any specific carrier or policy. No
premium figures. The subsidy-cliff numbers match /blog/aca-open-enrollment-2027-guide
and /aca-subsidy-calculator so the site cannot disagree with itself.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_lib as P

TODAY = "2026-09-12"
SLUG  = "private-health-insurance"

def section(inner, soft=False, width="820px"):
    return ('\n<section class="section%s">\n  <div class="container" style="max-width:%s">\n%s\n  </div>\n</section>'
            % (" bg-soft" if soft else "", width, inner))

def hero():
    return """
<section class="hero">
  <div class="container">
    <div style="max-width:780px">
      <span class="eyebrow">Private market coverage</span>
      <h1>Private health insurance plans, <span>outside the Marketplace</span></h1>
      <p class="hero-sub">Not everyone belongs on healthcare.gov. If you earn too much for a subsidy and you are
      healthy enough to answer the health questions, a privately underwritten plan can cost less and carry a broader
      PPO network. It can also turn you down. Here is the honest version of both.</p>
      <div class="hero-ctas"><a class="btn btn-primary" href="/quote?type=individual">Get my quote</a><a class="btn btn-secondary" href="/aca-subsidy-calculator">Check my subsidy first</a></div>
      <div class="hero-meta">
        <span><span class="dot"></span>Licensed independent brokerage</span>
        <span><span class="dot"></span>40+ states</span>
        <span><span class="dot"></span>Carriers pay our commission</span>
      </div>
    </div>
  </div>
</section>"""

def cta(h, p, label="Get my quote", href="/quote?type=individual"):
    return ('<div class="cta-strip"><h2>%s</h2><p>%s</p>'
            '<a class="btn" href="%s" style="background:#fff;color:var(--blue-700)">%s</a></div>' % (h, p, href, label))

FAQ = [
 ("What is private health insurance?",
  "In this context it means major medical coverage bought directly from an insurance company or through a broker "
  "rather than through healthcare.gov or a state exchange. The defining difference is not the network or the brand on "
  "the card, it is underwriting: a private plan asks health questions and decides whether to cover you, while a "
  "Marketplace plan has to take everyone who applies during an enrollment window."),
 ("Is private health insurance cheaper than a Marketplace plan?",
  "It depends entirely on whether you qualify for a premium tax credit. If you do, the credit is applied only to "
  "Marketplace coverage, and it is usually impossible for a private plan to beat a subsidised premium. If your income "
  "is above the cutoff, you pay the full Marketplace price, and that is the situation where a privately underwritten "
  "plan for a healthy applicant often comes in lower. Run your subsidy number before you shop either one."),
 ("Can I be turned down for a private plan?",
  "Yes. That is the trade for the lower price. Based on your answers to the health questions and, in some cases, a "
  "prescription history check, a carrier can accept you, charge more than the quoted rate, write the policy while "
  "excluding a specific condition, or decline you outright. Nothing about applying obligates you, and a decline on a "
  "private application does not affect your right to enroll in a Marketplace plan during an enrollment window."),
 ("Do private plans cover pre-existing conditions?",
  "Do not assume so. The Affordable Care Act's guarantee that pre-existing conditions are covered applies to "
  "ACA-compliant coverage. Underwritten private products are a different category, and they commonly exclude a "
  "condition you already have, apply a waiting period to it, or price for it. If you have a diagnosis, are pregnant, "
  "or take a maintenance medication, get the exclusion language in writing before you drop anything you already have."),
 ("Can I buy a private plan any time of year?",
  "Generally yes, which is one of the real advantages. Marketplace enrollment is limited to open enrollment "
  "(1 November 2026 to 15 January 2027 for 2027 coverage) or a special enrollment period triggered by a life event. "
  "Underwritten private plans are not tied to that calendar, so they are often the only route for someone who missed "
  "the window and has no qualifying life event."),
 ("Do subsidies work with private plans?",
  "No. Premium tax credits exist only on Marketplace plans. If you take a private plan, you are paying the full "
  "premium yourself, and you cannot claim a credit for it at tax time. Self-employed people can still generally deduct "
  "the premiums under the self-employed health insurance deduction, which is a different benefit and applies to both types."),
 ("Does a private plan satisfy the health insurance requirement?",
  "The federal penalty for going without coverage has been $0 since 2019, so at the federal level there is nothing to "
  "satisfy. A handful of states, including California, Massachusetts, New Jersey, Rhode Island, Vermont and the "
  "District of Columbia, run their own coverage requirements, and not every private product counts toward them. If you "
  "live in one of those states, ask specifically whether the plan is minimum essential coverage before you enroll."),
 ("Who should not buy a private plan?",
  "Anyone who qualifies for a meaningful premium tax credit, anyone with a significant existing condition, anyone who "
  "is pregnant or planning to be, and anyone who wants the certainty of guaranteed acceptance. For those situations a "
  "Marketplace plan is usually both cheaper and safer, and we will tell you so rather than sell you the other thing."),
]

def build():
    C = P.Chrome()
    body = [hero()]

    body.append(section("""
    <h2>There are two health insurance markets, and they work differently</h2>
    <p>Most coverage advice online is about one of them. People land on healthcare.gov, see the price without a
    subsidy, and conclude that individual health insurance simply costs that much. It does not always.</p>
    <p>The private market is the other half: the same kind of major medical coverage, bought directly from carriers
    instead of through the exchange, and priced on your health rather than only on your age and ZIP code.</p>
    <table class="cost-table">
      <tr><th></th><th>Marketplace (ACA)</th><th>Private market</th></tr>
      <tr><td>Can you be turned down?</td><td>No, acceptance is guaranteed in an enrollment window</td><td>Yes, the plan is medically underwritten</td></tr>
      <tr><td>Health questions</td><td>None</td><td>Yes, and often a prescription history check</td></tr>
      <tr><td>Pre-existing conditions</td><td>Covered</td><td>May be excluded, delayed or priced for</td></tr>
      <tr><td>Premium tax credits</td><td>Available if you qualify</td><td>Never</td></tr>
      <tr><td>When you can enroll</td><td>Open enrollment or a qualifying life event</td><td>Generally year-round</td></tr>
      <tr><td>What sets your price</td><td>Age, ZIP, tier, tobacco, household size</td><td>All of that, plus your health</td></tr>
    </table>
    <p style="font-size:.88rem;color:var(--muted)">General product-category behavior. Terms vary by carrier and state,
    and your policy documents govern.</p>
    """))

    body.append(section("""
    <h2>Who the private market actually fits</h2>
    <p>The honest short answer: healthy people whose income puts them above the subsidy cutoff, and people who need
    coverage outside an enrollment window.</p>
    <p><strong>Worth quoting if you are:</strong></p>
    <ul>
      <li>Earning above the premium tax credit cutoff, where the Marketplace charges you full price. With the enhanced
      credits expired, the 400% federal poverty level cliff is back for 2027 &mdash; roughly $63,000 for a single adult
      and about $130,000 for a family of four. Above that line there is no credit at all.</li>
      <li>Self-employed, an owner-operator, or a 1099 contractor in good health.</li>
      <li>In need of a broad national PPO network when the plans on your state's exchange are mostly HMO or EPO.</li>
      <li>Between jobs, past your COBRA decision, or outside open enrollment with no qualifying life event.</li>
      <li>Retired before 65 and bridging the years until Medicare.</li>
    </ul>
    <p><strong>Stay on the Marketplace if you are:</strong></p>
    <ul>
      <li>Eligible for a premium tax credit of any real size. A subsidy beats underwriting almost every time.</li>
      <li>Living with a diagnosed condition, or taking a maintenance medication you need covered.</li>
      <li>Pregnant or planning a pregnancy in the next year.</li>
      <li>Someone who would rather pay more than risk an exclusion on the thing most likely to happen to you.</li>
    </ul>
    <p><a href="/aca-subsidy-calculator">Run your subsidy estimate first</a>. It takes two minutes and it decides which
    of these two markets you should be shopping in.</p>
    """, soft=True))

    body.append(section(cta("Not sure which market you belong in?",
        "We quote both sides and show you the two numbers together. Free, and there is no obligation either way.")))

    body.append(section("""
    <h2>The health questions, and what a carrier can do with your answers</h2>
    <p>This is the part that gets glossed over in most private-plan advertising, so here it is plainly. When you apply,
    the carrier reviews your answers and can respond in four ways:</p>
    <ul>
      <li><strong>Accept you at the quoted rate.</strong> The common outcome for applicants in good health.</li>
      <li><strong>Accept you at a higher rate.</strong> The quote you saw online was for a standard risk, and your
      final offer may not match it.</li>
      <li><strong>Accept you with an exclusion.</strong> The policy is issued but a named condition, and sometimes
      anything related to it, is carved out.</li>
      <li><strong>Decline you.</strong> No policy is issued.</li>
    </ul>
    <p>A decline costs you nothing but time, and it does not affect your right to enroll through the Marketplace during
    an open enrollment period or a special enrollment period. What it can cost you is timing, so never cancel existing
    coverage until a private policy is approved and issued in writing.</p>
    """))

    body.append(section("""
    <h2>Seven things to confirm before you sign a private policy</h2>
    <p>Ask these of any private plan, ours included. A plan that answers all seven well is a real plan. A plan that
    gets vague on the middle three is where people get hurt.</p>
    <ol>
      <li><strong>Is this major medical, and is it minimum essential coverage?</strong> Supplemental products such as
      fixed indemnity or accident-only coverage pay set amounts per service. They are not a substitute for major medical.</li>
      <li><strong>Is there an annual or lifetime maximum?</strong> ACA-compliant plans cannot impose one. Other
      products can, and a cap is what turns a serious illness into a financial event.</li>
      <li><strong>What is the out-of-pocket maximum, and what counts toward it?</strong> Ask whether out-of-network
      care counts, because often it does not.</li>
      <li><strong>How are pre-existing conditions handled?</strong> Get the exclusion language and any waiting period
      in writing, not a verbal reassurance.</li>
      <li><strong>Is the policy guaranteed renewable?</strong> In other words, if you get sick this year, can the
      carrier decline to renew you next year or re-underwrite your rate?</li>
      <li><strong>What is the network, and does it travel?</strong> If you drive, split time between states, or have a
      child at college out of state, this matters more than the deductible.</li>
      <li><strong>What happens to a condition diagnosed after I enroll?</strong> The answer should be that it is
      covered like anything else. If it is not, you are looking at a different kind of product than you think.</li>
    </ol>
    """, soft=True))

    body.append(section("""
    <h2>What a private plan costs</h2>
    <p>We do not publish premium tables, because a private quote is built on your age, ZIP code, plan design, tobacco
    use, household and your answers to the health questions. Any number printed on a page would be wrong for most of
    the people reading it.</p>
    <p>What is worth knowing is where the crossover sits. Below the subsidy cutoff, the premium tax credit usually
    makes a Marketplace plan the cheaper choice, and often by a wide margin. Above it, you are paying full price on the
    exchange with nothing offsetting it, and that is the range where a healthy applicant frequently finds a private
    plan for less. The subsidy cliff is the hinge, which is why we check it before quoting anything.</p>
    <p>Related reading: <a href="/blog/how-much-does-health-insurance-cost-2026">what health insurance actually costs</a>,
    <a href="/ppo-health-insurance">how PPO plans work</a>, and
    <a href="/health-insurance-between-jobs">coverage between jobs</a>.</p>
    """))

    body.append(section("""
    <h2>How we handle it</h2>
    <p>We are an independent brokerage, which means we are not tied to one carrier and we do not get paid more for
    steering you to the private side. The process is the same either way:</p>
    <ol>
      <li>We run your subsidy number first, so you know what the Marketplace would cost you.</li>
      <li>If private underwriting is likely to beat that, we quote it and walk you through the health questions before
      anything is submitted, so there are no surprises in the decision.</li>
      <li>You see both options side by side, with the trade-offs stated, and you choose.</li>
      <li>Nothing gets cancelled until the new policy is issued.</li>
    </ol>
    <p>Carriers pay our commission, so the comparison costs you nothing.</p>
    """, soft=True))

    body.append(section('<h2>Private health insurance: common questions</h2>\n' + P.faq_html(FAQ)))

    body.append(section(cta("See both markets, side by side",
        "Tell us your age, ZIP and rough income. We come back with your Marketplace number and, if it fits, a private option.")))

    main = '<main>' + "\n".join(body) + '</main>'

    related = """
<section class="vs-related-guides" data-block="vs-private-market">
  <div class="vs-rg-inner">
    <h2>Before you decide</h2>
    <p class="vs-rg-sub">The four pages people read alongside this one. Ready for numbers? <a href="/quote" style="color:#16447f;font-weight:700">Get my quote &rarr;</a></p>
    <div class="vs-rg-grid">
      <a class="vs-rg-card" href="/aca-subsidy-calculator"><strong>ACA Subsidy Calculator</strong><span>Find out whether a credit is on the table before you shop private.</span><em>Run the numbers &rarr;</em></a>
      <a class="vs-rg-card" href="/ppo-health-insurance"><strong>PPO Health Insurance</strong><span>How PPO networks work, and why they are scarce on some exchanges.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-between-jobs"><strong>Coverage Between Jobs</strong><span>Your options when you are outside open enrollment with no employer plan.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/1099-health-insurance"><strong>1099 and Self-Employed</strong><span>How net income sets your subsidy, and what is deductible either way.</span><em>Read the guide &rarr;</em></a>
    </div>
  </div>
</section>"""

    schemas = [
        P.breadcrumbs([("Home", "/"), ("Private Health Insurance", "/" + SLUG)]),
        P.faq_schema(FAQ),
        P.article_schema(SLUG, "Private Health Insurance Plans Outside the Marketplace",
                         "How medically underwritten private health plans differ from ACA Marketplace coverage, who they fit, and what to confirm before enrolling.",
                         TODAY),
    ]

    html = C.page(
        SLUG,
        "Private Health Insurance: Non-Marketplace Plans 2027",
        "Private health plans are medically underwritten, sold outside the Marketplace and open year-round. Who they fit, what the health questions mean, and when ACA wins.",
        "private health insurance, private health insurance plans, non-marketplace health insurance, private ppo plans, underwritten health insurance, health insurance without subsidy",
        main, schemas,
        og_image="/compressed/independent.jpg",
        related_block=related,
        sticky_call=True,
    )
    path = P.write(SLUG, html)
    print("wrote", path, len(html), "bytes")

if __name__ == "__main__":
    build()
