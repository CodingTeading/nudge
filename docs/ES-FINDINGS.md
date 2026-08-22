# 스페인어 작업에서 나온 것들

스페인어 레슨 61편·사용법 61종을 쓰면서 PhET 스페인어 번역에서 발견한
오타·미번역과, 그것을 원고에서 어떻게 처리했는지 적어 둡니다.

- 작성일: 2026-08-22
- 기준: `wip/labels/es/` (PhET 포크 `C:/projects/phet` 의 babel 스페인어 문자열)
- 원칙: **화면에 그렇게 찍히면 원고도 그렇게 씁니다.** 학습자가 눈으로 찾을 글자라서요.
  대신 `gotchas` 에 "이건 ○○의 오타입니다" 한 줄을 답니다 (의뢰서 §8-8).

---

## 1. PhET 스페인어 번역의 오타 — 6곳

전부 **화면 그대로 인용**하고 해당 사용법의 `gotchas` 에 한 줄씩 적었습니다.

| 시뮬레이션 | 화면에 찍히는 글자 | 맞는 표기 | 무엇이 문제인가 |
|---|---|---|---|
| `faradays-electromagnetic-lab` | **Área se la espira** | Área **de** la espira | `de` 가 `se` 로 |
| `coulombs-law` | **Notación cientifica** | Notación cient**í**fica | í 빠짐 |
| `blackbody-spectrum` | **valores del gràfico** | valores del gr**á**fico | 악센트 방향 반대 |
| `graphing-quadratics` | **Vertice** | V**é**rtice | é 빠짐 |
| `graphing-quadratics` | **Eje de Simetria** | Eje de Simetr**í**a | í 빠짐 |
| `center-and-variability` | **Ordentar Datos** | Orde**n**ar Datos | t 가 하나 더 |
| `projectile-motion` | **Bala de cañon** | Bala de cañ**ó**n | ó 빠짐 |

`unit-rates` 의 Racing Lab 에는 `miles` 가 **`kilometros`** (kilómetros) 로 들어 있습니다.
단위 자체가 마일에서 킬로미터로 바뀐 데다 악센트도 빠졌는데, 이 레슨은 Racing Lab 을
가볍게만 언급하므로 인용하지 않았습니다.

---

## 2. 번역이 빠져 영어로 찍히는 자리

### 2-1. 시뮬레이션 통째로 영어 — 5종

```
alpha-decay · beta-decay · photoelectric-effect
quantum-bound-states · quantum-wave-interference
```

이 다섯은 `sim-locales.json` 에 `es` 가 없어 **`?locale=en` 으로 열립니다.**
한국어판과 같은 방식으로 처리했습니다.

- 사용법 `summary` 첫 문장에 "이 시뮬레이션은 영어로만 나옵니다" 를 적고
- 조작 이름은 **영어 그대로** 쓰고 괄호에 뜻을 답니다 — `Intensity` (intensidad)
- `gotchas` 첫 줄에 `La pantalla solo sale en inglés.`

### 2-2. 문자열 단위로 빠진 곳 — 12종

번역이 "있는" 시뮬레이션도 일부 문자열은 영어로 그려집니다. 실측 결과는 아래와 같고,
**이 레슨들이 인용하는 자리는 하나도 걸리지 않았습니다** — 딱 하나만 빼고.

| 시뮬레이션 | 영어로 남은 곳 | 이 원고에 영향 |
|---|---:|---|
| `greenhouse-effect` | 30 | 없음 — 전부 Micro 화면(`ControlPanel` · `SpectrumWindow`). 이 레슨은 Ondas · Fotones 만 씁니다 |
| `energy-skate-park` | 27 | 없음 — 전부 `keyboardHelpDialog` · `preferences` |
| `number-pairs` | 15 | **화면 이름 `Game` 하나** — 사용법 화면 목록에 "이름이 안 옮겨졌다" 고 적어 두었습니다 |
| `ph-scale` | 13 | 없음 — `keyboardHelpDialog` 과 `autoFill` |
| `calculus-grapher` | 6 | 없음 — `keyboardHelp` |
| `build-a-nucleus` | 5 | 없음 — 값 패턴(`{{name}} - {{mass}}` 따위) |
| `projectile-motion` | 4 | 없음 — Stats 화면. 이 레슨은 Introducción · Vectores 만 씁니다 |
| `graphing-quadratics` | 3 | 없음 — `keyboardHelpDialog` |
| `wave-on-a-string` | 2 | 없음 — `keyboardHelpDialog` |
| `charges-and-fields` | 1 | **`Snap to Grid`** — 사용법과 gotchas 에 "이 칸은 번역이 없어 영어로 나옵니다" 를 적었습니다 |
| `quantum-coin-toss` | 1 | 없음 — 화면이 하나뿐이라 화면 이름이 안 보입니다 |
| `quantum-measurement` | 1 | 없음 — `Average Polarization Representation` (이 레슨이 안 씁니다) |

