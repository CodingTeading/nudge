# -*- coding: utf-8 -*-
"""코스·레슨마다 <head> 를 구워 정적 HTML 로 냅니다.

  python tools/bake-head.py [dist]

왜 필요한가
  카카오톡·네이버·페이스북의 미리보기 수집기는 자바스크립트를 실행하지 않습니다.
  머리말을 화면에서 채우면 그 수집기들에는 <title> 도 og:image 도 빈 채로 보입니다.
  한국 학생들이 링크를 나르는 곳이 카카오톡이라, 여기가 비면 공유 카드가 통째로
  빈 채 돌아다니게 됩니다.

  쿼리 주소(lesson.html?l=…)로는 이걸 해결할 수 없습니다. 파일이 하나뿐이라
  61편이 전부 같은 머리말을 갖게 되니까요. 그래서 경로마다 파일을 따로 냅니다.

만드는 것 (dist 안)
  /index.html  /all.html            ko
  /c/<코스>.html  /l/<레슨>.html      ko
  /<lang>/index.html  …             그 밖의 언어

  확장자 없는 주소로 링크하면 Cloudflare Pages 가 알아서 .html 을 찾아 줍니다.

셸(course.html · lesson.html)은 그대로 남겨 둡니다. 옛 링크(?c= · ?l=)가 죽지
않도록. 다만 noindex 를 붙여 검색엔진이 구운 쪽만 보게 합니다.
"""
import html
import io
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

SITE = 'site'
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'dist'))
os.chdir(HERE)   # site/ 경로를 저장소 기준으로 읽습니다 (build.py 가 불러 쓰므로)
ORIGIN = 'https://nudge.codingteading.com'
LANGS = [('ko', 'ko'), ('en', 'en'), ('ja', 'ja'), ('es', 'es')]
BASE = 'ko'
OG_LOCALE = {'ko': 'ko_KR', 'en': 'en_US', 'ja': 'ja_JP', 'es': 'es_ES'}


def read(p):
    return io.open(p, encoding='utf-8').read()


def load(p):
    return json.load(open(p, encoding='utf-8'))


# ── 문구 ────────────────────────────────────────────────────────────
UI = {}
for code, _ in LANGS:
    base = load(f'{SITE}/i18n/ui.{BASE}.json')
    base.update({k: v for k, v in load(f'{SITE}/i18n/ui.{code}.json').items()})
    UI[code] = base


def t(lang, key, **vars):
    s = UI[lang].get(key) or UI[BASE].get(key) or key
    for k, v in vars.items():
        s = s.replace('{' + k + '}', str(v))
    return s


# ── 내용 ────────────────────────────────────────────────────────────
def content(name, lang):
    """그 언어의 원고. 없으면 기준 언어로 떨어집니다 — 화면과 같은 규칙입니다."""
    p = f'{SITE}/content/{lang}/{name}.json'
    return load(p) if os.path.exists(p) else load(f'{SITE}/content/{BASE}/{name}.json')


SIMS = {s['repo']: s for s in load(f'{DIST}/sims.json')}
TITLE_FIX = load(f'{SITE}/content/sim-titles.json')


def sim_title(repo, lang):
    fix = TITLE_FIX.get(repo, {})
    return fix.get(lang) or SIMS.get(repo, {}).get('title') or repo


# ── 주소 ────────────────────────────────────────────────────────────
def base_path(lang):
    return '/' if lang == BASE else f'/{lang}/'


def path_of(kind, ident, lang):
    b = base_path(lang)
    if kind == 'home':
        return b
    if kind == 'all':
        return b + 'all'
    return b + ('c/' if kind == 'course' else 'l/') + ident


def file_of(kind, ident, lang):
    b = '' if lang == BASE else f'{lang}/'
    if kind == 'home':
        return f'{b}index.html'
    if kind == 'all':
        return f'{b}all.html'
    return b + ('c/' if kind == 'course' else 'l/') + ident + '.html'


# ── 머리말 만들기 ────────────────────────────────────────────────────
def clamp(s, lang):
    mx = 90 if lang in ('ko', 'ja') else 158
    # 원고에 <b> 가 섞여 있으면 태그가 그대로 미리보기에 실립니다.
    s = html.unescape(re.sub(r'<[^>]+>', '', str(s or '')))
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= mx else s[:mx - 1].rstrip(' ,·') + '…'


