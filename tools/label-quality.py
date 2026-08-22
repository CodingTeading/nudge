"""PhET 번역 자체의 품질 이상 훑기 — 우리 원고가 아니라 **원본**을 봅니다.

  python tools/label-quality.py            # ko · ja · es 전부
  python tools/label-quality.py ko         # 하나만

`lint.mjs` 와 목적이 다릅니다. lint 는 **우리 원고**가 화면에 없는 글자를 인용하는지
보고 오류 0 을 지켜야 하는 검사이고, 이 도구는 **PhET 쪽 번역**의 이상을 모아
`docs/PHET-TRANSLATION-FIXES.md` 에 낼 거리를 찾습니다. 우리가 고칠 수 없는 것이라
언제나 종료 코드 0 입니다 — 보고서입니다.

보는 것:

  [A] 줄 나뉜 문자열   원문에 <br> · \\n 이 있는 자리. 줄마다 따로 옮기다 낱말이
                       겹치는 사고가 납니다 (한국어 '벽 제거 제거' 가 그것입니다)
  [B] 안 옮겨진 영어   CJK 번역 안에 영어 낱말이 그대로 남은 자리
  [C] 문장부호         마침표 겹침 · 스페인어 여는 ¿ ¡ 누락
  [D] 군더더기 공백    앞뒤 공백 · 줄 바꿈 없는 공백(U+00A0)

대조 기준은 PhET 포크입니다 — `NUDGE_PHET` 로 경로를 바꿀 수 있습니다.
"""
import io, json, os, re, sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHET = os.environ.get('NUDGE_PHET', os.path.join(HERE, '..', 'phet'))
LANGS = ['ko', 'ja', 'es']
CJK = {'ko', 'ja'}
SHARED = ['joist', 'scenery-phet', 'sun', 'vegas']

# 번역 안에 남아도 이상하지 않은 것들 — 단위 · 기호 · 고유명사
KEEP_EN = {
    'atm', 'kpa', 'nm', 'mol', 'ppm', 'ppb', 'kg', 'amu', 'iqr', 'mad', 'phet',
    'html', 'sim', 'url', 'led', 'dna', 'rna', 'atp', 'gps',
}


def flatten(node, prefix=''):
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


def load(path):
    try:
        with io.open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def lines(s):
    return [x.strip() for x in re.split(r'\n|<br\s*/?>', s) if x.strip()]


def strip_markup(s):
    """자리표시자와 태그를 걷어 낸 알맹이. 남은 영어를 셀 때 씁니다."""
    s = re.sub(r'\{\{[^}]*\}\}|\{\d+\}', ' ', s)
    return re.sub(r'<[^>]*>', ' ', s)


def repos_to_check():
    table = load(os.path.join(HERE, 'site', 'content', 'sim-locales.json')) or {}
    got = set(r for r, v in table.items() if isinstance(v, list)) | set(SHARED)
    for r in list(got):
        dep = load(os.path.join(PHET, r, 'dependencies.json')) or {}
        got |= {k for k in dep if k != 'comment'}
    return sorted(r for r in got
                  if os.path.isfile(os.path.join(PHET, r, '%s-strings_en.json' % r)))


