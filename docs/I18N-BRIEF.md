# Nudge 다국어 작업 의뢰서

이 문서 하나만 읽고 시작할 수 있게 썼습니다. 저장소는 `C:/projects/nudge`,
PhET 포크는 `C:/projects/phet` 입니다.

- 작성일: 2026-08-21
- 사이트: <https://nudge.codingteading.com>
- 지금 상태: **네 언어 원고 61편 완성** · 배포 중
- 마지막 갱신: 2026-08-23 (일본어 완료)

---

## 0. 한 줄 요약

**이 일은 번역이 아니라 재작성에 가깝습니다.**

원고의 미션과 사용법은 **시뮬레이션 화면에 실제로 그려지는 글자**를 그대로 인용합니다.
그 글자는 언어마다 다르고, 번역이 없는 시뮬레이션은 **영어로 열립니다.**
그래서 `<b>에너지 균형</b>`을 일본어로 옮길 때 정답은 「エネルギー収支」가 아니라
**"그 시뮬레이션을 `?locale=ja` 로 열었을 때 화면에 실제로 찍히는 글자"** 입니다.
일본어 번역이 없는 실험이라면 정답은 영어 `Energy Balance` 입니다.

여기를 틀리면 학습자는 **화면에 없는 글자를 찾게 됩니다.** 한국어판에서 실제로 그 사고가
22곳 있었고 이번 검수에서 전부 고쳤습니다(`docs/REVIEW-RESULT.md`). 같은 실수를 세 언어에서
반복하지 않는 것이 이 작업의 핵심입니다.

---

## 1. 지금 있는 것 / 없는 것

### 1-1. UI 문구 — 네 언어 모두 완료 ✅

```
site/i18n/ui.ko.json      97개 키 (기준)
site/i18n/ui.en.json      97개
site/i18n/ui.ja.json      97개
site/i18n/ui.es.json      97개
```

`node tools/lint.mjs` 의 [1][2] 검사가 키 누락과 자리표시자(`{n}` 등) 불일치를 잡습니다.
지금 오류 0입니다. 새 키를 넣으면 **네 파일 모두** 넣어야 합니다.

### 1-2. 학습 콘텐츠 — 한국어만 있습니다 ❌

```
site/content/ko/courses.json     코스 14개 · 약 6,300자      ✅
site/content/ko/lessons.json     레슨 61편 · 약 138,000자    ✅
site/content/ko/guides.json      사용법 61종 + 공통 · 약 102,000자  ✅

site/content/en/courses.json     ✅
site/content/en/lessons.json     ✅  레슨 61편
site/content/en/guides.json      ✅  사용법 61종 + 공통

site/content/es/courses.json     ✅
site/content/es/lessons.json     ✅  레슨 61편
site/content/es/guides.json      ✅  사용법 61종 + 공통

site/content/ja/courses.json     ✅
site/content/ja/lessons.json     ✅  레슨 61편
site/content/ja/guides.json      ✅  사용법 61종 + 공통
```

**학습 콘텐츠는 네 언어가 다 찼습니다.** 남은 것은 §5-3 의 **일본어 공유 이미지(OG)**
하나입니다 — Pretendard 에 한자가 없어 지금 구우면 두부(□)가 찍힙니다.

> 작업하며 나온 것은 언어별로 따로 남겨 두었습니다 — `docs/KO-FINDINGS.md`,
> `docs/ES-FINDINGS.md`, `docs/JA-FINDINGS.md`.

### 1-3. 언어 중립 파일 (번역 대상 아님, 그러나 손봐야 할 곳이 있음)

```
site/content/sim-locales.json    시뮬레이션별 번역 보유 언어표 — 자동 생성, 건드리지 마세요
site/content/sim-titles.json     PhET 제목 오역 덮어쓰기 9종 — ko 만 있음, §4-3 참고
site/og/*.png                    공유 이미지 76장 — 한국어 글자가 박혀 있음, §5-3 참고
```

### 1-4. 폴백이 어떻게 도는가

