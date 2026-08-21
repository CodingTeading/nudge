# -*- coding: utf-8 -*-
"""'Nudge' 워드마크를 Jua 의 글자 윤곽에서 뽑아 SVG 패스로 굽습니다.

지금까지는 화면에서 웹폰트로 그렸습니다. 폰트가 늦게 오거나 막히면 로고가
기기마다 다른 글자체로 보였습니다. 패스로 구우면 어디서나 같은 모양입니다.

만드는 것:
  site/brand/wordmark.svg   글자만 (패스)
  site/brand/logo.svg       기호 + 글자 (배포·공유용 한 장)
"""
import io, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

sys.stdout.reconfigure(encoding='utf-8')

FONT = 'tools/fonts/Jua-Regular.ttf'
WORD = 'Nudge'
CAP = 100.0          # 글자 높이를 이 값으로 맞춥니다 (SVG 좌표계 단위)

f = TTFont(FONT)
upem = f['head'].unitsPerEm
cmap = f.getBestCmap()
gs = f.getGlyphSet()
hmtx = f['hmtx']

scale = CAP / upem
# 폰트 좌표는 y 가 위로 자라고 SVG 는 아래로 자랍니다. 뒤집고 기준선을 내립니다.
ascent = f['hhea'].ascent * scale
descent = -f['hhea'].descent * scale

paths, x = [], 0.0
for ch in WORD:
    gname = cmap[ord(ch)]
    pen = SVGPathPen(gs)
    # 글자 하나를 옮기고(x), 뒤집고(-1), 기준선 위에 올립니다.
    tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, x, ascent))
    gs[gname].draw(tpen)
    d = pen.getCommands()
    if d:
        paths.append(d)
    x += hmtx[gname][0] * scale

W = round(x, 2)
H = round(ascent + descent, 2)

# 실제로 잉크가 닿는 범위로 여백을 다듬습니다 — 글자 옆 빈틈이 로고를 어긋나 보이게 합니다.
from fontTools.pens.boundsPen import BoundsPen
bx0 = by0 = 1e9
bx1 = by1 = -1e9
x = 0.0
for ch in WORD:
    gname = cmap[ord(ch)]
    bp = BoundsPen(gs)
    gs[gname].draw(bp)
    if bp.bounds:
        x0, y0, x1, y1 = bp.bounds
        bx0 = min(bx0, x + x0 * scale)
        bx1 = max(bx1, x + x1 * scale)
        by0 = min(by0, ascent - y1 * scale)
        by1 = max(by1, ascent - y0 * scale)
    x += hmtx[gname][0] * scale

PAD = 2.0
vb = (round(bx0 - PAD, 2), round(by0 - PAD, 2),
      round(bx1 - bx0 + PAD * 2, 2), round(by1 - by0 + PAD * 2, 2))

body = '\n  '.join(f'<path d="{d}"/>' for d in paths)

wordmark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img" aria-label="Nudge">
  <title>Nudge</title>
  <!-- Jua (SIL Open Font License 1.1) 의 글자 윤곽을 패스로 구운 것입니다.
       폰트 로딩과 무관하게 어디서나 같은 모양으로 보입니다. -->
  <g fill="currentColor">
  {body}
  </g>
</svg>
'''
io.open('site/brand/wordmark.svg', 'w', encoding='utf-8', newline='\n').write(wordmark)
print(f'site/brand/wordmark.svg  viewBox={vb}  패스 {len(paths)}개')

# ── 기호 + 글자를 합친 한 장 ────────────────────────────────────────
MARK = 32.0                     # 기호의 원래 좌표계
gap = 9.0
sh = vb[3]                      # 글자 높이
mark_h = sh * 1.28              # 기호를 글자보다 살짝 크게
ms = mark_h / MARK
total_w = mark_h + gap + vb[2]
off_y = (mark_h - sh) / 2       # 글자를 기호 세로 가운데에 맞춥니다

logo = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {round(total_w,2)} {round(mark_h,2)}" role="img" aria-label="Nudge">
  <title>Nudge</title>
  <g transform="scale({ms:.4f})">
    <line x1="4" y1="16" x2="28" y2="16" stroke="#262d5c" stroke-width="2.6" stroke-linecap="round"/>
    <line x1="8.5" y1="12" x2="8.5" y2="20" stroke="#6a72a8" stroke-width="2.2" stroke-linecap="round" opacity=".55"/>
    <line x1="13" y1="12.8" x2="13" y2="19.2" stroke="#6a72a8" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>
    <circle cx="21" cy="16" r="6" fill="#ffa53d"/>
  </g>
  <g fill="#e9ecff" transform="translate({round(mark_h + gap - vb[0], 2)} {round(off_y - vb[1], 2)})">
  {body}
  </g>
</svg>
'''
io.open('site/brand/logo.svg', 'w', encoding='utf-8', newline='\n').write(logo)
print(f'site/brand/logo.svg      {round(total_w,2)} × {round(mark_h,2)}')
