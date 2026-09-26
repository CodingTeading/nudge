"""sitemap.xml + robots.txt 생성.

  python tools/make-sitemap.py

언어판을 xhtml:link 로 서로 묶어 줍니다. 이게 없으면 네 언어판이 서로 중복 문서로
취급될 수 있습니다.

ORIGIN 은 site/lib/seo.js 의 값과 반드시 같아야 합니다. 도메인을 옮기면 두 곳을 함께 고치세요.

lastmod 는 "내용이 바뀐 날"입니다 — 빌드한 날이 아닙니다
────────────────────────────────────────────────────────────
빌드한 날을 넣으면 77개가 매번 같은 날짜로 올라갑니다. 그러면 크롤러는 그 신호를
쓰지 못하고, IndexNow 도 "바뀐 URL"을 가려낼 수 없습니다. 글꼴 한 줄 고친 배포에도
사이트 전체가 새로 쓰였다고 신고하는 셈입니다.

그래서 URL 마다 **그 페이지가 실제로 담아 내보내는 본문**의 지문을 남겨 두고
(data/sitemap-dates.json), 지문이 그대로면 저장된 날짜를 그대로 씁니다. 지문이
달라진 URL 만 오늘 날짜를 받습니다. ailearn.space 가 먼저 쓴 방식입니다.

지문에 넣지 않는 것
  UI 문구(i18n/ui.*.json) · 머리말 · 템플릿. 이것들을 넣으면 seo.keywords 한 줄만
  고쳐도 77개가 다 튀어 처음 문제로 돌아갑니다. 바뀐 것은 본문이 아니라 틀입니다.

지문에 넣는 것 — 네 언어를 모두 넣습니다
  사이트맵 항목 하나가 ko 주소 하나(loc)와 네 언어판(xhtml:link)을 함께 가리킵니다.
  즉 이 항목이 대표하는 것은 '그 레슨' 묶음 전체입니다. 그래서 일본어 원고만
  고쳐도 그 레슨의 날짜가 움직입니다 — 그래야 재크롤 신호가 나갑니다.

  모든 레슨 화면에 붙는 '모든 실험에 공통인 조작'(guides.json 의 _common)도 넣습니다.
  이건 틀이 아니라 화면에 나오는 글이라, 고치면 61편이 실제로 달라집니다.

파일 단위가 아니라 레슨 단위입니다
  레슨 61편이 lessons.json 한 파일에 들어 있어서 git log 나 파일 mtime 으로는
  하나만 고쳐도 61개가 같이 움직입니다. 지문은 레슨 하나의 본문으로만 계산하므로
  JSON 이 어떻게 묶여 있든 그 레슨만 움직입니다.

날짜는 KST 로 셉니다
  UTC 로 찍으면 한국 시간 오전 9시 이전 빌드가 전날로 적힙니다. 이 저장소는
  한국에서, 한국어를 원본으로 만듭니다. 블로그 쪽은 반대로 UTC 를 쓰는데, 어느
  쪽이든 하루 차이라 재크롤 신호에는 영향이 없습니다.

이 도구는 돌릴 때마다 지도를 덮어씁니다. 그러니 작업 중인 변경이 섞이지 않게
깨끗한 트리에서 돌리세요 — 고쳤다가 되돌린 것도 '바뀐 것'으로 한 번 잡힙니다.

지도가 비어 있으면 첫 실행에서 77개가 전부 오늘이 됩니다. 그건 사실이 아니므로
tools/seed-sitemap-dates.py 로 한 번 씨앗을 놓으세요 (한 번만 쓰는 도구입니다).
"""
import hashlib, io, json, os, sys
from datetime import datetime, timedelta, timezone
from xml.sax.saxutils import escape

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = 'site'
DATES = 'data/sitemap-dates.json'
ORIGIN = 'https://nudge.codingteading.com'
LANGS = [ 'ko', 'en', 'ja', 'es' ]
BASE = 'ko'
KST = timezone(timedelta(hours=9))


def url_for(path, lang):
    """경로 기반 주소. tools/bake-head.py 가 내는 파일 위치와 반드시 같아야 합니다."""
    base = '/' if lang == BASE else f'/{lang}/'
    return ORIGIN + base + path


def load(p):
    return json.load(io.open(p, encoding='utf-8'))


def blob(x):
    """지문 계산용 정규화. 키 순서가 바뀌어도 같은 글이면 같은 지문이 나옵니다."""
    return json.dumps(x, ensure_ascii=False, sort_keys=True)


def sig(*parts):
    """길이를 앞에 붙여 잇습니다 — 구분자가 본문에 나타나 경계가 흐려질 일이 없습니다."""
    h = hashlib.sha256()
    for part in parts:
        v = blob(part)
        h.update(('%d:' % len(v)).encode('utf-8'))
        h.update(v.encode('utf-8'))
    return h.hexdigest()[:16]