```js
// site/lib/i18n.js
export async function loadContent( name, lang ) {
  const want = await json( `/content/${ lang }/${ name }.json` );
  if ( want ) { return { data: want, langUsed: lang, fellBack: false }; }
  const base = await json( `/content/${ BASE }/${ name }.json` );   // BASE = 'ko'
  return { data: base, langUsed: BASE, fellBack: lang !== BASE };
}
```

**파일 단위 폴백입니다.** `content/ja/lessons.json` 이 없으면 61편 전체가 한국어로 나오고,
화면 위에 `lang.fallback` 안내가 뜹니다. 반쯤 번역된 파일을 두면 **안내가 사라진 채**
한국어와 일본어가 섞여 나옵니다 — 안 한 것보다 나쁩니다.

> **그래서 규칙:** 한 언어의 `lessons.json` 은 **61편이 다 될 때까지 커밋하지 마세요.**
> 중간 산출물은 저장소 루트의 `wip/ja/lessons.json` 에 두고, 다 차면 옮깁니다.
>
> 처음에는 `site/content/_wip/` 를 권했는데, 거기는 `tools/build.py` 가 `site/` 를
> 통째로 복사해 가는 곳이라 **번역 중인 원고가 그대로 배포됩니다.** 그래서 `wip/` 로
> 옮겼습니다. 빌드에도 `_wip` 을 걸러 내는 안전장치를 넣어 두었습니다. `wip/README.md` 참고.

---

## 2. 파일 구조와 스키마

### 2-1. `courses.json`

```jsonc
{
  "courses": [
    { "id": "force-unseen", "no": "01", "subject": "물리",
      "title": "보이지 않는 힘",
      "hook": "풍선을 머리에 문지르면 왜 머리카락이 따라 올라올까?",
      "lead": "닿지 않아도 밀고 당기는 힘. 전기와 자기를 …",
      "sims": [ "balloons-and-static-electricity", … ],
      "minutes": 60 }
  ],
  "lessons": {
    "force-unseen": [
      { "id": "static-1", "ready": true, "sim": "balloons-and-static-electricity",
        "title": "…", "hook": "…", "min": 14, "diff": 1 }
    ]
  }
}
```

- `id` · `no` · `sims` · `ready` · `min` · `diff` 는 **번역하지 않습니다.** 그대로 복사하세요.
- `subject` 는 번역합니다. 다만 `site/index.html` 의 `SUBJECT_COLOR` 표에 그 언어의 과목명이
  없으면 코스 카드 색이 회색으로 떨어집니다. 새 언어를 넣을 때 그 표도 함께 채우세요.
- `minutes` 는 그 코스 레슨 `min` 의 합과 **반드시 같아야 합니다.** (한국어판에서 코스 01이
  52 ↔ 60 으로 어긋나 있었습니다. 지금은 14/14 일치.)

### 2-2. `lessons.json`

```jsonc
"atom-1": {
  "course": "atom", "sim": "build-an-atom", "screens": 1,   // ← 번역 금지
  "mode": "solve",                                          // ← 수학 코스에만. 번역 금지
  "title": "무엇이 원소를 정하는가",
  "lead":  "수소에 중성자를 하나 더 넣으면 헬륨이 될까요? …",
  "hook":  "<p>…</p>",                                      // HTML
  "predict": { "q": "…", "opts": [ "…", "…", "…", "…" ] },  // ② 예상하기
  "missions": [ "…", … ],                                   // ③ 미션 9~12개
  "record": "…",                                            // ④ 기록하기
  "explain": { "right": 1, "body": "<p>…</p>" },            // ⑤ 설명 · right 는 0부터
  "real": "…",                                              // ⑥ 실생활
  "quiz": [ { "q": "…", "opts": [ … ], "right": 0 }, … ]     // ⑦ 확인 3문항
}
```

- **`right` 는 0부터 세는 인덱스입니다.** 선택지 순서를 바꾸면 반드시 함께 고치세요.
  (한국어판 240문항 전수 검사 결과 오류 0. 이 기록을 깨지 마세요.)