def check(lang, repo, en, tr):
    """(구분, key, 영어, 번역, 한 줄 설명) 목록."""
    out = []
    for key, e in en.items():
        if key == 'a11y' or key.startswith('a11y.'):
            continue
        t = tr.get(key)
        if not t or not t.strip():
            continue

        le, lt = lines(e), lines(t)

        # [A] 원문도 번역도 여러 줄 — 줄마다 따로 옮기다 겹치기 쉬운 자리
        if len(le) > 1 and len(lt) > 1:
            toks = [w for ln in lt for w in ln.split()]
            dup = len(toks) != len(set(toks))
            out.append(('A', key, e, t,
                        '줄 안에서 같은 낱말이 되풀이됨' if dup else '사람이 눈으로 볼 것'))

        # [B] CJK 번역에 영어가 그대로 남음
        if lang in CJK:
            body = strip_markup(t)
            if re.search(r'[가-힣ぁ-んァ-ヴ一-龥]', body):
                en_words = set(w.lower() for w in re.findall(r'[A-Za-z]+', strip_markup(e)))
                left = [w for w in re.findall(r'[A-Za-z]{4,}', body)
                        if w.lower() not in KEEP_EN and w.lower() in en_words]
                if left:
                    out.append(('B', key, e, t, '안 옮겨진 영어: ' + ' · '.join(sorted(set(left)))))

        # [C] 문장부호
        why = []
        if '..' in t.replace('...', ''):
            why.append('마침표가 겹침')
        # 스페인어 여는 부호. 낱말이 든 문장에서만 봅니다 — '??' 나 '( ?, ? )' 같은
        # 수학 자리표시자까지 잡으면 시끄럽기만 합니다.
        if lang == 'es' and re.search(r'[A-Za-zÁÉÍÓÚÑáéíóúñ]{2}', strip_markup(t)):
            if re.search(r'(^|\s)![A-Za-zÁÉÍÓÚÑáéíóúñ]', t) and '¡' not in t:
                why.append('여는 ¡ 가 없음')
            if t.rstrip().endswith('?') and '¿' not in t and ' ' in t.strip():
                why.append('여는 ¿ 가 없음')
        if why:
            out.append(('C', key, e, t, ' · '.join(why)))

        # [D] 군더더기 공백.
        # 숫자와 단위 사이의 U+00A0 은 PhET 이 줄 바꿈을 막으려고 일부러 넣은 것이라
        # 그 자체는 보지 않습니다. 눈에 띄는 두 가지만 봅니다 —
        # 보통 공백이 잇달아 둘, 그리고 앞뒤에 남은 공백(U+00A0 포함).
        why = []
        if t != t.strip() and e == e.strip():
            why.append('앞뒤에 공백이 남음')
        if '  ' in strip_markup(t).strip() and '  ' not in strip_markup(e):
            why.append('가운데 공백이 잇달아 둘')
        if why:
            out.append(('D', key, e, t, ' · '.join(why)))
    return out


def main():
    langs = sys.argv[1:] or LANGS
    bad = [l for l in langs if l not in LANGS]
    if bad:
        sys.exit('모르는 언어: %s (쓸 수 있는 것: %s)' % (', '.join(bad), ', '.join(LANGS)))

    repos = repos_to_check()
    if not repos:
        sys.exit('PhET 포크를 찾지 못했습니다. NUDGE_PHET 을 확인하세요.')

    TITLE = {'A': '줄 나뉜 문자열', 'B': '안 옮겨진 영어',
             'C': '문장부호', 'D': '군더더기 공백'}

    for lang in langs:
        rows = []
        for repo in repos:
            en = flatten(load(os.path.join(PHET, repo, '%s-strings_en.json' % repo)) or {})
            tr = flatten(load(os.path.join(
                PHET, 'babel', repo, '%s-strings_%s.json' % (repo, lang))) or {})
            if not tr:
                continue
            for kind, key, e, t, why in check(lang, repo, en, tr):
                rows.append((kind, repo, key, e, t, why))

        print('\n═══ %s — %d건 ═══' % (lang, len(rows)))
        for kind in 'ABCD':
            got = [r for r in rows if r[0] == kind]
            if not got:
                continue
            print('\n[%s] %s — %d건' % (kind, TITLE[kind], len(got)))
            for _, repo, key, e, t, why in got:
                print('  %s/%s  — %s' % (repo, key, why))
                print('      en : %s' % ' ⏎ '.join(lines(e)))
                print('      %s : %s' % (lang, ' ⏎ '.join(lines(t))))

    print('\n보고서입니다 — PhET 쪽 번역이라 우리가 고칠 수 없습니다.')
    print('낼 만한 것은 docs/PHET-TRANSLATION-FIXES.md 로 옮기세요.')


if __name__ == '__main__':
    main()
