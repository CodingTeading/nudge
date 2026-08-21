"""OG 이미지 생성 — 1200×630 PNG.

  python .claude/make-og.py

카카오톡·페이스북·X 는 og:image 로 SVG 를 받지 않습니다. 래스터가 필요합니다.
한국 학생들이 링크를 나르는 곳이 카카오톡이라 이 그림이 유입의 첫 관문입니다.

서체는 tools/fonts/ 에 넣어 둔 것을 씁니다 — 둘 다 SIL Open Font License 라
  저장소에 담아도 되고, 어느 기계에서 돌려도 같은 그림이 나옵니다.
  제목·워드마크는 Jua(사이트의 표시 서체), 본문은 Pretendard(사이트의 본문 서체).
"""
import io, json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = 'site'
OUT = f'{ROOT}/og'
W, H = 1200, 630

FONTS = 'tools/fonts'
FONT_KR_B = f'{FONTS}/Pretendard-Bold.otf'      # 본문 굵게
FONT_KR_R = f'{FONTS}/Pretendard-Regular.otf'   # 본문
FONT_DISPLAY = f'{FONTS}/Jua-Regular.ttf'       # 제목·워드마크 (사이트와 같은 서체)
FONT_LAT_B = FONT_DISPLAY

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
}


def font(path, size):
    return ImageFont.truetype(path, size)


_COVER = {}


def _covers(path, text):
    """그 서체가 이 글자들을 전부 갖고 있는지. 없으면 두부 상자가 찍힙니다."""
    if path not in _COVER:
        from fontTools.ttLib import TTFont
        _COVER[path] = set(TTFont(path).getBestCmap())
    have = _COVER[path]
    return all(ord(c) in have for c in text if not c.isspace())


def display_font(text, size):
    """제목은 사이트와 같은 Jua 로. 다만 Jua 에 없는 글자(· ² → − 등)가 섞이면
    그 줄만 통째로 본문 서체로 넘깁니다 — 한 글자 때문에 상자가 찍히는 게 더 나쁩니다."""
    return font(FONT_DISPLAY if _covers(FONT_DISPLAY, text) else FONT_KR_B, size)


def wrap(draw, text, f, max_w):
    """한국어는 어절 단위로 끊습니다 (음절 단위로 자르면 읽기가 나빠집니다)."""
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
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


def logo(d, x, y, s=1.0):
    """Nudge 마크 — 슬라이더 손잡이가 살짝 밀린 모양."""
    def p(v):
        return v * s
    d.line([(x + p(4), y + p(16)), (x + p(28), y + p(16))], fill=LINE, width=int(p(2.6)))
    d.line([(x + p(8.5), y + p(12)), (x + p(8.5), y + p(20))], fill=(90, 97, 145), width=int(p(2.2)))
    d.line([(x + p(13), y + p(12.8)), (x + p(13), y + p(19.2))], fill=INK_FAINT, width=int(p(2.2)))
    r = p(6)
    d.ellipse([x + p(21) - r, y + p(16) - r, x + p(21) + r, y + p(16) + r], fill=AMBER)


def chip(d, x, y, text, f, fg=INK_SOFT):
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 34, y + 46], radius=23, outline=LINE, width=2)
    d.text((x + 17, y + 10), text, font=f, fill=fg)
    return x + tw + 34 + 12


def card(path, kicker, title, sub, chips, accent):
    img = Image.new('RGB', (W, H), BG)
    nebula(img)
    d = ImageDraw.Draw(img)

    f_word = font(FONT_LAT_B, 40)
    f_title = display_font(title, 62)
    f_sub = font(FONT_KR_R, 30)
    f_chip = font(FONT_KR_R, 24)

    # 왼쪽 과목색 띠
    d.rounded_rectangle([0, 0, 14, H], radius=0, fill=accent)

    # 로고 잠금 — 마크의 세로 중심을 워드마크 글자 중심에 맞춥니다
    logo(d, 74, 47, 2.0)
    d.text((156, 56), 'Nudge', font=f_word, fill=INK)

    d.text((74, 168), kicker, font=display_font(kicker, 26), fill=accent)

    y = 210
    for line in wrap(d, title, f_title, W - 160)[:3]:
        d.text((74, y), line, font=f_title, fill=INK)
        y += 78

    y += 8
    for line in wrap(d, sub, f_sub, W - 160)[:2]:
        d.text((74, y), line, font=f_sub, fill=INK_SOFT)
        y += 44

    x = 74
    for c in chips:
        x = chip(d, x, H - 96, c, f_chip)

    img.save(path, 'PNG', optimize=True)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    ui = json.load(io.open(f'{ROOT}/i18n/ui.ko.json', encoding='utf-8'))
    data = json.load(io.open(f'{ROOT}/content/ko/courses.json', encoding='utf-8'))
    lessons = json.load(io.open(f'{ROOT}/content/ko/lessons.json', encoding='utf-8'))
    sims = json.load(io.open('../phet/deploy/sims.json', encoding='utf-8'))
    simname = {s['repo']: s['title'] for s in sims}

    made = []
    made.append(card(
        f'{OUT}/default.png', ui['site.tagline'],
        '읽고 끝내지 말고 만져 보고 알아내세요',
        '질문 하나에서 시작해 실험으로 답을 찾는 코스 14개',
        ['실험 61종', '코스 14개', '무료 · 가입 없음', '광고 없음'],
        (46, 230, 214)))

    for c in data['courses']:
        accent = SUBJECT.get(c['subject'], (127, 136, 184))
        made.append(card(
            f"{OUT}/c-{c['id']}.png", f"{c['no']} · {c['subject']}",
            c['title'], c['hook'],
            [f"실험 {len(c['sims'])}종", f"약 {c['minutes']}분", '무료 · 가입 없음'],
            accent))

    for lid, L in lessons.items():
        if lid.startswith('_'):
            continue          # _note 같은 메모 키는 레슨이 아닙니다
        course = next(x for x in data['courses'] if x['id'] == L['course'])
        meta = next(x for x in data['lessons'][L['course']] if x['id'] == lid)
        accent = SUBJECT.get(course['subject'], (127, 136, 184))
        made.append(card(
            f'{OUT}/l-{lid}.png', f"{course['no']} {course['title']}",
            L['title'], meta['hook'],
            [simname.get(L['sim'], L['sim']), f"{meta['min']}분", '무료 · 가입 없음'],
            accent))

    print('made %d images in %s' % (len(made), OUT))
    for p in made:
        print('  %-46s %6.1f KB' % (os.path.basename(p), os.path.getsize(p) / 1024))


if __name__ == '__main__':
    main()
