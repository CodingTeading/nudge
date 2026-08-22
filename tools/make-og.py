"""OG 이미지 생성 — 1200×630 PNG, 언어별로 굽습니다.

  python tools/make-og.py            # 네 언어 전부 (76 × 4 = 304장)
  python tools/make-og.py ja         # 한 언어만
  python tools/make-og.py ko ja      # 골라서

카카오톡·페이스북·X 는 og:image 로 SVG 를 받지 않습니다. 래스터가 필요합니다.
한국 학생들이 링크를 나르는 곳이 카카오톡이라 이 그림이 유입의 첫 관문입니다.

나오는 자리는 `site/og/<lang>/` 입니다. `lib/seo.js` 와 `tools/bake-head.py` 가
같은 규칙으로 경로를 만듭니다 — 셋 중 하나만 고치면 안 됩니다.

서체는 tools/fonts/ 에 넣어 둔 것을 씁니다 — 전부 SIL Open Font License 라
  저장소에 담아도 되고, 어느 기계에서 돌려도 같은 그림이 나옵니다.
  제목·워드마크는 Jua(사이트의 표시 서체), 본문은 Pretendard(사이트의 본문 서체),
  일본어는 Noto Sans JP — Jua 에도 Pretendard 에도 한자가 없습니다.
"""
import io, json, os, sys
from PIL import Image, ImageDraw, ImageFont

# 윈도우 콘솔은 cp949 라 한글·일본어 진행 표시에서 죽습니다.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = 'site'
OUT = f'{ROOT}/og'
W, H = 1200, 630

LANGS = ('ko', 'en', 'ja', 'es')

FONTS = 'tools/fonts'
JUA     = f'{FONTS}/Jua-Regular.ttf'          # 제목·워드마크 (사이트와 같은 서체)
PRE_B   = f'{FONTS}/Pretendard-Bold.otf'      # 본문 굵게
PRE_R   = f'{FONTS}/Pretendard-Regular.otf'   # 본문
NOTO_B  = f'{FONTS}/NotoSansJP-Bold.otf'      # 일본어 제목
NOTO_R  = f'{FONTS}/NotoSansJP-Regular.otf'   # 일본어 본문

# 언어마다 서체 사슬이 다릅니다. 앞에서부터 그 줄을 통째로 덮는 서체를 고르고,
# 아무것도 못 덮으면 글자 단위로 나눠 그립니다 (일본어의 ₂ 가 그런 자리입니다 —
# Noto Sans JP 에 U+2082 가 없어서 CO₂ 의 아래첨자만 Pretendard 로 떨어집니다).
CHAIN = {
    'ko': {'display': [JUA, PRE_B], 'body': [PRE_R]},
    'en': {'display': [JUA, PRE_B], 'body': [PRE_R]},
    'es': {'display': [JUA, PRE_B], 'body': [PRE_R]},
    'ja': {'display': [NOTO_B, PRE_B], 'body': [NOTO_R, PRE_R]},
}
# 띄어쓰기로 줄을 끊을 수 없는 언어. 글자 단위로 접습니다.
NO_SPACES = {'ja'}

BG        = (8, 11, 24)
INK       = (238, 241, 255)
INK_SOFT  = (165, 173, 219)
INK_FAINT = (106, 114, 168)
LINE      = (38, 45, 92)
AMBER     = (255, 165, 61)

SUBJECT = {
    '물리': (157, 92, 255), '수학': (77, 155, 255), '화학': (255, 77, 141),
    '생명과학': (53, 224, 143), '지구과학': (46, 230, 214),
    'Physics': (157, 92, 255), 'Math': (77, 155, 255), 'Chemistry': (255, 77, 141),
    'Biology': (53, 224, 143), 'Earth science': (46, 230, 214),
    '物理': (157, 92, 255), '数学': (77, 155, 255), '化学': (255, 77, 141),
    '生物': (53, 224, 143), '地学': (46, 230, 214),
    'Física': (157, 92, 255), 'Matemáticas': (77, 155, 255), 'Química': (255, 77, 141),
    'Biología': (53, 224, 143), 'Ciencias de la Tierra': (46, 230, 214),
}

_FONT = {}
_COVER = {}


def font(path, size):
    key = (path, size)
    if key not in _FONT:
        _FONT[key] = ImageFont.truetype(path, size)
    return _FONT[key]


def _covers(path, text):
    """그 서체가 이 글자들을 전부 갖고 있는지. 없으면 두부 상자가 찍힙니다."""
    if path not in _COVER:
        from fontTools.ttLib import TTFont
        _COVER[path] = set(TTFont(path).getBestCmap())
    have = _COVER[path]
    return all(ord(c) in have for c in text if not c.isspace())


