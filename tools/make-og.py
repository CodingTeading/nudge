"""OG 이미지 생성 — 1200×630 JPEG, 언어별로 굽습니다.

  python tools/make-og.py            # 네 언어 전부 (77 × 4 = 308장)
  python tools/make-og.py ja         # 한 언어만
  python tools/make-og.py ko ja      # 골라서

카카오톡·페이스북·X 는 og:image 로 SVG 를 받지 않습니다. 래스터가 필요합니다.
한국 학생들이 링크를 나르는 곳이 카카오톡이라 이 그림이 유입의 첫 관문입니다.

나오는 자리는 `site/og/v2/<lang>/<이름>.jpg` 입니다. `lib/seo.js` 와 `tools/bake-head.py` 가
같은 규칙으로 경로를 만듭니다 — 셋 중 하나만 고치면 안 됩니다.

서체는 tools/fonts/ 에 넣어 둔 것을 씁니다 — 전부 SIL Open Font License 라
  저장소에 담아도 되고, 어느 기계에서 돌려도 같은 그림이 나옵니다.
  제목·워드마크는 Jua(사이트의 표시 서체), 본문은 Pretendard(사이트의 본문 서체),
  일본어는 Noto Sans JP — Jua 에도 Pretendard 에도 한자가 없습니다.
"""
import io, json, os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

# 윈도우 콘솔은 cp949 라 한글·일본어 진행 표시에서 죽습니다.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = 'site'
# 판(v2)을 경로에 둡니다. 카카오·페이스북은 og:image 를 주소 단위로 오래 붙들고
# 있어서, 같은 이름에 덮어쓰면 옛 카드가 한참 더 나갑니다. 주소를 바꾸면 새로 받습니다.
# 옛 og/<lang>/*.png 는 지우지 않습니다 — 엣지가 옛 HTML 을 들고 있는 동안 그 주소를
# 가리킵니다. 충분히 지난 뒤(몇 주) 따로 치웁니다.
OUT = f'{ROOT}/og/v2'
EXT = 'jpg'
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


# ── 네이버 썸네일이 잘라 가는 자리 ──────────────────────────────────
# 네이버는 가로 그림의 가운데를 정사각으로 잘라 씁니다. 1200×630 이면 x 285~915.
# 카카오·페이스북은 1200×630 을 그대로 씁니다. 그래서 한 장으로 둘 다 맞추되,
# "무엇에 대한 카드인가" 는 전부 이 가운데 칸 안에 둡니다. 양옆에는 잘려도
# 되는 것만 둡니다. 옛 카드는 제목을 왼쪽에 붙여서 네이버에서 '지 말고 만져 보고
# 알아내세' 처럼 중간이 잘렸습니다.
SAFE_L, SAFE_R = 285, 915
MID = (SAFE_L + SAFE_R) // 2          # 600
PAD = 30                              # 가운데 칸 가장자리에서 띄우는 거리
COL = (SAFE_R - PAD) - (SAFE_L + PAD)  # 가운데 글이 쓸 수 있는 폭 = 570

# ── 그림 ──────────────────────────────────────────────────────────
# 카드가 글로만 차 있으면 목록에서 눈에 걸리지 않습니다. 이 사이트에는 그림이
# 두 가지 있습니다 — 실험 화면(PhET 포크가 구운 thumbs/, 600×394)과 코스
# 표지(site/covers/*.svg, 사이트가 직접 그린 선 그림). 페이지마다 그 페이지가
# 실제로 보여 주는 쪽을 씁니다.
#   레슨      그 실험의 화면을 액자로
#   코스      코스 표지를 크게, 양옆에 그 코스의 실험 화면
#   홈        코스 표지 카드 14장 — 홈 화면의 코스 격자 그대로
#   전체 실험 실험 화면 모자이크 — 전체 실험 화면 그대로
PHET = os.environ.get('NUDGE_PHET', os.path.join('..', 'phet'))
THUMBS = os.path.join(PHET, 'deploy', 'thumbs')
COVERS = f'{ROOT}/covers'
SURFACE = (18, 23, 52)

_THUMB = {}
_COVER_IMG = {}


def thumb(repo):
    if repo not in _THUMB:
        _THUMB[repo] = Image.open(os.path.join(THUMBS, repo + '.png')).convert('RGBA')
    return _THUMB[repo]


def cover_img(cid, w):
    """코스 표지 SVG 를 그 폭으로 래스터화합니다. 선 그림이라 늘려도 깨지지 않습니다."""
    key = (cid, w)
    if key not in _COVER_IMG:
        import cairosvg
        png = cairosvg.svg2png(url=f'{COVERS}/{cid}.svg', output_width=w)
        _COVER_IMG[key] = Image.open(io.BytesIO(png)).convert('RGBA')
    return _COVER_IMG[key]


