# -*- coding: utf-8 -*-
"""Fix /open-enrollment.

1. The desktop nav wraps onto three lines. This page's nav CSS is missing the
   `white-space:nowrap` and `font-size:.94rem` that every other page's chrome
   carries, and its CTA label ("Get Open Enrollment Help") is twice the length
   of the site standard. Both fixed.
2. Route everything to /quote. The page ran its own duplicate two-form lead
   capture writing to Firebase, HubSpot and GHL from the page. Replaced with
   segmented links into /quote, which already supports ?type=individual and
   ?type=business deep links and is the funnel the rest of the site uses.
   The dead JS, the success modal and three Firebase module imports come out
   with it.
3. The countdown stopped dead at Nov 1. Extended through both real deadlines.
"""
import re, sys

F = "open-enrollment.html"
c = open(F, encoding="utf-8").read()
orig = c
log = []
def did(w): log.append(w)

def sub1(pat, rep, label, flags=0):
    global c
    c2, n = re.subn(pat, rep, c, count=1, flags=flags)
    if n != 1:
        print("MISS:", label); sys.exit(1)
    c = c2; did(label)

# --- 1. nav CSS: stop the wrap -------------------------------------------
sub1(r"\.nav-links a\{border:0;padding:8px 12px;min-height:auto\}",
     ".nav-links a{border:0;padding:8px 10px;min-height:auto;font-size:.94rem;white-space:nowrap}",
     "nav CSS: nowrap + .94rem on links")
sub1(r"\.nav-links button\.nav-login\{border:0;padding:8px 12px;min-height:auto;width:auto\}",
     ".nav-links button.nav-login{border:0;padding:8px 10px;min-height:auto;width:auto;font-size:.94rem;white-space:nowrap}",
     "nav CSS: nowrap + .94rem on login button")
sub1(r"\.nav-links a\.nav-cta\{margin:0 0 0 6px;padding:10px 18px\}",
     ".nav-links a.nav-cta{margin:0 0 0 6px;padding:10px 18px;white-space:nowrap}",
     "nav CSS: nowrap on CTA")

# --- 2. nav CTA: shorter label, points at /quote --------------------------
sub1(r'<a class="nav-cta" href="#support">Get Open Enrollment Help</a>',
     '<a class="nav-cta" href="/quote">Get a Quote</a>',
     "nav CTA -> /quote, label shortened")

# --- 3. hero copy no longer promises a form below ------------------------
sub1(r"Add your name below and a licensed independent broker will personally reach out to get you ready\.",
     "Start your free quote and a licensed independent broker will personally reach out to get you ready.",
     "hero copy")

# --- 4. form card -> router into /quote ----------------------------------
NEW_CARD = '''<div class="form-card" id="oe-form">
        <span class="badge">Free, no obligation</span>
        <h2 id="formTitle">Get Ready for Open Enrollment</h2>
        <p class="sub" id="formSub">Who are we preparing for? Pick one to start.</p>

        <div class="choice-grid" id="oeChoice">
          <a class="choice-card" href="/quote?type=individual" data-oe-cta="individual">
            <span class="choice-ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
            <span class="choice-h">Individual / Family</span>
            <span class="choice-p">Coverage for you and your loved ones</span>
          </a>
          <a class="choice-card" href="/quote?type=business" data-oe-cta="business">
            <span class="choice-ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/></svg></span>
            <span class="choice-h">Business / Group</span>
            <span class="choice-p">Group coverage for your employees</span>
          </a>
        </div>

        <p style="text-align:center;margin:16px 0 0;font-size:.9rem;color:var(--muted)">
          Takes about two minutes. Or <a href="tel:+19548251009" style="font-weight:700">call (954) 825-1009</a>
          and we will do it with you.
        </p>

        <div class="trust-row">
          <span><span class="tick">\u2713</span> Licensed broker</span>
          <span><span class="tick">\u2713</span> Free consult</span>
          <span><span class="tick">\u2713</span> Secure &amp; private</span>
        </div>
      </div>'''
m = re.search(r'<div class="form-card" id="oe-form">.*?<div class="trust-row">.*?</div>\s*</div>', c, re.S)
if not m: print("MISS: form card"); sys.exit(1)
c = c[:m.start()] + NEW_CARD + c[m.end():]
did("form card -> segmented /quote links, both inline forms removed")

# choice-card is an <a> now: keep it looking identical
sub1(r"(\.choice-card\{)", r"\1text-decoration:none;", "choice-card anchor styling")

