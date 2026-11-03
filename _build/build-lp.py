#!/usr/bin/env python3
"""State landing pages: one per niche per state (2026-11-03, SEO redesign).

    python3 _build/build-lp.py        # writes lp/**.html

- Indexable SEO pages with state-specific content, FAQ + breadcrumb + agency schema,
  hreflang EN<->ES pairs, and internal links. Where an older page already ranks for the
  same state (FL/TX truckers, FL camioneros) the canonical points there to avoid cannibalising it.
- Quote buttons route by niche: truckers -> /trucking-health-quote, everyone else -> /quote.
  ZIP, state and ad tracking (gclid/utm) are carried over.
- /lp/<niche> (no state) is routed by middleware.js to the visitor's state page.
"""
import html, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://www.vshealthbenefits.com'
PHONE, TEL = '(954) 825-1009', 'tel:+19548251009'

# code, slug, English name, Spanish name, cities, interstates, freight hubs (EN), freight hubs (ES)
STATES = [
 ('FL', 'florida', 'Florida', 'Florida', ['Miami', 'Orlando', 'Tampa', 'Jacksonville'], ['I-95', 'I-75', 'I-10', 'I-4'],
  ['PortMiami', 'JAXPORT in Jacksonville', 'Port Tampa Bay'], ['PortMiami', 'JAXPORT en Jacksonville', 'Port Tampa Bay']),
 ('GA', 'georgia', 'Georgia', 'Georgia', ['Atlanta', 'Savannah', 'Macon', 'Augusta'], ['I-75', 'I-85', 'I-95', 'I-16', 'I-20'],
  ['the Port of Savannah', 'the Atlanta distribution corridor'], ['el Puerto de Savannah', 'el corredor de distribución de Atlanta']),
 ('TX', 'texas', 'Texas', 'Texas', ['Dallas', 'Houston', 'San Antonio', 'Laredo'], ['I-35', 'I-10', 'I-45', 'I-20', 'I-30'],
  ['the Laredo border crossings', 'the Port of Houston', 'the Dallas-Fort Worth hub'], ['los cruces fronterizos de Laredo', 'el Puerto de Houston', 'el centro de Dallas-Fort Worth']),
 ('IL', 'illinois', 'Illinois', 'Illinois', ['Chicago', 'Joliet', 'Rockford', 'Peoria'], ['I-80', 'I-55', 'I-57', 'I-90', 'I-94'],
  ['the Chicago freight hub', 'the Joliet intermodal yards'], ['el centro de carga de Chicago', 'los patios intermodales de Joliet']),
 ('OH', 'ohio', 'Ohio', 'Ohio', ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo'], ['I-70', 'I-71', 'I-75', 'I-77', 'I-80'],
  ['the Columbus distribution hub', 'the Toledo and Cleveland lake ports'], ['el centro de distribución de Columbus', 'los puertos de Toledo y Cleveland']),
 ('KY', 'kentucky', 'Kentucky', 'Kentucky', ['Louisville', 'Lexington', 'Bowling Green', 'Paducah'], ['I-65', 'I-64', 'I-75', 'I-71'],
  ['the Louisville air cargo hub', 'the Northern Kentucky distribution centers'], ['el centro de carga aérea de Louisville', 'los centros de distribución del norte de Kentucky']),
 ('MO', 'missouri', 'Missouri', 'Misuri', ['Kansas City', 'St. Louis', 'Springfield', 'Joplin'], ['I-70', 'I-44', 'I-55', 'I-29', 'I-35'],
  ['the Kansas City rail and truck hub', 'the St. Louis riverfront terminals'], ['el centro ferroviario y de camiones de Kansas City', 'las terminales de St. Louis']),
 ('MD', 'maryland', 'Maryland', 'Maryland', ['Baltimore', 'Hagerstown', 'Frederick', 'Salisbury'], ['I-95', 'I-70', 'I-81', 'I-68'],
  ['the Port of Baltimore', 'the Hagerstown I-81/I-70 crossroads'], ['el Puerto de Baltimore', 'el cruce de la I-81 y la I-70 en Hagerstown']),
]
# an older page already targets these exact searches: point the canonical there
CANONICAL_OVERRIDE = {
 ('truckers', 'florida'): '/truck-driver-health-insurance-florida',
 ('truckers', 'texas'): '/truck-driver-health-insurance-texas',
 ('es-camioneros', 'florida'): '/seguro-medico-camioneros-florida',
}

