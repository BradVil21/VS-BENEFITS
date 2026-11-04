/* IndexNow: tells Bing (which feeds ChatGPT search and Copilot), Yandex, Seznam and Naver
   about new or changed pages right away instead of waiting for a crawl.
   Run in Terminal AFTER a push has deployed:
     node indexnow.js                      -> sends every URL in sitemap.xml
     node indexnow.js /private-health-insurance /llms.txt   -> sends only these
   Key file (must stay at the site root): /f8abf33e1b0ea59e12a678da74ad0941.txt */
const fs = require('fs');
const https = require('https');
const HOST = 'www.vshealthbenefits.com';
const KEY = 'f8abf33e1b0ea59e12a678da74ad0941';
let urls = process.argv.slice(2).map(p => 'https://' + HOST + (p.startsWith('/') ? p : '/' + p));
if (!urls.length) {
  const xml = fs.readFileSync(__dirname + '/sitemap.xml', 'utf8');
  urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].trim()).filter(u => u.includes(HOST));
}
const body = JSON.stringify({ host: HOST, key: KEY, keyLocation: 'https://' + HOST + '/' + KEY + '.txt', urlList: urls.slice(0, 10000) });
const req = https.request({ hostname: 'api.indexnow.org', path: '/indexnow', method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) } }, res => {
  let d = ''; res.on('data', c => d += c);
  res.on('end', () => {
    const ok = res.statusCode === 200 || res.statusCode === 202;
    console.log((ok ? 'OK ' : 'FAILED ') + res.statusCode + ' - sent ' + urls.length + ' URL(s)' + (d ? ': ' + d : ''));
    if (res.statusCode === 403) console.log('Key file not found on the live site. Check https://' + HOST + '/' + KEY + '.txt');
    if (res.statusCode === 422) console.log('A URL is not on ' + HOST + ' or the key does not match.');
  });
});
req.on('error', e => console.log('Network error: ' + e.message));
req.end(body);