- `mode: "solve"` 가 붙은 레슨은 화면의 ②·⑤ 제목이 `lesson.block2.solve` /
  `lesson.block5.solve` 로 바뀝니다. 수학 코스에서 "예상하기" 대신 "먼저 풀어 보기"를
  쓰기 위한 장치입니다. 네 언어 ui 파일에 이미 두 벌 다 있습니다.
- 맨 위 `_note` 키는 사람이 읽는 메모입니다. 그대로 두거나 그 언어로 옮기세요.

### 2-3. `guides.json`

```jsonc
"build-an-atom": {
  "summary":  "…",                                    // 한 문단
  "screens":  [ { "name": "…", "what": "…" } ],       // 화면별 설명
  "controls": [ { "name": "…", "desc": "…", "tip": "…" } ],  // 조작 하나하나
  "steps":    [ "…", … ],                             // 추천 순서
  "gotchas":  [ "…", … ]                              // 헷갈리기 쉬운 것
}
```

키는 **시뮬레이션 저장소 이름**입니다(레슨 id가 아닙니다). 한 시뮬레이션을 두 레슨이
공유해도 사용법은 하나입니다.

`_common` 은 61종 전체에 공통으로 붙는 "PhET 실험 공통 규칙" 여덟 가지입니다.
분량이 크지 않으니 **여기부터 번역하는 편이 좋습니다** — 61편 모든 레슨 아래에 붙습니다.

---

## 3. 허용 태그와 조판

`tools/lint.mjs` 의 `[7] 본문 조판` 검사가 다음을 잡습니다. 커밋 전에 반드시 통과시키세요.

| 필드 | 태그 |
|---|---|
| `hook` · `explain.body` | `<p> <ul> <li> <strong> <b> <em>` |
| `lead` · `record` · `real` · `missions[]` · 사용법 전부 | `<b>` 만 (인라인) |
| `predict.q` · `predict.opts[]` · `quiz[].q` · `quiz[].opts[]` | `<b>` 만 |

- `title` 은 **태그 금지**입니다(`<title>`·OG에 그대로 실립니다).
- 여는 태그와 닫는 태그 개수가 맞아야 하고, 폭 없는 공백(U+200B 등)이 있으면 오류입니다.
- 화면의 조작 이름은 `<b>` 로 감쌉니다. 학습자가 눈으로 찾을 대상이라서요.

### 한국어 조판 규칙 — 다른 언어에는 적용하지 마세요

한국어는 조사가 앞말에 붙습니다(`<b>모형</b>을`, `<b>모형</b> 을` 아님). 린트가 이걸
경고합니다. 검사는 있는 언어 파일 전부에 돌지만 정규식이 **한국어 조사만** 찾으므로
영어·스페인어에는 사실상 걸리지 않습니다 — 그쪽은 `the <b>Energy Balance</b> checkbox` 처럼
띄어 쓰는 것이 맞습니다. 일본어는 한국어와 같이 조사를 붙여 쓰세요.

또 하나: 한국어판에서 `<b>모형:</b> 을` 처럼 **문장 한가운데 콜론이 남는** 사고가 6건
있었습니다. 화면 라벨을 복사하다 딸려 온 것입니다. 라벨의 콜론은 인용할 때 떼세요.

---

## 4. 가장 중요한 부분 — 시뮬레이션 화면 글자 맞추기

### 4-1. 어느 언어로 열리는지부터 확인

```js
// site/lib/i18n.js
export function simLocaleFor( table, repo, lang ) {
  const have = table[ repo ] || [ 'en' ];
  return have.includes( lang ) ? lang : 'en';     // 없으면 영어로 엽니다
}
```

`site/content/sim-locales.json` 기준 보유 현황:

| 언어 | 번역 있는 시뮬레이션 |
|---|---:|
| en | 61 / 61 |
| es | 56 / 61 |
| ko | 55 / 61 |
| **ja** | **43 / 61** |

