#!/usr/bin/env python3
"""Tell Bing (and Yandex, Seznam, Naver via IndexNow) which pages changed.

Run AFTER the deploy is live:
    python3 _build/indexnow-ping.py                 # pages dated today in sitemap.xml
    python3 _build/indexnow-ping.py --all           # every URL in sitemap.xml
    python3 _build/indexnow-ping.py /quote /blog/x  # specific paths
Google does not use IndexNow; it reads sitemap.xml (resubmit it in Search Console).
"""
import datetime, json, os, re, sys, urllib.request

KEY = 'f8abf33e1b0ea59e12a678da74ad0941'
HOST = 'www.vshealthbenefits.com'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def sitemap_rows():
    s = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    return re.findall(r'<loc>(.*?)</loc><lastmod>(.*?)</lastmod>', s)

args = sys.argv[1:]
if '--all' in args:
    urls = [u for u, _ in sitemap_rows()]
elif args:
    urls = ['https://' + HOST + (a if a.startswith('/') else '/' + a) for a in args]
else:
    today = datetime.date.today().isoformat()
    urls = [u for u, d in sitemap_rows() if d == today]
urls = sorted(set(urls))
if not urls:
    sys.exit('No URLs to send (nothing in sitemap.xml is dated today). Use --all or pass paths.')

# key file must be live first, or the engines reject the ping
try:
    live = urllib.request.urlopen('https://%s/%s.txt' % (HOST, KEY), timeout=15).read().decode().strip()
    if live != KEY: sys.exit('Key file is live but does not match. Deploy first.')
except Exception as e:
    sys.exit('Key file not reachable yet (%s). Push and wait for the deploy, then run again.' % e)

body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': 'https://%s/%s.txt' % (HOST, KEY), 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    r = urllib.request.urlopen(req, timeout=30)
    print('IndexNow accepted %d URL(s): HTTP %s' % (len(urls), r.status))
except urllib.error.HTTPError as e:
    print('IndexNow HTTP %s: %s' % (e.code, e.read().decode()[:300]))
for u in urls[:20]: print('  ', u)
if len(urls) > 20: print('   ... and %d more' % (len(urls) - 20))
