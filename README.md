# Nudge

**만지면서 배우는 과학·수학** — PhET 시뮬레이션 61종을 코스 14개로 묶고,
각 레슨에 이론과 사용 방법을 붙인 10대용 학습 사이트.

<https://nudge.codingteading.com>

이름 그대로입니다. PhET 실험에서 실제로 하는 행동은 하나 — **값을 살짝 밀어 보는 것.**
로고는 오른쪽으로 밀린 슬라이더 손잡이와, 방금 전까지 그것이 있던 자리입니다.

- 무료 · 회원가입 없음 · **광고 없음**
- 한국어 기준, 영어 · 일본어 · 스페인어 틀 준비됨
- 진도는 서버가 아니라 브라우저(localStorage)에 남습니다

## 레슨은 어떻게 짜여 있나

`예상 → 실험 → 설명`(POE) 7블록입니다.

| # | 블록 | 핵심 |
|---|---|---|
| ① | 훅 | 현상 질문 하나 |
| ② | **예상하기** | **정답을 알려주지 않고 저장만 합니다** |
| ③ | 실험하기 | 시뮬레이션 조작 미션 2~4개 |
| ④ | 관찰 기록 | 본 것을 직접 적습니다 |
| ⑤ | **개념 정리** | **②의 예상과 대조하며 밝힙니다** |
| ⑥ | 실생활 연결 | |
| ⑦ | 확인 문제 | |

②에서 정답을 미루는 것이 이 구조의 전부입니다. 예상이 틀렸다는 걸 ⑤에서 스스로
발견할 때 개념이 박힙니다. 정답을 먼저 주면 그냥 읽고 넘어갑니다.

## 구조

```
site/                  사이트 소스 (이 저장소가 가진 전부)
  index.html           홈 — 코스 14개
  course.html          코스 — 레슨 목록
  lesson.html          레슨 — 이론 + 시뮬레이션 + 사용 방법
  all.html             전체 실험 61종 (과목·학년 필터) ※ 리스킨 대기
  brand.html           로고 후보 검토 기록
  site.css tokens.css  디자인 토큰과 화면 스타일
  lib/                 i18n · SEO 런타임
  i18n/ui.<lang>.json  UI 문구 (ko en ja es)
  content/<lang>/      코스 · 레슨 본문 · 시뮬레이션 사용법
  brand/  og/          로고 · 공유 이미지
tools/                 빌드 · 검사 도구
dist/                  배포본 (git 에 넣지 않음)
```

### 시뮬레이션은 이 저장소에 없습니다

`sims/`(61종, 약 205MB) · `thumbs/` · `assets/fonts/` · `sims.json` 은
**PhET 포크에서 구운 산출물**이라 여기 두지 않습니다. 빌드할 때 가져옵니다.

```bash
python tools/build.py          # site/ + PhET 산출물 → dist/
```

기본값으로 `../phet/deploy` 를 찾습니다. 다른 곳이면 `NUDGE_PHET=/경로` 로 지정하세요.
포크는 `scenery`·`joist` 등의 색과 서체를 손본 것이고, GPL-3.0 이라 그쪽 저장소가
수정 소스 공개 의무를 집니다.

## 개발

```bash
python tools/build.py          # dist/ 조립 (+ Cloudflare Pages 한계 검사)
python tools/serve.py 8124     # dist/ 를 띄웁니다
node   tools/lint.mjs          # 정합성 검사
python tools/make-og.py        # og/*.png 16장 (1200×630)
python tools/make-sitemap.py   # sitemap.xml + robots.txt
```

`tools/serve.py` 가 따로 있는 이유: Windows 의 파이썬은 `.js` 의 MIME 을 레지스트리에서
읽는데 많은 기계에서 `text/plain` 으로 잡혀 ES 모듈 로딩이 막힙니다. 확장자 표를 고정합니다.

### 정합성 검사가 보는 것

