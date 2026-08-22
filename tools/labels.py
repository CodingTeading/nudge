"""화면 글자 사전 뽑기 — 번역 전에 한 번만 돌립니다.

  python tools/labels.py            # ko · en · es · ja 전부
  python tools/labels.py ja         # 하나만

docs/I18N-BRIEF.md §4-2 의 ① 방법을 세션마다 반복하지 않도록 미리 뽑아 둡니다.
결과는 wip/labels/<lang>/<repo>.json 입니다.

  screen    그 시뮬레이션을 그 언어로 열었을 때 화면에 실제로 찍히는 글자
  fallback  그 언어 번역이 빠져 있어 영어로 찍히는 글자 (인용할 때 영어로 쓰세요)
  hidden    a11y.* — 스크린리더 전용이라 어느 언어로도 화면에 안 나옵니다. 인용 금지

fallback 이 따로 있는 이유: sim-locales.json 은 "번역이 있다"만 알려 줍니다.
번역이 있어도 문자열 단위로 빠진 것은 영어로 그려집니다. 한국어판에서 화면에
없는 글자를 찾게 만든 사고가 22곳 있었고, 그 자리들이 이런 틈에서 나왔습니다.
"""
import io, json, os, re, sys

# 윈도우 콘솔이 cp949 라 한글·일본어를 그대로 못 찍습니다.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHET = os.environ.get('NUDGE_PHET', os.path.join(HERE, '..', 'phet'))
OUT = os.path.join(HERE, 'wip', 'labels')
LANGS = ['ko', 'en', 'es', 'ja']

# 실험마다 붙는 공통 화면 요소. 조작 이름을 인용할 때 자주 쓰입니다.
# 이 넷은 _shared.json 에 따로 뽑으므로 시뮬레이션마다 다시 넣지 않습니다.
SHARED = ['joist', 'scenery-phet', 'sun', 'vegas']


def load(path):
    try:
        with io.open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def flatten(node, prefix=''):
    """{ "a": { "value": "…" } } 와 { "a11y": { "b": { "value": "…" } } } 를
       같은 평평한 표로 폅니다. value 가 있는 곳이 잎입니다."""
    out = {}
    if not isinstance(node, dict):
        return out
    if isinstance(node.get('value'), str):
        out[prefix] = node['value']
        return out
    for k, v in node.items():
        if k == 'history':
            continue
        out.update(flatten(v, k if not prefix else prefix + '.' + k))
    return out


def strings_en(repo):
    return flatten(load(os.path.join(PHET, repo, '%s-strings_en.json' % repo)) or {})


def strings_lang(repo, lang):
    if lang == 'en':
        return strings_en(repo)
    p = os.path.join(PHET, 'babel', repo, '%s-strings_%s.json' % (repo, lang))
    return flatten(load(p) or {})


IMPORT = re.compile(r"from '(?:\.\./)+([a-z0-9-]+)/js/")


def deps(repo):
    """시뮬레이션이 끌어다 쓰는 저장소들. 화면 글자의 일부가 여기서 옵니다 —
       예를 들어 coulombs-law 의 'Force Values' 와 'Hidden' 은
       inverse-square-law-common 에 있습니다. 시뮬레이션 파일만 읽으면 놓칩니다.

       dependencies.json 이 오래된 경우가 있습니다 — alpha-decay 는
       nuclear-decay-common 을 빠뜨리는데 화면 글자는 대부분 거기 있습니다.
       그래서 소스의 import 문도 함께 훑습니다."""
    names = set(k for k in (load(os.path.join(PHET, repo, 'dependencies.json')) or {})
                if k != 'comment')

    js = os.path.join(PHET, repo, 'js')
    for root, dirs, files in os.walk(js):
        dirs[:] = [d for d in dirs if d != 'node_modules']
        for f in files:
            if not f.endswith(('.ts', '.js')):
                continue
            try:
                with io.open(os.path.join(root, f), encoding='utf-8') as fh:
                    names.update(IMPORT.findall(fh.read()))
            except Exception:
                pass

    return [k for k in sorted(names)
            if k not in SHARED and k != repo
            and os.path.isfile(os.path.join(PHET, k, '%s-strings_en.json' % k))]