---

## 3. 영어와 이름이 크게 다른 라벨

같은 조작인데 스페인어 이름이 영어와 **말이 달라** 그대로 옮기면 화면에서 못 찾는 자리들입니다.
전부 스페인어 화면 글자로 고쳐 썼습니다.

| 시뮬레이션 | 영어 | 스페인어 |
|---|---|---|
| `projectile-motion` | Cannon Angle | **Ángulo** (그냥 «각도») |
| `projectile-motion` | Range | **Distancia horizontal** |
| `build-an-atom` | Element Name | **Elemento** |
| `build-an-atom` | Neutral Atom or Ion | **Neutro/Ion** |
| `build-an-atom` | Nuclear Stability | **Estable/Inestable** |
| `build-an-atom` | Shells | **Órbitas** |
| `hookes-law` | Spring Force | **Fuerza restauradora** |
| `models-of-the-hydrogen-atom` | Spectrometer (…) | **Espectro** (…) |
| `mean-share-and-balance` | Number of Cups | **Número de Contenedores** |
| `rutherford-scattering` | Protons | **Número de protones** |
| `states-of-matter` | States (화면 이름) | **Estado** (단수) |

`wave-on-a-string` 은 `amplitud` · `tensión` · `amortiguación` · `frecuencia` 가
**소문자**로 찍힙니다. 화면 그대로 소문자로 인용했습니다.

---

## 4. 한국어판에서 문제였는데 스페인어에서는 괜찮은 것

- `mean-share-and-balance` 의 **Distribute** 는 스페인어로 **`Distribuir`** 로 제대로
  옮겨져 있습니다. 한국어판은 이것을 통계 용어 «분산» 으로 옮겨 화면 설명이 어긋났습니다
  (`docs/KO-FINDINGS.md` §1-2). 스페인어 원고는 그 문제가 없습니다.
- 제목 오역도 없습니다. 한국어는 `sims.json` 생성기가 제목을 못 찾아 엉뚱한 문자열을
  집어 온 것이 9종 있었지만, 스페인어는 **56종 전부 제대로 된 제목**이 있었습니다
  (§5 참고).

---

## 5. `a11y.*` 전용 이름 — 스페인어도 똑같습니다

의뢰서 §4-2 의 목록(9종 22곳)은 **언어와 무관합니다.** 스크린리더 전용 문자열이라
스페인어로도 화면에 그려지지 않습니다. 한국어판이 그림 설명으로 고쳐 둔 서술을
그대로 옮겼습니다.

- `vector-addition` — Componentes 의 네 단추, 좌표 단추 두 개, 눈금 단추: 전부 **그림**
- `ratio-and-proportion` — 눈금 단추 세 개: **그림** (눈 가림 · 가로줄 · 숫자 붙은 줄)
- `balancing-chemical-equations` — Vista 의 세 단추: **그림** (입자 · 저울 · 막대)
- `greenhouse-effect` — 농도 방식 단추 두 개: **그림** (수량 · 달력)
- `energy-skate-park` — 트랙 단추 네 개: **그림** (포물선 · 경사 · 두 골짜기 · 고리)
- `number-pairs` — 왼쪽 단추들(교환 · 가리기 · 정리): **그림**

---

## 6. 결정한 것

### 6-1. 스페인어 실험 제목을 `sim-titles.json` 에 넣었습니다

`sims.json` 의 `title` 은 한국어이고 `titleEn` 만 있습니다. 그대로 두면 스페인어
페이지에 «Build an Atom» 이 뜨는데, 학습자가 실험을 열면 화면에는
«Construye un Átomo» 라고 찍힙니다 — 이 프로젝트의 원칙과 어긋납니다.

그래서 `site/content/sim-titles.json` 에 **`es` 키 56개**를 넣었습니다.
값은 PhET 스페인어 번역의 `<repo>.title` 을 앞뒤 공백(nbsp 포함)만 떼어 그대로
가져온 것입니다. **영어로 열리는 5종은 넣지 않았습니다** — 화면이 영어이므로
영어 제목이 맞습니다.

`site/lib/i18n.js` 의 `applySimTitles` 와 `tools/bake-head.py` 의 `sim_title()` 은
이미 이 파일을 언어별로 읽으므로 **코드는 손대지 않았습니다.**

### 6-2. 공유 이미지(OG)는 여전히 한국어입니다

`site/og/` 의 76장은 언어 구분이 없어 스페인어 페이지의 `og:image` 도 한국어 그림을
가리킵니다. `python tools/font-check.py` 결과 **Pretendard 가 스페인어를 다 덮으므로**
(악센트 · `¿` · `¡` 전부 있음) 굽는 것 자체는 언제든 가능합니다. 의뢰서 §5-3 의
두 갈래 중 "당분간 그대로 둔다" 를 유지했습니다.