UI 문구 키가 네 언어에서 일치하는지 · 자리표시자 `{n}` 개수가 같은지 ·
코스가 시뮬레이션 61종을 빠짐없이 중복 없이 덮는지 · `ready` 레슨의 본문이 있는지 ·
정답 번호가 선택지 범위 안인지 · 언어표에 61종이 다 있는지.

## 배포

Cloudflare Pages 직접 업로드입니다 (Git 연동 아님).

```bash
python tools/build.py
npx wrangler pages deploy dist --project-name nudge
```

## 알아 둘 것

### 언어가 세 층입니다

가용 범위가 서로 달라 따로 다룹니다.

| 층 | 어디 | 지금 |
|---|---|---|
| UI 문구 | `i18n/ui.<lang>.json` | 4개 언어 전부 |
| 학습 콘텐츠 | `content/<lang>/` | ko 만 (없으면 ko 로 떨어지고 화면에 알림) |
| 시뮬레이션 | `?locale=<lang>` | 종마다 다름 (ko 55 · ja 43 · es 56 / 61) |

지금은 언어를 `?lang=` 쿼리로 넘깁니다. 정식 빌드에서는 `/ko/` `/ja/` 처럼 경로로 갈라
**언어별 정적 HTML** 을 구워야 합니다.

### 검색·공유 머리말은 정적으로 구워야 합니다

`lib/seo.js` 는 자바스크립트로 `<head>` 를 채웁니다. 구글은 JS 를 실행하지만
**카카오톡·네이버·페이스북의 미리보기 수집기는 실행하지 않습니다.**
한국 학생이 링크를 나르는 곳이 카카오톡이라, 여기가 비면 공유 카드가 통째로 빈 채
돌아다닙니다. 그래서 각 HTML `<head>` 에 한국어 기준값을 박아 두었고, 정식 빌드는
**언어 × 페이지마다** 구워야 합니다.

### 시뮬레이션을 iframe 으로 다룰 때

`lesson.html` 에 전부 들어 있습니다.

1. **포스터를 눌러야 로드.** 평균 3.4MB 를 미리 받지 않습니다
2. **`postMessageOnLoad` 는 값을 붙이면 안 됩니다.** `type:'flag'` 라 `=true` 를 주면
   PhET 의 QueryStringMachine 이 죽습니다
3. **크기는 `aspect-ratio: 1024/618`** (`ScreenView.DEFAULT_LAYOUT_BOUNDS`).
   높이를 제한할 때 `max-height` 를 쓰면 비율이 깨집니다 — `.stage` 의 `--stage-max-h` 로
   `max-width` 를 계산합니다
4. **`allowLinks=false`** 로 시뮬레이션 안에서 외부로 나가지 못하게 합니다
5. **저작자 표시는 시뮬레이션 바로 아래.** 푸터가 아닙니다

## 라이선스

| | |
|---|---|
| 이 저장소의 코드·원고 | **MIT** (`LICENSE`) |
| PhET 시뮬레이션 | **CC BY-NC 4.0** — PhET Interactive Simulations, University of Colorado Boulder |
| PhET 시뮬레이션 코드 | **GPL-3.0** (수정본 소스는 PhET 포크 저장소) |

**광고를 붙이면 CC BY-NC 를 어길 소지가 큽니다.** 이 사이트를 비영리로 두는 이유입니다.

PhET 의 로고와 이름은 CC 와 별개인 상표라 변경도 제거도 하지 않습니다.

## 남은 것

- 시뮬레이션 사용 방법 57종 (코스 01 의 4종만 작성됨)
- 레슨 본문 — `static-2` 한 편만
- `ja` `es` 학습 콘텐츠
- `all.html` 을 같은 토큰으로 리스킨
- 워드마크를 패스로 고정 (지금은 시스템 서체라 기기마다 달라집니다)
- OG 이미지를 OFL 서체로 재생성 (지금은 Windows 맑은 고딕)
- 썸네일을 `?locale=ko` 로 재촬영 (지금 영어 제목이 박혀 있습니다)
