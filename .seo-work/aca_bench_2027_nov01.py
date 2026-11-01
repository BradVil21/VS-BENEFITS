# -*- coding: utf-8 -*-
"""2026-11-01: 2027 benchmark premiums in every ACA estimate tool.
Old: BASE21 = 375 everywhere (about $479/mo at age 40, nationwide).
New: KFF 2027 average benchmark (second-lowest silver) for a 40-year-old, BY STATE from the ZIP the visitor
enters; national $704 when there is no ZIP. Age 40 = 1.278 on the federal age curve, so base21 = bench40/1.278.
Source: KFF State Health Facts, Marketplace Average Benchmark Premiums (2027 data, checked Nov 1 2026)."""
import re
B40 = dict(AL=712,AK=1284,AZ=609,AR=757,CA=655,CO=615,CT=1005,DE=876,DC=678,FL=738,GA=733,HI=592,ID=553,IL=707,IN=537,IA=528,KS=748,KY=667,LA=730,ME=804,MD=491,MA=551,MI=595,MN=525,MS=814,MO=675,MT=889,NE=780,NV=565,NH=486,NJ=665,NM=725,NY=1041,NC=660,ND=610,OH=603,OK=686,OR=519,PA=648,RI=629,SC=702,SD=704,TN=796,TX=737,UT=716,VT=1313,VA=549,WA=768,WV=1185,WI=720,WY=1190)
ZIP3 = [(10,27,'MA'),(28,29,'RI'),(30,38,'NH'),(39,49,'ME'),(50,54,'VT'),(55,55,'MA'),(56,59,'VT'),(60,69,'CT'),(70,89,'NJ'),
 (100,149,'NY'),(150,196,'PA'),(197,199,'DE'),(200,200,'DC'),(201,201,'VA'),(202,205,'DC'),(206,219,'MD'),(220,246,'VA'),(247,268,'WV'),
 (270,289,'NC'),(290,299,'SC'),(300,319,'GA'),(320,349,'FL'),(350,369,'AL'),(370,385,'TN'),(386,397,'MS'),(398,399,'GA'),(400,427,'KY'),
 (430,459,'OH'),(460,479,'IN'),(480,499,'MI'),(500,528,'IA'),(530,549,'WI'),(550,567,'MN'),(570,577,'SD'),(580,588,'ND'),(590,599,'MT'),
 (600,629,'IL'),(630,658,'MO'),(660,679,'KS'),(680,693,'NE'),(700,714,'LA'),(716,729,'AR'),(730,749,'OK'),(750,799,'TX'),(800,816,'CO'),
 (820,831,'WY'),(832,838,'ID'),(840,847,'UT'),(850,865,'AZ'),(870,884,'NM'),(885,885,'TX'),(889,898,'NV'),(900,961,'CA'),(967,968,'HI'),
 (970,979,'OR'),(980,994,'WA'),(995,999,'AK')]
helper = ('/* 2027 benchmark (second-lowest silver) for a 40-year-old, by state. KFF, checked Nov 1 2026.\n'
  '     Estimate base = state benchmark / 1.278 (age 40 on the federal age curve); $704 national without a ZIP. */\n'
  '  var VS_B40=' + '{' + ','.join('%s:%d' % kv for kv in sorted(B40.items())) + '};\n'
  '  var VS_ZIP3=[' + ','.join('[%d,%d,"%s"]' % z for z in ZIP3) + '];\n'
  '  function vsState(z){z=String(z||"").replace(/\\D/g,"");if(z.length<3)return "";var p=parseInt(z.slice(0,3),10);for(var i=0;i<VS_ZIP3.length;i++){if(p>=VS_ZIP3[i][0]&&p<=VS_ZIP3[i][1])return VS_ZIP3[i][2];}return "";}\n'
  '  function vsBase21(){var el=document.getElementById("zip")||document.getElementById("tc-zip");var st=vsState(el&&el.value);return (VS_B40[st]||704)/1.278;}\n')
files = ['aca-subsidy-calculator.html','health-insurance-premium-increase-calculator.html','cobra-vs-marketplace-calculator.html',
         'owner-operator-subsidy-cliff-calculator.html','truck-driver-health-insurance-cost-calculator.html','ichra-vs-group-health-calculator.html']
for f in files:
    s = open(f, encoding='utf-8').read()
    if 'VS_B40' in s: print('skip', f); continue
    n0 = s.count('BASE21')
    if 'var INDIV_BASE21 = 375;' in s:
        s = s.replace('  var INDIV_BASE21 = 375;', '  ' + helper.strip('\n').replace('\n', '\n'), 1)
        s = s.replace('INDIV_BASE21*', 'vsBase21()*')
    elif 'var BASE21=375;' in s:
        s = s.replace('  var BASE21=375;', '  ' + helper.rstrip('\n'), 1)
    elif 'BASE21=375, ' in s:
        s = s.replace('BASE21=375, ', '', 1)
        s = s.replace('  var FPL_BASE=15960,', '  ' + helper + '  var FPL_BASE=15960,', 1)
    s = re.sub(r'(?<![A-Za-z_])BASE21\*', 'vsBase21()*', s)
    left = [l.strip()[:90] for l in s.split('\n') if re.search(r'(?<![A-Za-z_])(INDIV_)?BASE21(?![A-Za-z_(])', l) and not l.strip().startswith('//')]
    open(f, 'w', encoding='utf-8').write(s)
    print(f, n0, '-> leftover code refs:', left)