def fit_cover(im, w, h):
    """꽉 채우고 넘치는 쪽을 가운데 기준으로 자릅니다."""
    s = max(w / im.width, h / im.height)
    r = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x, y = (r.width - w) // 2, (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


def round_mask(w, h, r):
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


def shadow(canvas, x, y, w, h, r, strength=150, spread=18, dy=10):
    s = Image.new('RGBA', (w + spread * 4, h + spread * 4), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle(
        [spread * 2, spread * 2 + dy, spread * 2 + w, spread * 2 + h + dy],
        radius=r, fill=(0, 0, 0, strength))
    s = s.filter(ImageFilter.GaussianBlur(spread))
    canvas.alpha_composite(s, (x - spread * 2, y - spread * 2))


def frame(canvas, im, x, y, w, h, r=16, edge=None, ew=3, glow=None):
    """사진 액자. 모서리를 둥글게 깎고 그림자와 테두리를 두릅니다."""
    if glow:
        g = Image.new('RGBA', (w + 160, h + 160), (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([80, 80, 80 + w, 80 + h], radius=r,
                                            fill=glow + (110,))
        canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)), (x - 80, y - 80))
    shadow(canvas, x, y, w, h, r)
    pic = fit_cover(im, w, h)
    canvas.paste(pic, (x, y), round_mask(w, h, r))
    if edge:
        ImageDraw.Draw(canvas).rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=r,
                                                 outline=edge, width=ew)


def tile(im, w, h, r=12, edge=LINE, ew=2):
    """기울여 붙일 작은 액자 한 장 (투명 바탕)."""
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    t.paste(fit_cover(im, w, h), (0, 0), round_mask(w, h, r))
    ImageDraw.Draw(t).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=edge, width=ew)
    return t


def fade(im, a):
    im = im.copy()
    im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    return im


def darken_below(canvas, y0, top=0, bottom=190):
    """아래쪽을 점점 어둡게 — 그림 위에 얹은 제목이 읽히게."""
    g = Image.new('L', (1, H), 0)
    for y in range(H):
        t = 0 if y < y0 else (y - y0) / max(1, H - y0)
        g.putpixel((0, y), int(top + (bottom - top) * min(1, t)))
    shade = Image.new('RGBA', (W, H), BG + (0,))
    shade.putalpha(g.resize((W, H)))
    canvas.alpha_composite(shade)


def glow_at(canvas, cx, cy, rx, ry, color, alpha=90):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color + (alpha,))
    canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))


# ── 글 ────────────────────────────────────────────────────────────
TITLE_SIZES = (60, 56, 52, 48, 44)    # 44 밑으로는 줄이지 않습니다


def center(d, y, text, chain, size, fill, mid=MID):
    write(d, (mid - measure(d, text, chain, size) / 2, y), text, chain, size, fill)


def chip_w(d, text, chain, size):
    return measure(d, text, chain, size) + 34


def chip(d, x, y, text, chain, size, fg=INK_SOFT, edge=LINE, fill=None):
    w = chip_w(d, text, chain, size)
    d.rounded_rectangle([x, y, x + w, y + 40], radius=20, outline=edge, width=2, fill=fill)
    write(d, (x + 17, y + 7), text, chain, size, fg)
    return w


def chips_row(d, y, texts, chain, size, fg=INK_SOFT, fill=None, width=COL):
    """가운데 칸 안에 나란히. 넘치면 뒤엣것부터 뺍니다 — 잘려 보이느니 없는 게 낫습니다."""
    gap = 12
    total = 0
    while texts:
        total = sum(chip_w(d, t, chain, size) for t in texts) + gap * (len(texts) - 1)
        if total <= width:
            break
        texts = texts[:-1]
    x = MID - total / 2
    for t in texts:
        x += chip(d, x, y, t, chain, size, fg, fill=fill) + gap


def fit_title(d, title, disp, by_char, sizes=TITLE_SIZES, width=COL):
    """두 줄에 들어가는 가장 큰 크기. 44 에서도 안 되면 44 로 세 줄까지 봅니다."""
    for size in sizes:
        lines = wrap(d, title, disp, size, width, by_char)
        if len(lines) <= 2:
            return size, lines
    size = sizes[-1]
    return size, wrap(d, title, disp, size, width, by_char)[:3]


