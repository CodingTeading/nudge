"""공유 이미지 서체가 그 언어 글자를 갖고 있는지 봅니다.

  python tools/font-check.py

make-og.py 는 제목을 Jua 로 그리고, Jua 에 없는 글자가 섞이면 그 줄만
Pretendard 로 떨어집니다. 그래서 마지막 방어선은 Pretendard 입니다.
Pretendard 에도 없으면 두부(□)가 찍힙니다.

표본은 wip/labels/<lang>/*.json 의 화면 글자입니다 — 실제로 그 언어에서
쓰게 될 글자들입니다. 먼저 python tools/labels.py 를 돌리세요.
"""
import io, json, os, sys, glob

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = {
    'Jua (제목)': 'tools/fonts/Jua-Regular.ttf',
    'Pretendard-Bold (제목 대체 · 본문 굵게)': 'tools/fonts/Pretendard-Bold.otf',
    'Pretendard-Regular (본문)': 'tools/fonts/Pretendard-Regular.otf',
}
# 스페인어에서 반드시 나오는 글자. 표본에 안 잡혀도 따로 넣습니다.
ES_EXTRA = 'áéíóúüñÁÉÍÓÚÜÑ¿¡'


def charset(path):
    f = TTFont(os.path.join(HERE, path), fontNumber=0, lazy=True)
    out = set()
    for t in f['cmap'].tables:
        out |= set(t.cmap.keys())
    f.close()
    return out


def sample(lang):
    chars = set()
    for p in glob.glob(os.path.join(HERE, 'wip', 'labels', lang, '*.json')):
        with io.open(p, encoding='utf-8') as fh:
            d = json.load(fh)
        bags = [d] if 'screen' in d else list(d.values())   # _shared.json 은 한 겹 더 깊습니다
        for b in bags:
            for v in b.get('screen', {}).values():
                chars |= set(v)
    return chars


def main():
    if not os.path.isdir(os.path.join(HERE, 'wip', 'labels')):
        sys.exit('wip/labels 가 없습니다. 먼저 python tools/labels.py 를 돌리세요.')

    fonts = {name: charset(p) for name, p in FONTS.items()}
    worst = 0

    for lang in ('en', 'es', 'ja'):
        chars = sample(lang)
        if lang == 'es':
            chars |= set(ES_EXTRA)
        if not chars:
            continue
        print('\n%s — 표본 %d자' % (lang, len(chars)))
        for name, have in fonts.items():
            miss = sorted(c for c in chars if ord(c) not in have and not c.isspace())
            if miss:
                worst += 1
                head = ''.join(miss[:40])
                print('  ✗ %-42s 없는 글자 %d자: %s%s'
                      % (name, len(miss), head, ' …' if len(miss) > 40 else ''))
            else:
                print('  ✓ %-42s 전부 있음' % name)

    print()
    if worst:
        print('Jua 에 없는 글자는 Pretendard 로 떨어지므로 괜찮습니다.')
        print('Pretendard 두 개 중 하나라도 ✗ 이면 그 언어 공유 이미지에 두부(□)가 찍힙니다.')
    else:
        print('세 서체 모두 표본을 덮습니다.')


if __name__ == '__main__':
    main()