def pick(chain, size, text):
    """그 줄을 통째로 덮는 첫 서체. 없으면 None — 글자 단위로 나눠 그려야 합니다."""
    for p in chain:
        if _covers(p, text):
            return font(p, size)
    return None


def _runs(chain, size, text):
    """글자를 덮는 서체가 바뀌는 자리에서 끊어 (글, 서체) 로 묶습니다."""
    out = []
    for ch in text:
        f = next((font(p, size) for p in chain if _covers(p, ch)), font(chain[-1], size))
        if out and out[-1][1] is f:
            out[-1][0] += ch
        else:
            out.append([ch, f])
    return out


def measure(d, text, chain, size):
    f = pick(chain, size, text)
    if f is not None:
        return d.textlength(text, font=f)
    return sum(d.textlength(s, font=f) for s, f in _runs(chain, size, text))


def write(d, xy, text, chain, size, fill):
    f = pick(chain, size, text)
    if f is not None:
        d.text(xy, text, font=f, fill=fill)
        return
    x, y = xy
    for s, sf in _runs(chain, size, text):
        d.text((x, y), s, font=sf, fill=fill)
        x += d.textlength(s, font=sf)


def wrap(d, text, chain, size, max_w, by_char=False):
    """어절 단위로 끊습니다 (음절 단위로 자르면 읽기가 나빠집니다).
    일본어처럼 띄어쓰기가 없는 언어, 또는 한 어절이 너무 길면 글자 단위로 접습니다."""
    def fit(s):
        return measure(d, s, chain, size) <= max_w

    def chars(word, lines, cur):
        for ch in word:
            t = cur + ch
            if fit(t) or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = ch
        return cur

    lines, cur = [], ''
    if by_char:
        cur = chars(text, lines, cur)
    else:
        for w in text.split(' '):
            t = (cur + ' ' + w).strip()
            if fit(t):
                cur = t
            elif fit(w):
                if cur:
                    lines.append(cur)
                cur = w
            else:                      # 한 어절이 한 줄보다 긺 — 글자로 접습니다
                if cur:
                    lines.append(cur)
                    cur = ''
                cur = chars(w, lines, cur)
    if cur:
        lines.append(cur)
    return lines


def nebula(img):
    """밤하늘 — 사이트와 같은 옅은 성운."""
    grad = Image.new('RGB', (W, H), BG)
    px = grad.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            a = max(0.0, 1 - (((x - 180) / 620.0) ** 2 + ((y + 60) / 520.0) ** 2)) * 0.13
            b = max(0.0, 1 - (((x - 1050) / 560.0) ** 2 + ((y + 30) / 460.0) ** 2)) * 0.11
            r = int(BG[0] + 77 * a + 157 * b)
            g = int(BG[1] + 155 * a + 92 * b)
            bl = int(BG[2] + 255 * a + 255 * b)
            for dy in (0, 1):
                for dx in (0, 1):
                    if x + dx < W and y + dy < H:
                        px[x + dx, y + dy] = (min(r, 255), min(g, 255), min(bl, 255))
    img.paste(grad, (0, 0))


_NEBULA = None


def background():
    """성운은 언어와 무관하게 같습니다. 304장을 굽느라 304번 그릴 필요가 없습니다."""
    global _NEBULA
    if _NEBULA is None:
        _NEBULA = Image.new('RGB', (W, H), BG)
        nebula(_NEBULA)
    return _NEBULA.copy()


def logo(d, x, y, s=1.0):
    """Nudge 마크 — 슬라이더 손잡이가 살짝 밀린 모양."""
    def p(v):
        return v * s
    d.line([(x + p(4), y + p(16)), (x + p(28), y + p(16))], fill=LINE, width=int(p(2.6)))
    d.line([(x + p(8.5), y + p(12)), (x + p(8.5), y + p(20))], fill=(90, 97, 145), width=int(p(2.2)))
    d.line([(x + p(13), y + p(12.8)), (x + p(13), y + p(19.2))], fill=INK_FAINT, width=int(p(2.2)))
    r = p(6)
    d.ellipse([x + p(21) - r, y + p(16) - r, x + p(21) + r, y + p(16) + r], fill=AMBER)


def chip(d, x, y, text, chain, size, fg=INK_SOFT):
    tw = measure(d, text, chain, size)
    d.rounded_rectangle([x, y, x + tw + 34, y + 46], radius=23, outline=LINE, width=2)
    write(d, (x + 17, y + 10), text, chain, size, fg)
    return x + tw + 34 + 12