I = {
 'phone': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 'check': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg>',
 'map': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l-6 3V6l6-3 6 3 6-3v15l-6 3-6-3zM9 3v15M15 6v15"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
 'user': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a8 8 0 0 1 16 0v1"/></svg>',
 'clock': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'route': '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h8.5a3.5 3.5 0 0 0 0-7h-9a3.5 3.5 0 0 1 0-7H16"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}
GSVG = '<svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
CARRIERS = [('unitedhealthcare', 'UnitedHealthcare'), ('aetna', 'Aetna'), ('bluecross', 'Blue Cross Blue Shield'), ('cigna', 'Cigna'), ('anthem', 'Anthem')]

def join(items, es):
    items = list(items)
    if len(items) == 1: return items[0]
    return ', '.join(items[:-1]) + (' y ' if es else ' and ') + items[-1]

N = {
 'truckers': dict(lang='en', path='lp/truckers', pair='es-camioneros', quote='/trucking-health-quote', trucker=True,
   img='/compressed/trucker-woman-cab-window.webp', img2='/compressed/trucker-red-semi-cab-900.webp',
   alt='Truck driver smiling in the cab of her truck', alt2='Owner-operator standing beside his red semi truck',
   kicker='Truck Driver Health Insurance', h1='Truck Driver Health Insurance in {S}', h1all='Truck Driver Health Insurance',
   title='Truck Driver Health Insurance in {S} | Owner-Operator PPO Plans', titleall='Truck Driver Health Insurance | Owner-Operator PPO Plans',
   desc='Health insurance for truck drivers and owner-operators in {S}: private PPO plans with nationwide networks from top A-rated carriers. Free quote from a licensed advisor.',
   descall='Health insurance for truck drivers and owner-operators: private PPO plans with nationwide networks from top A-rated carriers. Free quote from a licensed advisor.',
   sub='Private PPO plans for owner-operators, lease operators, 1099 and company drivers, compared across top A-rated carriers. Free.',
   cards=[('map', 'Coverage that rides with you', 'Select PPO plans have doctors in all 50 states, so a clinic three states from home is still in network.'),
          ('shield', 'Top A-rated carriers', 'We line up the big names side by side and show you the real monthly price for your ZIP code.'),
          ('clock', 'Fast, even from the cab', 'Start a quote in about two minutes on your phone, then an advisor calls you back.'),
          ('user', 'One advisor, start to finish', 'The same licensed person handles your quote, paperwork and every renewal.')],
   statehead='Health coverage built for {S} drivers',
   statep=('Drivers based in {S} run {I} and work out of {H}. Long runs mean you need a plan that still works when you get sick far from home. '
           'We match {S} drivers with PPO plans that have broad networks in {C} and nationwide coverage on the road.'),
   stateall='We help drivers based in Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Missouri and Maryland find PPO plans with broad local networks and nationwide coverage on the road.',
   faq=[('How much does truck driver health insurance cost in {S}?', 'It depends on your age, ZIP code, who is on the plan and the plan you pick. Start a quote and a licensed advisor shows you real prices from several carriers for your {S} ZIP code, usually the same day.'),
        ('Will my plan work when I am on the road outside {S}?', 'Select PPO plans have doctors in all 50 states, so you can see a provider in another state without going out of network. We point those plans out for you.'),
        ('Can owner-operators in {S} get their own health insurance?', 'Yes. Owner-operators and lease operators can buy a private PPO plan for themselves and their family, with no employer needed.'),
        ('Is health insurance tax deductible for owner-operators?', 'Self-employed drivers can often deduct what they pay for health insurance. Ask your tax preparer how it applies to you.'),
        ('Do I pay you anything?', 'No. Carriers pay us. Your premium is the same as buying direct, and you get a licensed advisor for free.')],
   guides=[('/truck-driver-health-insurance', 'Truck driver health insurance guide'), ('/truck-driver-health-insurance-cost', 'What truck drivers pay for health insurance'),
           ('/best-health-insurance-owner-operators', 'Best health insurance for owner-operators'), ('/does-health-insurance-cover-dot-physical', 'Does insurance cover a DOT physical?')],
   other='Truck driver health insurance in other states', crumb='Truck Drivers'),
 'self-employed': dict(lang='en', path='lp/self-employed', pair='es-independientes', quote='/quote', trucker=False,
   img='/compressed/10-99working.webp', img2='/compressed/business-owner-office-640.webp',
   alt='Self-employed worker at her laptop', alt2='Small business owner smiling in his office',
   kicker='Self-Employed Health Insurance', h1='Self-Employed Health Insurance in {S}', h1all='Self-Employed Health Insurance',
   title='Self-Employed Health Insurance in {S} | 1099 & Freelancer PPO Plans', titleall='Self-Employed Health Insurance | 1099 & Freelancer PPO Plans',
   desc='Health insurance for self-employed, 1099 and freelance workers in {S}: private PPO plans from top A-rated carriers. Free quote from a licensed advisor.',
   descall='Health insurance for self-employed, 1099 and freelance workers: private PPO plans from top A-rated carriers. Free quote from a licensed advisor.',
   sub='Private PPO plans for 1099 workers, freelancers and one-person businesses, compared across top A-rated carriers. Free.',
   cards=[('user', 'Coverage without an employer', 'Contractors, gig workers and owners get a real major medical plan of their own.'),
          ('shield', 'Top A-rated carriers', 'We line up the big names side by side and show you the real monthly price for your ZIP code.'),
          ('map', 'Pick your own doctors', 'PPO plans let you see specialists without referrals, with nationwide options if you travel.'),
          ('clock', 'Quote in minutes', 'Start online in about two minutes, then an advisor walks you through your options.')],
   statehead='Health coverage for self-employed people in {S}',
   statep=('From {C}, more people in {S} work for themselves than ever: contractors, real estate agents, rideshare drivers, consultants and small business owners. '
           'Without an employer plan, you choose your own coverage. We compare PPO plans with strong {S} networks so you can keep the doctors you already see.'),
   stateall='We help self-employed people in Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Missouri and Maryland compare PPO plans with strong local networks.',
   faq=[('Can I get health insurance if I am self-employed in {S}?', 'Yes. Self-employed and 1099 workers in {S} can buy a private PPO plan for themselves and their family. We compare plans from several carriers for you.'),
        ('How much does self-employed health insurance cost in {S}?', 'It depends on your age, ZIP code, who is on the plan and the plan you pick. Start a quote and a licensed advisor shows you real prices for your {S} ZIP code, usually the same day.'),
        ('Is health insurance tax deductible for self-employed people?', 'Self-employed people can often deduct what they pay for health insurance. Ask your tax preparer how it applies to you.'),
        ('Can I add my spouse and kids?', 'Yes. Most plans let you cover your spouse and children on the same policy.'),
        ('Do I pay you anything?', 'No. Carriers pay us. Your premium is the same as buying direct, and you get a licensed advisor for free.')],
   guides=[('/self-employed-health-insurance', 'Self-employed health insurance guide'), ('/1099-health-insurance', 'Health insurance for 1099 workers'),
           ('/private-health-insurance', 'How private PPO health insurance works'), ('/ppo-health-insurance', 'PPO health insurance explained')],
   other='Self-employed health insurance in other states', crumb='Self-Employed'),
 'es-camioneros': dict(lang='es', path='lp/es/camioneros', pair='truckers', quote='/trucking-health-quote', trucker=True,
   img='/compressed/trucker-woman-cab-window.webp', img2='/compressed/trucker-red-semi-cab-900.webp',
   alt='Camionera sonriendo en la cabina de su camión', alt2='Owner-operator junto a su camión rojo',
   kicker='Seguro Médico para Camioneros', h1='Seguro Médico para Camioneros en {S}', h1all='Seguro Médico para Camioneros',
   title='Seguro Médico para Camioneros en {S} | Planes PPO', titleall='Seguro Médico para Camioneros | Planes PPO para Owner-Operators',
   desc='Seguro médico para camioneros y owner-operators en {S}: planes PPO privados con redes nacionales de las mejores aseguradoras. Cotización gratis en español.',
   descall='Seguro médico para camioneros y owner-operators: planes PPO privados con redes nacionales de las mejores aseguradoras. Cotización gratis en español.',
   sub='Planes PPO privados para owner-operators, choferes 1099 y de compañía, comparados entre las mejores aseguradoras. Gratis y en español.',
   cards=[('map', 'Cobertura que viaja con usted', 'Algunos planes PPO tienen médicos en los 50 estados: una clínica lejos de casa sigue en la red.'),
          ('shield', 'Aseguradoras con calificación A', 'Comparamos las principales y le mostramos el precio mensual real para su código postal.'),
          ('clock', 'Rápido, desde la cabina', 'Empiece su cotización en unos dos minutos y un asesor le devuelve la llamada.'),
          ('user', 'Un asesor que habla español', 'La misma persona con licencia le ayuda con la cotización, los trámites y cada renovación.')],
   statehead='Cobertura médica para choferes de {S}',
   statep=('Los choferes con base en {S} recorren la {I} y trabajan desde {H}. En viajes largos necesita un plan que funcione si se enferma lejos de casa. '
           'Le ayudamos a encontrar planes PPO con redes amplias en {C} y cobertura nacional en la carretera.'),
   stateall='Ayudamos a choferes en Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Misuri y Maryland a encontrar planes PPO con buenas redes locales y cobertura nacional.',
   faq=[('¿Cuánto cuesta el seguro médico para camioneros en {S}?', 'Depende de su edad, código postal, familia y el plan. Empiece su cotización y un asesor le muestra precios reales para su código postal de {S}, casi siempre el mismo día.'),
        ('¿Mi plan funciona fuera de {S}?', 'Algunos planes PPO tienen médicos en los 50 estados, así puede ver a un proveedor en otro estado sin salir de la red.'),
        ('¿Un owner-operator puede tener su propio seguro médico?', 'Sí. Los owner-operators pueden comprar un plan PPO privado para ellos y su familia, sin necesidad de un empleador.'),
        ('¿El seguro médico se puede deducir de impuestos?', 'Los choferes que trabajan por su cuenta a menudo pueden deducir lo que pagan. Consulte con su preparador de impuestos.'),
        ('¿Les pago algo?', 'No. Las aseguradoras nos pagan. Su prima es la misma que si compra directo, y recibe un asesor con licencia gratis.')],
   guides=[('/seguro-medico-camioneros', 'Guía de seguro médico para camioneros'), ('/seguro-medico-owner-operators', 'Seguro médico para owner-operators'),
           ('/costo-seguro-medico-camioneros', 'Cuánto cuesta el seguro para camioneros'), ('/examen-medico-dot', 'Examen médico DOT')],
   other='Seguro médico para camioneros en otros estados', crumb='Camioneros'),
 'es-independientes': dict(lang='es', path='lp/es/independientes', pair='self-employed', quote='/quote', trucker=False,
   img='/compressed/10-99working.webp', img2='/compressed/business-owner-office-640.webp',
   alt='Trabajadora independiente en su computadora', alt2='Dueño de negocio sonriendo en su oficina',
   kicker='Seguro Médico para Independientes', h1='Seguro Médico para Trabajadores Independientes en {S}', h1all='Seguro Médico para Trabajadores Independientes',
   title='Seguro Médico para Independientes en {S} | Planes PPO', titleall='Seguro Médico para Trabajadores Independientes | Planes PPO',
   desc='Seguro médico para trabajadores independientes y 1099 en {S}: planes PPO privados de las mejores aseguradoras. Cotización gratis con un asesor que habla español.',
   descall='Seguro médico para trabajadores independientes y 1099: planes PPO privados de las mejores aseguradoras. Cotización gratis con un asesor que habla español.',
   sub='Planes PPO privados para trabajadores 1099, freelancers y dueños de negocio, comparados entre las mejores aseguradoras. Gratis y en español.',
   cards=[('user', 'Cobertura sin empleador', 'Contratistas, trabajadores 1099 y dueños con un plan médico completo propio.'),
          ('shield', 'Aseguradoras con calificación A', 'Comparamos las principales y le mostramos el precio mensual real para su código postal.'),
          ('map', 'Escoja sus médicos', 'Con un PPO ve especialistas sin referidos, con opciones nacionales si viaja.'),
          ('clock', 'Cotización en minutos', 'Empiece en línea en unos dos minutos y un asesor le explica sus opciones en español.')],
   statehead='Cobertura médica para independientes en {S}',
   statep=('Desde {C}, cada vez más personas en {S} trabajan por su cuenta: contratistas, agentes de bienes raíces, choferes de aplicaciones y dueños de negocio. '
           'Sin un plan del empleador, usted escoge su cobertura. Comparamos planes PPO con buenas redes en {S} para que siga con sus médicos.'),
   stateall='Ayudamos a trabajadores independientes en Florida, Georgia, Texas, Illinois, Ohio, Kentucky, Misuri y Maryland a comparar planes PPO con buenas redes locales.',
   faq=[('¿Puedo tener seguro médico si trabajo por mi cuenta en {S}?', 'Sí. Los trabajadores independientes y 1099 en {S} pueden comprar un plan PPO privado para ellos y su familia.'),
        ('¿Cuánto cuesta el seguro médico para independientes en {S}?', 'Depende de su edad, código postal, familia y el plan. Empiece su cotización y un asesor le muestra precios reales para su código postal de {S}.'),
        ('¿El seguro médico se puede deducir de impuestos?', 'Los trabajadores independientes a menudo pueden deducir lo que pagan. Consulte con su preparador de impuestos.'),
        ('¿Puedo incluir a mi cónyuge e hijos?', 'Sí. La mayoría de los planes permite cubrir a su cónyuge e hijos en la misma póliza.'),
        ('¿Les pago algo?', 'No. Las aseguradoras nos pagan. Su prima es la misma que si compra directo, y recibe un asesor con licencia gratis.')],
   guides=[('/seguro-de-salud-miami', 'Seguro de salud en Miami'), ('/self-employed-health-insurance', 'Self-employed health insurance (English)'),
           ('/private-health-insurance', 'Private PPO plans (English)'), ('/1099-health-insurance', '1099 health insurance (English)')],
   other='Seguro médico para independientes en otros estados', crumb='Independientes'),
}

T = {
 'en': dict(call='Call', callfull='Talk to a licensed advisor', zipl='Enter your ZIP code', zipbtn='Get My Free Quote', ziperr='Please enter a 5-digit ZIP code.',
   zipnote='Free. No obligation. Takes about 2 minutes.', rating='5.0 from 53 Google reviews', lic='Licensed in 40+ states', free='100% free service',
   carriers='We compare plans from top A-rated carriers', why='Why {who} choose VS Health Benefits', whoT='drivers', whoS='self-employed people',
   how='How it works', steps=[('Enter your ZIP', 'Tell us where you live and who needs coverage.'), ('Compare real prices', 'A licensed advisor lines up plans from several A-rated carriers.'), ('Pick your plan', 'We handle the paperwork and you are covered.')],
   faqh='{S} questions', faqhall='Common questions', guidesh='Helpful guides', cta_h='Ready to see your price?', cta_p='Get a free quote in about 2 minutes, or call and talk it through.',
   hours='Mon-Fri 8am-6pm, Sat-Sun 8am-1pm ET', home='Home', routes='Major routes', hubs='Freight hubs', cities='Cities we serve',
   disc='VS BENEFITS LLC is a licensed independent insurance agency, not an insurance company, and is not affiliated with or endorsed by any government agency. We do not offer every plan available in your area. Prices depend on eligibility and are estimates, not quotes. Content is general information, not tax, legal or medical advice.',
   nav=[('/truck-driver-health-insurance', 'Truck Drivers'), ('/self-employed-health-insurance', 'Self-Employed'), ('/small-business-health-insurance', 'Small Business'), ('/about', 'About'), ('/contact', 'Contact')],
   foot=[('/privacy', 'Privacy Policy'), ('/terms', 'Terms'), ('/contact', 'Contact'), ('/about', 'About us')]),
 'es': dict(call='Llamar', callfull='Hable con un asesor con licencia', zipl='Escriba su código postal', zipbtn='Quiero Mi Cotización', ziperr='Escriba un código postal de 5 dígitos.',
   zipnote='Gratis. Sin compromiso. Toma unos 2 minutos.', rating='5.0 en 53 reseñas de Google', lic='Licencia en más de 40 estados', free='Servicio 100% gratis',
   carriers='Comparamos planes de las mejores aseguradoras', why='Por qué {who} escogen VS Health Benefits', whoT='los choferes', whoS='los independientes',
   how='Cómo funciona', steps=[('Escriba su código postal', 'Díganos dónde vive y quién necesita cobertura.'), ('Compare precios reales', 'Un asesor con licencia le muestra planes de varias aseguradoras.'), ('Escoja su plan', 'Nosotros hacemos los trámites y queda cubierto.')],
   faqh='Preguntas sobre {S}', faqhall='Preguntas frecuentes', guidesh='Guías útiles', cta_h='¿Listo para ver su precio?', cta_p='Cotización gratis en unos 2 minutos, o llame y hable con un asesor en español.',
   hours='Lun-vie 8am-6pm, sáb-dom 8am-1pm ET', home='Inicio', routes='Rutas principales', hubs='Centros de carga', cities='Ciudades que atendemos',
   disc='VS BENEFITS LLC es una agencia de seguros independiente con licencia, no una aseguradora, y no está afiliada ni respaldada por ninguna agencia del gobierno. No ofrecemos todos los planes disponibles en su área. Los precios dependen de la elegibilidad y son estimados, no cotizaciones. El contenido es información general, no asesoría fiscal, legal ni médica.',
   nav=[('/seguro-medico-camioneros', 'Camioneros'), ('/lp/es/independientes', 'Independientes'), ('/about', 'Nosotros'), ('/contact', 'Contacto')],
   foot=[('/privacy', 'Privacidad'), ('/terms', 'Términos'), ('/contact', 'Contacto'), ('/about', 'Nosotros')]),
}

COMP = {'truckers': ('What to compare before you pick a plan', [('Network reach outside {S}', 'Check that the plan has in-network doctors and urgent care along the routes you run, not just near home.'), ('Deductible vs. monthly premium', 'A lower premium usually means a higher deductible. Pick the balance that fits how often you see a doctor.'), ('Your prescriptions', "Blood pressure, diabetes and cholesterol medicines are common for drivers. Make sure yours are on the plan's drug list."), ('Who is on the plan', 'Adding a spouse or kids changes the price and the network you need. We price every option side by side.')]), 'self-employed': ('What to compare before you pick a plan', [('Your doctors in {S}', "Check that the doctors and hospitals you already use are in the plan's network."), ('Deductible and out-of-pocket max', 'These decide what a bad year costs you. Compare them, not just the monthly premium.'), ('Your prescriptions', "Make sure the medicines you take are on the plan's drug list and see what they cost."), ('When coverage starts', 'Private PPO plans accept applications year-round, and if approved, coverage can often start the first of next month.')]), 'es-camioneros': ('Qué comparar antes de escoger un plan', [('Red de médicos fuera de {S}', 'Revise que el plan tenga médicos y urgencias dentro de la red en las rutas que usted maneja, no solo cerca de casa.'), ('Deducible y prima mensual', 'Una prima más baja suele tener un deducible más alto. Escoja el balance que le convenga.'), ('Sus medicinas', 'Medicinas para la presión, la diabetes y el colesterol son comunes entre choferes. Revise que las suyas estén cubiertas.'), ('Quién está en el plan', 'Agregar a su cónyuge o hijos cambia el precio y la red que necesita. Comparamos cada opción.')]), 'es-independientes': ('Qué comparar antes de escoger un plan', [('Sus médicos en {S}', 'Revise que los médicos y hospitales que ya usa estén en la red del plan.'), ('Deducible y gasto máximo', 'Estos números deciden cuánto le cuesta un mal año. Compárelos, no solo la prima mensual.'), ('Sus medicinas', 'Revise que sus medicinas estén en la lista del plan y cuánto cuestan.'), ('Cuándo empieza la cobertura', 'Los planes PPO privados aceptan solicitudes todo el año y, si lo aprueban, la cobertura puede empezar el primero del próximo mes.')])}

CSS = r'''
:root{--navy:#0b2346;--navy2:#16447f;--blue:#1f6fe5;--blue-d:#1559c2;--teal:#0db5a6;--teal-d:#0b9b8e;--ink:#1f2933;--muted:#5a6b80;--line:#e3e8ee;--soft:#f5f8fc;--cream:#faf8f5}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;font-family:'DM Sans',system-ui,-apple-system,sans-serif;color:var(--ink);background:#fff;line-height:1.6}
img{max-width:100%;display:block}a{color:inherit}
h1,h2,h3{font-family:'Poppins',system-ui,sans-serif;line-height:1.15;margin:0;color:var(--navy);text-wrap:balance;letter-spacing:-.01em}
.wrap{max-width:1140px;margin:0 auto;padding:0 max(18px,env(safe-area-inset-left))}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.topbar{background:var(--navy);color:#fff;font-size:.8rem;font-weight:600}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:34px}
.topbar a{color:#fff;text-decoration:none}.topbar .r{display:flex;gap:18px}.topbar svg{color:#5eead4;vertical-align:-3px;margin-right:4px;width:14px;height:14px}
@media(max-width:640px){.topbar .mail,.topbar .l{display:none}.topbar .wrap{justify-content:center}}
.hd{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:66px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0}
.badge{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#16447f,#0db5a6);color:#fff;display:grid;place-items:center;font:800 .92rem 'Poppins',sans-serif}
.bname{font:700 1.04rem 'Poppins',sans-serif;color:var(--navy);white-space:nowrap}
.nav{display:none;gap:22px;font-weight:600;font-size:.94rem}.nav a{text-decoration:none;color:#334155}.nav a:hover{color:var(--navy2)}
@media(min-width:980px){.nav{display:flex}}
.hbtns{display:flex;gap:8px;align-items:center}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-weight:700;text-decoration:none;border-radius:999px;padding:11px 18px;white-space:nowrap;border:0;cursor:pointer;font-family:inherit;font-size:.95rem}
.btn-call{background:var(--teal);color:#fff;box-shadow:0 8px 20px -10px rgba(13,181,166,.8)}.btn-call:hover{background:var(--teal-d)}
.btn-q{background:var(--blue);color:#fff;box-shadow:0 10px 22px -12px rgba(31,111,229,.8)}.btn-q:hover{background:var(--blue-d)}
.hd .btn-q{display:none}@media(min-width:720px){.hd .btn-q{display:inline-flex}}
.hd .btn-call .n{display:none}@media(min-width:560px){.hd .btn-call .n{display:inline}.hd .btn-call .c{display:none}}
.crumbs{font-size:.82rem;color:var(--muted);padding:12px 0 0}.crumbs a{color:var(--navy2);text-decoration:none}.crumbs span{margin:0 6px;opacity:.5}
.hero{position:relative;background:var(--cream);overflow:hidden}
.hero .wrap{display:grid;gap:26px;padding-top:18px;padding-bottom:40px;align-items:center}
@media(min-width:960px){.hero .wrap{grid-template-columns:1.08fr .92fr;gap:48px;padding-top:26px;padding-bottom:60px}}
.kicker{display:inline-flex;align-items:center;gap:8px;font-size:.74rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--navy2);background:#fff;border:1px solid #dbe7f7;border-radius:999px;padding:6px 13px;margin-bottom:14px}
.kicker i{width:7px;height:7px;border-radius:50%;background:var(--teal)}
.hero h1{font-size:clamp(2rem,5.2vw,3.25rem)}
.hero h1 span{background:linear-gradient(90deg,#16447f,#0db5a6);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:1.1rem;color:#334155;margin:14px 0 20px;max-width:560px}
.zq{background:#fff;border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:0 24px 50px -30px rgba(11,35,70,.5);max-width:520px}
.zq label{display:block;font-weight:700;font-size:.9rem;color:var(--navy);margin:0 0 8px}
.zrow{display:flex;gap:8px}
.zrow input{flex:1 1 0;min-width:0;width:0;font:inherit;font-size:1.12rem;font-weight:600;letter-spacing:.06em;padding:13px 14px;border:1.5px solid #d5dde8;border-radius:12px;outline:none}
.zrow input:focus{border-color:var(--teal);box-shadow:0 0 0 3px rgba(13,181,166,.15)}
.zrow .btn{border-radius:12px;padding:13px 18px;font-size:1rem}
.znote{font-size:.84rem;color:var(--muted);margin:8px 0 0}.zerr{color:#b42318;font-size:.86rem;margin:8px 0 0}
.or{display:flex;align-items:center;gap:12px;margin:16px 0 0;flex-wrap:wrap}
.or a.ph{display:inline-flex;align-items:center;gap:8px;font-weight:700;color:var(--navy);text-decoration:none;font-size:1.02rem}
.or a.ph svg{color:var(--teal)}.or small{color:var(--muted);font-size:.84rem}
.rating{display:flex;align-items:center;gap:8px;margin-top:14px;font-size:.92rem;color:#475569;flex-wrap:wrap}
.rating .st{color:#f5a400;letter-spacing:1px}
.himg{position:relative}
.himg .ph1{border-radius:22px;overflow:hidden;aspect-ratio:4/3.4;box-shadow:0 30px 60px -30px rgba(11,35,70,.55)}
.himg .ph1 img{width:100%;height:100%;object-fit:cover}
.himg .chip{position:absolute;background:#fff;border-radius:14px;padding:10px 14px;box-shadow:0 16px 34px -14px rgba(11,35,70,.4);font-size:.8rem;font-weight:700;color:var(--navy);display:flex;gap:10px;align-items:center}
.himg .chip b{display:block;font-size:1.05rem;color:var(--teal-d)}
.himg .chip i{width:34px;height:34px;border-radius:10px;background:#e6f7f5;color:var(--teal-d);display:grid;place-items:center;flex-shrink:0}
.himg .c1{left:-14px;bottom:26px}.himg .c2{right:-10px;top:22px}
@media(max-width:959px){.himg{max-width:560px}.himg .c1{left:10px}.himg .c2{right:10px}}
.trust{background:#fff;border-bottom:1px solid var(--line)}
.trust .wrap{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 30px;padding:16px max(18px,env(safe-area-inset-left));font-weight:600;color:#334155;font-size:.93rem}
.trust span{display:inline-flex;align-items:center;gap:8px}.trust svg{color:var(--teal)}
.carriers{padding:26px 0 8px;text-align:center}
.carriers p{font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 14px}
.logos{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:18px 40px}
.logos img{height:30px;width:auto;object-fit:contain;filter:grayscale(1);opacity:.75}
.sec{padding:56px 0}.sec.soft{background:var(--soft)}
.sh{text-align:center;max-width:720px;margin:0 auto 30px}
.sh h2{font-size:clamp(1.55rem,3.6vw,2.2rem)}.sh p{color:#475569;margin:10px 0 0;font-size:1.04rem}
.eyb{display:inline-block;font-size:.74rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--teal-d);margin-bottom:8px}
.cards{display:grid;gap:16px}@media(min-width:700px){.cards{grid-template-columns:1fr 1fr}}@media(min-width:1040px){.cards{grid-template-columns:repeat(4,1fr)}}
.ben{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;transition:transform .2s,box-shadow .2s}
.ben:hover{transform:translateY(-3px);box-shadow:0 18px 36px -22px rgba(11,35,70,.4)}
.ben i{width:48px;height:48px;border-radius:14px;background:linear-gradient(135deg,#eaf2fd,#e6f7f5);color:var(--navy2);display:grid;place-items:center;margin-bottom:14px}
.ben h3{font-size:1.06rem;margin-bottom:6px}.ben p{margin:0;color:#475569;font-size:.95rem}
.split{display:grid;gap:30px;align-items:center}@media(min-width:900px){.split{grid-template-columns:1fr 1fr;gap:50px}}
.split .pic{border-radius:22px;overflow:hidden;aspect-ratio:4/3;box-shadow:0 26px 50px -28px rgba(11,35,70,.5)}.split .pic img{width:100%;height:100%;object-fit:cover}
.split h2{font-size:clamp(1.5rem,3.4vw,2.05rem);margin-bottom:12px}.split p{color:#334155;margin:0 0 18px;font-size:1.03rem}
.facts{display:grid;gap:12px}
.fact{display:flex;gap:12px;align-items:flex-start;background:var(--soft);border-radius:14px;padding:14px 16px}
.fact i{color:var(--navy2);flex-shrink:0;margin-top:2px}.fact b{display:block;color:var(--navy);font-size:.92rem}.fact span{color:#475569;font-size:.94rem}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}.tags em{font-style:normal;background:#fff;border:1px solid #dbe7f7;border-radius:999px;padding:3px 10px;font-size:.84rem;font-weight:700;color:var(--navy2)}
.cmp{display:grid;gap:14px;max-width:960px;margin:0 auto}@media(min-width:760px){.cmp{grid-template-columns:1fr 1fr}}
.cmp div{border-left:4px solid var(--teal);background:#fff;border-radius:0 14px 14px 0;padding:16px 18px;box-shadow:0 10px 24px -20px rgba(11,35,70,.4)}
.cmp h3{font-size:1.04rem;margin-bottom:4px}.cmp p{margin:0;color:#475569}
.steps{display:grid;gap:16px}@media(min-width:800px){.steps{grid-template-columns:repeat(3,1fr)}}
.step{background:#fff;border-radius:18px;padding:24px;border:1px solid var(--line);position:relative}
.step b{display:grid;place-items:center;width:40px;height:40px;border-radius:12px;background:var(--navy);color:#fff;font-family:'Poppins';margin-bottom:12px}
.step h3{font-size:1.06rem;margin-bottom:6px}.step p{margin:0;color:#475569}
.faq{max-width:800px;margin:0 auto}
.faq details{background:#fff;border:1px solid var(--line);border-radius:14px;padding:17px 20px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:700;color:var(--navy);list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";font-size:1.35rem;color:var(--navy2);font-weight:400;line-height:1}
.faq details[open] summary:after{content:"\2212"}.faq p{margin:10px 0 0;color:#334155}
.links{display:grid;gap:10px}@media(min-width:700px){.links{grid-template-columns:1fr 1fr}}
.links a{display:flex;justify-content:space-between;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-decoration:none;font-weight:700;color:var(--navy2)}
.links a:hover{border-color:var(--teal)}
.states{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:12px}
.states a{background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:8px 15px;font-weight:600;font-size:.92rem;text-decoration:none;color:#334155}
.states a:hover{border-color:var(--teal);color:var(--navy)}
.cta{background:linear-gradient(135deg,#0b2346,#16447f 60%,#0b7f74);color:#fff;text-align:center;padding:54px 0}
.cta h2{color:#fff;font-size:clamp(1.6rem,3.6vw,2.2rem);margin-bottom:8px}.cta p{color:rgba(255,255,255,.86);margin:0 0 22px;font-size:1.05rem}
.cta .row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.cta .btn{padding:15px 24px;font-size:1.04rem}.cta .btn-w{background:#fff;color:var(--navy)}
.ft{background:#081a35;color:rgba(255,255,255,.75);padding:34px 0;font-size:.84rem;line-height:1.6}
.ft .top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:18px;margin-bottom:16px}
.ft a{color:#fff;text-decoration:none}.ft .lk{display:flex;gap:16px;flex-wrap:wrap;font-weight:600}
.ft .bn{font:700 1.02rem 'Poppins',sans-serif;color:#fff}
@media(min-width:900px){.ft{padding-bottom:34px}}
.mbar{position:fixed;left:0;right:0;bottom:0;z-index:50;display:grid;grid-template-columns:1fr 1.3fr;gap:8px;padding:10px max(12px,env(safe-area-inset-left)) calc(10px + env(safe-area-inset-bottom));background:#fff;border-top:1px solid var(--line);box-shadow:0 -10px 26px -14px rgba(11,35,70,.35)}
.mbar .btn{border-radius:12px;padding:13px}
@media(min-width:900px){.mbar{display:none}}
'''

JS = r'''
(function(){
  var C=window.LPC||{};
  function carry(extra){
    var src=new URLSearchParams(location.search),o=new URLSearchParams();
    src.forEach(function(v,k){ if(/^(utm_|gclid|gbraid|wbraid|fbclid|msclkid)/i.test(k)) o.set(k,v); });
    Object.keys(extra).forEach(function(k){ if(extra[k]) o.set(k,extra[k]); });
    return C.quote+'?'+o.toString();
  }
  function base(z){ var e={from:C.from,state:C.state,zip:z||''}; if(!C.trucker) e.type='individual'; return e; }
  document.querySelectorAll('a[data-quote]').forEach(function(a){ a.href=carry(base('')); });
  var f=document.getElementById('zq'); if(!f) return;
  var zi=f.querySelector('input'), er=f.querySelector('.zerr');
  zi.addEventListener('input',function(){ zi.value=zi.value.replace(/\D/g,'').slice(0,5); er.hidden=true; });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var z=zi.value.trim();
    if(!/^\d{5}$/.test(z)){ er.hidden=false; zi.focus(); return; }
    try{ if(window.gtag) gtag('event','lp_zip_submit',{niche:C.niche,state:C.state||'all'}); }catch(x){}
    location.href=carry(base(z));
  });
})();
'''

def e(s): return html.escape(s, quote=True)
def url_for(nk, slug): return '/' + N[nk]['path'] + ('/' + slug if slug else '')

def page(nk, st):
    n = N[nk]; t = T[n['lang']]; es = n['lang'] == 'es'
    slug = st[1] if st else ''
    if st:
        code, _, en_name, es_name, cities, roads, hubs_en, hubs_es = st
        S = es_name if es else en_name
        h1 = n['h1'].format(S=S); title = n['title'].format(S=S); desc = n['desc'].format(S=S)
        statep = n['statep'].format(S=S, I=join(roads, es), H=join(hubs_es if es else hubs_en, es), C=join(cities, es))
        statehead = n['statehead'].format(S=S)
        faqh = t['faqh'].format(S=S)
        faqs = [(q.format(S=S), a.format(S=S)) for q, a in n['faq']]
    else:
        code = S = ''; cities = roads = []; hubs_en = hubs_es = []
        h1 = n['h1all']; title = n['titleall']; desc = n['descall']
        statep = n['stateall']; statehead = n['statehead'].replace(' {S}', '').replace(' en {S}', '').replace(' de {S}', '').replace(' in {S}', '')
        faqh = t['faqhall']
        faqs = [(q.replace(' en {S}', '').replace(' in {S}', '').replace(' fuera de {S}', ' en otros estados').replace(' outside {S}', ' in other states').format(S=''),
                 a.replace(' para su código postal de {S}', ' para su código postal').replace(' for your {S} ZIP code', ' for your ZIP code').replace(' en {S}', '').replace(' in {S}', '').format(S=''))
                for q, a in n['faq']]
    path = url_for(nk, slug)
    canon = SITE + CANONICAL_OVERRIDE.get((nk, slug), path)
    pair = url_for(n['pair'], slug)
    en_url, es_url = (path, pair) if not es else (pair, path)
    # headline: gradient on the state / last words
    if st:
        tail = (' en ' if es else ' in ') + S
        h1html = e(h1[:-len(tail)]) + ' <span>' + e(tail.strip()) + '</span>'
    else:
        w = h1.split(' '); h1html = e(' '.join(w[:-2])) + ' <span>' + e(' '.join(w[-2:])) + '</span>'
    who = t['whoT'] if n['trucker'] else t['whoS']
    cfg = {'state': code, 'niche': nk, 'quote': n['quote'], 'trucker': n['trucker'], 'from': 'lp-' + nk + ('-' + code.lower() if code else '')}
    crumbs = [(t['home'], '/'), (n['crumb'], url_for(nk, ''))] + ([(S, path)] if st else [])
    # structured data
    ld = [
      {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
         {'@type': 'ListItem', 'position': i + 1, 'name': nm, 'item': SITE + u} for i, (nm, u) in enumerate(crumbs)]},
      {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
         {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
      {'@context': 'https://schema.org', '@type': 'InsuranceAgency', 'name': 'VS Health Benefits', 'url': SITE + '/', 'telephone': '+1-954-825-1009',
       'image': SITE + n['img'], 'priceRange': 'Free consultation',
       'areaServed': ({'@type': 'State', 'name': en_name} if st else [{'@type': 'State', 'name': s[2]} for s in STATES]),
       'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '5.0', 'reviewCount': '53'}},
    ]
    # page pieces
    ch, citems = COMP[nk]
    SS = S or ('su estado' if es else 'your state')
    cmphtml = ''.join('<div><h3>%s</h3><p>%s</p></div>' % (e(h.format(S=SS)), e(p.format(S=SS))) for h, p in citems)
    cards = ''.join('<div class="ben"><i>%s</i><h3>%s</h3><p>%s</p></div>' % (I[i], e(h), e(p)) for i, h, p in n['cards'])
    steps = ''.join('<div class="step"><b>%d</b><h3>%s</h3><p>%s</p></div>' % (k + 1, e(h), e(p)) for k, (h, p) in enumerate(t['steps']))
    faqhtml = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in faqs)
    guides = ''.join('<a href="%s">%s<span aria-hidden="true">%s</span></a>' % (u, e(lbl), I['arrow']) for u, lbl in n['guides']
                     + ([(CANONICAL_OVERRIDE[(nk, slug)], (('Guía completa para ' if es else 'Full guide for ') + S))] if (nk, slug) in CANONICAL_OVERRIDE else []))
    states = ''.join('<a href="%s">%s</a>' % (url_for(nk, s[1]), e(s[3] if es else s[2])) for s in STATES if s[1] != slug)
    logos = ''.join('<img src="/images/carriers/%s.png" alt="%s" loading="lazy" decoding="async" height="30" />' % (f, e(a)) for f, a in CARRIERS)
    if st:
        facts = ('<div class="facts">'
          + ('<div class="fact"><i>%s</i><div><b>%s</b><div class="tags">%s</div></div></div>' % (I['route'], e(t['routes']), ''.join('<em>%s</em>' % r for r in roads)) if n['trucker'] else '')
          + ('<div class="fact"><i>%s</i><div><b>%s</b><span>%s</span></div></div>' % (I['map'], e(t['hubs']), e(join(hubs_es if es else hubs_en, es))) if n['trucker'] else '')
          + '<div class="fact"><i>%s</i><div><b>%s</b><span>%s</span></div></div>' % (I['pin'], e(t['cities']), e(join(cities, es) + (' y todo el estado' if es else ' and statewide')))
          + '</div>')
    else:
        facts = '<div class="states" style="justify-content:flex-start">%s</div>' % ''.join('<a href="%s">%s</a>' % (url_for(nk, s[1]), e(s[3] if es else s[2])) for s in STATES)
    crumbhtml = '<span>/</span>'.join(('<a href="%s">%s</a>' % (u, e(nm))) if i < len(crumbs) - 1 else e(nm) for i, (nm, u) in enumerate(crumbs))
    navhtml = ''.join('<a href="%s">%s</a>' % (u, e(l)) for u, l in t['nav'])
    foothtml = ''.join('<a href="%s">%s</a>' % (u, e(l)) for u, l in t['foot'])
    chip1 = ('5.0 &#9733;', 'Google' if not es else 'Google') ; chip2 = ('$0', 'nuestro costo' if es else 'our fee')
    return f'''<!DOCTYPE html>
<html lang="{n['lang']}">
<head>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());</script>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}" />
<meta name="robots" content="index,follow,max-image-preview:large" />
<link rel="canonical" href="{canon}" />
<link rel="alternate" hreflang="en-US" href="{SITE}{en_url}" />
<link rel="alternate" hreflang="es-US" href="{SITE}{es_url}" />
<link rel="alternate" hreflang="x-default" href="{SITE}{en_url}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(desc)}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{SITE}{n['img']}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet" />
<link rel="preload" as="image" href="{n['img']}" />
<style>{CSS}</style>
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)}
</head>
<body>
<div class="topbar"><div class="wrap"><span class="l">{I['shield']}{e(t['lic'])}</span><span class="r"><a href="{TEL}">{I['phone']}{PHONE}</a><a class="mail" href="mailto:info@vshealthbenefits.com">info@vshealthbenefits.com</a></span></div></div>
<header class="hd"><div class="wrap">
  <a class="brand" href="/" aria-label="VS Health Benefits home"><span class="badge">VS</span><span class="bname">VS Health Benefits</span></a>
  <nav class="nav" aria-label="Main">{navhtml}</nav>
  <div class="hbtns"><a class="btn btn-call" href="{TEL}">{I['phone']}<span class="c">{e(t['call'])}</span><span class="n">{PHONE}</span></a><a class="btn btn-q" href="{n['quote']}" data-quote>{e(t['zipbtn'])}</a></div>
</div></header>
<main>
<section class="hero">
  <div class="wrap" style="display:block;padding-bottom:0"><nav class="crumbs" aria-label="Breadcrumb">{crumbhtml}</nav></div>
  <div class="wrap">
    <div>
      <span class="kicker"><i></i>{e(n['kicker'])}</span>
      <h1>{h1html}</h1>
      <p class="sub">{e(n['sub'])}</p>
      <form class="zq" id="zq" novalidate>
        <label for="zq-zip">{e(t['zipl'])}</label>
        <div class="zrow"><input id="zq-zip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="ZIP" /><button class="btn btn-q" type="submit">{e(t['zipbtn'])}</button></div>
        <p class="zerr" role="alert" hidden>{e(t['ziperr'])}</p>
        <p class="znote">{e(t['zipnote'])}</p>
      </form>
      <div class="or"><a class="ph" href="{TEL}">{I['phone']}{PHONE}</a><small>{e(t['callfull'])} &middot; {e(t['hours'])}</small></div>
      <div class="rating">{GSVG}<span class="st" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><span>{e(t['rating'])}</span></div>
    </div>
    <div class="himg">
      <div class="ph1"><img src="{n['img']}" alt="{e(n['alt'])}" width="900" height="760" fetchpriority="high" decoding="async" /></div>
      <div class="chip c1"><i>{I['shield']}</i><span><b>{chip2[0]}</b>{chip2[1]}</span></div>
      <div class="chip c2"><i>{I['user']}</i><span><b>40+</b>{'estados' if es else 'states licensed'}</span></div>
    </div>
  </div>
</section>
<div class="trust"><div class="wrap"><span>{I['check']}{e(t['lic'])}</span><span>{I['check']}{e(t['rating'])}</span><span>{I['check']}{e(t['free'])}</span></div></div>
<section class="carriers"><div class="wrap"><p>{e(t['carriers'])}</p><div class="logos">{logos}</div></div></section>
<section class="sec"><div class="wrap">
  <div class="sh"><span class="eyb">VS Health Benefits</span><h2>{e(t['why'].format(who=who))}</h2></div>
  <div class="cards">{cards}</div>
</div></section>
<section class="sec soft"><div class="wrap split">
  <div class="pic"><img src="{n['img2']}" alt="{e(n['alt2'])}" width="900" height="675" loading="lazy" decoding="async" /></div>
  <div><span class="eyb">{e(S or ('8 estados' if es else '8 states'))}</span><h2>{e(statehead)}</h2><p>{e(statep)}</p>{facts}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sh"><h2>{e(ch)}</h2></div>
  <div class="cmp">{cmphtml}</div>
</div></section>
<section class="sec soft"><div class="wrap">
  <div class="sh"><h2>{e(t['how'])}</h2></div>
  <div class="steps">{steps}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sh"><h2>{e(faqh)}</h2></div>
  <div class="faq">{faqhtml}</div>
</div></section>
<section class="sec soft"><div class="wrap">
  <div class="sh"><h2>{e(t['guidesh'])}</h2></div>
  <div class="links">{guides}</div>
  <div class="sh" style="margin-top:34px;margin-bottom:0"><h3 style="font-size:1.1rem">{e(n['other'])}</h3><div class="states">{states}</div></div>
</div></section>
<section class="cta"><div class="wrap">
  <h2>{e(t['cta_h'])}</h2><p>{e(t['cta_p'])}</p>
  <div class="row"><a class="btn btn-q" href="{n['quote']}" data-quote>{e(t['zipbtn'])} {I['arrow']}</a><a class="btn btn-w" href="{TEL}">{I['phone']}{PHONE}</a></div>
</div></section>
</main>
<footer class="ft"><div class="wrap">
  <div class="top"><span class="bn">VS Health Benefits</span><div class="lk">{foothtml}</div></div>
  <p>{t['disc']}</p>
  <p>NPN 22116298 &middot; &copy; VS BENEFITS LLC &middot; <a href="{TEL}">{PHONE}</a></p>
</div></footer>
<script>window.LPC={json.dumps(cfg, ensure_ascii=False)};</script>
<script>{JS}</script>
<script src="/vs-attribution.js" defer></script>
<script src="/vs-conversions.js" defer></script>
<script src="/vs-lead-system.js" defer></script>
</body>
</html>
'''

def main():
    count = 0
    for nk, n in N.items():
        base = os.path.join(ROOT, n['path']); os.makedirs(base, exist_ok=True)
        open(os.path.join(base, 'index.html'), 'w', encoding='utf-8').write(page(nk, None)); count += 1
        for st in STATES:
            open(os.path.join(base, st[1] + '.html'), 'w', encoding='utf-8').write(page(nk, st)); count += 1
    print('wrote', count, 'landing pages')

if __name__ == '__main__':
    main()