def build(repo, lang, opens_in):
    """opens_in 이 en 이면 그 언어 번역이 아예 없는 시뮬입니다 — 전부 영어입니다."""
    en = strings_en(repo)
    got = strings_lang(repo, opens_in)

    # screen 은 '실제로 그려지는 글자' 전부입니다. 그중 번역이 있는 시뮬인데도
    # 이 문자열만 영어로 떨어지는 자리를 fallback 에 한 번 더 적어 둡니다.
    screen, fallback, hidden = {}, {}, []
    for key in sorted(en):
        if key == 'a11y' or key.startswith('a11y.'):
            hidden.append(key)
            continue
        if key in got and got[key].strip():
            screen[key] = got[key]
        else:
            screen[key] = en[key]
            if opens_in != 'en':
                fallback[key] = en[key]
    # 딸린 저장소의 글자. 키 앞에 저장소 이름을 붙여 어디서 왔는지 남깁니다.
    common = {}
    for dep in deps(repo):
        den = strings_en(dep)
        if not den:
            continue
        dgot = strings_lang(dep, opens_in) if opens_in != 'en' else den
        for key in sorted(den):
            if key == 'a11y' or key.startswith('a11y.'):
                continue
            v = dgot.get(key)
            common['%s.%s' % (dep, key)] = v if v and v.strip() else den[key]

    return {
        'repo': repo,
        'lang': lang,
        'opensIn': opens_in,
        '_note': ('이 시뮬레이션은 %s 로 열립니다. screen 이 화면에 실제로 찍히는 글자 '
                  '전부이니 그대로 인용하세요. common 은 딸린 저장소에서 오는 글자로, '
                  '이것도 화면에 나옵니다. fallback 은 번역이 빠져 영어로 찍히는 '
                  '자리입니다. hidden 은 화면에 절대 안 나옵니다.' % opens_in),
        'screen': screen,
        'common': common,
        'fallback': fallback,
        'hidden': hidden,
    }


def main():
    langs = sys.argv[1:] or LANGS
    bad = [l for l in langs if l not in LANGS]
    if bad:
        sys.exit('모르는 언어: %s (쓸 수 있는 것: %s)' % (', '.join(bad), ', '.join(LANGS)))

    table = load(os.path.join(HERE, 'site', 'content', 'sim-locales.json')) or {}
    repos = sorted(r for r, v in table.items() if isinstance(v, list))
    if not repos:
        sys.exit('sim-locales.json 을 읽을 수 없습니다')

    for lang in langs:
        d = os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        english, holes, missing = [], 0, []

        for repo in repos:
            opens_in = lang if lang in table[repo] else 'en'
            if opens_in == 'en' and lang != 'en':
                english.append(repo)
            data = build(repo, lang, opens_in)
            if not data['screen']:
                missing.append(repo)
            if opens_in != 'en' and data['fallback']:
                holes += 1
            with io.open(os.path.join(d, repo + '.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=1)

        shared = {}
        for repo in SHARED:
            opens_in = lang if strings_lang(repo, lang) else 'en'
            shared[repo] = build(repo, lang, opens_in)
        with io.open(os.path.join(d, '_shared.json'), 'w', encoding='utf-8') as f:
            json.dump(shared, f, ensure_ascii=False, indent=1)

        print('%s — %d종' % (lang, len(repos)))
        if english:
            print('   영어로 열림 %d종: %s' % (len(english), ' '.join(english)))
        if holes:
            print('   번역이 있으나 일부 문자열이 영어로 찍히는 시뮬 %d종 (fallback 을 보세요)' % holes)
        if missing:
            print('   ! 문자열 파일을 못 찾음: %s' % ' '.join(missing))


if __name__ == '__main__':
    main()