def esc(s):
    return html.escape(str(s), quote=True)


def head(lang, kind, ident, title, desc, image, jsonld):
    d = clamp(desc, lang)
    url = ORIGIN + path_of(kind, ident, lang)
    img = f'{ORIGIN}/og/{image}'
    out = [
        f'<title>{esc(title)}</title>',
        f'<meta name="description" content="{esc(d)}">',
        f'<meta name="keywords" content="{esc(t(lang, "seo.keywords"))}">',
        f'<link rel="canonical" href="{esc(url)}">',
    ]
    for code, htmllang in LANGS:
        out.append(f'<link rel="alternate" hreflang="{htmllang}" '
                   f'href="{esc(ORIGIN + path_of(kind, ident, code))}">')
    out.append(f'<link rel="alternate" hreflang="x-default" '
               f'href="{esc(ORIGIN + path_of(kind, ident, BASE))}">')
    out += [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Nudge">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(d)}">',
        f'<meta property="og:url" content="{esc(url)}">',
        f'<meta property="og:image" content="{esc(img)}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(title)}">',
        f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
    ]
    for code, _ in LANGS:
        if code != lang:
            out.append(f'<meta property="og:locale:alternate" content="{OG_LOCALE[code]}">')
    out += [
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(d)}">',
        f'<meta name="twitter:image" content="{esc(img)}">',
        '<link rel="icon" href="/brand/favicon.svg" type="image/svg+xml">',
        '<meta name="theme-color" content="#080b18">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
    ]
    if jsonld:
        out.append('<script type="application/ld+json">'
                   + json.dumps(jsonld, ensure_ascii=False, separators=(',', ':'))
                   + '</script>')
    return '\n'.join(out)


# ── 셸에서 머리말만 갈아 끼우기 ───────────────────────────────────────
HEAD_RE = re.compile(r'<head>(.*?)</head>', re.S)
KEEP = ('<meta charset', '<meta name="viewport"', '<link rel="stylesheet"')


def bake(shell, lang, kind, ident, title, desc, image, jsonld):
    """셸의 <head> 안에서 우리가 만드는 태그만 갈아 끼웁니다.
    글꼴·스타일시트처럼 페이지마다 다를 게 없는 줄은 그대로 둡니다."""
    m = HEAD_RE.search(shell)
    inner = m.group(1)
    kept = [l for l in inner.split('\n') if l.strip().startswith(KEEP)]
    new_head = '\n'.join(kept[:2] + [head(lang, kind, ident, title, desc, image, jsonld)] + kept[2:])
    out = shell[:m.start(1)] + '\n' + new_head + '\n' + shell[m.end(1):]

    out = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', out, count=1)
    # 어느 문서인지 스크립트에 알려 줍니다 — 경로에는 ?c= 가 없으니까요.
    boot = ('<script>window.__NUDGE={kind:%s,id:%s,lang:%s};</script>'
            % (json.dumps(kind), json.dumps(ident), json.dumps(lang)))
    out = out.replace('</head>', boot + '\n</head>', 1)
    return out


def write(rel, text):
    p = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(text)


# ── 구조화 데이터 ────────────────────────────────────────────────────
def site_jsonld(lang):
    """seo.js 의 siteJsonLd 와 같은 모양이어야 합니다 — 구운 값과 화면이 갈리면
    검색엔진이 둘 중 무엇을 믿을지 알 수 없게 됩니다."""
    return [{
        '@context': 'https://schema.org', '@type': 'EducationalOrganization',
        'name': 'Nudge', 'url': ORIGIN, 'logo': ORIGIN + '/brand/mark.svg',
        'description': t(lang, 'seo.home.desc'), 'isAccessibleForFree': True,
    }, {
        '@context': 'https://schema.org', '@type': 'WebSite',
        'name': 'Nudge', 'url': ORIGIN,
        'inLanguage': [c for c, _ in LANGS],
        'potentialAction': {
            '@type': 'SearchAction',
            'target': {'@type': 'EntryPoint',
                       'urlTemplate': ORIGIN + path_of('all', None, BASE) + '?q={search_term_string}'},
            'query-input': 'required name=search_term_string',
        },
    }]