def titles(d, y, title, disp, by_char, sizes=TITLE_SIZES, width=COL):
    size, lines = fit_title(d, title, disp, by_char, sizes, width)
    lh = int(size * 1.24)
    for line in lines:
        center(d, y, line, disp, size, INK)
        y += lh
    return y


def canvas_of(base=None):
    return (base or background()).convert('RGBA')


def finish(canvas, path, accent, lang):
    d = ImageDraw.Draw(canvas)
    body = CHAIN[lang]['body']
    # 위쪽 과목색 띠. 옛 카드의 왼쪽 세로 띠는 네이버 썸네일에서 잘려 안 보였습니다.
    d.rectangle([0, 0, W, 10], fill=accent)

    # 아래 — 도메인(경로 없이)과 로고. 둘 다 가운데 칸 밖입니다. 도메인이 285 를
    # 넘어가면 네이버 썸네일 구석에 꼬리만 걸쳐 보입니다 — 안 넘어가는 크기를 고릅니다.
    dom = 'nudge.codingteading.com'
    dsize = next((z for z in (22, 20, 18, 16)
                  if 60 + measure(d, dom, body, z) <= SAFE_L - 20), 16)
    write(d, (60, H - 62), dom, body, dsize, INK_SOFT)
    mark = font(JUA, 30)
    wm_w = d.textlength('Nudge', font=mark)
    d.text((W - 60 - wm_w, H - 68), 'Nudge', font=mark, fill=INK)
    logo(d, W - 60 - wm_w - 62, H - 72, 1.6)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = canvas.convert('RGB')
    # 실험 화면과 흐린 바탕이 들어가 PNG 로는 200KB 를 쉽게 넘습니다. 256색으로 줄이면
    # 로고의 주황이 분홍으로 뭉개졌습니다. JPEG 로 굽고, 색 글자가 번지지 않게
    # 색 정보를 솎지 않습니다(4:4:4). 200KB 를 넘으면 품질을 한 단계씩 내립니다.
    for q in (86, 82, 78, 74, 70):
        out.save(path, 'JPEG', quality=q, optimize=True, progressive=True, subsampling=0)
        if os.path.getsize(path) <= 190 * 1024:
            break
    return path


# ── 유형별 판짜기 ──────────────────────────────────────────────────

def lesson_card(path, lang, kicker, title, minutes, accent, repo):
    """레슨 — 그 실험의 화면이 주인공입니다. 흐리게 늘린 같은 화면이 바탕이 됩니다."""
    disp, body = CHAIN[lang]['display'], CHAIN[lang]['body']
    by_char = lang in NO_SPACES
    shot = thumb(repo)

    amb = fit_cover(shot, W, H).convert('RGB').filter(ImageFilter.GaussianBlur(34))
    amb = ImageEnhance.Brightness(amb).enhance(0.42)
    c = canvas_of(Image.blend(background(), amb, 0.62))
    darken_below(c, 300, 0, 200)

    fx, fy, fw, fh = 338, 44, 524, 344              # 600:394 비율
    frame(c, shot, fx, fy, fw, fh, r=18, edge=accent, ew=3, glow=accent)
    d = ImageDraw.Draw(c)

    # 코스 이름과 걸리는 시간은 액자 윗변에 한 칩으로 얹습니다. 액자 안쪽 아래
    # 띠에는 PhET 표지와 실험 이름이 있어 가리지 않습니다 — 출처이기도 합니다.
    label = f'{kicker} · {minutes}'
    kw = chip_w(d, label, body, 22)
    chip(d, MID - kw / 2, fy - 20, label, body, 22, accent, accent, fill=BG)

    titles(d, fy + fh + 26, title, disp, by_char, sizes=(54, 50, 46, 44))
    return finish(c, path, accent, lang)


