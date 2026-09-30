"""공유 카드가 제대로 걸려 있는지 단언합니다.

  python tools/build.py       # 빌드가 부릅니다 (보통은 이쪽)
  python tools/check-og.py [dist]

왜 필요한가
  카드를 새로 구운 뒤 옛 카드가 조용히 돌아오거나, 레슨을 새로 넣고 카드를 굽지
  않아 404 카드가 나가는 일을 막습니다. 카카오·네이버가 받아 가는 것은 태그가
  아니라 파일이라, 태그만 보지 않고 가리키는 파일을 열어 실제 픽셀과 용량까지
  봅니다.

보는 것
  og:image 가 한 장인가 · twitter:image 가 그것과 같은가 · og:image:alt 이 있는가
  width 1200 · height 630 태그가 있는가 · 가리키는 파일이 실제로 1200x630 인가
  200KB 이하인가

  네이버는 가로 그림의 가운데를 정사각으로 잘라 쓰므로(1200x630 이면 x 285~915)
  카드의 알맹이는 그 안에 있어야 합니다. 그건 tools/make-og.py 의 판짜기가
  맡습니다 — 여기서는 크기와 연결만 봅니다.
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'dist'))

# 우리가 만든 쪽이 아닌 것. 시뮬레이션은 PhET 산출물이고 색인에서도 빼 둡니다.
SKIP_TOP = ('sims', '_proto')

MAX_KB = 200
WANT = (1200, 630)


def png_size(path):
    """PNG 머리에서 픽셀 크기를 읽습니다. 태그 값이 아니라 파일을 믿기 위해서입니다.
    (Pillow 를 쓰면 빌드에 의존성이 하나 늘어납니다 — 여기서는 24바이트면 됩니다.)"""
    with io.open(path, 'rb') as f:
        head = f.read(24)
    if len(head) < 24 or head[1:4] != b'PNG' or head[12:16] != b'IHDR':
        return None
    return (int.from_bytes(head[16:20], 'big'), int.from_bytes(head[20:24], 'big'))


def jpeg_size(path):
    """JPEG 의 SOF 표지에서 픽셀 크기를 읽습니다. 표지를 차례로 건너뛰며 찾습니다."""
    SOF = set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}
    with io.open(path, 'rb') as f:
        if f.read(2) != bytes([0xFF, 0xD8]):
            return None
        while True:
            b = f.read(1)
            while b and b[0] != 0xFF:
                b = f.read(1)
            while b and b[0] == 0xFF:
                b = f.read(1)
            if not b:
                return None
            marker = b[0]
            seg = f.read(2)
            if len(seg) < 2:
                return None
            n = int.from_bytes(seg, 'big')
            if marker in SOF:
                data = f.read(5)
                return (int.from_bytes(data[3:5], 'big'), int.from_bytes(data[1:3], 'big'))
            f.seek(n - 2, 1)


def image_size(path):
    return png_size(path) or jpeg_size(path)


def pages_of(dist):
    for root, _, files in os.walk(dist):
        rel = os.path.relpath(root, dist).replace(os.sep, '/')
        if rel.split('/')[0] in SKIP_TOP:
            continue
        for name in sorted(files):
            if name.endswith('.html'):
                yield os.path.join(root, name)


def check(dist):
    bad = []
    seen = 0
    cards = set()

    for path in pages_of(dist):
        page = os.path.relpath(path, dist).replace(os.sep, '/')
        html = io.open(path, encoding='utf-8').read()
        og = re.findall(r'<meta property="og:image" content="([^"]+)"', html)
        if not og:
            continue
        seen += 1

        if len(og) > 1:
            bad.append((page, 'og:image 가 %d개입니다 — 한 장이어야 합니다' % len(og)))
        tw = re.findall(r'<meta name="twitter:image" content="([^"]+)"', html)
        if tw[:1] != og[:1]:
            bad.append((page, 'twitter:image 가 og:image 와 다릅니다'))
        if not re.search(r'<meta property="og:image:alt" content="[^"]+"', html):
            bad.append((page, 'og:image:alt 이 없거나 비었습니다'))
        for key, want in (('width', WANT[0]), ('height', WANT[1])):
            if '<meta property="og:image:%s" content="%d">' % (key, want) not in html:
                bad.append((page, 'og:image:%s 태그가 없거나 %d 이 아닙니다' % (key, want)))

        # 절대 주소에서 경로만 떼어 배포본 안의 파일을 찾습니다.
        rel = og[0].split('//', 1)[-1].split('/', 1)[-1] if '//' in og[0] else og[0].lstrip('/')
        f = os.path.join(dist, *rel.split('/'))
        cards.add(rel)
        if not os.path.isfile(f):
            bad.append((page, '카드 파일이 없습니다 — %s' % og[0]))
            continue
        size = image_size(f)
        if size != WANT:
            bad.append((page, '카드가 %dx%d 이 아닙니다 — %s %s' % (WANT + (rel, size))))
        kb = os.path.getsize(f) / 1024
        if kb > MAX_KB:
            bad.append((page, '카드가 %dKB 를 넘습니다 — %s %.0fKB' % (MAX_KB, rel, kb)))

    print('공유 카드 확인')
    print('  og:image 를 쓰는 쪽 %d개 · 카드 %d장' % (seen, len(cards)))
    if bad:
        print('  문제 %d건' % len(bad))
        for page, why in bad[:20]:
            print('    ! %s — %s' % (page, why))
        if len(bad) > 20:
            print('    … 그리고 %d건' % (len(bad) - 20))
        sys.exit('공유 카드가 어긋났습니다. python tools/make-og.py 를 돌렸는지 확인하세요.')
    print('  전부 %dx%d · %dKB 이하 · alt · twitter=og  OK' % (WANT + (MAX_KB,)))


if __name__ == '__main__':
    if not os.path.isdir(DIST):
        sys.exit('배포본이 없습니다: %s' % DIST)
    check(DIST)
