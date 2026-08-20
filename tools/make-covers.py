"""코스 커버 SVG 14장 생성 — site/covers/<id>.svg

  python tools/make-covers.py

`<img>` 로 쓰이므로 CSS 변수를 못 씁니다. 색을 박아 넣되 tokens.css 와 같은 값입니다.
바탕은 투명 — 카드의 배경이 그대로 비쳐야 합니다.

규격
  viewBox 320×180 · 선 굵기 3.5 · 둥근 끝 · 내용은 30..290 × 25..155 안에
  주 색 = 과목색, 보조 = ink-soft, 흐림 = ink-faint
"""
import io, os

OUT = 'site/covers'

VIOLET, BLUE, PINK, GREEN, CYAN = '#9d5cff', '#4d9bff', '#ff4d8d', '#35e08f', '#2ee6d6'
SOFT, FAINT, AMBER = '#a5addb', '#6a72a8', '#ffa53d'


def wrap(body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" '
            f'fill="none" role="img" aria-label="{label}">\n'
            f'  <g stroke-linecap="round" stroke-linejoin="round">\n{body}\n  </g>\n</svg>\n')


def dots(pts, r, fill, op=1):
    return '\n'.join(f'    <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{op}"/>'
                     for x, y in pts)


COVERS = {}

# 01 보이지 않는 힘 — 두 전하와 그 사이의 역선
COVERS['force-unseen'] = ('두 전하와 역선', f'''
    <path d="M128 62 C 160 48, 192 48, 224 62" stroke="{FAINT}" stroke-width="3" opacity=".65"/>
    <path d="M126 90 L 226 90" stroke="{FAINT}" stroke-width="3" opacity=".65"/>
    <path d="M128 118 C 160 132, 192 132, 224 118" stroke="{FAINT}" stroke-width="3" opacity=".65"/>
    <circle cx="100" cy="90" r="23" fill="{VIOLET}"/>
    <path d="M100 80 L100 100 M90 90 L110 90" stroke="#0a0c18" stroke-width="4"/>
    <circle cx="250" cy="90" r="23" fill="{SOFT}"/>
    <path d="M240 90 L260 90" stroke="#0a0c18" stroke-width="4"/>''')

# 02 던지면 어디에 떨어질까 — 포물선
COVERS['throw'] = ('포물선 궤적', f'''
    <path d="M34 146 L286 146" stroke="{FAINT}" stroke-width="3"/>
    <path d="M56 146 Q 160 6, 264 146" stroke="{VIOLET}" stroke-width="3.5"/>
    <path d="M56 146 L86 108" stroke="{AMBER}" stroke-width="3.5"/>
    <path d="M78 110 L88 106 L86 118" stroke="{AMBER}" stroke-width="3.5"/>
{dots([(160,76),(264,146)], 7, VIOLET)}
    <circle cx="56" cy="146" r="8" fill="{AMBER}"/>''')

# 03 흔들림과 파동 — 위상이 어긋난 두 파동
COVERS['wave'] = ('두 파동', f'''
    <path d="M34 90 C 64 34, 94 34, 124 90 S 184 146, 214 90 S 274 34, 290 62"
          stroke="{FAINT}" stroke-width="3" opacity=".55"/>
    <path d="M30 118 C 60 62, 90 62, 120 118 S 180 174, 210 118 S 270 62, 292 84"
          stroke="{VIOLET}" stroke-width="3.5"/>
    <path d="M30 90 L292 90" stroke="{FAINT}" stroke-width="2" opacity=".4" stroke-dasharray="1 8"/>''')

# 04 빛의 정체 — 볼록렌즈에 모이는 평행 광선
COVERS['light'] = ('렌즈와 광선', f'''
    <path d="M148 34 C 176 62, 176 118, 148 146 C 120 118, 120 62, 148 34 Z"
          stroke="{SOFT}" stroke-width="3.5"/>
    <path d="M34 56 L136 56 M34 90 L134 90 M34 124 L136 124" stroke="{VIOLET}" stroke-width="3.5"/>
    <path d="M160 56 L262 90 M162 90 L262 90 M160 124 L262 90" stroke="{VIOLET}"
          stroke-width="3.5" opacity=".9"/>
    <circle cx="266" cy="90" r="7" fill="{AMBER}"/>''')