def course_jsonld(c, rows, lang):
    return {
        '@context': 'https://schema.org', '@type': 'Course',
        'name': c['title'], 'description': c['lead'],
        'url': ORIGIN + path_of('course', c['id'], lang),
        'inLanguage': lang, 'isAccessibleForFree': True,
        'educationalLevel': 'secondary education', 'about': c['subject'],
        'timeRequired': f'PT{c["minutes"]}M',
        'provider': {'@type': 'EducationalOrganization', 'name': 'Nudge', 'url': ORIGIN},
        'hasCourseInstance': {'@type': 'CourseInstance', 'courseMode': 'online',
                              'courseWorkload': f'PT{c["minutes"]}M'},
        'syllabusSections': [{'@type': 'Syllabus', 'name': r['title'],
                              'position': i + 1, 'timeRequired': f'PT{r["min"]}M'}
                             for i, r in enumerate(rows)],
    }


def lesson_jsonld(row, body, c, lang):
    return [{
        '@context': 'https://schema.org', '@type': 'LearningResource',
        'name': body['title'], 'description': body['lead'],
        'url': ORIGIN + path_of('lesson', row['id'], lang),
        'inLanguage': lang, 'isAccessibleForFree': True,
        'learningResourceType': 'interactive simulation lesson',
        'educationalLevel': 'secondary education',
        'timeRequired': f'PT{row["min"]}M',
        'teaches': c['title'],
        'isPartOf': {'@type': 'Course', 'name': c['title'],
                     'url': ORIGIN + path_of('course', c['id'], lang)},
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Nudge',
             'item': ORIGIN + path_of('home', None, lang)},
            {'@type': 'ListItem', 'position': 2, 'name': c['title'],
             'item': ORIGIN + path_of('course', c['id'], lang)},
            {'@type': 'ListItem', 'position': 3, 'name': body['title']},
        ],
    }]


# ── 본작업 ──────────────────────────────────────────────────────────
def main():
    shells = {k: read(f'{SITE}/{k}.html') for k in ('index', 'all', 'course', 'lesson')}
    n_home = n_all = n_course = n_lesson = 0

    for lang, _ in LANGS:
        cdata = content('courses', lang)
        ldata = content('lessons', lang)
        courses = cdata['courses']
        n_sims = len(SIMS)

        # 홈
        write(file_of('home', None, lang), bake(
            shells['index'], lang, 'home', None,
            t(lang, 'seo.home.title'), t(lang, 'seo.home.desc'),
            'default.png', site_jsonld(lang)))
        n_home += 1

        # 전체 실험
        write(file_of('all', None, lang), bake(
            shells['all'], lang, 'all', None,
            t(lang, 'seo.all.title', n=n_sims), t(lang, 'all.lead'),
            'default.png', None))
        n_all += 1

        for c in courses:
            rows = cdata['lessons'].get(c['id'], [])
            write(file_of('course', c['id'], lang), bake(
                shells['course'], lang, 'course', c['id'],
                t(lang, 'seo.course.title', course=c['title'], subject=c['subject'],
                  n=len(c['sims'])),
                t(lang, 'seo.course.desc', hook=c['hook'], lead=c['lead'],
                  n=len(c['sims']), min=c['minutes']),
                f'c-{c["id"]}.png', course_jsonld(c, rows, lang)))
            n_course += 1

            for row in rows:
                body = ldata.get(row['id'])
                if not body:
                    continue
                write(file_of('lesson', row['id'], lang), bake(
                    shells['lesson'], lang, 'lesson', row['id'],
                    t(lang, 'seo.lesson.title', lesson=body['title'], course=c['title']),
                    t(lang, 'seo.lesson.desc', hook=body['lead'],
                      min=row['min'], sim=sim_title(body['sim'], lang)),
                    f'l-{row["id"]}.png', lesson_jsonld(row, body, c, lang)))
                n_lesson += 1

    # 셸은 남기되 색인에서는 뺍니다 — 구운 쪽이 정본입니다.
    for k in ('course', 'lesson'):
        p = os.path.join(DIST, f'{k}.html')
        s = io.open(p, encoding='utf-8').read()
        s = s.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                      '<meta name="robots" content="noindex, follow">', 1)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

    total = n_home + n_all + n_course + n_lesson
    print(f'머리말 구움 — 홈 {n_home} · 전체 {n_all} · 코스 {n_course} · 레슨 {n_lesson} = {total} 장')
    print(f'셸(course.html · lesson.html)은 noindex 로 남겨 둠 — 옛 ?c= · ?l= 주소용')


if __name__ == '__main__':
    main()