**일본어는 18종이 영어로 열립니다.** 그 18편의 미션·사용법은 **영어 라벨을 인용해야 합니다.**
스페인어는 5종, 영어는 0종입니다. 어느 것이 그런지는 아래 한 줄로 뽑으세요.
(일본어 18종의 목록과 코스별 분포는 `docs/JA-FINDINGS.md` §2 에 있습니다.)

```bash
python -c "import json,io;t=json.load(io.open('site/content/sim-locales.json',encoding='utf-8'));print([r for r,v in t.items() if isinstance(v,list) and 'ja' not in v])"
```

### 4-2. 라벨을 확인하는 세 가지 방법

**① 미리 뽑아 둔 사전을 봅니다 (가장 빠름 — 이걸로 대부분 끝납니다)**

```bash
python tools/labels.py          # en · es · ja 전부 다시 뽑기 (한 번만)
```

`wip/labels/<lang>/<repo>.json` 한 장에 `opensIn` · `screen` · `fallback` · `hidden` 이
들어 있습니다. `screen` 이 **화면에 실제로 찍히는 글자 전부**이고, `hidden` 이 `a11y.*`
(인용 금지)입니다. 아래 ②는 사전에 없는 것을 확인할 때만 쓰세요.

> **`sim-locales.json` 만 믿으면 안 됩니다.** 번역이 "있는" 시뮬레이션도 문자열 단위로
> 빠진 것은 영어로 그려집니다. 실측해 보니 **일본어는 43종 중 33종, 스페인어는 56종 중
> 12종**이 그렇습니다. 그 자리들이 `fallback` 에 모여 있습니다 — 인용할 때 영어로 쓰세요.

**② 번역 원본을 직접 읽습니다**

```bash
python -c "
import json,io,sys; sys.stdout.reconfigure(encoding='utf-8')
d=json.load(io.open('C:/projects/phet/babel/build-an-atom/build-an-atom-strings_ja.json',encoding='utf-8'))
def w(o,p=''):
    if isinstance(o,dict):
        if 'value' in o and isinstance(o['value'],str): print(p,'=',o['value'])
        for k,v in o.items(): w(v,p+'.'+k)
w(d)"
```

**여기서 반드시 확인할 것 — `a11y.*` 아래에만 있는 이름은 화면에 절대 안 나옵니다.**
스크린리더 전용이고, 어느 언어로도 그려지지 않습니다. 아이콘만 있는 단추에 붙여 둔
접근성 이름이라서요. 한국어판이 이걸 화면 글자로 착각한 곳이 **9개 시뮬레이션 22곳**
있었습니다. 대표적으로:

| 시뮬레이션 | `a11y.*` 전용이라 화면에 없는 이름 |
|---|---|
| `vector-addition` | Angles · Grid · Scene · Cartesian · Polar · Hidden · Right triangle · From vector tail · Projected onto x y axes |
| `ratio-and-proportion` | No/Tick/Numbered Tick Marks |
| `balancing-chemical-equations` | Particles · Balance Scales · Bar Charts · Reaction Type |
| `energy-skate-park` | Parabola · Ramp · Double Well · Loop |
| `greenhouse-effect` | Experiment Mode · By concentration · By time period |
| `quantum-wave-interference` | Particle Type · Detection Mode |
| `number-pairs` / `photoelectric-effect` / `quantum-bound-states` | Representation Type · Representation · Circuit · Hide Curves |

이 자리들은 한국어판에서 이미 "글자 없이 **그림**으로 구별합니다" 식으로 고쳐 두었습니다.
번역할 때 그 서술을 그대로 옮기면 됩니다 — 언어와 무관하게 사실이니까요.

**③ 실제로 띄워 좌표까지 잽니다 (자리를 새로 쓸 때)**

```bash
python tools/serve.py 8123 dist      # 먼저 python tools/build.py
```
브라우저에서 `http://localhost:8123/sims/<repo>.html?locale=ja` 를 열고 콘솔에:

