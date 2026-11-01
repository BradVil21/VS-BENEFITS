# 2026-11-01: 2027 ACA benchmark premiums in every estimate tool

Old: BASE21 = 375 everywhere (about $479/mo at age 40, same for every state) - well under real 2027 prices.
New: KFF 2027 average benchmark (second-lowest silver) for a 40-year-old, by state, picked from the visitor's ZIP;
national $704 when the tool has no ZIP. base21 = state benchmark / 1.278 (age 40 on the federal age curve).
  US $704 (2026: $625, +13%) · FL $738 (2026: $683) · TX $737 · GA $733 · TN $796 · NC $660 · NY $1,041 ...
Source: KFF State Health Facts, Marketplace Average Benchmark Premiums (2027 data), checked Nov 1 2026.

Tools: aca-subsidy-calculator, health-insurance-premium-increase-calculator, cobra-vs-marketplace-calculator,
owner-operator-subsidy-cliff-calculator, truck-driver-health-insurance-cost-calculator, ichra-vs-group-health-calculator.
Unchanged (already 2027): FPL $15,960 + $5,680 (2026 HHS, used for 2027 coverage); Rev. Proc. 2026-26 contribution scale;
400% cliff. Live HealthSherpa plans (when HEALTHSHERPA_API_KEY is active) always show HealthSherpa's current prices.
Copy: "$625 a month" related-guide blurb on 3 pages -> "$704 for a 40-year-old in 2027 ($738 in Florida)".
Calculator fine print now says the benchmark is the 2027 average for your state, adjusted for age.
Script: .seo-work/aca_bench_2027_nov01.py