def course_card(path, lang, cid, kicker, title, facts, accent, repos):
    """코스 — 사이트가 그린 코스 표지를 크게. 양옆에는 그 코스의 실험 화면."""
    disp, body = CHAIN[lang]['display'], CHAIN[lang]['body']
    by_char = lang in NO_SPACES

    c = canvas_of()
    glow_at(c, MID, 230, 300, 170, accent, 70)

    # 양옆 — 잘려도 되는 자리. 살짝 기울여 책상 위에 흩어 놓은 느낌으로.
    spots = [(-6, 40, 70), (5, 60, 318), (6, 950, 70), (-5, 930, 318)]
    for (ang, x, y), repo in zip(spots, repos[:4]):
        t = fade(tile(thumb(repo), 210, 138), 0.9)
        t = t.rotate(ang, resample=Image.BICUBIC, expand=True)
        shadow(c, x + 6, y + 6, t.width - 12, t.height - 12, 12, strength=120, spread=14)
        c.alpha_composite(t, (x, y))

    d = ImageDraw.Draw(c)
    kw = chip_w(d, kicker, body, 22)
    chip(d, MID - kw / 2, 42, kicker, body, 22, accent, accent, fill=BG)

    art = cover_img(cid, 540)                       # 320×180 → 540×304
    c.alpha_composite(art, (MID - art.width // 2, 70))

    d = ImageDraw.Draw(c)
    y = titles(d, 378, title, disp, by_char, sizes=(62, 58, 54, 50, 46, 44))
    chips_row(d, y + 14, list(facts), body, 22, fill=BG)
    return finish(c, path, accent, lang)


def home_card(path, lang, kicker, title, facts, accent, cids):
    """홈 — 홈 화면의 코스 격자 그대로. 코스 14개를 두 줄로 깝니다."""
    disp, body = CHAIN[lang]['display'], CHAIN[lang]['body']
    by_char = lang in NO_SPACES

    c = canvas_of()
    glow_at(c, MID, 420, 360, 160, accent, 45)

    tw, th, gap = 158, 100, 12
    x0 = (W - (7 * tw + 6 * gap)) // 2
    for i, cid in enumerate(cids[:14]):
        col, row = i % 7, i // 7
        x, y = x0 + col * (tw + gap), 34 + row * (th + gap)
        shadow(c, x, y, tw, th, 12, strength=110, spread=10, dy=6)
        card = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(card).rounded_rectangle([0, 0, tw - 1, th - 1], radius=12,
                                               fill=SURFACE + (255,), outline=LINE, width=2)
        art = cover_img(cid, tw + 30)
        card.alpha_composite(art, ((tw - art.width) // 2, (th - art.height) // 2))
        mask = round_mask(tw, th, 12)
        card.putalpha(Image.composite(card.getchannel('A'), Image.new('L', (tw, th), 0), mask))
        c.alpha_composite(card, (x, y))

    d = ImageDraw.Draw(c)
    y = 34 + 2 * th + gap + 24
    kw = chip_w(d, kicker, body, 22)
    chip(d, MID - kw / 2, y, kicker, body, 22, accent, accent, fill=BG)
    y = titles(d, y + 58, title, disp, by_char, sizes=(56, 52, 48, 44))
    chips_row(d, y + 14, list(facts), body, 22, fill=BG)
    return finish(c, path, accent, lang)


def all_card(path, lang, kicker, title, facts, accent, repos):
    """전체 실험 — 실험 화면 모자이크. 전체 실험 화면이 실제로 그렇게 생겼습니다."""
    disp, body = CHAIN[lang]['display'], CHAIN[lang]['body']
    by_char = lang in NO_SPACES

    c = canvas_of()
    tw, th, gap = 140, 92, 10
    cols, rows = 8, 6
    x0 = (W - (cols * tw + (cols - 1) * gap)) // 2
    y0 = 18
    i = 0
    for row in range(rows):
        for col in range(cols):
            repo = repos[i % len(repos)]
            i += 1
            t = tile(thumb(repo), tw, th, r=10, edge=(30, 36, 78), ew=1)
            c.alpha_composite(fade(t, 0.8), (x0 + col * (tw + gap), y0 + row * (th + gap)))

    # 모자이크를 가라앉히고 가운데에 판을 얹습니다. 아래쪽은 더 어둡게 —
    # 도메인과 로고가 실험 화면 위에서 읽히지 않았습니다.
    veil = Image.new('RGBA', (W, H), BG + (120,))
    c.alpha_composite(veil)
    darken_below(c, 470, 0, 230)

    d = ImageDraw.Draw(c)
    px0, px1, py0, py1 = 318, 882, 176, 452
    shadow(c, px0, py0, px1 - px0, py1 - py0, 26, strength=190, spread=22)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([px0, py0, px1, py1], radius=26, fill=BG + (238,), outline=accent, width=2)

    kw = chip_w(d, kicker, body, 22)
    chip(d, MID - kw / 2, py0 + 30, kicker, body, 22, accent, accent)
    y = titles(d, py0 + 92, title, disp, by_char, sizes=(64, 60, 56, 52, 48, 44), width=px1 - px0 - 60)
    chips_row(d, y + 16, list(facts), body, 22, width=px1 - px0 - 60)
    return finish(c, path, accent, lang)


def sim_names(lang, titles_, sims):
    """실험 이름 — 언어별 덮어쓰기가 있으면 그것을, 없으면 영어 제목을 씁니다.
    한국어만 sims.json 에 제목이 들어 있습니다 (site/content/sim-titles.json 의 주석 참고)."""
    out = {}
    for s in sims:
        over = titles_.get(s['repo'], {}).get(lang)
        out[s['repo']] = over or (s['title'] if lang == 'ko' else s.get('titleEn') or s['title'])
    return out


# 모자이크 순서 — 과목이 골고루 섞이게. 같은 과목이 한데 몰리면 한 가지 색만 보입니다.
def mosaic_order(sims):
    by = {}
    for s in sorted(sims, key=lambda s: s['repo']):
        by.setdefault(s.get('subject'), []).append(s['repo'])
    out, groups = [], list(by.values())
    while any(groups):
        for g in groups:
            if g:
                out.append(g.pop(0))
    return out


def build(lang, titles_, sims):
    ui = json.load(io.open(f'{ROOT}/i18n/ui.{lang}.json', encoding='utf-8'))
    data = json.load(io.open(f'{ROOT}/content/{lang}/courses.json', encoding='utf-8'))
    lessons = json.load(io.open(f'{ROOT}/content/{lang}/lessons.json', encoding='utf-8'))

    def t(key, **kw):
        s = ui[key]
        for k, v in kw.items():
            s = s.replace('{' + k + '}', str(v))
        return s

    nsims = len(sims)
    ncourses = len(data['courses'])
    out = f'{OUT}/{lang}'
    cids = [c['id'] for c in data['courses']]
    made = []

    # 홈 제목은 세 토막으로 나뉘어 있습니다. 띄어쓰기가 없는 언어는 붙여 씁니다.
    join = '' if lang in NO_SPACES else ' '
    made.append(home_card(
        f'{out}/default.{EXT}', lang, t('site.tagline'),
        join.join([t('home.title.a'), t('home.title.b'), t('home.title.c')]),
        [t('og.sims', n=nsims), t('og.courses', n=ncourses), t('og.free')],
        (46, 230, 214), cids))

    # 전체 실험 — 지금까지 홈 카드를 같이 썼습니다. 홈 제목("읽고 끝내지 말고…")이
    # 이 페이지를 설명하지 못해 따로 굽습니다. seo.all.title 은 네 언어 모두
    # '제목 — 설명 | Nudge' 꼴이라 앞 토막만 씁니다.
    made.append(all_card(
        f'{out}/all.{EXT}', lang, f"{t('all.subject')} · {t('all.grade')}",
        t('seo.all.title', n=nsims).split(' — ')[0],
        [t('og.free'), t('og.noAds')],
        (46, 230, 214), mosaic_order(sims)))

    for c in data['courses']:
        accent = SUBJECT.get(c['subject'], (127, 136, 184))
        made.append(course_card(
            f"{out}/c-{c['id']}.{EXT}", lang, c['id'], f"{c['no']} · {c['subject']}",
            c['title'],
            [t('og.sims', n=len(c['sims'])), t('course.minutes', n=c['minutes'])],
            accent, c['sims']))

    for lid, L in lessons.items():
        if lid.startswith('_'):
            continue          # _note 같은 메모 키는 레슨이 아닙니다
        course = next(x for x in data['courses'] if x['id'] == L['course'])
        meta = next(x for x in data['lessons'][L['course']] if x['id'] == lid)
        accent = SUBJECT.get(course['subject'], (127, 136, 184))
        made.append(lesson_card(
            f'{out}/l-{lid}.{EXT}', lang, f"{course['no']} {course['title']}",
            L['title'], t('og.lessonMinutes', n=meta['min']), accent, L['sim']))
    return made


def main():
    want = [a for a in sys.argv[1:] if not a.startswith('-')] or list(LANGS)
    bad = [w for w in want if w not in LANGS]
    if bad:
        sys.exit(f'모르는 언어: {", ".join(bad)} (쓸 수 있는 것: {", ".join(LANGS)})')

    titles_ = json.load(io.open(f'{ROOT}/content/sim-titles.json', encoding='utf-8'))
    sims = json.load(io.open(os.path.join(PHET, 'deploy', 'sims.json'), encoding='utf-8'))

    total = 0
    for lang in want:
        made = build(lang, titles_, sims)
        kb = sum(os.path.getsize(p) for p in made) / 1024
        big = max(os.path.getsize(p) for p in made) / 1024
        print('%s — %3d장  %7.1f KB  (가장 큰 것 %.0f KB)  → %s/%s/' % (lang, len(made), kb, big, OUT, lang))
        total += len(made)
    print('\n%d장 구웠습니다.' % total)


if __name__ == '__main__':
    main()
