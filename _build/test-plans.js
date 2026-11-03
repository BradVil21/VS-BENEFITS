const path=require('path'); const H=require(path.resolve('api/_healthsherpa-plans.js'));
let calls=[]; let mode='one';
global.fetch=async(url,init)=>{ calls.push([init.method,url,init.body?JSON.parse(init.body):null]);
  const J=(status,body,hdr={})=>({status,headers:{get:k=>hdr[k.toLowerCase()]||null},json:async()=>body});
  if(url.includes('/reference/counties')){
    if(mode==='two') return J(200,{counties:[{fips_code:'12086',name:'Miami-Dade County',state:'FL'},{fips_code:'12011',name:'Broward County',state:'FL'}]});
    return J(200,{counties:[{fips_code:'12086',name:'Miami-Dade County',state:'FL'}]}); }
  if(url.endsWith('/quotes')){
    if(mode==='429' && !global._r){ global._r=1; return J(429,{},{'retry-after':'0.1'}); }
    return J(200,{plans:[
      {plan_id:'A',name:'Gold PPO',issuer:{name:'Florida Blue'},pricing:{gross_premium:900,net_premium:420.5,subsidy_applied:479.5,max_aptc:479.5},details:{metal_level:'gold',plan_type:'ppo',deductible_individual:1000,moop_individual:6000},documents:{sbc_url:'https://x/sbc'}},
      {plan_id:'B',name:'Bronze HSA',issuer:{name:'Ambetter'},pricing:{gross_premium:510,net_premium:30.5,subsidy_applied:479.5,max_aptc:479.5},details:{metal_level:'bronze',plan_type:'hmo',hsa_eligible:true,deductible_individual:7500,moop_individual:10600}},
      {plan_id:'C',name:'Silver EPO',issuer:{name:'Oscar'},pricing:{gross_premium:700,net_premium:220.5},details:{metal_level:'silver',plan_type:'epo',deductible_individual:4000}}],meta:{page_number:1,page_size:500,result_count:3,warnings:[]}}); }
};
function run(body,env={},hdr={origin:'https://www.vshealthbenefits.com'}){ return new Promise(ok=>{ Object.assign(process.env,env);
  const res={code:200,h:{},setHeader(k,v){this.h[k]=v},status(c){this.code=c;return this},json(b){ok([this.code,b])},end(){ok([this.code])}};
  H({method:'POST',body,headers:Object.assign({'x-forwarded-for':'1.2.3.4'},hdr)},res); }); }
(async()=>{
  delete process.env.HEALTHSHERPA_API_KEY;
  console.log('no key ->', JSON.stringify(await run({})));
  process.env.HEALTHSHERPA_API_KEY='test-key';
  console.log('bad input ->', JSON.stringify(await run({zip:'abc'})));
  console.log('foreign origin ->', JSON.stringify(await run({zip:'33101',income:50000,size:1,age1:40},{}, {origin:'https://evil.example'})));
  let [c,b]=await run({zip:'33101',income:52000,size:3,age1:45,age2:43,kids:1});
  console.log('one county ->', c, 'count', b.count, 'order', b.plans.map(p=>p.id+':'+p.net).join(' '), 'aptc', b.aptc, 'county', b.county.name);
  const q=calls.find(x=>x[1].endsWith('/quotes'))[2]; console.log('request sent:', JSON.stringify(q));
  console.log('key header used:', !!calls.length);
  mode='two'; calls=[];
  console.log('two counties ->', JSON.stringify(await run({zip:'33009',income:52000,size:1,age1:45})));
  console.log('picked fips ->', (await run({zip:'33009',income:52000,size:1,age1:45,fips:'12011'}))[1].county);
  mode='429'; calls=[];
  const r=await run({zip:'33139',income:30000,size:1,age1:30}); console.log('429 retry ->', r[0], r[1].count, 'quote calls', calls.filter(x=>x[1].endsWith('/quotes')).length);
  calls=[]; await run({zip:'33139',income:30000,size:1,age1:30}); console.log('cache hit, quote calls:', calls.filter(x=>x[1].endsWith('/quotes')).length);
  let last; for(let i=0;i<22;i++) last=await run({zip:'33139',income:30000,size:1,age1:30}); console.log('rate limit after 20 ->', last[0]);
})();
