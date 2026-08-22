"""공유 이미지 서체가 그 언어 글자를 갖고 있는지 봅니다.

  python tools/font-check.py

`make-og.py` 는 언어마다 서체 사슬이 다릅니다 (거기 CHAIN 을 그대로 가져다 씁니다).
앞에서부터 그 줄을 통째로 덮는 서체를 고르고, 아무것도 못 덮으면 글자 단위로
나눠 그립니다. 그래서 두부(□)가 찍히는 건 **사슬의 어느 서체에도 없는 글자**뿐입니다.

표본은 실제로 카드에 그려지는 글자입니다 — 코스·레슨 제목과 훅, 과목 이름,
실험 이름, 그리고 칩에 쓰는 UI 문구. 시뮬레이션 화면 글자가 아닙니다.
"""
import io, json, os, sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module

og = import_module('make-og') if os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make-og.py')) else None
if og is None:                                    # 파일 이름에 하이픈이 있어 직접 읽습니다
    sys.exit('tools/make-og.py 를 찾지 못했습니다.')

ROOT = 'site'
CHIP_KEYS = ('site.tagline', 'home.title.a', 'home.title.b', 'home.title.c',
             'home.lead', 'og.sims', 'og.courses', 'og.free', 'og.noAds',
             'og.lessonMinutes', 'course.minutes')


def cover(path):
    f = TTFont(path, lazy=True)
    out = set()
    for t in f['cmap'].tables:
        out |= set(t.cmap.keys())
    f.close()
    return out


def og_chars(lang, titles, sims):
    """그 언어의 카드에 실제로 그려질 글자."""
    chars = set()
    ui = json.load(io.open(f'{ROOT}/i18n/ui.{lang}.json', encoding='utf-8'))
    for k in CHIP_KEYS:
        chars |= set(str(ui.get(k, '')))
    c = json.load(io.open(f'{ROOT}/content/{lang}/courses.json', encoding='utf-8'))
    L = json.load(io.open(f'{ROOT}/content/{lang}/lessons.json', encoding='utf-8'))
    for x in c['courses']:
        chars |= set(x['title'] + x['hook'] + x['subject'] + x['no'])
        for m in c['lessons'][x['id']]:
            chars |= set(m['title'] + m['hook'])
    for k, v in L.items():
        if not k.startswith('_'):
            chars |= set(v['title'])
    for name in og.sim_names(lang, titles, sims).values():
        chars |= set(name)
    return {ch for ch in chars if not ch.isspace()}


def main():
    if not os.path.isdir(ROOT):
        sys.exit('저장소 뿌리에서 돌리세요.')
    titles = json.load(io.open(f'{ROOT}/content/sim-titles.json', encoding='utf-8'))
    try:
        sims = json.load(io.open('../phet/deploy/sims.json', encoding='utf-8'))
    except OSError:
        sys.exit('../phet/deploy/sims.json 이 없습니다. NUDGE_PHET 쪽을 확인하세요.')

    have = {}
    bad = 0

    for lang in og.LANGS:
        chars = og_chars(lang, titles, sims)
        chain = og.CHAIN[lang]
        paths = list(dict.fromkeys(chain['display'] + chain['body']))
        for p in paths:
            have.setdefault(p, cover(p))

        # 사슬을 통틀어 아무도 못 가진 글자만이 두부가 됩니다.
        union = set().union(*(have[p] for p in paths))
        tofu = sorted(ch for ch in chars if ord(ch) not in union)

        print('\n%s — 카드 표본 %d자' % (lang, len(chars)))
        for p in paths:
            miss = sorted(ch for ch in chars if ord(ch) not in have[p])
            name = os.path.basename(p)
            if miss:
                print('  · %-24s 없는 글자 %3d자 → 다음 서체로 넘김' % (name, len(miss)))
            else:
                print('  ✓ %-24s 전부 있음' % name)
        if tofu:
            bad += 1
            print('  ✗ 사슬 어디에도 없는 글자 %d자: %s' % (len(tofu), ''.join(tofu)))
        else:
            print('  ✓ 사슬이 표본을 전부 덮습니다')

    print()
    if bad:
        print('✗ 두부(□)가 찍힐 언어가 %d개 있습니다. 사슬에 서체를 더하세요.' % bad)
        sys.exit(1)
    print('네 언어 모두 두부 없이 그려집니다.')


if __name__ == '__main__':
    main()
