#!/usr/bin/env python3
"""Build a standalone report from trusted local authoring files. Python 3.9+."""
import argparse
import base64
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

MIMES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
         '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml'}


def text(value):
    return escape(str(value), quote=True)


def link(url, label):
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc:
        raise ValueError(f'Expected HTTP(S) source URL: {url}')
    return f'<a href="{text(url)}" target="_blank" rel="noopener noreferrer">{text(label)}</a>'


def picture(root, item):
    assets = (root / 'assets').resolve()
    path = (assets / item['file']).resolve()
    if assets not in path.parents:
        raise ValueError(f'Asset escapes assets directory: {item["file"]}')
    if path.suffix.lower() not in MIMES:
        raise ValueError(f'Unsupported image: {path.name}')
    width, height = int(item['width']), int(item['height'])
    if width <= 0 or height <= 0:
        raise ValueError('Image dimensions must be positive')
    raw = path.read_bytes()
    if path.suffix.lower() == '.svg':
        svg = raw.decode('utf-8')
        if re.search(r'<(?:script|foreignObject)\b|\bon\w+\s*=|(?:href|url)\s*[=(]|@import|<!ENTITY', svg, re.I):
            raise ValueError('SVG must be a static, self-contained image without resource references')
    encoded = base64.b64encode(raw).decode('ascii')
    src = f'data:{MIMES[path.suffix.lower()]};base64,{encoded}'
    alt = item.get('alt', item['title'] + '：完整标题与摘要截图')
    caption = item.get('desc', item.get('crop', ''))
    return (f'<button type="button" class="zoom" data-title="{text(item["title"])}" '
            f'data-caption="{text(caption)}" aria-label="放大：{text(item["title"])}">'
            f'<img src="{src}" width="{width}" height="{height}" alt="{text(alt)}" loading="lazy">'
            '<span>点击放大 ↗</span></button>')


class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.errors, self.images = set(), [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append('Duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href', '').startswith('#') and len(a['href']) > 1:
            self.refs.append(a['href'][1:])
        if tag == 'img' and a.get('id') != 'modal-image':
            self.images += 1
            if not a.get('alt') or not a.get('width') or not a.get('height'):
                self.errors.append('Image missing alt or dimensions')
            if not a.get('src', '').startswith('data:image/') or a.get('srcset'):
                self.errors.append('Image is not fully embedded')
        if tag == 'script' and a.get('src'):
            self.errors.append('External script')
        if tag == 'link' and a.get('rel') in ('stylesheet', 'preload', 'modulepreload'):
            self.errors.append('External stylesheet or preload')
        if tag in ('iframe', 'video', 'audio', 'source', 'object', 'embed'):
            self.errors.append('Unsupported embedded media: ' + tag)


def build(root):
    source = root / 'source'
    html = (source / 'article.template.html').read_text(encoding='utf-8')
    css = (source / 'style.css').read_text(encoding='utf-8')
    js = (source / 'app.js').read_text(encoding='utf-8')
    if re.search(r'@import|url\(', css, re.I):
        raise ValueError('Starter compiler requires CSS without external resource references')
    if re.search(r'</style\s*>', css, re.I) or re.search(r'</script\s*>', js, re.I):
        raise ValueError('Unsafe closing tag in inline asset')
    figures = json.loads((root / 'figures.json').read_text(encoding='utf-8'))
    papers = json.loads((root / 'papers.json').read_text(encoding='utf-8'))
    for key, item in figures.items():
        marker = f'<figure data-figure="{key}"></figure>'
        if html.count(marker) != 1:
            raise ValueError(f'Figure {key} must occur exactly once')
        credit = text(item['credit']) + ' · ' + text(item['rights'])
        if item.get('url'):
            credit += ' · ' + link(item['url'], '原文 / 图源')
        elif item['rights'] != '原创示意':
            raise ValueError('A sourced figure needs a URL')
        body = (f'<figure id="fig-{text(key)}">' + picture(root, item) +
                f'<figcaption><b>{text(item["title"])}</b><p>{text(item["desc"])}</p>' +
                f'<small>{credit}</small></figcaption></figure>')
        html = html.replace(marker, body)
    cards = []
    for item in papers:
        cards.append(f'<article class="paper-card" id="paper-{text(item["id"])}">'
                     f'<small>{text(item["date"])}</small><h3>{text(item["title"])}</h3>'
                     f'<p class="muted">{text(item["authors"])}</p>' + picture(root, item) +
                     f'<p>{text(item["summary"])}</p><p>' + link(item['url'], '论文原文') + ' · ' +
                     link(item['pdf'], 'PDF') + f'</p><small>{text(item["crop"])} · '
                     f'{text(item["rights"])}</small></article>')
    for marker, content in {'<!--PAPER_CARDS-->': '\n'.join(cards),
                            '/*INLINE_CSS*/': css, '/*INLINE_JS*/': js}.items():
        if html.count(marker) != 1:
            raise ValueError(f'Expected exactly one marker: {marker}')
        html = html.replace(marker, content)
    if re.search(r'data-figure=|/\*INLINE_|<!--PAPER_CARDS-->', html):
        raise ValueError('Unreplaced template marker')
    check = Check()
    check.feed(html)
    check.errors.extend('Missing anchor: ' + r for r in check.refs if r not in check.ids)
    if check.errors:
        raise ValueError('\n'.join(check.errors))
    out = root / 'dist' / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = out.with_suffix('.tmp')
    temporary.write_text(html, encoding='utf-8')
    temporary.replace(out)
    return {'output': str(out), 'bytes': out.stat().st_size, 'figures': len(figures),
            'papers': len(papers), 'images': check.images}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report_directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.report_directory.resolve()), ensure_ascii=False))
