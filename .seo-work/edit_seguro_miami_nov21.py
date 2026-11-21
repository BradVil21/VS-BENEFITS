# -*- coding: utf-8 -*-
"""seguro-de-salud-miami (2026-11-21): match 'seguros médicos' searches, 2027 prices
and income limits in Spanish, Cigna exit, fuller FAQ + schema."""
import re, json, html
P = "seguro-de-salud-miami.html"
s = open(P, encoding="utf-8").read()
def ed(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)

ed('<h1>Seguro de Salud Asequible en <span>Miami y Florida</span></h1>',
   '<h1>Seguros Médicos en Miami: <span>Planes de Salud 2027</span></h1>')
ed('Florida Blue, UnitedHealthcare, Aetna, Cigna, Molina, y otros.',
   'Florida Blue, Ambetter, Oscar, UnitedHealthcare, Aetna, Molina y otros. Cigna dejó de vender planes individuales en Florida para 2027.')

TS = 'style="width:100%;border-collapse:collapse;font-size:.93rem"'
TH = 'style="text-align:left;padding:10px 12px;background:#0b2346;color:#fff"'
TD = 'style="padding:10px 12px;border-bottom:1px solid #e4e9f2"'
def table(head, rows):
    h = '<div style="overflow-x:auto;margin:14px 0 6px"><table %s><thead><tr>%s</tr></thead><tbody>' % (TS, "".join('<th %s>%s</th>' % (TH, x) for x in head))
    return h + "".join("<tr>" + "".join('<td %s>%s</td>' % (TD, c) for c in r) + "</tr>" for r in rows) + "</tbody></table></div>"

COST = '''
<!-- PRECIOS 2027 -->
<section class="section" id="precios-2027">
  <div class="container" style="max-width:860px">
    <div class="center" style="margin-bottom:22px"><span class="eyebrow">Precios 2027</span>
      <h2>¿Cuánto Cuesta un Seguro Médico en Miami en 2027?</h2></div>
    <p>Lo que usted paga depende sobre todo de sus <strong>ingresos</strong>. Con un plan del mercado (Obamacare), el gobierno limita cuánto paga por el plan Silver de referencia según sus ingresos, y el crédito fiscal paga el resto. Estos son los límites para <strong>una persona</strong> en 2027:</p>
    %s
    <p style="font-size:.85rem;color:#5a6b80">Cifras de 2027 para una persona. Los precios reales en Miami-Dade y Broward dependen de su edad, código postal y el plan que escoja.</p>
    <h3 style="margin-top:28px">Límites de ingresos 2027 para recibir subsidio</h3>
    <p>Califica para un crédito fiscal si sus ingresos del hogar están entre el 100%% y el 400%% del nivel federal de pobreza. Por encima del 400%% no hay subsidio, y ahí es donde un PPO privado muchas veces cuesta menos.</p>
    %s
    <h3 style="margin-top:28px">Lo que cambió para 2027 en Miami</h3>
    <ul>
      <li><strong>Cigna se fue.</strong> Cigna dejó de vender planes individuales y familiares en Florida para 2027. Si tenía Cigna, tiene que escoger un plan nuevo. <a href="/blog/mejores-seguros-medicos-miami-2027">Vea las mejores compañías en Miami para 2027</a>.</li>
      <li><strong>Volvió el límite del 400%%.</strong> Los subsidios ampliados terminaron, así que una familia que gana un poco más del límite puede perder todo el crédito fiscal.</li>
      <li><strong>Primas más altas.</strong> Muchas personas recibieron avisos de renovación con aumentos grandes. Comparar antes del 15 de diciembre es la manera más fácil de bajar el costo.</li>
    </ul>
    <p style="text-align:center;margin-top:22px"><a class="btn btn-primary" href="/quote?type=individual&amp;from=seguro-de-salud-miami_precios">Ver mi precio exacto gratis</a></p>
  </div>
</section>
''' % (
  table(["Ingresos (1 persona)", "Máximo de sus ingresos", "Lo máximo que paga por el plan Silver"], [
    ["Hasta $15,960", "2.15%", "$29 al mes"], ["$23,940", "4.30%", "$86 al mes"], ["$31,920", "6.78%", "$180 al mes"],
    ["$39,900", "8.66%", "$288 al mes"], ["$47,880", "10.22%", "$408 al mes"], ["$63,840", "10.22%", "$544 al mes"],
    ["Más de $63,840", "Sin límite", "Precio completo (sin subsidio)"]]),
  table(["Personas en el hogar", "Mínimo (100%)", "Máximo (400%)"], [
    ["1", "$15,960", "$63,840"], ["2", "$21,640", "$86,560"], ["3", "$27,320", "$109,280"], ["4", "$33,000", "$132,000"], ["5", "$38,680", "$154,720"]]))
ed("\n<!-- INSCRIPCION ABIERTA 2027 -->", COST + "\n<!-- INSCRIPCION ABIERTA 2027 -->")

NEWQ = [
 ("¿Es lo mismo seguro médico que seguro de salud?", "Sí. Seguro médico, seguro de salud y plan médico se refieren a lo mismo: una póliza que paga sus visitas al médico, hospital, recetas y emergencias. En Miami también se dice Obamacare para los planes del mercado ACA."),
 ("¿Cuál es el mejor seguro médico en Miami?", "Depende de sus médicos, sus ingresos y su presupuesto. Florida Blue tiene la red más amplia en el sur de Florida, mientras que Ambetter y Oscar suelen tener primas más bajas con redes más pequeñas. Comparamos todas las compañías por usted y verificamos que sus médicos estén en la red. Vea nuestra guía de los mejores seguros médicos en Miami 2027."),
]
ed('    <div class="faq">\n', '    <div class="faq">\n' + "".join('      <details class="faq-item"><summary>%s</summary><p>%s</p></details>\n' % q for q in NEWQ))

# FAQ schema = every question on the page
qs = re.findall(r'<details class="faq-item"><summary>(.*?)</summary><p>(.*?)</p></details>', s, re.S)
clean = lambda t: html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
m = re.search(r'<script type="application/ld\+json">\s*(\{[^<]*"@type": *"FAQPage".*?)\s*</script>', s, re.S)
d = json.loads(m.group(1))
d["mainEntity"] = [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qs]
s = s.replace(m.group(1), json.dumps(d, ensure_ascii=False))
ed("<h2>Preguntas Sobre Seguro de Salud en Miami y Florida</h2>", "<h2>Preguntas Sobre Seguros Médicos en Miami</h2>")
assert "Cigna, Molina" not in s
open(P, "w", encoding="utf-8").write(s)
print("ok", len(qs), "faqs")