```js
window.D = function(si){
  const d=phet.joist.display, W=d.width, H=d.height, out=[], seen=new Set();
  const walk=n=>{ if(!n||n.visible===false) return;
    const s=(typeof n.string==='string')?n.string:null;
    if(s&&s.trim()){ const b=n.getGlobalBounds();
      if(b&&b.isFinite()){ const cx=Math.round(b.centerX), cy=Math.round(b.centerY);
        const k=s+'@'+cx+','+cy;
        if(!seen.has(k)){ seen.add(k);
          const hx=cx<W/3?'L':(cx>2*W/3?'R':'C'), hy=cy<H/3?'T':(cy>2*H/3?'B':'M');
          out.push(`${hy}${hx}(${cx},${cy}) ${s}`); } } }
    (n.children||[]).forEach(walk); };
  walk(phet.joist.sim.screens[si].view);
  return {size:[W,H], items:out};
};
JSON.stringify(window.D(1));   // 화면이 여럿이면 screens[0] 은 홈입니다
```

돌려주는 것은 **화면에 실제로 그려진 글자 + 정규화된 자리**입니다. 짐작으로 쓴 위치는
대부분 틀립니다 — 한국어판에서 15곳이 틀렸고, 그중 8곳이 레슨의 **첫 미션**이었습니다.

### 4-3. 위치 표현은 언어와 무관합니다

`왼쪽 위` · `오른쪽 아래` · `아래 가운데` 같은 서술은 그대로 옮기면 됩니다.
한국어판의 위치는 이번 검수에서 61종 전부 실측으로 맞춰 두었으니 **믿고 쓰세요.**

### 4-4. PhET 제목 오역 — 언어마다 다시 봐야 합니다

`site/content/sim-titles.json` 이 시뮬레이션 제목을 언어별로 덮어씁니다. 쓰임이 둘입니다.

- **`ko`** — PhET 한국어 번역이 잘못 잡은 제목 9종을 바로잡습니다 (`_why` 에 이유).
- **`es`** — 스페인어 제목 56종. 오역 교정이 아니라 **원래 없어서 채운 것**입니다.
  `sims.json` 에는 `title`(한국어)과 `titleEn` 밖에 없어, 그냥 두면 스페인어 페이지에
  영어 제목이 뜹니다. 영어로 열리는 5종은 넣지 않았습니다 — 화면이 영어니까요.
- **`ja`** — 일본어 제목 42종. 스페인어와 같은 이유입니다. 영어로 열리는 18종과
  제목만 영어로 떨어지는 `number-compare` 는 넣지 않았습니다.

`applySimTitles`(i18n.js)와 `sim_title()`(bake-head.py)이 이미 언어별로 읽으므로
**코드는 손댈 필요가 없습니다.**

```jsonc
{ "number-play": { "_why": "Number Play 를 '게임 횟수'로 옮겨 놓았습니다. …", "ko": "수 놀이" } }
```

같은 문제가 일본어·스페인어에도 있을 수 있습니다. 원인은 `sims.json` 생성기가 제목을
못 찾으면 **시뮬레이션 안의 아무 문자열이나 집어 오기** 때문입니다(9종 중 5종이 그렇습니다).
새 언어를 넣을 때 61종 제목을 한 번 훑고, 이상한 것은 이 파일에 그 언어 키를 더하세요.

```bash
python -c "
import json,io,sys; sys.stdout.reconfigure(encoding='utf-8')
for s in json.load(io.open('dist/sims.json',encoding='utf-8')): print(s['repo'],'|',s['title'])"
```

---

## 5. 언어를 하나 더 켤 때 손봐야 하는 곳

### 5-1. 콘텐츠 (이 작업의 본체)

```
site/content/<lang>/courses.json
site/content/<lang>/lessons.json
site/content/<lang>/guides.json
```

### 5-2. 코스 카드 색

`site/index.html` 의 `SUBJECT_COLOR` 에 그 언어의 과목명을 더합니다.
**네 언어가 다 들어 있습니다.** 언어를 더 늘릴 때 잊지 마세요.

