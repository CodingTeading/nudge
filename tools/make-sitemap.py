"""sitemap.xml + robots.txt 생성.

  python .claude/make-sitemap.py

언어판을 xhtml:link 로 서로 묶어 줍니다. 이게 없으면 네 언어판이 서로 중복 문서로
취급될 수 있습니다.

ORIGIN 은 site/lib/seo.js 의 값과 반드시 같아야 합니다. 도메인을 옮기면 두 곳을 함께 고치세요.
"""
import io, json, os
from xml.sax.saxutils import escape

ROOT = 'site'
ORIGIN = 'https://nudge.codingteading.com'
LANGS = [ 'ko', 'en', 'ja', 'es' ]
BASE = 'ko'


def url_for(path, lang):
    if lang == BASE:
        return f'{ORIGIN}/{path}'
    sep = '&' if '?' in path else '?'
    return f'{ORIGIN}/{path}{sep}lang={lang}'


def entry(path, priority, changefreq):
    out = ['  <url>']
    out.append(f'    <loc>{escape(url_for(path, BASE))}</loc>')
    for l in LANGS:
        out.append(f'    <xhtml:link rel="alternate" hreflang="{l}" '
                   f'href="{escape(url_for(path, l))}"/>')
    out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" '
               f'href="{escape(url_for(path, BASE))}"/>')
    out.append(f'    <changefreq>{changefreq}</changefreq>')
    out.append(f'    <priority>{priority}</priority>')
    out.append('  </url>')
    return '\n'.join(out)


def main():
    data = json.load(io.open(f'{ROOT}/content/{BASE}/courses.json', encoding='utf-8'))
    sims = json.load(io.open('../phet/deploy/sims.json', encoding='utf-8'))

    rows = [entry('index.html', '1.0', 'weekly')]
    for c in data['courses']:
        rows.append(entry(f"course.html?c={c['id']}", '0.9', 'monthly'))
    ready = 0
    for cid, ls in data['lessons'].items():
        for l in ls:
            if l.get('ready'):
                rows.append(entry(f"lesson.html?l={l['id']}", '0.8', 'monthly'))
                ready += 1

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + '\n'.join(rows) + '\n</urlset>\n')
    io.open(f'{ROOT}/sitemap.xml', 'w', encoding='utf-8').write(xml)

    robots = (
        '# Nudge\n'
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        '# 시뮬레이션 원본(각 2~5MB)은 색인할 값어치가 없습니다.\n'
        '# 학습자가 도달해야 할 곳은 레슨 페이지입니다.\n'
        'Disallow: /sims/\n'
        'Disallow: /test.html\n'
        'Disallow: /_proto/\n'
        '\n'
        f'Sitemap: {ORIGIN}/sitemap.xml\n'
    )
    io.open(f'{ROOT}/robots.txt', 'w', encoding='utf-8').write(robots)

    print('sitemap.xml : %d urls (home 1 + courses %d + lessons %d)'
          % (len(rows), len(data['courses']), ready))
    print('robots.txt  : written')
    print('sims not indexed: %d files under /sims/' % len(sims))
    print('\nORIGIN = %s   (site/lib/seo.js must match)' % ORIGIN)


if __name__ == '__main__':
    main()
