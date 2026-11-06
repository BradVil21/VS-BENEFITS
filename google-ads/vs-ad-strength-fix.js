/* VS Ad strength fix (Oct 28 2026). PREVIEW first, then RUN. Safe to re-run.
   Replaces the 4 English ads rated AVERAGE with new responsive search ads (15 unique headlines with the ad
   group's search words, no pinned headlines, 4 descriptions). The old ad is paused only after the new one saves.
   Premium Increase 2027 now lands on /premium-increase-review; Businesses With 1099 Workers lands on /1099-health-insurance. */
var SITE = "https://www.vshealthbenefits.com";
var FIX = {
  "828627567829": { name: "Small Biz > Group Health 2-50 Employees", url: "/small-business-health-quote", p1: "small-business", p2: "group-health",
    h: ["Group Health Insurance", "Group Health for 2-50 Staff", "Small Group Health Insurance", "Employee Health Insurance FL",
        "Free Group Health Quotes", "Compare Top Carriers Free", "Plans Can Start Any Month", "Level-Funded & ICHRA Options",
        "No Fee to Your Business", "Keep Your Team's Doctors", "Licensed FL Health Broker", "Renewal Up? Get a 2nd Opinion",
        "Quote in Minutes, Census Later", "Benefits That Keep Staff", "Talk to a Licensed Advisor"],
    d: ["Group health insurance for 2-50 employees. We compare carriers side by side, free.",
        "Level-funded, ICHRA and fully insured plans for Florida small businesses. No fee to you.",
        "Plans start the 1st of any month. See real numbers for your team before you commit.",
        "Renewal went up for 2027? Send it over and a licensed advisor shops it before you sign."] },
  "828643289164": { name: "Trucker > 1099 Driver", url: "/trucking-health-quote", p1: "truckers", p2: "1099-drivers",
    h: ["1099 Truck Driver Insurance", "Independent Trucker Coverage", "Self-Employed Driver Plans", "Health Plans for 1099 Drivers",
        "No Employer Plan? We Can Help", "Premiums May Be Tax Deductible", "Florida Trucker Health Plans", "Plans That Work on the Road",
        "Nationwide PPO Options", "Check Your Tax Credits Free", "Licensed Florida Broker", "Free Quote in 2 Minutes",
        "Enroll by Dec 15 for Jan 1", "Cover Your Spouse & Kids", "Talk to a Licensed Advisor"],
    d: ["1099 and independent truck drivers: compare Marketplace and PPO plans free.",
        "Tax credits are based on net income after truck expenses. We check yours free.",
        "Doctors across the country, so your coverage works on the road, not just at home.",
        "Licensed Florida broker. Carriers pay us, not you: same price as going direct."] },
  "828706210226": { name: "Small Biz > Businesses With 1099 Workers", url: "/1099-health-insurance", p1: "1099", p2: "health-plans",
    h: ["Health Insurance for 1099s", "1099 Contractor Health Plans", "Self-Employed Health Plans", "Have 1099 Workers?",
        "Benefits for Your Crew", "ICHRA & Group Health Options", "Check Your Tax Credits Free", "Compare Top Carriers Free",
        "Licensed FL Health Broker", "Free Quote, No Obligation", "Plans for You or Your Team", "Premiums May Be Deductible",
        "Enroll by Dec 15 for Jan 1", "No Fee to Use an Advisor", "Talk to a Licensed Advisor"],
    d: ["1099 contractor? Compare Marketplace and PPO plans and check your tax credit free.",
        "Run a crew of 1099 workers? See group, ICHRA and individual options side by side.",
        "Licensed Florida broker. Carriers pay us, not you. Same price as buying direct.",
        "Enroll by Dec 15 for coverage on Jan 1. Quote in minutes from your phone."] },
  "829780867595": { name: "Individual > Premium Increase 2027", url: "/premium-increase-review", p1: "rate-increase", p2: "review",
    h: ["Health Insurance Went Up?", "2027 Premium Increase?", "Premium Increase 2027", "Lower Your 2027 Premium",
        "Don't Auto-Renew the Increase", "Free 2027 Rate Review", "Your Renewal Is Not Final", "Compare FL Plans Free",
        "See Lower-Cost Options", "Licensed Florida Broker", "Check Your 2027 Subsidy", "HSA & Lower-Premium Plans",
        "Enroll by Dec 15 for Jan 1", "Same Price as Buying Direct", "Talk to a Licensed Advisor"],
    d: ["Premium went up for 2027? Send your renewal and we compare every plan in your area.",
        "Free rate review by a licensed Florida advisor before you auto-renew. No obligation.",
        "Carriers pay us, not you. Same price as buying direct, with a real person to call.",
        "Open enrollment runs Nov 1 to Jan 15. Switch by Dec 15 for Jan 1 coverage."] }
};
function L(ok, m, r) { Logger.log((ok ? "OK: " : "FAILED: ") + m + (ok || !r ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); }
function main() {
  var bad = [];
  Object.keys(FIX).forEach(function (id) { var f = FIX[id], seen = {};
    if (f.h.length !== 15) bad.push(f.name + " headlines " + f.h.length);
    f.h.forEach(function (x) { if (x.length > 30) bad.push(f.name + " H>30: " + x + " (" + x.length + ")"); if (seen[x.toLowerCase()]) bad.push("dup " + x); seen[x.toLowerCase()] = 1; });
    f.d.forEach(function (x) { if (x.length > 90) bad.push(f.name + " D>90: " + x + " (" + x.length + ")"); });
    if (f.p1.length > 15 || f.p2.length > 15) bad.push(f.name + " path >15"); });
  if (bad.length) { Logger.log("CHECK FAILED, nothing changed:\n" + bad.join("\n")); return; }
  Logger.log("Lengths OK");
  Object.keys(FIX).forEach(function (id) {
    var f = FIX[id];
    var it = AdsApp.search("SELECT ad_group.resource_name, ad_group_ad.resource_name, ad_group_ad.status FROM ad_group_ad WHERE ad_group_ad.ad.id = " + id);
    if (!it.hasNext()) { Logger.log("MISSING ad " + id + " (" + f.name + ")"); return; }
    var r = it.next();
    if (r.adGroupAd.status !== "ENABLED") { Logger.log("Already replaced: " + f.name); return; }
    var nr = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: r.adGroup.resourceName, status: "ENABLED", ad: { finalUrls: [SITE + f.url],
      responsiveSearchAd: { headlines: f.h.map(function (t) { return { text: t }; }), descriptions: f.d.map(function (t) { return { text: t }; }), path1: f.p1, path2: f.p2 } } } } });
    L(nr.isSuccessful(), "new ad: " + f.name + " -> " + f.url, nr);
    if (nr.isSuccessful()) { var pr = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: r.adGroupAd.resourceName, status: "PAUSED" }, updateMask: "status" } });
      L(pr.isSuccessful(), "  paused old ad " + id, pr); }
  });
  Logger.log("DONE");
}