# 05 원자 속으로 — 핵과 전자 궤도
COVERS['atom'] = ('원자 궤도', f'''
    <ellipse cx="160" cy="90" rx="112" ry="42" stroke="{FAINT}" stroke-width="3" opacity=".6"/>
    <ellipse cx="160" cy="90" rx="112" ry="42" stroke="{PINK}" stroke-width="3.5"
             transform="rotate(60 160 90)"/>
    <ellipse cx="160" cy="90" rx="112" ry="42" stroke="{PINK}" stroke-width="3.5"
             transform="rotate(-60 160 90)" opacity=".55"/>
{dots([(150,80),(170,80),(160,98),(148,96),(172,98)], 9, PINK)}
{dots([(216,141),(90,52)], 8, AMBER)}''')

# 06 양자 — 겹쳐 있는 두 상태
COVERS['quantum'] = ('겹친 두 상태', f'''
    <circle cx="128" cy="90" r="52" stroke="{VIOLET}" stroke-width="3.5" stroke-dasharray="1 10"/>
    <circle cx="192" cy="90" r="52" stroke="{CYAN}" stroke-width="3.5" stroke-dasharray="1 10"/>
    <path d="M160 42 A 52 52 0 0 1 160 138 A 52 52 0 0 1 160 42 Z" fill="{VIOLET}" opacity=".3"/>
    <circle cx="160" cy="90" r="9" fill="{AMBER}"/>''')

# 07 우주는 어떻게 도는가 — 항성과 궤도
COVERS['space'] = ('궤도를 도는 행성', f'''
    <ellipse cx="150" cy="90" rx="122" ry="58" stroke="{FAINT}" stroke-width="3" opacity=".55"/>
    <ellipse cx="150" cy="90" rx="82" ry="36" stroke="{CYAN}" stroke-width="3.5"/>
    <circle cx="122" cy="90" r="20" fill="{AMBER}"/>
    <circle cx="232" cy="90" r="10" fill="{CYAN}"/>
    <circle cx="272" cy="90" r="8" fill="{SOFT}" opacity=".8"/>
{dots([(60,38),(268,36),(46,142),(250,146)], 3, SOFT, .7)}''')

# 08 물질의 세 얼굴 — 고체 · 액체 · 기체
COVERS['matter'] = ('고체 액체 기체', f'''
    <path d="M112 30 L112 150 M208 30 L208 150" stroke="{FAINT}" stroke-width="2.5"
          opacity=".5" stroke-dasharray="1 8"/>
{dots([(48,62),(76,62),(48,90),(76,90),(48,118),(76,118)], 9, PINK)}
{dots([(140,66),(168,74),(184,58),(146,98),(176,104),(152,128),(182,130)], 9, PINK, .8)}
{dots([(236,44),(288,58),(248,86),(292,110),(232,124),(272,146)], 8, PINK, .55)}''')

# 09 섞으면 무슨 일이 — 두 비커와 반응
COVERS['react'] = ('섞이는 두 용액', f'''
    <path d="M42 40 L42 128 A14 14 0 0 0 56 142 L86 142 A14 14 0 0 0 100 128 L100 40"
          stroke="{SOFT}" stroke-width="3.5"/>
    <path d="M42 100 L100 100 L100 128 A14 14 0 0 1 86 142 L56 142 A14 14 0 0 1 42 128 Z"
          fill="{PINK}" opacity=".75"/>
    <path d="M220 40 L220 128 A14 14 0 0 0 234 142 L264 142 A14 14 0 0 0 278 128 L278 40"
          stroke="{SOFT}" stroke-width="3.5"/>
    <path d="M220 90 L278 90 L278 128 A14 14 0 0 1 264 142 L234 142 A14 14 0 0 1 220 128 Z"
          fill="{CYAN}" opacity=".7"/>
    <path d="M126 90 L192 90" stroke="{AMBER}" stroke-width="3.5"/>
    <path d="M178 78 L192 90 L178 102" stroke="{AMBER}" stroke-width="3.5"/>
{dots([(238,66),(258,52),(266,74)], 5, "#ffffff", .55)}''')

# 10 분수는 사실 나눗셈 — 4등분 중 3칸
COVERS['fraction'] = ('4분의 3', f'''
    <path d="M160 26 A64 64 0 0 1 224 90 L160 90 Z" fill="{BLUE}"/>
    <path d="M224 90 A64 64 0 0 1 160 154 L160 90 Z" fill="{BLUE}" opacity=".8"/>
    <path d="M160 154 A64 64 0 0 1 96 90 L160 90 Z" fill="{BLUE}" opacity=".6"/>
    <circle cx="160" cy="90" r="64" stroke="{SOFT}" stroke-width="3.5"/>
    <path d="M96 90 L224 90 M160 26 L160 154" stroke="{SOFT}" stroke-width="3.5"/>''')