```js
const SUBJECT_COLOR = {
  수학: 'var(--s-math)', 물리: 'var(--s-phys)', …
  Math: 'var(--s-math)', Physics: 'var(--s-phys)', …
  'Matemáticas': 'var(--s-math)', 'Física': 'var(--s-phys)', …
  // ← 일본어 과목명을 여기에
};
```

넣지 않으면 코스 카드가 전부 회색으로 떨어집니다. `courses.json` 의 `subject` 값과
**글자 하나까지 같아야** 합니다.

### 5-3. 공유 이미지 (OG) — 지금 76장이 전부 한국어입니다

`site/og/` 에 `default.png` + 코스 14장 + 레슨 61장이 있고, **파일 이름에 언어가 없습니다.**
그래서 `/ja/l/atom-1` 의 `og:image` 도 한국어 그림을 가리킵니다.

두 가지 길이 있습니다.

- **당분간 그대로 둔다** — 카카오톡 공유 카드에 한국어 그림이 뜹니다. 일본어 사용자에게는
  어색하지만 깨지지는 않습니다.
- **언어별로 굽는다** — `tools/make-og.py` 를 언어 인자를 받게 고치고
  `site/og/<lang>/…` 으로 내보낸 뒤, `tools/bake-head.py` 의 `img` 경로와
  `site/lib/seo.js` 의 `applySeo({ image })` 를 함께 고칩니다. 76 × 4 = 304장이 되고
  파일 수는 여유가 있습니다(632 / 20,000).

`make-og.py` 는 이미 Jua(제목)와 Pretendard(본문)로 그리고 있고, Jua 에 없는 글자는
Pretendard 로 떨어지게 되어 있습니다. 확인은 아래 한 줄로 끝납니다.

```bash
python tools/font-check.py
```

**확인 결과(2026-08-21):**

| 언어 | 결과 |
|---|---|
| en · es | Pretendard 가 다 덮습니다. 악센트 · `¿` · `¡` 전부 있음 — **그대로 가면 됩니다** |
| **ja** | **Pretendard 에 한자가 없습니다 (표본 757자 중 491자 없음)** — 지금 구우면 두부(□) |

그래서 일본어 공유 이미지를 굽기 전에 **CJK 서체를 하나 더 얹어야 합니다.**
저장소 서체 정책이 OFL 이므로 Noto Sans JP(OFL)가 맞습니다. `tools/fonts/` 에 넣고
`make-og.py` 의 `display_font()` 처럼 "없으면 다음 서체" 사슬에 이어 붙이면 됩니다.

> **썸네일은 손대지 마세요.** `thumbs/` 의 시뮬레이션 미리보기는 **모든 언어에서 영어인
> 채로 두기로** 정해져 있습니다(사용자 결정).

### 5-4. 자동으로 따라오는 것 (손댈 필요 없음)

- **경로** — `/ja/`, `/ja/all`, `/ja/c/<코스>`, `/ja/l/<레슨>` 이 이미 만들어지고 있습니다.
- **정적 `<head>`** — `tools/bake-head.py` 가 네 언어 × 77쪽 = 308장을 굽습니다.
  `content/<lang>/…` 을 채우면 그 언어 머리말이 자동으로 그 언어가 됩니다.
- **hreflang · canonical · sitemap** — 네 언어가 이미 서로 묶여 있습니다.
- **언어 선택기** — 지금 페이지의 같은 문서로 건너뜁니다(`samePageIn`).

---

## 6. 작업을 쪼개는 방법 (제안)

한 세션에 246,000자를 다룰 수 없으니 이렇게 나누기를 권합니다.

