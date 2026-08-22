# 일본어 작업에서 나온 것들

일본어 레슨 61편·사용법 61종을 쓰면서 PhET 일본어 번역에서 발견한
오역·미번역과, 그것을 원고에서 어떻게 처리했는지 적어 둡니다.

- 작성일: 2026-08-23
- 기준: `wip/labels/ja/` (PhET 포크 `C:/projects/phet` 의 babel 일본어 문자열)
- 원칙: **화면에 그렇게 찍히면 원고도 그렇게 씁니다.** 학습자가 눈으로 찾을 글자라서요.
  대신 `gotchas` 에 "이건 ○○의 오역입니다" 한 줄을 답니다 (의뢰서 §8-8).

---

## 0. 한눈에

| | 종 수 |
|---|---:|
| 완전한 일본어 | 10 |
| 일본어로 열리지만 **일부가 영어** | 33 |
| **통째로 영어**로 열림 | 18 |
| 계 | 61 |

일본어는 세 언어 중 미번역이 가장 많습니다. 한국어는 55/61, 스페인어는 56/61 이
번역을 가지고 있는데 일본어는 43/61 이고, 그 43종 중에서도 완전한 것은 10종뿐입니다.
**사용법 61종 가운데 절반 이상에 "이 자리는 영어로 나옵니다" 한 줄이 들어간** 이유입니다.

---

## 1. PhET 일본어 번역의 오역 — 9곳

전부 **화면 그대로 인용**하고 해당 사용법의 `gotchas` 에 한 줄씩 적었습니다.

| 시뮬레이션 | 화면에 찍히는 글자 | 원문 | 무엇이 문제인가 |
|---|---|---|---|
| `rutherford-scattering` | **電気エネルギーレベル** | Electron Energy Level | 電**子**를 電**気**로 — 전자와 전기를 혼동 |
| `build-a-nucleus` | **地球の年齢** | Age of the Universe | 우주의 나이를 지구의 나이로 |
| `gas-properties` | **仕事率** | Sample Period | 충돌 계수기의 표본 시간인데 '일률'로 |
| `gas-properties` | **規模を表示** | Scale | 확산 화면의 자(ものさし)인데 '규모'로 |
| `beers-law-lab` | **硫化銅** | Copper Sulfate | 황산구리(硫酸銅)를 황화구리로 — 다른 물질 |
| `reactants-products-and-leftovers` | **反応** | Reactants | 반응물(反応物)이 아니라 그냥 '반응' |
| `reactants-products-and-leftovers` | **生産** | Products | 생성물(生成物)이 아니라 '생산' |
| `graphing-quadratics` | **対象軸** | Axis of Symmetry | 対**称**軸의 동음 오타 |
| `graphing-quadratics` | **中心** | Focus | 포물선의 초점(焦点)인데 '중심'으로 |

`graphing-quadratics` 의 `二次方程式`(Quadratic Terms, 2차항)과
`fractions-mixed-numbers` 의 `方程式`(Equation) 도 말이 헐겁습니다. 뜻이 통하지 않는
정도는 아니라 표에는 넣지 않고 각 사용법 `gotchas` 에만 한 줄씩 달았습니다.

### 제목이 원제와 어긋나는 것 — 3종

`site/content/sim-titles.json` 에는 **화면에 찍히는 대로** 넣었습니다. 사이트 이름과
실험 안 제목이 어긋나면 그게 더 큰 사고라서요. 뜻은 사용법에 적었습니다.

| 시뮬레이션 | 일본어 제목 | 원제 |
|---|---|---|
| `function-builder` | マジックスコープ | Function Builder |
| `build-a-fraction` | 分数の計算 | Build a Fraction |
| `fraction-matcher` | 分数を作ろう | Fraction Matcher |

뒤의 두 종이 특히 헷갈립니다 — 같은 코스(10 분수) 안에서 **서로의 뜻을 가리키는**
제목이 붙어 있습니다. Build a Fraction 이 '분수의 계산', Fraction Matcher 가
'분수를 만들자'입니다.

> 한국어판의 제목 문제와 원인이 다릅니다. 한국어 9종은 `sims.json` 생성기가 제목을
> 못 찾아 **엉뚱한 문자열을 집어 온 것**이고, 일본어 3종은 **번역 자체가 그렇게 되어
> 있는 것**입니다. 그래서 한국어는 덮어썼고 일본어는 그대로 씁니다.

