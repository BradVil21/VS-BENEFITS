#!/usr/bin/env python3
"""Ad landing pages: one per niche per state (2026-11-03).

    python3 _build/build-lp.py            # writes lp/**.html

Pages are noindex (ads only; the SEO pages stay the ones Google ranks).
/lp/<niche> (no state) is routed by middleware.js to the visitor's state page.
Form: 4 fields -> /api/lead-sync (same path as the quote form) -> GoHighLevel + portal board.
"""
import html, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PHONE, TEL = '(954) 825-1009', 'tel:+19548251009'

STATES = [
 ('FL', 'florida', 'Florida', 'Florida', ['Miami', 'Orlando', 'Tampa', 'Jacksonville']),
 ('GA', 'georgia', 'Georgia', 'Georgia', ['Atlanta', 'Savannah', 'Macon', 'Augusta']),
 ('TX', 'texas', 'Texas', 'Texas', ['Dallas', 'Houston', 'San Antonio', 'Laredo']),
 ('IL', 'illinois', 'Illinois', 'Illinois', ['Chicago', 'Joliet', 'Rockford', 'Peoria']),
 ('OH', 'ohio', 'Ohio', 'Ohio', ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo']),
 ('KY', 'kentucky', 'Kentucky', 'Kentucky', ['Louisville', 'Lexington', 'Bowling Green', 'Paducah']),
 ('MO', 'missouri', 'Missouri', 'Misuri', ['Kansas City', 'St. Louis', 'Springfield', 'Joplin']),
 ('MD', 'maryland', 'Maryland', 'Maryland', ['Baltimore', 'Hagerstown', 'Frederick', 'Salisbury']),
]

ICON = {
 'phone': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 'check': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg>',
 'map': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l-6 3V6l6-3 6 3 6-3v15l-6 3-6-3zM9 3v15M15 6v15"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
 'user': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a8 8 0 0 1 16 0v1"/></svg>',
}

N = {
 'truckers': dict(lang='en', path='lp/truckers', tag='lp-trucker', img='/compressed/trucker-woman-cab-window.webp', alt='Truck driver smiling in the cab of her truck',
   h1='Truck Driver Health Insurance{in}', h1all='Truck Driver Health Insurance',
   title='Truck Driver Health Insurance{in} | Free Quote', desc='Private PPO health insurance for truck drivers and owner-operators{in}. Compare top A-rated carriers free with a licensed advisor.',
   sub='Private PPO plans for owner-operators, 1099 and company drivers, compared across top A-rated carriers. Free.',
   bullets=['Doctors in all 50 states on select PPO plans', 'Quote in about 2 minutes, no fee', 'A licensed advisor calls you back fast'],
   cards=[('map', 'Coverage that rides with you', 'Nationwide PPO networks, so a clinic in another state is not out of network.'),
          ('shield', 'Top A-rated carriers', 'We compare the big names side by side and show you the real monthly price.'),
          ('user', 'One advisor, start to finish', 'Quote, paperwork and every renewal handled by the same licensed person.')],
   local='We help drivers based anywhere in {state}, from {cities}.', localall='We help drivers in Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Missouri and Maryland.',
   faq=[('How much does truck driver health insurance cost?', 'It depends on your age, ZIP code, household and the plan you pick. Tell us those on the form and an advisor shows you real prices from several carriers, usually the same day.'),
        ('Will my plan work when I am on the road?', 'Select PPO plans have doctors in all 50 states, so you can see a provider in another state without going out of network. We point those plans out for you.'),
        ('Do I pay you anything?', 'No. Carriers pay us. Your premium is the same as buying direct, and you get a licensed advisor for free.')]),
 'self-employed': dict(lang='en', path='lp/self-employed', tag='lp-self-employed', img='/compressed/10-99working.webp', alt='Self-employed worker at her laptop',
   h1='Self-Employed Health Insurance{in}', h1all='Self-Employed Health Insurance',
   title='Self-Employed Health Insurance{in} | Free Quote', desc='Private PPO health insurance for self-employed, 1099 and freelance workers{in}. Compare top A-rated carriers free with a licensed advisor.',
   sub='Private PPO plans for 1099 workers, freelancers and one-person businesses, compared across top A-rated carriers. Free.',
   bullets=['Pick your own doctors with a PPO', 'Quote in about 2 minutes, no fee', 'A licensed advisor calls you back fast'],
   cards=[('user', 'Built for people without an employer plan', 'Contractors, gig workers and owners get real coverage of their own.'),
          ('shield', 'Top A-rated carriers', 'We compare the big names side by side and show you the real monthly price.'),
          ('map', 'Doctors where you need them', 'Broad PPO networks, with nationwide options if you travel for work.')],
   local='We help self-employed people across {state}, from {cities}.', localall='We help self-employed people in Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Missouri and Maryland.',
   faq=[('Can I get health insurance if I am self-employed?', 'Yes. Self-employed and 1099 workers can buy a private PPO plan for themselves and their family. We compare plans from several carriers for you.'),
        ('Is health insurance tax deductible for self-employed people?', 'Self-employed people can often deduct what they pay for health insurance. Ask your tax preparer how it applies to you.'),
        ('Do I pay you anything?', 'No. Carriers pay us. Your premium is the same as buying direct, and you get a licensed advisor for free.')]),
 'es-camioneros': dict(lang='es', path='lp/es/camioneros', tag='lp-trucker', img='/compressed/trucker-woman-cab-window.webp', alt='Camionera sonriendo en la cabina de su camión',
   h1='Seguro Médico para Camioneros{in}', h1all='Seguro Médico para Camioneros',
   title='Seguro Médico para Camioneros{in} | Cotización Gratis', desc='Planes PPO privados para camioneros y owner-operators{in}. Compare las mejores aseguradoras gratis con un asesor con licencia que habla español.',
   sub='Planes PPO privados para owner-operators, choferes 1099 y de compañía, comparados entre las mejores aseguradoras. Gratis.',
   bullets=['Médicos en los 50 estados con planes PPO selectos', 'Cotización en unos 2 minutos, sin costo', 'Un asesor con licencia le llama pronto'],
   cards=[('map', 'Cobertura que viaja con usted', 'Redes PPO nacionales: una clínica en otro estado no queda fuera de la red.'),
          ('shield', 'Aseguradoras con calificación A', 'Comparamos las principales y le mostramos el precio mensual real.'),
          ('user', 'Un solo asesor, de principio a fin', 'Cotización, trámites y renovaciones con la misma persona, en español.')],
   local='Ayudamos a choferes en todo {state}, desde {cities}.', localall='Ayudamos a choferes en Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Misuri y Maryland.',
   faq=[('¿Cuánto cuesta el seguro médico para camioneros?', 'Depende de su edad, código postal, familia y el plan. Complete el formulario y un asesor le muestra precios reales de varias aseguradoras, casi siempre el mismo día.'),
        ('¿Mi plan funciona cuando estoy en la carretera?', 'Algunos planes PPO tienen médicos en los 50 estados, así puede ver a un proveedor en otro estado sin salir de la red.'),
        ('¿Les pago algo?', 'No. Las aseguradoras nos pagan. Su prima es la misma que si compra directo, y recibe un asesor con licencia gratis.')]),
 'es-independientes': dict(lang='es', path='lp/es/independientes', tag='lp-self-employed', img='/compressed/10-99working.webp', alt='Trabajadora independiente en su computadora',
   h1='Seguro Médico para Trabajadores Independientes{in}', h1all='Seguro Médico para Trabajadores Independientes',
   title='Seguro Médico para Independientes{in} | Cotización Gratis', desc='Planes PPO privados para trabajadores independientes y 1099{in}. Compare las mejores aseguradoras gratis con un asesor que habla español.',
   sub='Planes PPO privados para trabajadores 1099, freelancers y dueños de negocio, comparados entre las mejores aseguradoras. Gratis.',
   bullets=['Escoja sus propios médicos con un PPO', 'Cotización en unos 2 minutos, sin costo', 'Un asesor con licencia le llama pronto'],
   cards=[('user', 'Para quien no tiene plan del empleador', 'Contratistas, trabajadores 1099 y dueños con su propia cobertura.'),
          ('shield', 'Aseguradoras con calificación A', 'Comparamos las principales y le mostramos el precio mensual real.'),
          ('map', 'Médicos donde los necesita', 'Redes PPO amplias, con opciones nacionales si viaja por trabajo.')],
   local='Ayudamos a trabajadores independientes en todo {state}, desde {cities}.', localall='Ayudamos a trabajadores independientes en Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Misuri y Maryland.',
   faq=[('¿Puedo tener seguro médico si trabajo por mi cuenta?', 'Sí. Los trabajadores independientes y 1099 pueden comprar un plan PPO privado para ellos y su familia. Comparamos varias aseguradoras por usted.'),
        ('¿El seguro médico se puede deducir de impuestos?', 'Los trabajadores independientes a menudo pueden deducir lo que pagan. Consulte con su preparador de impuestos.'),
        ('¿Les pago algo?', 'No. Las aseguradoras nos pagan. Su prima es la misma que si compra directo, y recibe un asesor con licencia gratis.')]),
}

T = {
 'en': dict(call='Call Now', callfull='Call a licensed advisor', form_h='Get your free quote', form_p='Takes 30 seconds. An advisor calls you back.',
   name='Full name', phone='Phone', zip='ZIP code', who='Who needs coverage?', whoopts=['Just me', 'Me + spouse', 'Me + kids', 'Whole family'],
   btn='Get My Free Quote', note='No fee. No obligation.', err='Please fill in all four fields with a valid phone and 5-digit ZIP.',
   ok_h='Thanks{n}! You are all set.', ok_p='A licensed advisor will call you shortly. During business hours that is usually within 5 minutes.', ok_call='Want to talk now? Call',
   rating='5.0 from 53 Google reviews', lic='Licensed in 40+ states', free='Free, no obligation', how='How it works',
   steps=[('Tell us about you', 'Name, phone, ZIP and who needs coverage.'), ('We compare carriers', 'An advisor pulls real prices from top A-rated carriers.'), ('You pick a plan', 'We handle the paperwork and you are covered.')],
   faqh='Questions', cta_h='Rather talk it through?', cta_p='Call and a licensed advisor answers.', hours='Mon to Fri 8am to 6pm, Sat and Sun 8am to 1pm ET',
   consent='By submitting, you agree to our <a href="/privacy">Privacy Policy</a> and that a licensed advisor from VS BENEFITS LLC (d/b/a VS Health Benefits) may call, text or email you at the contact info provided about health coverage, including by automated technology. Consent is not a condition of purchase. Msg &amp; data rates may apply; reply STOP to opt out. We never sell your information.',
   disc='VS BENEFITS LLC is a licensed independent insurance agency, not an insurance company, and is not affiliated with or endorsed by HealthCare.gov, the Centers for Medicare &amp; Medicaid Services (CMS) or any government agency. We do not offer every plan available in your area; HealthCare.gov or your state marketplace lists all options. Prices depend on eligibility and are estimates, not quotes.',
   inn=' in {state}', srclabel='Ad landing page'),
 'es': dict(call='Llamar', callfull='Llame a un asesor con licencia', form_h='Reciba su cotización gratis', form_p='Toma 30 segundos. Un asesor le devuelve la llamada.',
   name='Nombre completo', phone='Teléfono', zip='Código postal', who='¿Quién necesita cobertura?', whoopts=['Solo yo', 'Yo + cónyuge', 'Yo + hijos', 'Toda la familia'],
   btn='Quiero Mi Cotización', note='Sin costo. Sin compromiso.', err='Complete los cuatro campos con un teléfono válido y un código postal de 5 dígitos.',
   ok_h='¡Gracias{n}! Ya está listo.', ok_p='Un asesor con licencia le llamará pronto. En horario de oficina suele ser en menos de 5 minutos.', ok_call='¿Prefiere hablar ahora? Llame al',
   rating='5.0 en 53 reseñas de Google', lic='Licencia en más de 40 estados', free='Gratis, sin compromiso', how='Cómo funciona',
   steps=[('Cuéntenos de usted', 'Nombre, teléfono, código postal y quién necesita cobertura.'), ('Comparamos aseguradoras', 'Un asesor busca precios reales de las mejores aseguradoras.'), ('Usted elige', 'Nosotros hacemos los trámites y queda cubierto.')],
   faqh='Preguntas', cta_h='¿Prefiere hablar con alguien?', cta_p='Llame y le atiende un asesor con licencia en español.', hours='Lun a vie 8am a 6pm, sáb y dom 8am a 1pm ET',
   consent='Al enviar, acepta nuestra <a href="/privacy">Política de Privacidad</a> y que un asesor con licencia de VS BENEFITS LLC (d/b/a VS Health Benefits) le llame, envíe mensajes de texto o correos sobre cobertura de salud, incluso con tecnología automatizada. El consentimiento no es condición de compra. Pueden aplicar tarifas de mensajes y datos; responda STOP para cancelar. Nunca vendemos su información.',
   disc='VS BENEFITS LLC es una agencia de seguros independiente con licencia, no una aseguradora, y no está afiliada ni respaldada por HealthCare.gov, los Centros de Servicios de Medicare y Medicaid (CMS) ni ninguna agencia del gobierno. No ofrecemos todos los planes disponibles en su área; HealthCare.gov o el mercado de su estado lista todas las opciones. Los precios dependen de la elegibilidad y son estimados, no cotizaciones.',
   inn=' en {state}', srclabel='Página de anuncio'),
}

CSS = r'''
:root{--navy:#0b2346;--blue:#1f6fe5;--blue-d:#1559c2;--teal:#0db5a6;--ink:#1f2933;--muted:#5a6b80;--line:#e3e8ee;--soft:#f6f8fb;--cream:#faf8f5}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:'DM Sans',system-ui,-apple-system,sans-serif;color:var(--ink);background:#fff;line-height:1.55}
img{max-width:100%;display:block}a{color:inherit}
h1,h2,h3{font-family:'Poppins',system-ui,sans-serif;line-height:1.15;margin:0;color:var(--navy);text-wrap:balance}
.wrap{max-width:1080px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
.top{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}
.badge{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#16447f,#0db5a6);color:#fff;display:grid;place-items:center;font:800 .92rem 'Poppins',sans-serif;flex-shrink:0}
.bname{font:700 1.02rem 'Poppins',sans-serif;color:var(--navy);white-space:nowrap}
.callbtn{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#fff;text-decoration:none;font-weight:700;border-radius:999px;padding:11px 18px;white-space:nowrap;box-shadow:0 8px 20px -8px rgba(13,181,166,.7)}
.callbtn:hover{filter:brightness(.95)}
.callbtn .num{display:none}
@media(min-width:720px){.callbtn .num{display:inline}.callbtn .lbl{display:none}}
.hero{background:var(--cream);padding:20px 0 34px}
.hero .wrap{display:grid;gap:18px;align-items:start;grid-template-areas:'intro' 'form' 'extra'}
.intro{grid-area:intro}.card{grid-area:form}.extra{grid-area:extra}
@media(min-width:900px){.hero{padding:48px 0 56px}.hero .wrap{grid-template-columns:1.05fr .95fr;column-gap:40px;row-gap:0;grid-template-areas:'intro form' 'extra form'}}
.kicker{display:inline-block;font-size:.74rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#16447f;background:#fff;border:1px solid #dbe7f7;border-radius:999px;padding:6px 12px;margin-bottom:12px}
.hero h1{font-size:clamp(1.9rem,5vw,2.9rem)}
.hero h1 span{background:linear-gradient(90deg,#16447f,#0db5a6);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:1.04rem;color:#334155;margin:10px 0 0;max-width:540px}
.extra .bul{margin-top:18px}
@media(max-width:899px){.extra .bigcall{display:none}.kicker .k2{display:none}}
.bul{list-style:none;padding:0;margin:0 0 18px;display:grid;gap:8px}
.bul li{display:flex;gap:10px;align-items:flex-start;font-weight:600;color:var(--navy)}
.bul svg{color:var(--teal);flex-shrink:0;margin-top:3px}
.bigcall{display:flex;align-items:center;justify-content:center;gap:10px;background:var(--navy);color:#fff;text-decoration:none;font-weight:700;font-size:1.08rem;border-radius:14px;padding:15px 20px;max-width:420px}
.bigcall small{display:block;font-weight:500;font-size:.78rem;opacity:.8}
.rating{display:flex;align-items:center;gap:8px;margin-top:14px;font-size:.92rem;color:#475569;flex-wrap:wrap}
.rating .st{color:#f5a400;letter-spacing:1px}
.photo{display:none}
@media(min-width:900px){.photo{display:block;margin-top:22px;border-radius:18px;overflow:hidden;aspect-ratio:16/10;max-width:520px}.photo img{width:100%;height:100%;object-fit:cover}}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:0 20px 50px -28px rgba(11,35,70,.45)}
.card h2{font-size:1.35rem}.card .fp{color:var(--muted);margin:6px 0 16px;font-size:.95rem}
.fld{display:block;margin-bottom:12px}
.fld span{display:block;font-weight:700;font-size:.88rem;color:var(--navy);margin-bottom:5px}
.fld input,.fld select{width:100%;font:inherit;font-size:16px;padding:13px 14px;border:1.5px solid #d5dde8;border-radius:12px;background:#fff;color:var(--ink);outline:none;appearance:none;-webkit-appearance:none}
.fld select{background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%235a6b80' stroke-width='2.5'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 14px center}
.fld input:focus,.fld select:focus{border-color:var(--teal);box-shadow:0 0 0 3px rgba(13,181,166,.15)}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.go{width:100%;border:0;border-radius:12px;background:var(--blue);color:#fff;font:700 1.08rem 'DM Sans',sans-serif;padding:15px;cursor:pointer;box-shadow:0 12px 26px -12px rgba(31,111,229,.75)}
.go:hover{background:var(--blue-d)}.go[disabled]{opacity:.6;cursor:wait}
.fnote{text-align:center;color:var(--muted);font-size:.84rem;margin:10px 0 0}
.ferr{color:#b42318;font-size:.88rem;margin:0 0 10px}
.consent{font-size:.72rem;color:#7a8797;line-height:1.5;margin:12px 0 0}
.consent a{color:#16447f}
.done{text-align:center;padding:10px 0}
.done .ic{width:56px;height:56px;border-radius:50%;background:#e6f7f5;color:var(--teal);display:grid;place-items:center;margin:0 auto 12px}
.done h2{margin-bottom:8px}.done p{color:#334155;margin:0 0 14px}
.done .bigcall{margin:0 auto}
.trust{border-bottom:1px solid var(--line);padding:14px 0}
.trust .wrap{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 26px;font-weight:600;color:#334155;font-size:.92rem}
.trust span{display:inline-flex;align-items:center;gap:7px}.trust svg{color:var(--teal)}
.sec{padding:44px 0}.sec.soft{background:var(--soft)}
.sec h2{font-size:clamp(1.4rem,3.4vw,1.9rem);text-align:center;margin-bottom:22px}
.cards{display:grid;gap:14px}@media(min-width:760px){.cards{grid-template-columns:repeat(3,1fr)}}
.ben{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px}
.ben i{width:46px;height:46px;border-radius:12px;background:#eaf2fd;color:#16447f;display:grid;place-items:center;margin-bottom:10px}
.ben h3{font-size:1.06rem;margin-bottom:6px}.ben p{margin:0;color:#475569;font-size:.95rem}
.local{text-align:center;color:#334155;margin:18px auto 0;max-width:640px}
.steps{display:grid;gap:14px;counter-reset:s}@media(min-width:760px){.steps{grid-template-columns:repeat(3,1fr)}}
.step{background:#fff;border-radius:16px;padding:20px;border:1px solid var(--line)}
.step b{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--navy);color:#fff;font-family:'Poppins';margin-bottom:10px}
.step h3{font-size:1.02rem;margin-bottom:4px}.step p{margin:0;color:#475569;font-size:.94rem}
.faq{max-width:760px;margin:0 auto}
.faq details{background:#fff;border:1px solid var(--line);border-radius:12px;padding:15px 18px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:700;color:var(--navy);list-style:none;display:flex;justify-content:space-between;gap:10px}
.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";font-size:1.3rem;color:#16447f;font-weight:400}
.faq details[open] summary:after{content:"\2212"}
.faq p{margin:10px 0 0;color:#334155}
.cta{background:var(--navy);color:#fff;text-align:center;padding:40px 0}
.cta h2{color:#fff;margin-bottom:6px}.cta p{color:rgba(255,255,255,.85);margin:0 0 18px}
.cta .bigcall{background:var(--teal);margin:0 auto}
.foot{padding:26px 0 90px;font-size:.78rem;color:#7a8797;line-height:1.55}
.foot a{color:#16447f}.foot .lk{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px;font-weight:600}
.mbar{position:fixed;left:0;right:0;bottom:0;z-index:30;display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px max(12px,env(safe-area-inset-left)) calc(10px + env(safe-area-inset-bottom));background:#fff;border-top:1px solid var(--line);box-shadow:0 -8px 24px -12px rgba(11,35,70,.3)}
.mbar a{display:flex;align-items:center;justify-content:center;gap:8px;border-radius:12px;padding:13px;font-weight:700;text-decoration:none}
.mbar .c{background:var(--teal);color:#fff}.mbar .q{background:#eaf2fd;color:#16447f}
@media(min-width:900px){.mbar{display:none}.foot{padding-bottom:26px}}
'''

JS = r'''
(function(){
  var f=document.getElementById('lpf'); if(!f) return;
  var C=window.LPC||{};
  function digits(v){return String(v||'').replace(/\D/g,'');}
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var name=f.name.value.trim(), ph=digits(f.phone.value), zip=digits(f.zip.value).slice(0,5), who=f.who.value;
    if(ph.length===11&&ph.charAt(0)==='1') ph=ph.slice(1);
    var err=document.getElementById('lperr');
    if(name.length<2||ph.length!==10||zip.length!==5||!who){err.hidden=false;return;}
    err.hidden=true;
    var b=f.querySelector('.go'); b.disabled=true;
    var parts=name.split(/\s+/), first=parts.shift()||'', last=parts.join(' ');
    var attr=null; try{attr=window.vsAttribution&&window.vsAttribution();}catch(x){}
    var body={firstName:first,lastName:last,phone:ph,zip:zip,state:C.state||'',
      source:C.source,notes:C.whoLabel+': '+who+'\n'+C.source,
      tags:[C.tag,'ad-lp'].concat(C.state?['state-'+C.state.toLowerCase()]:[]).concat(C.lang==='es'?['spanish']:[]),
      attribution:attr};
    var done=function(){
      try{ if(window.gtag){ var a=window.VS_ADS; if(a&&a.labels&&a.labels.lead) gtag('event','conversion',{send_to:a.id+'/'+a.labels.lead}); gtag('event','generate_lead',{form:'ad-lp',niche:C.tag,state:C.state||'all'}); } }catch(x){}
      var ok=document.getElementById('lpdone'); ok.querySelector('h2').textContent=C.okH.replace('{n}',first?', '+first:'');
      f.hidden=true; ok.hidden=false; ok.scrollIntoView({behavior:'smooth',block:'center'});
    };
    fetch('/api/lead-sync',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),keepalive:true})
      .then(done,done);
  });
})();
'''

GSVG = '<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'

def e(s): return html.escape(s, quote=True)

def page(nk, st):
    n = N[nk]; t = T[n['lang']]; es = n['lang'] == 'es'
    if st:
        code, slug, en_name, es_name, cities = st
        sname = es_name if es else en_name
        inn = t['inn'].format(state=sname)
        local = n['local'].format(state=sname, cities=(', '.join(cities[:-1]) + (' y ' if es else ' and ') + cities[-1]))
        url = '/' + n['path'] + '/' + slug
    else:
        code, sname, inn, local, url = '', '', '', n['localall'], '/' + n['path']
    h1 = n['h1'].format(in_=inn, **{'in': inn}) if st else n['h1all']
    # gradient on the state / last words
    if st:
        h1html = e(n['h1'].format(**{'in': ''})) + ' <span>' + e(inn.strip()) + '</span>'
    else:
        w = h1.split(' '); h1html = e(' '.join(w[:-2])) + ' <span>' + e(' '.join(w[-2:])) + '</span>'
    title = n['title'].format(**{'in': inn}); desc = n['desc'].format(**{'in': inn})
    src = t['srclabel'] + ' - ' + ('Truckers' if 'truck' in n['tag'] else 'Self-Employed') + (' ES' if es else '') + ' ' + (code or 'all')
    cfg = {'state': code, 'tag': n['tag'], 'lang': n['lang'], 'source': src, 'whoLabel': t['who'], 'okH': t['ok_h']}
    opts = ''.join('<option>%s</option>' % e(o) for o in t['whoopts'])
    cards = ''.join('<div class="ben"><i>%s</i><h3>%s</h3><p>%s</p></div>' % (ICON[i], e(h), e(p)) for i, h, p in n['cards'])
    steps = ''.join('<div class="step"><b>%d</b><h3>%s</h3><p>%s</p></div>' % (k + 1, e(h), e(p)) for k, (h, p) in enumerate(t['steps']))
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in n['faq'])
    bul = ''.join('<li>%s<span>%s</span></li>' % (ICON['check'], e(b)) for b in n['bullets'])
    return f'''<!DOCTYPE html>
<html lang="{n['lang']}">
<head>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());</script>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}" />
<meta name="robots" content="noindex,follow" />
<link rel="canonical" href="https://www.vshealthbenefits.com{url}" />
<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet" />
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="VS Health Benefits"><span class="badge">VS</span><span class="bname">VS Health Benefits</span></a>
  <a class="callbtn" href="{TEL}" data-call="top">{ICON['phone']}<span class="lbl">{e(t['call'])}</span><span class="num">{PHONE}</span></a>
</div></header>
<main>
<section class="hero"><div class="wrap">
  <div class="intro">
    <span class="kicker">{e(t['lic'])}<span class="k2"> &middot; {e(t['free'])}</span></span>
    <h1>{h1html}</h1>
    <p class="sub">{e(n['sub'])}</p>
  </div>
  <div class="extra">
    <ul class="bul">{bul}</ul>
    <a class="bigcall" href="{TEL}" data-call="hero">{ICON['phone']}<span>{e(t['callfull'])}<small>{PHONE} &middot; {e(t['hours'])}</small></span></a>
    <div class="rating">{GSVG}<span class="st" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><span>{e(t['rating'])}</span></div>
    <div class="photo"><img src="{n['img']}" alt="{e(n['alt'])}" width="900" height="560" loading="eager" decoding="async" /></div>
  </div>
  <div class="card" id="quote">
    <form id="lpf" novalidate>
      <h2>{e(t['form_h'])}</h2>
      <p class="fp">{e(t['form_p'])}</p>
      <label class="fld"><span>{e(t['name'])}</span><input name="name" autocomplete="name" required /></label>
      <label class="fld"><span>{e(t['phone'])}</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" required /></label>
      <div class="row2">
        <label class="fld"><span>{e(t['zip'])}</span><input name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" required /></label>
        <label class="fld"><span>{e(t['who'])}</span><select name="who" required><option value="" disabled selected></option>{opts}</select></label>
      </div>
      <p class="ferr" id="lperr" role="alert" hidden>{e(t['err'])}</p>
      <button class="go" type="submit">{e(t['btn'])}</button>
      <p class="fnote">{e(t['note'])}</p>
      <p class="consent">{t['consent']}</p>
    </form>
    <div class="done" id="lpdone" hidden>
      <div class="ic">{ICON['check']}</div>
      <h2></h2>
      <p>{e(t['ok_p'])}</p>
      <a class="bigcall" href="{TEL}" data-call="thanks">{ICON['phone']}<span>{e(t['ok_call'])} {PHONE}</span></a>
    </div>
  </div>
</div></section>
<div class="trust"><div class="wrap"><span>{ICON['check']}{e(t['lic'])}</span><span>{ICON['check']}{e(t['rating'])}</span><span>{ICON['check']}{e(t['free'])}</span></div></div>
<section class="sec"><div class="wrap"><div class="cards">{cards}</div><p class="local">{e(local)}</p></div></section>
<section class="sec soft"><div class="wrap"><h2>{e(t['how'])}</h2><div class="steps">{steps}</div></div></section>
<section class="sec"><div class="wrap"><h2>{e(t['faqh'])}</h2><div class="faq">{faq}</div></div></section>
<section class="cta"><div class="wrap"><h2>{e(t['cta_h'])}</h2><p>{e(t['cta_p'])}</p><a class="bigcall" href="{TEL}" data-call="bottom">{ICON['phone']}<span>{PHONE}<small>{e(t['hours'])}</small></span></a></div></section>
</main>
<footer class="foot"><div class="wrap">
  <div class="lk"><a href="/privacy">{'Privacidad' if es else 'Privacy Policy'}</a><a href="/terms">{'Términos' if es else 'Terms'}</a><a href="/contact">{'Contacto' if es else 'Contact'}</a></div>
  <p>{t['disc']}</p>
  <p>NPN 22116298 &middot; &copy; VS BENEFITS LLC</p>
</div></footer>
<nav class="mbar" aria-label="Quick actions"><a class="c" href="{TEL}" data-call="sticky">{ICON['phone']}{e(t['call'])}</a><a class="q" href="#quote">{e(t['btn'].replace('My ', '').replace('Mi ', ''))}</a></nav>
<script>window.LPC={json.dumps(cfg, ensure_ascii=False)};</script>
<script>{JS}</script>
<script src="/vs-attribution.js" defer></script>
<script src="/vs-conversions.js" defer></script>
<script src="/vs-lead-system.js" defer></script>
</body>
</html>
'''

def main():
    n_written = 0
    for nk, n in N.items():
        base = os.path.join(ROOT, n['path'])
        os.makedirs(base, exist_ok=True)
        open(os.path.join(base, 'index.html'), 'w', encoding='utf-8').write(page(nk, None)); n_written += 1
        for st in STATES:
            open(os.path.join(base, st[1] + '.html'), 'w', encoding='utf-8').write(page(nk, st)); n_written += 1
    print('wrote', n_written, 'landing pages')

if __name__ == '__main__':
    main()