def entry(path, priority, changefreq, lastmod):
    out = ['  <url>']
    out.append(f'    <loc>{escape(url_for(path, BASE))}</loc>')
    out.append(f'    <lastmod>{lastmod}</lastmod>')
    for l in LANGS:
        out.append(f'    <xhtml:link rel="alternate" hreflang="{l}" '
                   f'href="{escape(url_for(path, l))}"/>')
    out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" '
               f'href="{escape(url_for(path, BASE))}"/>')
    out.append(f'    <changefreq>{changefreq}</changefreq>')
    out.append(f'    <priority>{priority}</priority>')
    out.append('  </url>')
    return '\n'.join(out)


def collect():
    """URL 마다 (경로, 우선순위, changefreq, 지문). 지문은 네 언어의 본문으로 만듭니다."""
    C = {l: load(f'{ROOT}/content/{l}/courses.json') for l in LANGS}
    L = {l: load(f'{ROOT}/content/{l}/lessons.json') for l in LANGS}
    G = {l: load(f'{ROOT}/content/{l}/guides.json') for l in LANGS}
    titles = load(f'{ROOT}/content/sim-titles.json')
    sims = load('../phet/deploy/sims.json')

    rows = []

    # 홈 — 코스 카드 목록이 본문입니다
    rows.append(('', '1.0', 'weekly', sig(*[
        [{k: c.get(k) for k in ('no', 'subject', 'title', 'hook', 'lead', 'minutes')}
         | {'nsims': len(c['sims'])} for c in C[l]['courses']] for l in LANGS ])))

    # 전체 실험 — 실험 목록과 이름이 본문입니다
    rows.append(('all', '0.7', 'weekly', sig(
        [{k: s.get(k) for k in ('repo', 'title', 'subject', 'grade')} for s in sims],
        titles)))

    # 코스 — 코스 머리말과 그 안의 레슨 줄
    for i, c0 in enumerate(C[BASE]['courses']):
        cid = c0['id']
        parts = []
        for l in LANGS:
            c = C[l]['courses'][i]
            parts.append({k: c.get(k) for k in
                          ('subject', 'title', 'hook', 'lead', 'minutes', 'sims')})
            parts.append(C[l]['lessons'].get(cid, []))
        rows.append((f'c/{cid}', '0.9', 'monthly', sig(*parts)))

    # 레슨 — 본문 + 그 실험의 사용 방법 + 공통 조작 + 실험 이름
    for cid, ls in C[BASE]['lessons'].items():
        for row0 in ls:
            if not row0.get('ready'):
                continue
            lid = row0['id']
            repo = L[BASE][lid]['sim']
            parts = []
            for l in LANGS:
                parts.append(L[l].get(lid))
                parts.append(next((r for r in C[l]['lessons'].get(cid, [])
                                   if r['id'] == lid), None))
                parts.append(G[l].get(repo))
                parts.append(G[l].get('_common'))
                parts.append(titles.get(repo, {}).get(l))
            rows.append((f'l/{lid}', '0.8', 'monthly', sig(*parts)))

    return rows


def main():
    rows = collect()

    today = datetime.now(KST).strftime('%Y-%m-%d')
    seen = load(DATES) if os.path.exists(DATES) else {}
    dates, fresh = {}, []

    out = []
    for path, priority, changefreq, h in rows:
        loc = url_for(path, BASE)
        before = seen.get(loc)
        same = bool(before) and before.get('hash') == h
        lastmod = before['date'] if same else today
        if not same:
            fresh.append(loc)
        dates[loc] = {'hash': h, 'date': lastmod}
        out.append(entry(path, priority, changefreq, lastmod))

    os.makedirs(os.path.dirname(DATES), exist_ok=True)
    io.open(DATES, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(dates, ensure_ascii=False, indent=2) + '\n')

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + '\n'.join(out) + '\n</urlset>\n')
    io.open(f'{ROOT}/sitemap.xml', 'w', encoding='utf-8', newline='\n').write(xml)

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
    io.open(f'{ROOT}/robots.txt', 'w', encoding='utf-8', newline='\n').write(robots)

    print('sitemap.xml : %d urls' % len(rows))
    print('robots.txt  : written')
    print('lastmod     : %s 로 새로 받은 URL %d개' % (today, len(fresh)))
    for loc in fresh[:10]:
        print('              %s' % loc)
    if len(fresh) > 10:
        print('              … 그리고 %d개' % (len(fresh) - 10))
    if not fresh:
        print('              (내용이 그대로라 날짜가 움직인 곳이 없습니다)')
    print('\nORIGIN = %s   (site/lib/seo.js must match)' % ORIGIN)


if __name__ == '__main__':
    main()
