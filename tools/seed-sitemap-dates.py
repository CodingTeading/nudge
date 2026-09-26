"""data/sitemap-dates.json 의 날짜를 "내용이 실제로 바뀐 날"로 한 번 채웁니다.

  python tools/seed-sitemap-dates.py

왜 필요한가
  make-sitemap.py 는 지문이 처음 보이는 URL 에 오늘 날짜를 줍니다. 그래서 지도를
  처음 만들면 77개가 전부 오늘이 되는데, 그건 사실이 아닙니다. 실제로 이 사이트
  본문은 2026-08 에 네 언어 원고를 마친 뒤로 크게 바뀌지 않았습니다.

  그래서 각 URL 의 본문이 어느 파일에서 나오는지 보고, 그 파일들의 마지막 커밋
  날짜 중 가장 늦은 것을 넣습니다. 지문은 건드리지 않습니다.

정밀도는 파일 단위입니다 — 그래도 괜찮습니다
  레슨 61편이 lessons.json 한 파일에 들어 있어 씨앗 날짜는 61개가 같아집니다.
  하지만 씨앗은 한 번뿐이고, 그다음부터는 make-sitemap.py 의 지문이 레슨 단위로
  갈라 줍니다. 그래서 이 도구를 다시 돌릴 일은 없습니다.

  네 언어를 모두 보는 이유는 지문도 네 언어를 함께 보기 때문입니다. 한국어
  파일만 보면 일본어판을 낸 날이 지워져 실제보다 옛 날짜가 붙습니다.
"""
import io, json, os, subprocess, sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DATES = 'data/sitemap-dates.json'
LANGS = ['ko', 'en', 'ja', 'es']

# URL 꼬리 → 그 페이지의 본문이 담긴 파일들
COURSES = [f'site/content/{l}/courses.json' for l in LANGS]
LESSONS = ([f'site/content/{l}/lessons.json' for l in LANGS]
           + [f'site/content/{l}/guides.json' for l in LANGS])
ALL = ['site/content/sim-titles.json']


def git_date(path):
    out = subprocess.run(['git', 'log', '-1', '--format=%ad', '--date=short', '--', path],
                         capture_output=True, text=True).stdout.strip()
    if not out:
        sys.exit('커밋 기록이 없습니다: %s' % path)
    return out


def files_for(loc):
    tail = loc.rstrip('/').rsplit('/', 1)[-1] if loc.rstrip('/') else ''
    if '/l/' in loc:
        # 레슨 화면에는 코스 줄(걸리는 시간·난이도)도 함께 나옵니다.
        return LESSONS + COURSES
    if '/c/' in loc:
        return COURSES + LESSONS
    if tail == 'all':
        return ALL
    return COURSES


def main():
    if not os.path.exists(DATES):
        sys.exit('%s 가 없습니다. 먼저 python tools/make-sitemap.py 를 돌리세요.' % DATES)

    cache = {}
    def date_of(path):
        if path not in cache:
            cache[path] = git_date(path)
        return cache[path]

    m = json.load(io.open(DATES, encoding='utf-8'))
    before, after = {}, {}
    for loc, v in m.items():
        before[v['date']] = before.get(v['date'], 0) + 1
        v['date'] = max(date_of(p) for p in files_for(loc))
        after[v['date']] = after.get(v['date'], 0) + 1

    io.open(DATES, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(m, ensure_ascii=False, indent=2) + '\n')

    print('참고한 파일의 마지막 커밋 날짜')
    for p, d in sorted(cache.items()):
        print('  %s  %s' % (d, p))
    print('\nURL %d개' % len(m))
    print('  전:', json.dumps(before, ensure_ascii=False))
    print('  후:', json.dumps(after, ensure_ascii=False))
    print('\n이제 python tools/make-sitemap.py 를 다시 돌려 sitemap.xml 에 반영하세요.')


if __name__ == '__main__':
    main()