---

## 2. 통째로 영어로 열리는 18종

`site/content/sim-locales.json` 에 `ja` 가 없는 것들입니다. 이 편들은 **미션과 사용법이
영어 이름을 그대로 인용**하고 괄호에 뜻을 답니다 — `<b>Predict Mean</b>（平均を予想する）`
같은 식입니다. 레슨 훅에도 `<b>この実験は英語で開きます。</b>` 를 넣었습니다.

| 코스 | 시뮬레이션 |
|---|---|
| 01 | `faradays-electromagnetic-lab` |
| 02 | `projectile-data-lab` |
| 03 | `fourier-making-waves` |
| 04 | `photoelectric-effect` · `quantum-wave-interference` |
| 05 | `models-of-the-hydrogen-atom` · `alpha-decay` · `beta-decay` |
| 06 | `quantum-coin-toss` · `quantum-measurement` · `quantum-bound-states` (3종 전부) |
| 07 | `my-solar-system` · `keplers-laws` |
| 11 | `mean-share-and-balance` |
| 12 | `calculus-grapher` |
| 13 | `membrane-transport` |
| 14 | `number-pairs` · `quadrilateral` |

코스 06 은 **세 종이 다 영어**입니다. 코스 08·09·10 은 반대로 **한 종도 없습니다.**

---

## 3. 일부만 영어인 33종 — 눈에 띄는 자리

일본어로 열리지만 문자열 단위로 번역이 빠진 곳입니다. **화면 이름이 영어로 남는 경우가
특히 많아** 사용법의 `screens` 를 `Waves（波）` 처럼 적었습니다.

| 시뮬레이션 | 영어로 남는 자리 |
|---|---|
| `greenhouse-effect` | 화면 이름 4개 전부 · Sunlight · Infrared · Surface Albedo · Solar Intensity · Absorbing Layers |
| `center-and-variability` | 화면 이름 Variability · Range · IQR · MAD · Interval Tool · Outliers |
| `balancing-chemical-equations` | 화면 이름 3개 전부 · View · Reactants · Products · Synthesis · Decomposition · Combustion · Simplified |
| `build-a-nucleus` | 화면 이름 2개 · Full Chart · Partial Nuclide Chart · Magic Numbers · 축 이름 2개 |
| `molecule-polarity` | 화면 이름 3개 전부 · more ionic · more covalent · Dipole direction |
| `number-pairs` 계열 밖 `number-compare` | 실험 제목만 (`Number Compare`) |
| `gas-properties` | 단위 기호(atm · kPa) · Wall Velocity |
| `acid-base-solutions` | 표시 선택지 `Particles` |
| `gravity-and-orbits` | 줄자 단위 `kilometers` · 속도 화살표 `V` |
| `beers-law-lab` | 단위 전환 안내 2줄 |
| `number-line-distance` | `Terminology` · `Displacement` |
| `equality-explorer` · `number-play` | 게임 수준 설명 |

### 공용 저장소 쪽

`joist` · `scenery-phet` · `vegas` 에도 미번역이 많습니다. 61종 전부에 영향을 줍니다.

- **`Fast`** — 속도 조절 단추 셋 중 빠르기만 영어입니다 (`スロー再生 · 再生 · Fast`).
  공통 사용법 `_common` 에 적어 두었습니다.
- **`Reset All`** · **`Toggle Sound`** — 아이콘 단추라 화면에 글자로는 안 보입니다.
- **`Short circuit!`** — `acid-base-solutions` 의 전기 회로에 영어로 뜹니다.
- **`New Game`** · **`Levels`** · **`Choose Your Level!`** — 게임 화면 일부.
  나머지(`答え合わせ` · `もう一回やる` · `答えを見る` · `点数`)는 일본어입니다.

---

## 4. `a11y.*` 전용이라 화면에 없는 이름

의뢰서 §4-2 의 표에 있는 것들은 일본어에서도 **똑같이 화면에 안 나옵니다.**
언어와 무관한 문제라 한국어판의 "글자 없이 그림으로 구별합니다" 서술을 그대로 옮겼습니다.

이번 작업에서 **새로 찾은 것 세 곳**은 한국어판이 아직 글자로 인용하고 있습니다.
일본어판만 그림으로 서술해 두었고, **한국어는 손대지 않았습니다.**