| 단계 | 내용 | 분량 | 왜 이 순서인가 |
|---|---|---:|---|
| **1** | `guides.json` 의 `_common` | 약 3,000자 | 61편 전부에 붙습니다. 가장 값이 큽니다 |
| **2** | `courses.json` (ja · es) | 약 6,300자 | 홈과 코스 페이지가 먼저 그 언어가 됩니다 |
| **3** | `lessons.json` — 코스 단위로 14회 | 편당 약 2,300자 | 한 코스가 다 되면 눈으로 확인할 수 있습니다 |
| **4** | `guides.json` — 시뮬레이션 단위로 | 종당 약 1,700자 | 레슨이 참조하므로 3과 짝지어 진행하면 좋습니다 |
| **5** | 제목 오역 점검 · OG 이미지 | — | 마무리 |

**언어 순서는 en → es → ja 를 권합니다.** 영어는 61종 전부 번역이 있어 §4 문제가 없고,
그 영어판이 나머지 두 언어의 참조가 됩니다. 일본어는 18종이 영어로 열려 가장 까다로우니
마지막입니다.

**중간 산출물은 `wip/<lang>/` 에 두세요.** §1-4 의 이유입니다.
한 언어의 파일이 완성되면 `site/content/<lang>/` 으로 옮기고 그때 커밋합니다.

---

## 7. 검사 · 빌드 · 배포

```bash
node   tools/lint.mjs                 # 태그 · 조판 — 반드시 오류 0 · 경고 0
node   tools/parity.mjs               # 한국어와 뼈대 대조 — 반드시 오류 0
python tools/labels.py                # 화면 글자 사전 (번역 시작 전 한 번)
python tools/font-check.py            # 공유 이미지 서체가 그 언어를 덮는지
python tools/build.py                 # site/ + PhET 산출물 → dist/ (+ head 굽기)
python tools/serve.py 8123 dist       # 확장자 없는 주소도 풀어 줍니다
python tools/make-og.py               # 공유 이미지
python tools/make-sitemap.py          # sitemap.xml + robots.txt
npx wrangler pages deploy dist --project-name nudge
```

린트가 보는 것:

| 검사 | 내용 |
|---|---|
| [1] | 네 언어 ui 파일의 키가 전부 일치하는가 |
| [2] | `{n}` 같은 자리표시자가 언어마다 같은가 |
| [3] | 코스 14개가 시뮬레이션 61종을 중복 없이 덮는가 |
| [4] | `ready: true` 인 레슨에 본문이 다 있는가 |
| [5] | 사용법이 61종 다 있는가 |
| [6] | 시뮬레이션 언어표가 61종을 다 담는가 |
| [7] | 태그 균형 · 조사 띄어쓰기 · 라벨 콜론 · 폭 없는 공백 (있는 언어 전부) |
| [8] | 코스 `minutes` 가 그 코스 레슨 `min` 의 합과 같은가 |

`lint.mjs` 는 태그와 조판만 봅니다. **번역본이 한국어와 같은 뼈대인지는 `parity.mjs` 가**
봅니다 — 빠진 레슨, `right` 인덱스 어긋남, 선택지 개수 불일치, 번역 금지 필드 변조,
한국어 그대로 남은 자리. `wip/` 의 미완성 파일도 진행률로 보고하며 같이 검사합니다.
§8 의 함정 2·3 을 사람 눈 대신 기계가 지키는 자리입니다.

빌드가 Cloudflare Pages 한계도 봅니다 — **20,000 파일 / 파일당 25 MiB.**
지금 632 파일 / 222.7 MB, 가장 큰 파일이 25 MB 아래입니다.

---

## 8. 함정 모음

1. **반쯤 번역된 `lessons.json` 을 두지 마세요.** 폴백이 파일 단위라 안내 문구가 사라진 채
   두 언어가 섞입니다. §1-4.
