#!/usr/bin/env python3
"""Build /search-index.json for the site search (vs-search.js).

Run from the site folder after adding or editing pages:
    python3 _build/build-search-index.py

Indexes every public .html page except: pages marked noindex, pages whose
canonical points somewhere else, URLs that vercel.json redirects away, private
tools (admin, client, census), and (while EXCLUDE_ACA is True) ACA/subsidy pages.
"""
import json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXCLUDE_ACA = True
ACA_RE = re.compile(r'\b(aca|obamacare|subsid\w*|marketplace|open[- ]enrollment|inscripci[oó]n)\b', re.I)
SKIP_DIRS = {'_to_delete', 'node_modules', '.seo-work', '_build', 'ghl', 'ghl-email-templates',
             'google-ads', 'contractor-outreach', 'Claude outputs', 'restaurant-list', '.git', 'api', 'data'}
SKIP_FILES = {'admin.html', 'client.html', 'census.html', '404.html'}
SITE = 'https://www.vshealthbenefits.com'


class Page(HTMLParser):
    SKIP = {'script', 'style', 'svg', 'noscript', 'header', 'nav', 'footer', 'form', 'template'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''; self.desc = ''; self.robots = ''; self.canon = ''
        self.h1 = ''; self.heads = []; self.text = []
        self._skip = 0; self._in = None; self._buf = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'meta':
            n = (a.get('name') or '').lower()
            if n == 'description' and not self.desc: self.desc = a.get('content') or ''
            if n == 'robots': self.robots = (a.get('content') or '').lower()
        elif tag == 'link' and (a.get('rel') or '').lower() == 'canonical':
            self.canon = a.get('href') or ''
        if tag in self.SKIP: self._skip += 1
        if tag in ('title', 'h1', 'h2', 'h3') and not self._skip:
            self._in = tag; self._buf = []

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip: self._skip -= 1
        if tag == self._in:
            t = ' '.join(''.join(self._buf).split())
            if tag == 'title': self.title = self.title or t
            elif tag == 'h1': self.h1 = self.h1 or t
            elif t: self.heads.append(t)
            self._in = None

    def handle_data(self, d):
        if self._in == 'title': self._buf.append(d); return
        if self._skip: return
        if self._in: self._buf.append(d)
        self.text.append(d)


def clean_url(rel):
    rel = rel.replace(os.sep, '/')
    if rel == 'index.html': return '/'
    if rel.endswith('/index.html'): return '/' + rel[:-11]
    return '/' + rel[:-5]


def kind(u, t):
    s = (u + ' ' + t).lower()
    if u.startswith('/blog/'): return 'Blog'
    if re.search(r'calculator|checker|finder', s): return 'Tool'
    if re.search(r'truck|trucker|cdl|owner-operator|owner operator|dot physical|camioner|examen-medico', s): return 'Truck drivers'
    if re.search(r'dental|vision', s): return 'Dental & vision'
    if re.search(r'small-business|small business|group|employer|employees|contractors|companies|industry', s): return 'Small business'
    if re.search(r'^/health-insurance-[a-z-]+$', u) and 'for' not in u: return 'By state'
    return 'Coverage'


def main():
    redirects = set()
    try:
        v = json.load(open(os.path.join(ROOT, 'vercel.json'), encoding='utf-8'))
        for r in v.get('redirects', []):
            src = r.get('source', '')
            if src and not re.search(r'[:*(]', src): redirects.add(src.rstrip('/') or '/')
    except Exception as e:
        print('warning: could not read vercel.json redirects:', e)

    out, skipped = [], {}
    for dp, dns, fns in os.walk(ROOT):
        rel_dir = os.path.relpath(dp, ROOT)
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in fns:
            if not fn.endswith('.html') or fn in SKIP_FILES: continue
            rel = os.path.normpath(os.path.join(rel_dir, fn))
            u = clean_url(rel)
            p = Page()
            try:
                p.feed(open(os.path.join(dp, fn), encoding='utf-8', errors='ignore').read())
            except Exception:
                continue
            why = None
            if 'noindex' in p.robots: why = 'noindex'
            elif u in redirects: why = 'redirected'
            elif p.canon:
                cpath = re.sub(r'^https?://[^/]+', '', p.canon).split('?')[0].split('#')[0].rstrip('/') or '/'
                if cpath.endswith('.html'): cpath = cpath[:-5]
                if cpath != u: why = 'canonical elsewhere'
            title = re.sub(r'\s*[|–—-]\s*VS Health Benefits.*$', '', p.title).strip() or p.h1
            if not why and EXCLUDE_ACA and ACA_RE.search(u.replace('-', ' ') + ' ' + title): why = 'ACA'
            if not why and not title: why = 'no title'
            if why:
                skipped[why] = skipped.get(why, 0) + 1
                continue
            body = ' '.join(' '.join(p.text).split())
            out.append({
                'u': u, 't': title, 'k': kind(u, title),
                'd': p.desc.strip()[:240],
                'h': ' | '.join(([p.h1] if p.h1 else []) + p.heads)[:500],
                'b': body[:900],
            })
    out.sort(key=lambda x: (x['u'] != '/', x['u'].startswith('/blog/'), x['u']))
    with open(os.path.join(ROOT, 'search-index.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    size = os.path.getsize(os.path.join(ROOT, 'search-index.json'))
    print(f'indexed {len(out)} pages ({size // 1024} KB); skipped {skipped}')


if __name__ == '__main__':
    main()
