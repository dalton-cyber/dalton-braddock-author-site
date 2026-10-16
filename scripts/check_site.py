#!/usr/bin/env python3
"""Check the static site's local links, metadata, structured data and sitemap."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://dalton-cyber.github.io/dalton-braddock-author-site/'
PAGES = ('index.html', 'about.html', 'books.html', 'contact.html')

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.meta, self.structured = path, set(), [], {}, []
        self.h1, self.current, self.canonical = 0, 0, None
        self.json_data, self.in_json, self.title = '', False, ''
        self.in_title = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'{self.path.name}: duplicate id {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.in_title = True
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a['href']
        if tag == 'a' and a.get('aria-current') == 'page': self.current += 1
        for key in ('href', 'src'):
            if key in a: self.links.append(a[key])
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_json, self.json_data = True, ''

    def handle_data(self, data):
        if self.in_json: self.json_data += data
        if self.in_title: self.title += data

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script' and self.in_json:
            self.structured.append(json.loads(self.json_data))
            self.in_json = False

pages = {name: Page(ROOT / name) for name in PAGES}
titles, descriptions = set(), set()
for name, page in pages.items():
    assert page.h1 == 1, f'{name}: expected one h1'
    assert page.title and page.title not in titles, f'{name}: missing or duplicate title'
    titles.add(page.title)
    desc = page.meta.get('description')
    assert desc and desc not in descriptions, f'{name}: missing or duplicate description'
    descriptions.add(desc)
    assert page.canonical == BASE + ('' if name == 'index.html' else name)
    assert page.meta.get('robots') == 'index,follow'
    assert page.structured and page.current == 2  # header and footer
    assert 'main' in page.ids
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        target = unquote(url.path) or name
        file = ROOT / target
        assert file.is_file(), f'{name}: missing local target {link}'
        if url.fragment:
            assert target in pages and url.fragment in pages[target].ids, f'{name}: missing anchor {link}'
    for data in page.structured:
        assert data['@context'] == 'https://schema.org'
        assert any(item['@type'] == 'Person' for item in data['@graph'])
book_data = next(x for x in pages['books.html'].structured[0]['@graph'] if x['@type'] == 'ItemList')
assert len(book_data['itemListElement']) == 4
assert all(x['item']['sameAs'].startswith('https://www.amazon.com/dp/') for x in book_data['itemListElement'])
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = {x.text for x in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)}
assert urls == {p.canonical for p in pages.values()}
assert f'Sitemap: {BASE}sitemap.xml' in (ROOT / 'robots.txt').read_text()
assert (ROOT / 'assets/social-card.png').is_file()
assert (ROOT / '.nojekyll').is_file()
print('PASS: four pages; unique SEO metadata; local links/assets/anchors; author and four book records; sitemap and robots.txt.')