2. **`right` 인덱스는 0부터.** 선택지 순서를 바꾸면 함께 고치세요.
3. **`id` · `sim` · `course` · `screens` · `ready` · `mode` 는 번역 금지.** 코드가 씁니다.
4. **`minutes` 는 레슨 `min` 합과 같아야 합니다.**
5. **`title` 에 태그 금지.** `<title>` 과 OG 에 그대로 들어갑니다.
6. **`a11y.*` 이름을 화면 글자로 쓰지 마세요.** §4-2.
7. **일본어 18종 · 스페인어 5종은 영어로 열립니다.** 그 편들은 영어 라벨을 인용하세요.
8. **PhET 번역 자체가 틀린 곳이 있습니다.** 한국어에서 14건 찾았습니다
   (`트랜지스터`=Transitions, `푸우리에`=Fourier, `소숫점`=소수점, `감폭`=감쇠,
   `망`=Grid, `관례`=Custom, `읿부`=일부, `비울과 비`=비율과 비, `표면 아베도`=알베도 …).
   **화면에 그렇게 나오면 원고도 그렇게 써야 합니다** — 학습자가 찾을 글자니까요.
   대신 `gotchas` 에 "이건 ○○의 오타입니다" 한 줄을 답니다. 다른 언어에도 같은 종류의
   오역이 있을 테니 같은 방식으로 처리하세요.
9. **`<sup>` 깨짐** — `my-solar-system` · `keplers-laws` 의 줌 표시가 `×10<sup>-2</sup`
   처럼 닫는 태그가 깨져 보입니다. PhET 쪽 버그이고 우리가 고칠 수 없습니다.
10. **Windows 에서 파이썬 스크립트를 stdin(heredoc)으로 넘기면 한글이 깨집니다.**
    콘솔 코드페이지로 읽어서 그렇습니다. 한글이 든 스크립트는 **파일로 저장해서** 실행하세요.
11. **`dist/` 를 여는 서버가 떠 있으면 빌드가 실패합니다**(`PermissionError WinError 32`).
    빌드 전에 `Get-CimInstance Win32_Process` 로 `serve.py` 를 정리하세요.

---

## 9. 참고 문서

| 파일 | 내용 |
|---|---|
| `README.md` | 저장소 구조 · 빌드 · 배포 |
| `docs/REVIEW-BRIEF.md` | 한국어 원고 검수를 의뢰할 때 쓴 문서. 무엇을 어떻게 봐야 하는지 |
| `docs/REVIEW-RESULT.md` | 그 회신(64건). §3 의 `a11y` 이야기가 특히 중요합니다 |
| `docs/KO-FINDINGS.md` | 한국어 원고에서 아직 안 고친 것 28곳 + 오역 1건 |
| `docs/ES-FINDINGS.md` | 스페인어 작업에서 나온 것 — PhET 오타 7 · 미번역 · 영어와 다른 라벨 |
| `site/lib/i18n.js` | 언어 판정 · 폴백 · 경로 · 시뮬 언어 매칭 |
| `site/lib/seo.js` | 머리말. `tools/bake-head.py` 와 **같은 모양을 내야 합니다** |
| `tools/bake-head.py` | 정적 머리말 굽기 · 경로 규칙 |
| `tools/lint.mjs` | 검사 여덟 가지 — 태그 · 조판 |
| `tools/parity.mjs` | 한국어와 뼈대 대조 — `right` · 개수 · 번역 금지 필드 |
| `tools/labels.py` | 화면 글자 사전 뽑기 → `wip/labels/` |
| `tools/font-check.py` | 공유 이미지 서체 글자 덮개 확인 |
| `wip/README.md` | 작업 폴더 규칙과 사전 보는 법 |

---

## 10. 이 세션에 바라는 것

1. 위 §6 의 어느 단계를 할지 먼저 정하고 알려 주세요.
2. 번역 전에 **그 시뮬레이션이 그 언어로 열리는지** 확인하고, 열린다면 라벨을 §4-2 의
   방법으로 뽑아 두세요. 짐작으로 쓰지 마세요.
3. 끝나면 `node tools/lint.mjs` 와 `node tools/parity.mjs` 가 **오류 0** 이어야 합니다.
4. 미완성 파일은 `wip/<lang>/` 에 두고, 완성분만 `site/content/<lang>/` 으로 옮기세요.
5. PhET 번역 자체가 이상한 곳을 발견하면 §8-8 방식으로 처리하고, 목록을 따로 남겨 주세요.
