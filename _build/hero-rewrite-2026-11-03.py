import re, sys, html
NEW = {
 'truck-driver-health-insurance.html':
  'Private PPO coverage for truck drivers and owner-operators, with nationwide networks, compared across top A-rated carriers, free.',
 'seguro-medico-camioneros.html':
  'Cobertura PPO privada para camioneros y owner-operators, con redes nacionales, comparada entre las mejores aseguradoras con calificaci&oacute;n A, gratis.',
 'truck-driver-health-insurance-texas.html':
  'Texas has more truck drivers than any other state, and few PPOs for them: no Medicaid expansion and two insurers leaving for 2027. We compare private PPO coverage for Texas drivers across top A-rated carriers for your ZIP code, free.',
 'aca-vs-private-health-insurance-truck-drivers.html':
  'Private PPO coverage for truck drivers, compared across top A-rated carriers, free. Here is the honest comparison of ACA plans and private PPOs for drivers, and how to tell which one actually costs you less in about two minutes.',
 'ooida-health-insurance-vs-aca.html':
  "OOIDA's benefits package is real and worth having. It is also mostly supplemental rather than major medical, and that distinction decides whether a driver is covered for the things that actually happen. Here is what is in it, and how it compares with a full major medical plan.",
 'kentucky-small-business-health-insurance.html':
  'Group plans for teams of 2 to 50 across all eight Kentucky rating areas &mdash; Louisville, Lexington, Northern Kentucky, Bowling Green, Owensboro and eastern Kentucky &mdash; compared across top A-rated carriers, free. Kentucky&rsquo;s state small business exchange is closed, so coverage now runs through a carrier or a broker. We do it for nothing; carriers pay our commission either way.',
 'ichra-florida-small-business.html':
  'If a group plan quote just came back 20% higher, there is a second door. An Individual Coverage HRA lets you set a fixed monthly budget, hand it to your employees tax-free, and let them pick their own individual plan from top A-rated carriers. Here is the honest version: the rules, the math, and the cases where it is the wrong move.',
 'premium-increase-review.html':
  'Florida individual health insurance rates rose about 10% on average for 2027, and some plans rose far more. Tell us what you paid this year and what the renewal says. A licensed advisor compares private PPO options across top A-rated carriers for your ZIP code and shows you what it would cost to switch, before the December 15 deadline.',
 'blog/aca-open-enrollment-2027-guide.html':
  'ACA Open Enrollment 2027 opens November 1, 2026 and closes January 15, 2027. That is the window when anyone can enroll in, change, or drop an ACA health insurance plan. Miss it and you typically wait until open enrollment 2028. This guide covers the exact 2027 open enrollment dates, how to estimate your ACA subsidy, which plan tier to choose, and the five mistakes that cost people thousands every November.',
 'blog/sleep-apnea-cpap-cdl-health-insurance.html':
  'A driver gets sent for a sleep study, sits out three weeks waiting on results, and then finds out the machine costs $1,200 out of pocket. That sequence has ended more careers than any wreck. Here is what the regulation actually requires, what your examiner is actually looking at, and what your health plan actually pays for.',
 'blog/hsa-for-truck-drivers.html':
  'An HSA used to need a special plan. Since 2026, any bronze plan bought through HealthCare.gov or a state exchange qualifies, which makes it one of the easiest tax breaks a driver can take.',
 'blog/benefits-of-private-health-insurance.html':
  'Most people only know one side of health insurance: the government exchange plans on HealthCare.gov. The private market is the other side, and for the right buyer it is faster, more flexible and cheaper. Here are the real benefits, followed by the trade-offs nobody puts in the ad.',
 'blog/start-group-health-insurance-january-1-south-florida.html':
  'January 1 is the most popular start date for small business health insurance, and for good reason. Deductibles reset with the calendar year, it lines up with tax planning, and employees coming off individual plans get a clean switch. It is also the date owners most often miss, because carrier paperwork deadlines land in the middle of the holidays. This checklist gives South Florida employers in Miami-Dade, Broward and Palm Beach the timeline, the documents and the one exception window that makes January 1, 2027 easier than you think.',
 'blog/private-health-insurance-small-business-owners.html':
  'Small business owners have more options than a HealthCare.gov plan and a traditional group plan. The private market covers both sides: underwritten plans for you and your family, and level-funded group plans for your team. Here is how each works and who each one fits.',
}
KW = re.compile(r'marketplace|mercado', re.I)
def plain(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()

root = sys.argv[1]
done = 0
for f, new in NEW.items():
    p = root + '/' + f
    s = open(p, encoding='utf-8').read()
    h = s.find('</h1>')
    cands = []
    m = re.search(r'<p\b[^>]*>(.*?)</p>', s[h:h+4000], re.S)
    if m: cands.append((h + m.start(1), h + m.end(1), m.group(1)))
    for m2 in re.finditer(r'<p\b[^>]*class="[^"]*(?:hero-sub|hero-lede|lede|subhead|hero-sub-m)[^"]*"[^>]*>(.*?)</p>', s[:h+6000], re.S):
        cands.append((m2.start(1), m2.end(1), m2.group(1)))
    hit = [c for c in cands if KW.search(plain(c[2]))]
    seen = set(); hit2 = []
    for c in hit:
        if c[0] not in seen: seen.add(c[0]); hit2.append(c)
    assert hit2, f
    old_plain = plain(hit2[0][2])
    for a, b, _ in sorted(hit2, key=lambda c: -c[0]):
        s = s[:a] + new + s[b:]
    # same sentence reused in meta descriptions / other hero copies (e.g. mobile duplicate)
    extra = 0
    for m in list(re.finditer(r'<p\b[^>]*>(.*?)</p>', s, re.S))[::-1]:
        if plain(m.group(1)) == old_plain:
            s = s[:m.start(1)] + new + s[m.end(1):]; extra += 1
    open(p, 'w', encoding='utf-8').write(s)
    done += 1
    print(f'{f}: replaced {len(hit2)} hero line(s), {extra} duplicate(s)')
print('pages', done)