def card(path, lang, kicker, title, sub, chips, accent):
    disp, body = CHAIN[lang]['display'], CHAIN[lang]['body']
    by_char = lang in NO_SPACES

    img = background()
    d = ImageDraw.Draw(img)

    # 왼쪽 과목색 띠
    d.rounded_rectangle([0, 0, 14, H], radius=0, fill=accent)

    # 로고 잠금 — 마크의 세로 중심을 워드마크 글자 중심에 맞춥니다.
    # 워드마크는 로마자라 어느 언어에서나 Jua 로 그립니다.
    logo(d, 74, 47, 2.0)
    d.text((156, 56), 'Nudge', font=font(JUA, 40), fill=INK)

    write(d, (74, 168), kicker, disp, 26, accent)

    y = 210
    for line in wrap(d, title, disp, 62, W - 160, by_char)[:3]:
        write(d, (74, y), line, disp, 62, INK)
        y += 78

    y += 8
    for line in wrap(d, sub, body, 30, W - 160, by_char)[:2]:
        write(d, (74, y), line, body, 30, INK_SOFT)
        y += 44

    x = 74
    for c in chips:
        x = chip(d, x, H - 96, c, body, 24)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, 'PNG', optimize=True)
    return path


def sim_names(lang, titles, sims):
    """실험 이름 — 언어별 덮어쓰기가 있으면 그것을, 없으면 영어 제목을 씁니다.
    한국어만 sims.json 에 제목이 들어 있습니다 (site/content/sim-titles.json 의 주석 참고)."""
    out = {}
    for s in sims:
        over = titles.get(s['repo'], {}).get(lang)
        out[s['repo']] = over or (s['title'] if lang == 'ko' else s.get('titleEn') or s['title'])
    return out


def build(lang, titles, sims):
    ui = json.load(io.open(f'{ROOT}/i18n/ui.{lang}.json', encoding='utf-8'))
    data = json.load(io.open(f'{ROOT}/content/{lang}/courses.json', encoding='utf-8'))
    lessons = json.load(io.open(f'{ROOT}/content/{lang}/lessons.json', encoding='utf-8'))
    simname = sim_names(lang, titles, sims)

    def t(key, **kw):
        s = ui[key]
        for k, v in kw.items():
            s = s.replace('{' + k + '}', str(v))
        return s

    nsims = sum(len(c['sims']) for c in data['courses'])
    ncourses = len(data['courses'])
    out = f'{OUT}/{lang}'
    made = []

    # 홈 제목은 세 토막으로 나뉘어 있습니다. 띄어쓰기가 없는 언어는 붙여 씁니다.
    join = '' if lang in NO_SPACES else ' '
    made.append(card(
        f'{out}/default.png', lang, t('site.tagline'),
        join.join([t('home.title.a'), t('home.title.b'), t('home.title.c')]),
        t('home.lead', n=ncourses).split('.')[0].split('。')[0],
        [t('og.sims', n=nsims), t('og.courses', n=ncourses),
         t('og.free'), t('og.noAds')],
        (46, 230, 214)))

    for c in data['courses']:
        accent = SUBJECT.get(c['subject'], (127, 136, 184))
        made.append(card(
            f"{out}/c-{c['id']}.png", lang, f"{c['no']} · {c['subject']}",
            c['title'], c['hook'],
            [t('og.sims', n=len(c['sims'])), t('course.minutes', n=c['minutes']),
             t('og.free')],
            accent))

    for lid, L in lessons.items():
        if lid.startswith('_'):
            continue          # _note 같은 메모 키는 레슨이 아닙니다
        course = next(x for x in data['courses'] if x['id'] == L['course'])
        meta = next(x for x in data['lessons'][L['course']] if x['id'] == lid)
        accent = SUBJECT.get(course['subject'], (127, 136, 184))
        made.append(card(
            f'{out}/l-{lid}.png', lang, f"{course['no']} {course['title']}",
            L['title'], meta['hook'],
            [simname.get(L['sim'], L['sim']), t('og.lessonMinutes', n=meta['min']),
             t('og.free')],
            accent))
    return made


def main():
    want = [a for a in sys.argv[1:] if not a.startswith('-')] or list(LANGS)
    bad = [w for w in want if w not in LANGS]
    if bad:
        sys.exit(f'모르는 언어: {", ".join(bad)} (쓸 수 있는 것: {", ".join(LANGS)})')

    titles = json.load(io.open(f'{ROOT}/content/sim-titles.json', encoding='utf-8'))
    sims = json.load(io.open('../phet/deploy/sims.json', encoding='utf-8'))

    total = 0
    for lang in want:
        made = build(lang, titles, sims)
        kb = sum(os.path.getsize(p) for p in made) / 1024
        print('%s — %3d장  %7.1f KB  → %s/%s/' % (lang, len(made), kb, OUT, lang))
        total += len(made)
    print('\n%d장 구웠습니다.' % total)


if __name__ == '__main__':
    main()
