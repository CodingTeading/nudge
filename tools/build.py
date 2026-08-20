"""배포본 조립 — site/ + PhET 산출물 → dist/

  python tools/build.py

dist/ 는 git 에 넣지 않습니다. 시뮬레이션 61종(약 205MB)은 PhET 포크에서 구운
산출물이라 이 저장소의 소스가 아닙니다. 자세한 사정은 README 를 보세요.

  NUDGE_PHET=../phet python tools/build.py   # PhET 포크 위치를 바꾸려면
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHET = os.environ.get('NUDGE_PHET', os.path.join(HERE, '..', 'phet'))
DEPLOY = os.path.join(PHET, 'deploy')
DIST = os.path.join(HERE, 'dist')

# PhET 포크에서 가져오는 것 — 전부 빌드 산출물입니다
FROM_PHET = ['sims', 'thumbs', 'assets', 'sims.json']


def human(n):
    for u in ('B', 'KB', 'MB', 'GB'):
        if n < 1024:
            return '%.1f %s' % (n, u)
        n /= 1024
    return '%.1f TB' % n


def size_of(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    return sum(os.path.getsize(os.path.join(r, f))
               for r, _, fs in os.walk(path) for f in fs)


def count_of(path):
    if os.path.isfile(path):
        return 1
    return sum(len(fs) for _, _, fs in os.walk(path))


def main():
    if not os.path.isdir(DEPLOY):
        sys.exit('PhET 산출물을 찾을 수 없습니다: %s\n'
                 'NUDGE_PHET 으로 포크 위치를 지정하세요.' % DEPLOY)

    missing = [n for n in FROM_PHET if not os.path.exists(os.path.join(DEPLOY, n))]
    if missing:
        sys.exit('PhET 쪽에 없는 것: %s' % ', '.join(missing))

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    rows = []

    # 1) 포털 (이 저장소)
    for name in os.listdir(os.path.join(HERE, 'site')):
        src = os.path.join(HERE, 'site', name)
        dst = os.path.join(DIST, name)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
    rows.append(('site/ (this repo)', count_of(os.path.join(HERE, 'site')),
                 size_of(os.path.join(HERE, 'site'))))

    # 2) PhET 산출물
    for name in FROM_PHET:
        src = os.path.join(DEPLOY, name)
        dst = os.path.join(DIST, name)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
        rows.append(('%s (phet fork)' % name, count_of(src), size_of(src)))

    print('dist/ 조립 완료\n')
    for label, n, sz in rows:
        print('  %-26s %5d files  %10s' % (label, n, human(sz)))
    total_n, total_sz = count_of(DIST), size_of(DIST)
    print('  %-26s %5d files  %10s' % ('total', total_n, human(total_sz)))

    # Cloudflare Pages 한계 — 넘으면 업로드가 통째로 실패합니다
    big = [(os.path.relpath(os.path.join(r, f), DIST), os.path.getsize(os.path.join(r, f)))
           for r, _, fs in os.walk(DIST) for f in fs
           if os.path.getsize(os.path.join(r, f)) > 25 * 1024 * 1024]
    print('\nCloudflare Pages 한계 확인')
    print('  파일 수  %6d / 20,000  %s' % (total_n, 'OK' if total_n <= 20000 else '초과!'))
    print('  25MB 초과 파일 %d개  %s' % (len(big), 'OK' if not big else '초과!'))
    for p, s in big:
        print('    !', p, human(s))
    if big or total_n > 20000:
        sys.exit(1)


if __name__ == '__main__':
    main()