# --- 5. success modal markup (its JS is going too) ------------------------
m = re.search(r'<div class="modal-overlay" id="oeModal".*?</div>\s*</div>\s*', c, re.S)
if not m: print("MISS: modal"); sys.exit(1)
c = c[:m.start()] + c[m.end():]
did("success modal removed")

# --- 6. dead JS: selection flow, confetti, modal, both submit handlers ----
start = c.find("  // ---- selection-first flow ----")
end = c.find("</script>", start)
if start < 0 or end < 0: print("MISS: form JS"); sys.exit(1)
tail = c[start:end]
if "oeBizForm" not in tail: print("MISS: JS bounds look wrong"); sys.exit(1)
c = c[:start] + "  // Lead capture lives on /quote. The selection cards above link straight there.\n" + c[end:]
did("dead form JS removed (%d chars)" % len(tail))

# --- 7. the Firebase module only fed those forms -------------------------
m = re.search(r'<!-- ===== GoHighLevel \+ Admin portal integration.*?</script>\s*', c, re.S)
if not m: print("MISS: firebase module"); sys.exit(1)
c = c[:m.start()] + c[m.end():]
did("Firebase/GHL module removed (3 fewer imports on page load)")

# --- 8. countdown: run through both real deadlines -----------------------
OLD_CD = re.search(r"  // ---- countdown to Nov 1, 2026 \(Open Enrollment opens\) ----.*?\n  \}\)\(\);", c, re.S)
if not OLD_CD: print("MISS: countdown"); sys.exit(1)
NEW_CD = """  // ---- countdown: opens Nov 1, Jan 1 coverage deadline Dec 15, closes Jan 15 ----
  (function(){
    var OPEN =new Date('2026-11-01T00:00:00-04:00').getTime();
    var DEC15=new Date('2026-12-15T23:59:59-05:00').getTime();
    var END  =new Date('2027-01-15T23:59:59-05:00').getTime();
    var d=document.getElementById('cd-d'),h=document.getElementById('cd-h'),m=document.getElementById('cd-m'),s=document.getElementById('cd-s');
    var head=document.querySelector('#countdown h2'), sub=document.querySelector('#countdown p');
    function paint(target,title,note){
      if(head) head.textContent=title;
      if(sub)  sub.textContent=note;
      var diff=Math.max(0,target-Date.now());
      d.textContent=Math.floor(diff/86400000);
      h.textContent=Math.floor((diff%86400000)/3600000);
      m.textContent=Math.floor((diff%3600000)/60000);
      s.textContent=Math.floor((diff%60000)/1000);
    }
    function tick(){
      var now=Date.now();
      if(now<OPEN){
        paint(OPEN,'2027 Open Enrollment Opens Soon',
              'Start your quote now so you are ready the day it opens.');
      } else if(now<=DEC15){
        paint(DEC15,'Time Left for January 1 Coverage',
              'Enroll by Dec 15 to start Jan 1. Open Enrollment then runs through Jan 15.');
      } else if(now<=END){
        paint(END,'Last Chance to Enroll for 2027',
              'Open Enrollment closes Jan 15, 2027. A plan started now begins Feb 1.');
      } else {
        paint(Date.now(),'Open Enrollment Is Closed for 2027',
              'You may still qualify through a Special Enrollment Period. Ask us to check.');
      }
    }
    tick(); setInterval(tick,1000);
  })();"""
c = c[:OLD_CD.start()] + NEW_CD + c[OLD_CD.end():]
did("countdown -> 4 phases through Jan 15")

# --- 9. countdown gets its own CTA ---------------------------------------
sub1(r'(<div class="cd-grid">)',
     '<div style="margin:14px 0 4px"><a class="btn btn-primary" href="/quote">Start my free quote</a></div>\n      \\1',
     "countdown CTA -> /quote")

# --- 10. support section gets a /quote route -----------------------------
sub1(r'(<div class="support-actions">)',
     '\\1\n        <a href="/quote" style="font-weight:700">Start my free quote</a>',
     "support section CTA -> /quote")

# --- 11. FAQ referred to a form that no longer exists --------------------
sub1(r"Choose the business option on the form and we'll reach out\.",
     "Choose the business option when you start your quote and we&rsquo;ll reach out.",
     "FAQ copy: no longer points at a form")

print("edits applied to %s:" % F)
for l in log: print("   -", l)
print("\nsize: %d -> %d bytes (%+d)" % (len(orig), len(c), len(c)-len(orig)))
open(F, "w", encoding="utf-8").write(c)