| 시뮬레이션 | 한국어 원고가 인용한 글자 | 실제 |
|---|---|---|
| `quantum-coin-toss` | `Heads` · `Tails` | `a11y.coinsScreen.coinStates.*` 아래에만 있음 — 동전은 **그림**으로 구별 |
| `unit-rates` | `Erase` | 문자열 자체가 없음 — **지우개 아이콘** 단추 |
| `membrane-transport` | `Erase All Solutes` | `a11y.eraseSolutesButton.*` 아래에만 있음 — **지우개 아이콘** 단추 |

세 곳 다 `docs/KO-FINDINGS.md` 에 옮겨 적어 두면 좋겠습니다.

---

## 5. 원고 자체의 오류 — 고쳤습니다

일본어를 쓰다 발견한 것이라 여기 적습니다. 번역 문제가 아니라 **한국어 원고가 실제로
없는 화면을 설명하고 있었던** 것이라, 세 언어(ko · en · es)에서 함께 뺐습니다.

| 시뮬레이션 | 원고가 적어 둔 화면 | 실제 화면 |
|---|---|---|
| `number-play` | 10 · 20 · 게임 · **실험** | Ten · Twenty · Game (셋) |
| `number-compare` | 비교하기 · **실험** | Compare (하나) |

61종 전수로 화면 수를 대조했고, 나머지는 맞습니다. 반대 방향(있는 화면을 원고가
빼먹은 것)이 3종 있는데 레슨 범위 밖이라 그대로 두었습니다 —
`projectile-motion`(Stats) · `greenhouse-effect`(Micro) · `quantum-bound-states`(Superposition).

---

## 6. 일본어 조판에서 정한 것

- **조사는 앞말에 붙입니다.** 한국어와 같습니다 — `<b>元素</b>にチェック`.
  린트의 조사 검사 정규식은 한국어만 잡으므로 일본어에는 걸리지 않습니다.
- **레이블의 콜론은 떼고 인용합니다.** `モデル：` → `<b>モデル</b>`,
  `初期濃度:` → `<b>初期濃度</b>`, `Target Orbit:` → `<b>Target Orbit</b>`.
- **`<sup>` 같은 태그는 원고에 넣지 않습니다.** `×10⁻²` 처럼 유니코드 위첨자를 씁니다.
  한국어판과 같은 규칙이고, `my-solar-system` 의 깨진 `<sup>` 를 그대로 옮기면
  페이지의 HTML 이 망가집니다.
- **우성·열성은 `顕性` · `潜性`** 으로 씁니다. `natural-selection` 이 현행 용어를
  쓰고 있어 그대로 따랐습니다.
- **영어로 열리는 실험의 이름 인용**은 `<b>Predict Mean</b>（平均を予想する）` 꼴로
  통일했습니다. 괄호는 전각입니다.

---

## 7. 공유 이미지(OG) — 서체 이야기

Jua 에도 Pretendard 에도 **한자가 없습니다.** 그대로 구우면 일본어 카드가 통째로
두부(□)가 됩니다. 그래서 **Noto Sans JP**(SIL OFL, `notofonts/noto-cjk` 의 일본어
부분집합 OTF)를 `tools/fonts/` 에 넣고 사슬에 이었습니다.

| 언어 | 제목 | 본문 |
|---|---|---|
| ko · en · es | Jua → Pretendard-Bold | Pretendard-Regular |
| ja | Noto Sans JP Bold → Pretendard-Bold | Noto Sans JP Regular → Pretendard-Regular |

**Noto Sans JP 에는 `₂`(U+2082)가 없습니다.** 일본어 원고에서 `CO₂` · `H₂O` 가
나오는 카드가 둘 있어(`l-matter-3` · `l-mix-3`), 그 한 글자 때문에 줄 전체가
Pretendard 로 떨어지면 나머지 한자가 다 두부가 됩니다. 그래서 `make-og.py` 에
**글자 단위 대체**를 넣었습니다 — 줄을 통째로 덮는 서체가 없으면 글자마다 서체를
갈아 가며 그립니다.

`python tools/font-check.py` 가 이 사슬을 그대로 가져다, 실제로 카드에 그려질 글자를
표본으로 잡아 검사합니다. 못 덮는 글자가 있으면 종료 코드 1 입니다.

> **썸네일** — 모든 언어에서 영어로 두기로 되어 있습니다 (사용자 결정). 그대로입니다.