# 11 비율의 감각 — 2 : 3
COVERS['ratio'] = ('두 막대의 비 2 대 3', f'''
    <rect x="62" y="56" width="86" height="30" rx="15" fill="{BLUE}"/>
    <rect x="62" y="104" width="129" height="30" rx="15" fill="{BLUE}" opacity=".6"/>
    <path d="M105 56 L105 86" stroke="#0a0c18" stroke-width="3"/>
    <path d="M105 104 L105 134 M148 104 L148 134" stroke="#0a0c18" stroke-width="3"/>
    <path d="M215 71 L253 71" stroke="{AMBER}" stroke-width="3.5"/>
    <path d="M215 91 L253 91" stroke="{AMBER}" stroke-width="3.5" opacity=".45"/>
    <path d="M215 119 L253 119" stroke="{AMBER}" stroke-width="3.5"/>
    <path d="M215 99 L253 99" stroke="{AMBER}" stroke-width="3.5" opacity=".45"/>
    <path d="M234 62 L234 128" stroke="{FAINT}" stroke-width="2.5"
          opacity=".45" stroke-dasharray="1 7"/>''')


# 12 그래프로 말하기 — 축 위의 직선과 곡선
COVERS['graph'] = ('직선과 곡선', f'''
    <path d="M56 30 L56 146 L286 146" stroke="{FAINT}" stroke-width="3"/>
    <path d="M70 138 Q 160 26, 250 138" stroke="{SOFT}" stroke-width="3.5" opacity=".6"/>
    <path d="M70 132 L262 44" stroke="{BLUE}" stroke-width="3.5"/>
{dots([(70,132),(166,88),(262,44)], 7, BLUE)}
    <path d="M166 88 L262 88 M262 88 L262 44" stroke="{AMBER}" stroke-width="3"
          stroke-dasharray="1 8"/>''')

# 13 살아있는 것들과 지구 — 세포막을 지나는 물질
COVERS['life'] = ('세포막 통과', f'''
    <path d="M30 70 L290 70 M30 110 L290 110" stroke="{GREEN}" stroke-width="3.5" opacity=".85"/>
{dots([(50,70),(82,70),(114,70),(146,70),(178,70),(210,70),(242,70),(274,70)], 7, GREEN, .55)}
{dots([(50,110),(82,110),(114,110),(146,110),(178,110),(210,110),(242,110),(274,110)], 7, GREEN, .55)}
    <path d="M130 34 L130 146" stroke="{AMBER}" stroke-width="3.5" stroke-dasharray="1 10"/>
    <path d="M118 134 L130 146 L142 134" stroke="{AMBER}" stroke-width="3.5"/>
    <circle cx="130" cy="34" r="9" fill="{AMBER}"/>
{dots([(206,42),(252,52)], 8, SOFT, .5)}''')

# 14 숫자와 친해지기 — 수직선 위의 거리
COVERS['number'] = ('수직선 위의 거리', f'''
    <path d="M34 112 L288 112" stroke="{FAINT}" stroke-width="3"/>
{"".join(f'    <path d="M{34+ i*36} 104 L{34 + i*36} 120" stroke="{FAINT}" stroke-width="3"/>' + chr(10) for i in range(8))}
    <path d="M106 62 L214 62" stroke="{AMBER}" stroke-width="3.5"/>
    <path d="M118 50 L106 62 L118 74 M202 50 L214 62 L202 74" stroke="{AMBER}" stroke-width="3.5"/>
    <path d="M106 62 L106 104 M214 62 L214 104" stroke="{AMBER}" stroke-width="2.5"
          opacity=".5" stroke-dasharray="1 7"/>
    <circle cx="106" cy="112" r="10" fill="{BLUE}"/>
    <circle cx="214" cy="112" r="10" fill="{BLUE}"/>''')


def main():
    os.makedirs(OUT, exist_ok=True)
    for cid, (label, body) in COVERS.items():
        p = f'{OUT}/{cid}.svg'
        io.open(p, 'w', encoding='utf-8').write(wrap(body.rstrip(), label))
    print('made %d covers in %s' % (len(COVERS), OUT))
    for cid in COVERS:
        print('  %-14s %5d B' % (cid, os.path.getsize(f'{OUT}/{cid}.svg')))


if __name__ == '__main__':
    main()
