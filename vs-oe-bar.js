/* =====================================================================
   OE BAR  (vs-oe-bar.js)

   253 pages carry a static #oe-annc-bar with one message for everyone.
   This rewrites it in place, by date and by who is reading:

     audience   trucker  (driver, owner-operator, CDL pages)  -> /truckers/quote
                business (small business, group, fleet pages) -> /small-business-renewal-review
                everyone else                                 -> /quote
     phase      pre      before Nov 1 2026: 2027 rates are up, check early
                oe       Nov 1 - Dec 15: countdown to the Jan 1 deadline
                late     Dec 16 - Jan 15: last chance, Feb 1 start
                after    after Jan 15: special enrollment checker

   Group plans are not tied to open enrollment, so business pages get the
   renewal message instead of the countdown. Spanish pages get Spanish.
   If this script fails, the static bar already on the page still works.
   ===================================================================== */
(function () {
  "use strict";
  var bar = document.getElementById("oe-annc-bar");
  if (!bar) return;

  var path = (location.pathname || "/").toLowerCase();
  var es = (document.documentElement.lang || "").toLowerCase().indexOf("es") === 0 ||
           /seguro|camioner|examen-medico|cotizar/.test(path);

  // Fleet / employer pages first: a "trucking company" is a business buyer, not a driver.
  var biz = !/switching-trucking/.test(path) &&
    /small-business|group-health|business|employer|employee|ichra|level-funded|section-125|trucking-compan|fleet|freight-broker|restaurant|crew|skilled-trades|health-insurance-for-(?!self-employed|truck|uber|small-business-owners)|renewal-review|census/.test(path);
  var trucker = !biz && /truck|trucker|owner-operator|lease-operator|cdl|dot-physical|otr|camioner|ooida|examen-medico|on-the-road|subsidy-cliff|occupational-accident/.test(path);
  var aud = biz ? "business" : trucker ? "trucker" : "general";

  // Dates are local midnight. Year roll is explicit so this keeps working
  // next season once the dates below are bumped.
  var now = new Date();
  var OPENS = new Date(2026, 10, 1), JAN1_DEADLINE = new Date(2026, 11, 15, 23, 59), CLOSES = new Date(2027, 0, 15, 23, 59);
  var phase = now < OPENS ? "pre" : now <= JAN1_DEADLINE ? "oe" : now <= CLOSES ? "late" : "after";
  var daysTo = function (d) { return Math.max(0, Math.ceil((d - now) / 86400000)); };
  var dLeft = daysTo(JAN1_DEADLINE), dClose = daysTo(CLOSES);

  var Q = { trucker: es ? "/truckers/cotizar" : "/truckers/quote", business: "/small-business-renewal-review", general: "/quote" };
  var T;
  if (es) {
    T = {
      pre: { trucker: ["Las primas de 2027 suben. La inscripción abierta empieza el 1 de noviembre; vea su precio antes.", "Cotizar gratis"],
             business: ["¿Su renovación de plan grupal 2027 subió? Le hacemos una revisión gratis antes de firmar.", "Revisar mi renovación"],
             general: ["Las primas de 2027 suben. La inscripción abierta empieza el 1 de noviembre.", "Cotizar gratis"] },
      oe:  { any: ["Quedan " + dLeft + (dLeft === 1 ? " día" : " días") + " para inscribirse con cobertura desde el 1 de enero (fecha límite: 15 de dic).", "Cotizar ahora"] },
      late:{ any: ["Última oportunidad: la inscripción abierta cierra el 15 de enero. Cobertura desde el 1 de febrero.", "Cotizar ahora"] },
      after:{ any: ["¿Se le pasó la inscripción abierta? Vea si califica para un período especial.", "Verificar"] }
    };
  } else {
    T = {
      pre: { trucker: ["2027 premiums are going up. Open enrollment starts Nov 1. See your new price before it hits.", "Check my 2027 rate"],
             business: ["2027 group renewals are up 8–15%+. Get a free renewal review before you sign.", "Review my renewal"],
             general: ["2027 premiums are going up. Open enrollment starts Nov 1. See your new price early.", "Get a Free Quote"] },
      oe:  { trucker: [dLeft + (dLeft === 1 ? " day" : " days") + " left to lock in January 1 coverage. Drivers: quote from the cab in 60 seconds.", "Get my quote"],
             general: [dLeft + (dLeft === 1 ? " day" : " days") + " left to enroll for January 1 coverage (deadline Dec 15).", "Get a Free Quote"] },
      late:{ trucker: ["Last chance: open enrollment closes Jan 15 (" + dClose + (dClose === 1 ? " day" : " days") + " left). Coverage starts Feb 1.", "Get my quote"],
             general: ["Last chance: open enrollment closes Jan 15 (" + dClose + (dClose === 1 ? " day" : " days") + " left). Coverage starts Feb 1.", "Get a Free Quote"] },
      after:{ trucker: ["Missed open enrollment? A job change, move or lost coverage may still let you enroll.", "Check if I qualify"],
              general: ["Missed open enrollment? A job change, move or lost coverage may still let you enroll.", "Check if I qualify"] }
    };
    // Group plans start any month: business pages keep the renewal pitch all season.
    T.oe.business = ["Group renewal up for 2027? Small-group plans can start any month. Get a free renewal review.", "Review my renewal"];
    T.late.business = T.oe.business;
    T.after.business = ["Group plans can start the 1st of any month. Compare your renewal or start a plan for your team.", "Get a group quote"];
  }
  var set = T[phase];
  var pair = set[aud] || set.any || set.general;
  var href = phase === "after" && aud !== "business" ? "/special-enrollment-period-checker" : Q[aud];
  var info = aud === "business" ? "/small-business-renewal-review" :
             aud === "trucker" ? (es ? "/seguro-medico-camioneros" : "/truck-driver-open-enrollment-2027") : "/blog/aca-open-enrollment-2027-guide";
  if (path.indexOf(href) === 0) href = "#review";

  var a1 = document.createElement("a");
  a1.href = info; a1.textContent = pair[0];
  a1.style.cssText = "color:#fff;text-decoration:underline;text-underline-offset:3px";
  var a2 = document.createElement("a");
  a2.href = href + (href.charAt(0) === "/" ? (href.indexOf("?") < 0 ? "?" : "&") + "from=oe-bar-" + aud : "");
  a2.textContent = pair[1] + " →";
  a2.style.cssText = "background:#fff;color:#16447f;border-radius:999px;padding:3px 12px;font-weight:800;white-space:nowrap;text-decoration:none";
  a2.addEventListener("click", function () {
    try { window.vsTrack && window.vsTrack("quote_cta", { from_page: location.pathname, cta: "oe-bar", audience: aud, phase: phase }); } catch (e) {}
  });

  var wrap = document.createElement("span");
  wrap.style.cssText = "display:inline-flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap";
  var s1 = document.createElement("span"); s1.appendChild(a1);
  wrap.appendChild(s1); wrap.appendChild(a2);
  if (phase === "oe" && dLeft <= 7 && aud !== "business") bar.style.background = "linear-gradient(135deg,#b42318,#16447f)";
  bar.innerHTML = ""; bar.appendChild(wrap);
  bar.setAttribute("data-aud", aud); bar.setAttribute("data-phase", phase);
})();
