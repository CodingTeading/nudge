# Nudge 콘텐츠 검증 결과

`docs/REVIEW-BRIEF.md` 의뢰에 대한 회신입니다. 검증 대상은 `site/content/ko/` 의 한국어 원고이며,
PhET 시뮬레이션 자체는 대상이 아닙니다.

- 검증일: 2026-08-21
- 대상: 코스 14 · 레슨 61 · 미션 600 · 퀴즈 179 · ② 61 · 사용법 61

---

## 0. 한 줄 요약

**정답 인덱스 240문항은 오류 0건입니다.** 수치·연도·상수도 한 건도 틀리지 않았습니다.
반면 **미션과 사용법의 조작 위치·이름에서 37건**이 나왔고, 그중 **8건은 레슨의 첫 미션**입니다.
의뢰서 4-B에서 우려하신 바로 그 유형입니다.

가장 큰 발견은 개별 오타가 아니라 **한 가지 반복 패턴**입니다 — PhET의 **화면에 그려지지 않는
접근성 전용 이름(`a11y.*`, 스크린리더 전용)** 을 화면에 보이는 글자로 오인해 옮겨 적은 곳이
9개 시뮬레이션에 걸쳐 22건 있습니다. 자세한 것은 §3에 있습니다.

**가장 급한 것 다섯 개**만 먼저 꼽으면 다음과 같습니다.

| 위치 | 무엇이 |
|---|---|
| `life-3` 미션 ① | 에너지 균형 체크박스가 **왼쪽 위가 아니라 오른쪽 아래** |
| `space-3` 미션 ① | 이심률 손잡이가 **왼쪽 위가 아니라 오른쪽 위** |
| `throw-2` 미션 ① | 가변성 화면에서는 발사각·발사속도를 **정할 수 없음** (표시용 체크박스) |
| `atom-3` 미션 ⑧ | 트랜지스터는 **접이 상자가 아니라 팝업을 여는 단추**, 자리도 아래 왼편 |
| `throw-3` 미션 ② | 에너지 막대가 **접힌 채**라 펼치라는 안내가 빠짐 |

---

## 1. 검증 방법

의뢰서 4-B의 "짐작으로 쓴 위치는 대부분 틀립니다"에 맞춰, **문자열만 보고 판단하지 않았습니다.**

| 방법 | 내용 |
|---|---|
| ① 원본 저장소 대조 | `C:/projects/phet` 의 시뮬레이션 소스와 `babel/*_ko.json` 번역 원본을 직접 읽어 **어떤 문자열이 화면에 그려지고 어떤 것이 스크린리더 전용인지** 구분 |
| ② 실제 구동 계측 | 61종을 `localhost:8124` 에서 실제로 띄우고, scenery 장면 그래프를 훑어 **모든 화면 글자의 실좌표(1276×716 기준)** 를 수집해 원고의 위치 표현과 대조 |
| ③ 배치 코드 확인 | 위치가 애매한 것은 소스의 레이아웃 코드(`leftTop`, `xAlign` 등)로 최종 확정 |
| ④ 기계 검사 | 정답 인덱스 240문항, ②↔⑦ 중복도, 코스 메타데이터 합계, 용어 일관성 |

이 방법 덕분에 아래 보고는 대부분 `confidence: certain` 입니다. 화면을 못 열어 본 항목은 없습니다.

---

## 2. 심각도별 건수

총 **64건**입니다.

| 심각도 | 건수 | 주된 내용 |
|---|---:|---|
| high | 14 | 미션의 조작 위치·이름이 실제와 달라 그 자리에서 막히는 것 |
| medium | 32 | 부정확한 안내, 사실 오류, 상호 참조 오류, ②↔⑦ 중복 |
| low | 18 | 표현·근사·미세한 위치·새 오역 |

| 유형(`kind`) | 건수 |
|---|---:|
| `mission` | 40 |
| `quiz` | 8 |
| `fact` | 6 |
| `wording` | 6 |
| `difficulty` | 3 |
| `crossref` | 1 |

**`mission` 40건은 원인이 셋뿐입니다.**

| 원인 | 건수 | 레슨 미션 / 사용법 |
|---|---:|---|
| 화면에 없는 이름을 가리킴 (§3) | 22 | 11 / 11 |
| 조작의 위치가 실제와 다름 | 15 | 6 / 9 |
| 조작의 종류를 잘못 앎 (접이 상자↔단추, 설정↔표시, 접힘) | 3 | 1 / 2 |

같은 원인끼리 묶여 있어 **한 번에 고칠 수 있습니다.** 22건은 §3의 한 가지 원칙만 적용하면 되고,
15건은 좌우·상하 표현만 바꾸면 됩니다.

**항목별 전수 확인 결과는 §12에 있습니다.**

---

## 3. 가장 중요한 발견 — 화면에 없는 이름을 가리키고 있습니다

PhET 시뮬레이션에는 두 종류의 문자열이 있습니다.

- **화면에 그려지는 문자열** — `*-strings_en.json` 의 일반 키. 번역되면 한국어로 나옵니다.
- **스크린리더 전용 이름** — `a11y.*` 키. **눈에는 절대 보이지 않습니다.** 아이콘만 있는 단추에
  시각장애인용으로 붙여 둔 이름입니다.

원고 여러 곳이 두 번째를 첫 번째로 오인했습니다. 결과적으로 학습자는 **화면에 없는 글자를 찾게 됩니다.**

### 대표 사례 — `vector-addition` (throw-4)

사용법 요약은 "**한국어가 거의 적용되지 않아** 대부분의 단추가 영어로 나옵니다"라고 적혀 있습니다.
실제로 2D 탐색 화면에 그려지는 글자는 **전부 한국어**입니다:

```
합계 · 값 · 성분 · θ · a · b · c · 벡터가 선택되지 않음 · (축 눈금 숫자)
```

`Angles` · `Grid` · `Scene` · `Cartesian` · `Polar` · `Hidden` · `Right triangle` ·
`From vector tail` · `Projected onto x y axes` — 이 아홉 개는 **어느 언어로도 화면에 나오지 않습니다.**
소스에서 확인한 바로는 해당 컨트롤이 전부 아이콘입니다.

```
ComponentsRadioButtonGroup.ts  → createComponentStyleRadioButtonIcon() 4개 (글자 없음)
AnglesCheckbox.ts              → createAngleIcon()  (θ 아이콘)
VectorAdditionGridCheckbox.ts  → GridCheckbox (격자 아이콘)
CartesianPolarSceneRadioButtonGroup.ts → 아이콘 2개
```

그래서 미션 ⑨ "오른쪽 **성분**에서 **Projected onto x y axes**를 고르세요"는 따라 할 수 없습니다.
`성분`까지는 맞지만 그다음이 화면에 없습니다. **"성분의 아이콘 네 개 중 네 번째(가로·세로 축에
점선으로 내려 그은 그림)를 고르세요"** 같은 표현이어야 합니다.

### 같은 패턴이 나온 곳

| 시뮬레이션 | 화면에 없는 이름 | 실제 모습 | 원고 위치 |
|---|---|---|---|
| `vector-addition` | Angles · Grid · Scene · Cartesian · Polar · Hidden · Right triangle · From vector tail · Projected onto x y axes | 전부 아이콘 | throw-4 미션 ⑨⑩⑪, 사용법 요약·조작·헷갈리기 |
| `ratio-and-proportion` | No Tick Marks · Tick Marks · **Numbered Tick Marks** | 아이콘 단추 3개 | ratio-1 미션 ⑤, 사용법 조작[3]·헷갈리기[1] |
| `balancing-chemical-equations` | Particles · Balance Scales · Bar Charts · Equation · Reaction Type | 콤보박스 항목이 그림. `없음`만 글자 | mix-3 미션 ③⑧⑨, 사용법 조작[1][2][5] |
| `energy-skate-park` | Parabola · Ramp · Double Well · Loop | 트랙 모양 아이콘 | 사용법 조작[3]·헷갈리기[1] |
| `greenhouse-effect` | Experiment Mode · By concentration · By time period | 아이콘 단추 2개 | life-3 미션 ⑪, 사용법 조작[5]·헷갈리기[5] |
| `quantum-wave-interference` | Particle Type · Detection Mode | 묶음 제목이 없음(항목은 보임) | light-4 미션 ②⑦⑪ |
| `number-pairs` / `photoelectric-effect` / `quantum-bound-states` | Representation Type / Representation · Circuit / Hide Curves | 아이콘 | 각 사용법 조작 |

> **참고 — `calculus-grapher` 는 이 문제를 정확히 처리했습니다.**
> 헷갈리기[5] "모양 단추는 글자가 없습니다. 그림으로 구별해야 합니다."
> 위 일곱 곳도 이 방식으로 고치면 됩니다.

---

## 4. 미션이 실제로 작동하지 않는 곳 (의뢰서 4-B)

아래는 **소스 레이아웃 코드로 확정**한 것입니다.

### 4-1. `life-3` 미션 ① — 첫 지시부터 다른 곳을 가리킵니다

> 왼쪽 위 **에너지 균형**에 체크하세요.

`GreenhouseEffectObservationWindow.ts` 에서 두 요소가 서로 다른 자리에 놓입니다.

```ts
// 체크박스가 든 패널
this.controlsLayer.addChild( new AlignBox( this.instrumentVisibilityPanel, {
  alignBounds: this.windowFrame.bounds,
  xAlign: 'right', yAlign: 'bottom'      // ← 관찰창 오른쪽 아래
} ) );

// 체크했을 때 나타나는 막대 그래프
this.energyBalancePanel.leftTop = this.windowFrame.leftTop.plusXY( ... );  // ← 왼쪽 위
```

**체크박스는 오른쪽 아래**(실측 891, 543)이고, **왼쪽 위는 체크한 뒤 결과 막대가 뜨는 자리**입니다.
원고가 이 둘을 뒤바꿔 놓았습니다. 사용법 요약과 조작[0]에도 같은 오류가 있습니다.

### 4-2. `space-3` 미션 ① — 좌우가 반대입니다

> **왼쪽 위** 이심률 손잡이가…

이심률 손잡이는 **오른쪽 위**(실측 1108, 217)입니다. 케플러 법칙 실험의 조절판은 오른쪽에 있습니다.

### 4-3. `atom-2` 미션 ③ — 좌우가 반대입니다

> **왼쪽** 알파입자 성질에서 에너지를…

`RSBaseScreenView.ts` 의 `createControlPanelVBox()` 가 패널 묶음을 **놀이 영역 오른쪽**에 붙입니다.

```ts
return new RSControlPanelVBox( panels, {
  top: this.spaceNode.top,
  left: this.spaceNode.right + RSConstants.PANEL_SPACE_MARGIN   // ← 오른쪽
} );
```

같은 묶음에 든 `범례`·`원자` 는 사용법에 **오른쪽**이라고 옳게 적혀 있어, `알파입자 성질` 만 어긋납니다.

### 4-4. `atom-3` 미션 ⑧ — 위치도 조작 방식도 다릅니다

> **오른쪽 트랜지스터 상자를 펼치세요.**

`트랜지스터`는 **접이 상자가 아니라 누르는 단추**이고, 누르면 **별도 팝업 창**이 뜹니다.
자리도 오른쪽이 아니라 **빛 상자 바로 아래(화면 아래 왼편)** 입니다.

```ts
// MOTHAScreenView.ts
const bottomHBox = new HBox( {
  children: [ new VBox( { children: [ lightControlPanel, transitionsButton ] } ), spectrometerAccordionBox ],
  left: this.layoutBounds.left + MOTHAScreenView.X_MARGIN,     // ← 왼쪽 끝
  top: this.zoomedInBoxNode.bottom + 15                        // ← 관찰창 아래
} );
// TransitionsButton.ts → RectangularPushButton, listener: () => transitionsDialog.show()
```

### 4-5. `throw-2` 미션 ① — 없는 조작을 가리킵니다

> 가변성 화면에서 시작합니다. **왼쪽 아래 발사각과 발사속도를 정할 수 있습니다.**

두 가지가 틀렸습니다.

1. **자리** — 가변성 화면의 조절판(`방향` · `투사체` · `미스터리 발사기`)은 **왼쪽 위**입니다.
2. **기능** — `발사각` · `발사속도` 는 **오른쪽 도구 패널의 체크박스**로, 값을 **보여 주는** 도구입니다.
   설정하는 것이 아닙니다. 가변성 화면의 발사기는 설정이 감춰진 *미스터리 발사기*라 각도·속도를
   **정할 수 없습니다.**

```ts
// StaticToolPanel.ts
createNode: () => new PDLCheckboxRow( ProjectileDataLabStrings.launchAngleStringProperty, new AngleToolIconNode() ),
tandemName: 'launchAngleCheckbox'
```

사용법 조작[1] "발사각 · 발사속도 (왼쪽 아래) :: **발사 조건입니다. 앞 실험과 같습니다.**" 도 같은 오류입니다.
앞 실험(`projectile-motion`)에서는 실제 조절 손잡이가 맞지만, 이 실험에서는 표시용 체크박스입니다.

### 4-6. `throw-3` 미션 ② — 막대가 접혀 있어 보이지 않습니다

> 왼쪽 **에너지** 막대를 보세요. 운동 · 위치 · 열 · 합계 네 가지가 있습니다.

`EnergySkateParkModel.ts` 에서 `barGraphVisibleProperty = new BooleanProperty( false )` 입니다.
소개 화면을 열면 에너지 상자가 **접힌 채**라 막대가 하나도 안 보입니다. 실측에서도 소개 화면에는
`에너지` 글자만 있고 `운동`·`위치`·`열`·`합계` 는 없습니다(측정 화면에는 있습니다).

미션 ④⑤⑥⑨⑩이 전부 이 막대를 읽는 것이라, 여기서 막히면 레슨 전체가 멈춥니다.
**"왼쪽 `에너지` 상자의 ▸ 를 눌러 펼치세요"** 한 줄이 앞에 필요합니다.

### 4-7. `static-2` 미션 ③ — 사용법과 서로 어긋납니다

> **오른쪽 아래** 줄자를 꺼내…

줄자가 든 도구 상자는 `toolboxPanel.top = controlPanel.bottom + 10` 으로 놓여
실측 **x 1169–1265, y 291–477** — **오른쪽 가운데**입니다(줄자 아이콘은 y 422–465).
화면 오른쪽 아래(y 616)에는 `Reset All` 단추가 있습니다.

**사용법 쪽은 이미 옳게 적혀 있습니다** — 조작[5] "줄자 (**오른쪽 가운데** · 아래 칸)".
미션만 고치면 됩니다.

---

## 5. 사실 관계 (의뢰서 4-A)

`explain.body` 61편과 `real` 61편을 전수 확인했습니다. 수치는 대부분 정확했습니다 —
반감기 5730년, 태양 5800 K, 스테판–볼츠만 16배, 금성 460 °C·CO₂ 96 %, 해왕성 165년,
태양 질량비 33만, 물 104.5°, 사면체 109.5°, 나트륨·백금 일함수 대비, 노벨상 수상 사유,
러더퍼드 인용문, ²¹¹Po → ²⁰⁷Pb 의 211 = 207 + 4 · 84 = 82 + 2 까지 전부 맞습니다.

다음 세 곳만 손보시면 됩니다.

### 5-1. `throw-1` `real` — 원인이 다릅니다 (medium)

> 멀리뛰기 선수의 도약 각도가 45°보다 낮은 것도 공기저항 때문입니다.

멀리뛰기 도약각이 낮은(실제 18–22°) 이유는 **공기저항이 아닙니다.** 사람은 도약 순간에 큰 연직
속도를 만들려면 발을 오래 딛어야 하고, 그러면 助走로 얻은 수평 속도를 잃습니다. **몸이 낼 수 있는
연직 속도의 한계** 때문이지, 공기저항은 이 거리에서 무시할 수준입니다.

같은 문단의 포탄·골프공 설명은 맞습니다. 이 문장만 바꾸면 됩니다.

> **대안** — "멀리뛰기 선수의 도약 각도가 20° 안팎으로 훨씬 낮은 것은 다른 이유입니다. 크게 솟구치려면
> 발을 오래 딛어야 하는데, 그러면 달려온 속도를 잃기 때문이죠."

### 5-2. `wave-4` `explain.body` — 화면에서 본 것과 어긋납니다 (medium)

> 기본 파동(n=1)에 그 절반 파장(n=2), 3분의 1 파장(n=3)… 을 알맞은 크기로 더하면

미션 ⑤에서 학습자는 방금 `파형`을 **사각형**으로 골랐고, 그 순간 화면의 **A2 · A4 · A6 … 손잡이가
전부 0으로 내려갑니다.** 사각파는 **홀수 배음만** 씁니다.

```ts
// Waveform.ts — SQUARE
amplitudes.push( n % 2 === 0 ? 0 : ( 4 / ( n * PI ) ) );   // 4/1π, 0, 4/3π, 0, 4/5π, ...
```

"알맞은 크기"에 0이 포함된다고 볼 수는 있지만, 학습자가 바로 앞에서 본 화면과 어긋나 혼란을 줍니다.

> **대안** — "기본 파동(n=1)에 3분의 1 파장(n=3), 5분의 1 파장(n=5)… **홀수 번째만** 알맞은 크기로 더하면"
> (사각형을 골랐을 때 짝수 번째 손잡이가 0으로 내려간 것이 그 증거라고 한 줄 덧붙이면 더 좋습니다.)

### 5-3. `matter-3` `real` — 인과가 단순화되어 있습니다 (medium, likely)

> 1960년대 탈리도마이드 사고가 거울상 분자 때문이었습니다.

교과서에 흔한 서술이지만 사실과는 어긋납니다. 탈리도마이드는 **체내에서 두 거울상이 서로 뒤바뀝니다
(라세미화).** 안전한 쪽만 골라 투여했어도 사고를 막지 못했습니다. "거울상 분자 때문"이라고 못박으면
"광학이성질체만 분리하면 안전하다"는 잘못된 결론으로 이어집니다.

덧붙여 이 레슨의 주제는 **VSEPR 로 정해지는 결합 각도**인데, 거울상 이성질체는 그와 다른 종류의
"모양"이라 예시로도 어긋납니다.

> **대안** — "같은 원자로 되어 있어도 **원자가 붙은 순서와 각도**가 다르면 전혀 다른 물질이 됩니다 —
> 약이 몸속 단백질과 맞물릴 수 있느냐가 여기서 갈립니다."

### 5-4. 근사에 관한 낮은 순위 지적 (low)

| 위치 | 내용 |
|---|---|
| `wave-4` `explain.body` | "하모닉스를 늘릴수록 그 물결이 작아지지만" — 깁스 현상에서 **넘침의 높이는 약 9 %로 그대로**이고 폭만 좁아집니다. "물결이 **좁아지지만**"이 정확합니다. |
| `wave-2` `explain.body` | 등시성을 설명한 뒤 갈릴레오의 **진자** 일화를 붙였습니다. 용수철-추는 진폭과 무관하게 정확히 등시성이지만, **진자는 작은 각에서만** 그렇습니다. "진자도 작게 흔들리는 동안은"처럼 한정하면 좋겠습니다. |
| `wave-3` `real` | "소리, **빛**, 라디오 전파, 와이파이 — 전부 '물질은 그대로, 흔들림만 이동'" — 빛과 전파는 **매질이 아예 없습니다.** 04편에서 빛의 정체를 다루므로 여기서 매질이 있는 것처럼 읽히면 손해입니다. |

---

## 6. 상호 참조 (의뢰서 5-5)

교차 참조 30여 곳을 전부 따라가 확인했습니다. **한 곳만 틀렸습니다.**

### `ratio-2` `explain.body` (medium)

> **12편(그래프)** 에서 화면 해상도를 두 배로 키워도 화면 모양이 안 변한다고 했던 것과 같은 이야기죠.

화면 해상도(1920×1080 → 3840×2160) 예시는 **10편(분수) 2편** 의 `real` 에 있습니다.
12편(그래프)에는 해상도 이야기가 없습니다.

> **대안** — "**10편(분수) 2편**에서 화면 해상도를 두 배로 키워도 화면 모양이 안 변한다고 했던 것과 같은 이야기죠."

나머지는 모두 맞았습니다 — 02-1↔12-3, 02-2↔14-8·05-5, 02-4↔03-4·12-1, 05-3↔09-5·13-3,
05-5↔09-3, 07-1↔02-1, 07-2↔01-3, 10-2↔11-1, 03-2↔06-3, 04-4↔06-1·06-2 확인.

다만 참조 표기가 **두 가지로 섞여 있습니다** — "12편에서"(코스만)와 "02편 3편에서"(코스+레슨).
`편`이 두 뜻으로 쓰여 헷갈릴 수 있습니다(low).

---

## 7. 퀴즈 (의뢰서 4-C)

### 7-1. 정답 인덱스 — 240문항 전수 확인, 오류 0건

② 61문항의 `explain.right`, ⑦ 179문항의 `quiz[].right` 를 하나씩 대조했습니다.
계산이 들어가는 것(⑦ 6·8 직각합 10, 11/4 = 2와 3/4, 3과 1/5 = 16/5, (0,5)–(4,1) 기울기 −1,
2·4·6 평균 4, 3·5·7·9 평균 6, 1·2·3·4·90 평균 20 중앙값 3, pH 4↔6 100배, 빵 7 치즈 5 → 3개,
남는 것 빵 1 치즈 2, CH₄ + **2**O₂, 온도 2배 → 16배, (4+3)×2 = 14, (3−1)×4 = 8)도 전부 맞습니다.

**틀린 인덱스는 하나도 없습니다.**

### 7-2. 복수 정답 소지 (medium)

**`life-3` ⑦[2]**

> **구름**이 하는 일은?
> [0] 적외선을 붙잡아 데운다 [1] 햇빛을 되돌려 보내 식힌다 [2] 아무 영향이 없다 — 정답 1

실제 구름은 **둘 다 합니다.** 낮은 구름은 햇빛을 되돌려 식히고, 높은 구름은 적외선을 붙잡아 데웁니다.
[0]도 맞는 말이라 정답이 하나가 아닙니다. 같은 레슨 `explain.body` 가 "데우는 것과 식히는 것이 함께
움직이니까요"라고 이미 인정하고 있어 안에서도 어긋납니다.

> **대안** — 물음을 실험 안으로 한정하세요. "**이 실험에서** 구름이 하는 일은?"

### 7-3. ②와 ⑦이 같은 것을 두 번 묻는 곳

⑦의 정답 문장이 ②의 정답 문장과 사실상 같고, 오답까지 겹치는 곳입니다.

| 레슨 | ② 정답 | ⑦ 정답 | 판정 |
|---|---|---|---|
| `quantum-1` ⑦[2] | 앞도 뒤도 아닌 상태이고, 관측하는 순간 하나로 정해진다 | 앞도 뒤도 아닌 상태이고 관측할 때 정해진다 | 오답 3개까지 ②와 동일. **완전 중복** |
| `space-1` ⑦[0] | 그 순간의 방향으로 곧게 날아간다 | 곧게 날아간다 | 중복 |
| `light-1` ⑦[0] | 상 전체가 어두워질 뿐 모양은 그대로다 | 전체가 어두워진다 | 중복 |
| `atom-6` ⑦[2] | 중성자가 양성자로 바뀌면서 그 자리에서 생긴 것 | 붕괴하는 순간 만들어졌다 | 오답도 ②와 동일. 중복 |
| `wave-4` ⑦[0] | 많이 더할수록 사각파에 가까워진다 | 점점 더 사각파에 가까워진다 | 중복 |
| `space-2` ⑦[0] | 크기가 같다 — 방향만 반대다 | 태양이 지구를 당기는 힘과 같다 | 중복 |

②는 답을 감추고 ⑤에서 대조하는 구조라, ⑦이 ②를 그대로 되물으면 **확인 문항 3개 중 1개가 낭비**됩니다.
`quantum-1` · `atom-6` 은 오답 선택지까지 같아 특히 눈에 띕니다.

낮은 순위로 하나 더 — **`mix-4` ⑦[0]** 은 숫자를 바꾼 좋은 전이 문항인데 **정답이 ②와 똑같이 "3개"** 라
찍어서 넘어갈 수 있습니다. 숫자를 살짝 바꿔 답이 달라지게 하면 좋겠습니다(예: 빵 9, 치즈 5 → 4개).

**나머지 ②↔⑦ 짝은 문제없습니다.** `fraction-3` · `graph-1` · `graph-4` · `ratio-3` · `wave-1` 은
같은 유형에 숫자와 답이 달라 제대로 된 전이 문항입니다.

### 7-4. 그 밖

- 레슨 밖 지식을 요구하는 문항은 **없었습니다.**
- 오답이 너무 뻔한 문항도 눈에 띄지 않았습니다. `static-3` ⑦[1](큰 전하 쪽이 더 센 힘을 받는다)처럼
  **흔한 오개념을 정확히 겨눈** 문항이 많아 좋았습니다.

---

## 8. 난이도와 분량 (의뢰서 4-D)

의뢰서대로 **쉽게 만드는 방향의 지적은 넣지 않았습니다.**

### 8-1. 코스 01 메타데이터 불일치 (medium, certain)

`courses.json` 의 코스 01 `minutes` 가 **52** 인데, 레슨 4편의 `min` 합은 **14 + 16 + 12 + 18 = 60** 입니다.
나머지 13개 코스는 전부 일치합니다.

### 8-2. 코스 01만 미션 밀도가 다릅니다 (low)

| | 미션 수 | 배정 시간 | 분/미션 |
|---|---:|---:|---:|
| 코스 01 (static-1~4) | 6 | 12–18분 | 2.0–3.0 |
| 나머지 57편 | 9–12 | 11–15분 | 1.1–1.7 |

읽기 분량(한국어 500자/분)과 미션당 1분으로 추정하면 코스 01은 8.4–8.6분이면 끝나, 배정보다
**3.5–9.4분 남습니다.** 다른 코스는 추정과 배정이 평균 0.2분 차이로 잘 맞습니다.
코스 01의 시간을 줄이거나 미션을 3–5개 더 얹는 쪽이 일관됩니다.

### 8-3. `throw-1` 미션 ⑩⑪ 은 배정 시간에 안 들어갑니다 (medium, likely)

> ⑩ 각을 **15° · 30° · 45° · 60° · 75°** 로 바꿔 가며 **범위**를 적어 보세요.
> ⑪ 이제 **공기저항**을 켜고 **같은 각들을 다시** 해 보세요.

각도 설정 → 발사 → 착지 대기 → 값 기록이 한 번에 30–45초입니다. 두 미션이 **발사 10회**를 요구하니
6–8분입니다. 레슨 전체가 14분이고 미션이 11개인데, 이 두 개가 절반을 먹습니다.

> **대안** — ⑩은 `30° · 45° · 60°` 세 개로 줄여도 최적각을 찾는 데 충분하고,
> ⑪은 `30°` 와 `60°` 두 개만 다시 해 보면 "최적각이 내려간다"를 확인할 수 있습니다.

### 8-4. 고등학교용 시뮬레이션을 중학생 코스에 넣은 곳 — 적절합니다

`models-of-the-hydrogen-atom`(atom-3) · `calculus-grapher`(graph-4) · `quantum-*`(quantum-1~3) ·
`vector-addition`(throw-4) · `fourier-making-waves`(wave-4) 를 확인했습니다.

**멈추는 지점이 잘 잡혀 있습니다.**

- `atom-3` — 여섯 모형 중 "보어부터 실험과 맞는다"까지만 가고 드브로이·슈뢰딩거는 이름만 지나갑니다.
- `graph-4` — "도함수라는 이름은 몰라도 됩니다. **기울기를 모아 그린 그래프**라는 그림만 남으면 충분합니다."
  라고 명시적으로 선을 그었습니다. 사용법 헷갈리기[6]도 "파생적인 화면 하나만 씁니다"로 한정합니다.
- `wave-4` — 무한 급수와 깁스 현상을 "물결이 남는다"로만 다루고 수식으로 가지 않습니다.
- `quantum-3` — 상자 너비와 계단 간격의 정성적 관계까지만.

의뢰하신 "살짝 어려운 편"에 잘 맞습니다.

---

## 9. 새로 발견한 오역 (의뢰서 5-1 표에 없는 것)

의뢰서 5-1의 13건은 전부 원본에서 확인했습니다(`읿부` 는 `my-solar-system` 이 아니라
`solar-system-common` 에 있어, 두 실험이 공유합니다 — 표의 "외" 표기가 맞습니다).

아래는 **표에 없는 것**입니다.

| 시뮬레이션 | 키 | 화면에 나오는 말 | 실제 뜻 | 원고에서 |
|---|---|---|---|---|
| `greenhouse-effect` | `surfaceAlbedo` | **표면 아베도** | 표면 **알베도** | 층 모형 화면(레슨 범위 밖) |
| `fourier-making-waves` | 제목 외 4곳 | **푸우리에**: 파형만들기 / 푸우리에 급수 / 푸우리에 요소 / 푸우리에 요소의 진폭 | **푸리에** | 사용법이 제목만 언급, 나머지 3곳은 미언급 |
| `inverse-square-law-common` | `decimalNotation` | **소숫점** 표시법 | **소수점** 표시법 | `coulombs-law`(static-3) 오른쪽 아래 |
| `charges-and-fields` | `grid` | **망** | 격자 / 모눈 | 사용법이 뜻은 풀어 줬으나 오역 표기는 없음 |
| `wave-on-a-string` | `damping` | **감폭** | **감쇠** | wave-3 미션 ②⑫에서 그대로 사용 |
| `coulombs-law` | `jumpToMinimumLabel` | 최소한 **첨프** | 최소한 **점프** | 키보드 도움말(일반 사용 시 안 보임) |

`fourier-making-waves` 사용법 헷갈리기[0]은 "표기가 일반적이지 않을 뿐"이라고 썼는데,
`푸우리에`는 표기 차이가 아니라 **철자 오류**입니다. 그리고 제목 말고도 **화면 안에 3곳 더** 나옵니다.

`charges-and-fields` 는 미번역 `Snap to Grid` 를 사용법이 이미 다루고 있어 처리가 좋습니다.

### 참고 — 한국어 적용률

61종 중 55종에 한국어가 있고(5-3의 6종 제외와 일치), 화면 문구 기준 적용률을 계산했습니다.
**미번역이 남은 것 대부분은 키보드 도움말 문자열**이라 일반 조작에는 안 보입니다.
다만 다음은 화면에 영어로 나옵니다.

- `balancing-chemical-equations` — 화면 이름 `Intro` · `Equations`, `Synthesis` · `Decomposition` ·
  `Combustion`, `Simplified` (사용법이 이미 다룸 ✅)
- `my-solar-system` — `Orbital System 1~4`
- `keplers-laws` — `Target Orbit 1~4` (행성 이름 `금성`·`화성`·`목성` 은 번역됨)
- `gas-properties` — `Wall Velocity`
- `charges-and-fields` — `Snap to Grid` (사용법이 이미 다룸 ✅)

또 `my-solar-system` 의 줌 표시가 **`×10-2</sup`** 처럼 닫는 태그가 깨져 보입니다. 번역 원본의
`<sup>` 짝이 맞지 않아 생긴 것으로, PhET 쪽 버그입니다.

---

## 10. 표현 (의뢰서 4-E)

**용어 일관성은 좋습니다.** 알갱이/입자, 세기(강도 0회), 봉우리(피크 0회), 눈금(틱 0회),
견주다(비교 10회)로 방침이 지켜지고 있습니다. `node tools/lint.mjs` 도 오류 0 · 경고 0 입니다.

지적할 것은 두 가지뿐입니다.

- `static-3` 미션 ④ — "이번엔 **전하 1만 두 배로 올리세요.**" 전하 1의 기본값이 **−4 μC**(음수)라
  "올리다"가 −4 → −2 로 읽힐 수 있습니다. "**전하 1의 크기만 두 배로**(−4 → −8) 하세요"가 명확합니다. (low)
- 참조 표기 혼용 — §6 끝에 적은 "12편에서" vs "02편 3편에서". (low)

---

## 11. 결과 JSON

의뢰서 7의 형식입니다. `quote` 는 원문 그대로이며 `<b>` 등 태그를 포함합니다.

```json
[
  {
    "id": "life-3",
    "where": "missions[0]",
    "severity": "high",
    "kind": "mission",
    "quote": "왼쪽 위 <b>에너지 균형</b>에 체크하세요.",
    "problem": "에너지 균형 체크박스는 관찰창 오른쪽 아래에 있습니다(실측 891,543). 왼쪽 위는 체크한 뒤 막대 그래프가 나타나는 자리입니다. GreenhouseEffectObservationWindow.ts 에서 체크박스가 든 instrumentVisibilityPanel 은 xAlign 'right' / yAlign 'bottom' 으로, energyBalancePanel(막대)은 windowFrame.leftTop 으로 놓입니다. 첫 미션부터 없는 자리를 가리켜 학습자가 바로 막힙니다.",
    "fix": "관찰창 오른쪽 아래 <b>에너지 균형</b>에 체크하세요. 그러면 왼쪽 위에",
    "confidence": "certain"
  },
  {
    "id": "greenhouse-effect",
    "where": "controls[0].name",
    "severity": "high",
    "kind": "mission",
    "quote": "에너지 균형 (왼쪽 위 체크박스)",
    "problem": "체크박스는 관찰창 오른쪽 아래입니다. 왼쪽 위는 체크 결과(막대 그래프)가 나타나는 자리입니다.",
    "fix": "에너지 균형 (오른쪽 아래 체크박스 — 켜면 왼쪽 위에 막대가 나옵니다)",
    "confidence": "certain"
  },
  {
    "id": "greenhouse-effect",
    "where": "summary",
    "severity": "medium",
    "kind": "mission",
    "quote": "왼쪽 위 <b>에너지 균형</b> 계기판이 이 실험의 핵심이라, 그것부터 켜고 시작해야 합니다.",
    "problem": "켜는 체크박스는 오른쪽 아래입니다. 왼쪽 위는 켠 뒤 계기판이 나타나는 자리입니다.",
    "fix": "<b>에너지 균형</b> 계기판이 이 실험의 핵심이라, 오른쪽 아래에서 그것부터 켜고 시작해야 합니다.",
    "confidence": "certain"
  },
  {
    "id": "space-3",
    "where": "missions[0]",
    "severity": "high",
    "kind": "mission",
    "quote": "왼쪽 위 <b>이심률</b> 손잡이가 궤도를 얼마나 찌그러뜨릴지 정합니다.",
    "problem": "이심률 손잡이는 오른쪽 위입니다(실측 상자 x1064~1254, y110~226). 케플러 법칙 실험의 조절판은 화면 오른쪽에 있습니다. 좌우가 반대입니다.",
    "fix": "오른쪽 위 <b>이심률</b> 손잡이가 궤도를 얼마나 찌그러뜨릴지 정합니다.",
    "confidence": "certain"
  },
  {
    "id": "keplers-laws",
    "where": "controls[0].name",
    "severity": "high",
    "kind": "mission",
    "quote": "이심률 (왼쪽 위 손잡이)",
    "problem": "이심률 손잡이는 오른쪽 위 조절판 안에 있습니다.",
    "fix": "이심률 (오른쪽 위 손잡이)",
    "confidence": "certain"
  },
  {
    "id": "atom-2",
    "where": "missions[2]",
    "severity": "high",
    "kind": "mission",
    "quote": "왼쪽 <b>알파입자 성질</b>에서 <b>에너지</b>를 최소부터 최대까지 바꿔 보세요.",
    "problem": "알파입자 성질 패널은 화면 오른쪽입니다. RSBaseScreenView.ts 의 createControlPanelVBox() 가 패널 묶음을 left: spaceNode.right + margin 으로 붙입니다. 같은 묶음에 든 범례·원자를 사용법이 오른쪽이라고 옳게 적고 있어 이 항목만 어긋납니다.",
    "fix": "오른쪽 <b>알파입자 성질</b>에서 <b>에너지</b>를 최소부터 최대까지 바꿔 보세요.",
    "confidence": "certain"
  },
  {
    "id": "rutherford-scattering",
    "where": "controls[1].name",
    "severity": "high",
    "kind": "mission",
    "quote": "알파입자 성질 — 에너지 (왼쪽)",
    "problem": "이 패널은 범례·원자와 같은 세로 묶음에 들어 화면 오른쪽에 놓입니다.",
    "fix": "알파입자 성질 — 에너지 (오른쪽)",
    "confidence": "certain"
  },
  {
    "id": "atom-3",
    "where": "missions[7]",
    "severity": "high",
    "kind": "mission",
    "quote": "오른쪽 <b>트랜지스터</b> 상자를 펼치세요.",
    "problem": "트랜지스터는 접이 상자가 아니라 누르면 별도 팝업 창이 뜨는 단추이고(TransitionsButton.ts 는 RectangularPushButton, listener 가 transitionsDialog.show()), 자리도 오른쪽이 아니라 빛 상자 바로 아래(화면 아래 왼편)입니다. MOTHAScreenView.ts 의 bottomHBox 가 left: layoutBounds.left + X_MARGIN, top: zoomedInBoxNode.bottom + 15 로 놓입니다.",
    "fix": "빛 상자 아래 <b>트랜지스터</b> 단추를 누르세요. 창이 하나 뜹니다.",
    "confidence": "certain"
  },
  {
    "id": "models-of-the-hydrogen-atom",
    "where": "controls[4].name",
    "severity": "high",
    "kind": "mission",
    "quote": "트랜지스터 (오른쪽 접이 상자)",
    "problem": "접이 상자가 아니라 팝업 창을 여는 단추이고, 자리는 화면 아래 왼편(빛 상자 바로 아래)입니다.",
    "fix": "트랜지스터 (빛 상자 아래 단추 — 누르면 창이 뜹니다)",
    "confidence": "certain"
  },
  {
    "id": "throw-2",
    "where": "missions[0]",
    "severity": "high",
    "kind": "mission",
    "quote": "왼쪽 아래 <b>발사각</b>과 <b>발사속도</b>를 정할 수 있습니다.",
    "problem": "두 가지가 틀렸습니다. (1) 가변성 화면의 조절판(방향·투사체·미스터리 발사기)은 왼쪽 위입니다. (2) 발사각·발사속도는 오른쪽 도구 패널의 체크박스로 값을 보여 주는 도구이지 설정하는 것이 아닙니다(StaticToolPanel.ts 의 launchAngleCheckbox / launchSpeedCheckbox). 가변성 화면의 발사기는 설정이 감춰진 미스터리 발사기라 각도·속도를 정할 수 없습니다.",
    "fix": "왼쪽 위에서 <b>미스터리 발사기</b>를 고릅니다. 발사 조건은 감춰져 있어 바꿀 수 없습니다 — 그게 이 화면의 목적입니다.",
    "confidence": "certain"
  },
  {
    "id": "projectile-data-lab",
    "where": "controls[1].name",
    "severity": "high",
    "kind": "mission",
    "quote": "발사각 · 발사속도 (왼쪽 아래)",
    "problem": "발사각·발사속도는 오른쪽 도구 패널의 체크박스입니다. 왼쪽 위에 있는 것은 방향·투사체·미스터리 발사기 조절판입니다.",
    "fix": "발사각 · 발사속도 (오른쪽 체크박스)",
    "confidence": "certain"
  },
  {
    "id": "projectile-data-lab",
    "where": "controls[1].desc",
    "severity": "high",
    "kind": "mission",
    "quote": "발사 조건입니다. 앞 실험과 같습니다.",
    "problem": "발사 조건을 정하는 손잡이가 아니라, 발사각과 발사속도를 화면에 표시해 주는 체크박스입니다. 앞 실험(projectile-motion)에서는 실제 조절 손잡이였지만 이 실험에서는 다릅니다.",
    "fix": "켜면 발사각과 발사속도를 화면에 표시해 줍니다. 앞 실험과 달리 값을 정하는 것이 아니라 보여 주기만 합니다.",
    "confidence": "certain"
  },
  {
    "id": "throw-3",
    "where": "missions[1]",
    "severity": "high",
    "kind": "mission",
    "quote": "왼쪽 <b>에너지</b> 막대를 보세요. <b>운동 · 위치 · 열 · 합계</b> 네 가지가 있습니다.",
    "problem": "소개 화면을 열면 에너지 상자가 접힌 채라 막대가 하나도 안 보입니다(EnergySkateParkModel.ts 의 barGraphVisibleProperty 기본값 false). 실측에서도 소개 화면에는 에너지 글자만 있고 운동·위치·열·합계는 없습니다. 미션 4·5·6·9·10이 전부 이 막대를 읽는 것이라 여기서 막히면 레슨이 멈춥니다.",
    "fix": "왼쪽 <b>에너지</b> 상자의 ▸를 눌러 펼치세요. <b>운동 · 위치 · 열 · 합계</b> 네 가지 막대가 나옵니다.",
    "confidence": "certain"
  },
  {
    "id": "static-2",
    "where": "missions[2]",
    "severity": "medium",
    "kind": "mission",
    "quote": "오른쪽 아래 <b>줄자</b>를 꺼내",
    "problem": "줄자가 든 도구 상자는 오른쪽 가운데입니다(실측 x1169~1265, y291~477, 줄자 아이콘은 y422~465). 화면 오른쪽 아래에는 Reset All 단추가 있습니다. 같은 저장소의 사용법 조작[5]에는 줄자 (오른쪽 가운데 · 아래 칸)으로 옳게 적혀 있어 미션과 서로 어긋납니다.",
    "fix": "오른쪽 가운데 <b>줄자</b>를 꺼내",
    "confidence": "certain"
  },
  {
    "id": "my-solar-system",
    "where": "controls[2].name",
    "severity": "medium",
    "kind": "mission",
    "quote": "물체 (왼쪽 아래) — 천체 수",
    "problem": "물체 수 조절기는 화면 아래 가운데입니다(실측 x528~604, y589~649). 왼쪽 아래에 있는 것은 질량 조절판입니다.",
    "fix": "물체 (아래 가운데) — 천체 수",
    "confidence": "certain"
  },
  {
    "id": "throw-4",
    "where": "missions[8]",
    "severity": "high",
    "kind": "mission",
    "quote": "오른쪽 <b>성분</b>에서 <b>Projected onto x y axes</b>를 고르세요.",
    "problem": "Projected onto x y axes 는 화면에 그려지지 않습니다. PhET 의 a11y.projectionRadioButton.accessibleName 으로 스크린리더 전용입니다. ComponentsRadioButtonGroup.ts 는 아이콘 네 개(invisible/triangle/parallelogram/projection)만 그립니다. 학습자가 찾을 글자가 없습니다.",
    "fix": "오른쪽 <b>성분</b>의 아이콘 네 개 중 <b>네 번째</b>(가로·세로 축에 점선을 내려 그은 그림)를 고르세요.",
    "confidence": "certain"
  },
  {
    "id": "throw-4",
    "where": "missions[9]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>값</b>과 <b>Angles</b>를 켜면 크기와 각도가 숫자로 나옵니다.",
    "problem": "Angles 는 화면에 없습니다. AnglesCheckbox.ts 는 createAngleIcon() 만 그려서 θ 모양 아이콘으로 나옵니다. 값은 실제로 한국어 글자로 보입니다.",
    "fix": "<b>값</b>과 <b>θ 아이콘 체크박스</b>(각도 보기)를 켜면 크기와 각도가 숫자로 나옵니다.",
    "confidence": "certain"
  },
  {
    "id": "throw-4",
    "where": "missions[10]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Scene</b>을 <b>Polar</b>로 바꾸면 격자가 <b>각도 눈금</b>으로 바뀝니다.",
    "problem": "Scene 도 Polar 도 화면에 없습니다. CartesianPolarSceneRadioButtonGroup.ts 는 아이콘 두 개만 그립니다.",
    "fix": "오른쪽 아래 <b>아이콘 두 개</b> 중 <b>부채꼴 눈금 그림</b>을 고르면 격자가 <b>각도 눈금</b>으로 바뀝니다.",
    "confidence": "certain"
  },
  {
    "id": "vector-addition",
    "where": "summary",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>한국어가 거의 적용되지 않아</b> 대부분의 단추가 영어로 나옵니다.",
    "problem": "사실과 반대입니다. 2D 탐색 화면에 그려지는 글자는 합계·값·성분·θ·a·b·c·벡터가 선택되지 않음으로 전부 한국어입니다. 사용법에 적힌 영어 이름들은 화면에 아예 나오지 않는 스크린리더 전용 이름입니다.",
    "fix": "글자로 이름이 붙은 단추는 <b>합계 · 값 · 성분</b>뿐이고, 나머지는 <b>글자 없이 그림만</b> 있습니다.",
    "confidence": "certain"
  },
  {
    "id": "vector-addition",
    "where": "gotchas[0]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>대부분의 단추가 영어</b>로 나옵니다. 위 이름표에서 뜻을 찾으세요.",
    "problem": "영어로 나오는 것이 아니라 글자가 아예 없습니다. 각도·격자·성분 방식·좌표계 단추는 모두 아이콘입니다.",
    "fix": "<b>대부분의 단추에 글자가 없습니다.</b> 그림으로만 구별해야 하니 위 이름표에서 어떤 그림인지 찾으세요.",
    "confidence": "certain"
  },
  {
    "id": "vector-addition",
    "where": "controls[4].desc",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Hidden</b>(안 보기) · <b>Right triangle</b>(직각삼각형) · <b>From vector tail</b>(꼬리에서) · <b>Projected onto x y axes</b>(축에 투영) 네 가지입니다.",
    "problem": "네 이름 모두 화면에 나오지 않습니다. 스크린리더 전용 이름이고, 화면에는 아이콘 네 개만 2x2 로 놓입니다. 순서는 안 보기, 직각삼각형, 평행사변형(From vector tail), 축에 투영입니다.",
    "fix": "글자 없이 <b>그림 네 개</b>가 2×2로 놓입니다. 왼쪽 위부터 <b>안 보기 · 직각삼각형 · 평행사변형 · 축에 투영</b> 순서입니다.",
    "confidence": "certain"
  },
  {
    "id": "ratio-1",
    "where": "missions[4]",
    "severity": "high",
    "kind": "mission",
    "quote": "오른쪽 위 <b>Numbered Tick Marks</b>(눈금에 숫자)를 켜세요.",
    "problem": "Numbered Tick Marks 는 화면에 없습니다. a11y.tickMark.showNumbered 로 스크린리더 전용이며, 화면에는 아이콘 단추 세 개만 있습니다. 실제로 발견하기 화면에 그려지는 글자는 도전 1 하나뿐입니다. 또 세 갈래 고르개라 켜세요도 정확하지 않습니다.",
    "fix": "오른쪽 위 <b>눈금 단추 세 개</b> 중 <b>세 번째</b>(눈금에 숫자가 붙은 그림)를 고르세요.",
    "confidence": "certain"
  },
  {
    "id": "ratio-and-proportion",
    "where": "gotchas[1]",
    "severity": "medium",
    "kind": "mission",
    "quote": "눈금 단추 이름이 <b>영어</b>로 나옵니다. 왼쪽부터 눈금 없음 · 눈금 · 숫자 눈금입니다.",
    "problem": "영어로 나오는 것이 아니라 글자가 아예 없습니다. 아이콘 단추 세 개입니다. 순서 설명은 맞습니다.",
    "fix": "눈금 단추에는 <b>글자가 없습니다.</b> 그림으로 구별하며, 왼쪽부터 눈금 없음 · 눈금 · 숫자 눈금입니다.",
    "confidence": "certain"
  },
  {
    "id": "mix-3",
    "where": "missions[2]",
    "severity": "medium",
    "kind": "mission",
    "quote": "오른쪽 <b>View</b>에서 <b>Particles</b>(알갱이)를 고르세요.",
    "problem": "View 는 화면에 나옵니다(오른쪽 위, 미번역). 하지만 Particles 는 나오지 않습니다. ViewComboBox.ts 가 항목을 createIcon() 으로 그려서 알갱이·저울·막대는 그림이고, 없음만 글자입니다.",
    "fix": "오른쪽 <b>View</b>를 눌러 <b>알갱이 그림</b>(맨 위 항목)을 고르세요.",
    "confidence": "certain"
  },
  {
    "id": "mix-3",
    "where": "missions[7]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>View</b>를 <b>Balance Scales</b>(저울)와 <b>Bar Charts</b>(막대)로 바꿔 가며 같은 것을 세 방식으로 보세요.",
    "problem": "Balance Scales 와 Bar Charts 는 화면에 없습니다. 콤보박스 항목이 전부 그림입니다.",
    "fix": "<b>View</b>를 <b>저울 그림</b>과 <b>막대 그림</b>으로 바꿔 가며 같은 것을 세 방식으로 보세요.",
    "confidence": "certain"
  },
  {
    "id": "balancing-chemical-equations",
    "where": "controls[2].desc",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Particles</b>(알갱이) · <b>Balance Scales</b>(저울) · <b>Bar Charts</b>(막대) · <b>없음</b> 중에 고릅니다. 마지막만 한국어입니다.",
    "problem": "앞의 세 항목은 영어로 나오는 것이 아니라 글자 없이 그림으로만 나옵니다. 없음만 글자입니다.",
    "fix": "<b>알갱이 그림</b> · <b>저울 그림</b> · <b>막대 그림</b> · <b>없음</b> 중에 고릅니다. 앞의 셋은 글자 없이 그림만 있고, 마지막만 글자입니다.",
    "confidence": "certain"
  },
  {
    "id": "mix-3",
    "where": "missions[8]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Reaction Type</b>으로 종류를 고를 수 있습니다.",
    "problem": "Reaction Type 은 a11y.reactionType 으로 스크린리더 전용이라 화면에 없습니다. 다만 선택지인 Synthesis, Decomposition, Combustion 은 영어 글자로 화면 아래에 실제로 나옵니다.",
    "fix": "아래 <b>Synthesis</b>(합성) · <b>Decomposition</b>(분해) · <b>Combustion</b>(연소)으로 종류를 고를 수 있습니다.",
    "confidence": "certain"
  },
  {
    "id": "energy-skate-park",
    "where": "gotchas[1]",
    "severity": "medium",
    "kind": "mission",
    "quote": "트랙 이름 <b>Parabola · Ramp · Double Well · Loop</b>는 영어로 나옵니다.",
    "problem": "화면에 나오지 않습니다. a11y.trackSelectionRadioButtonGroup 아래 accessibleName 으로 스크린리더 전용이고, 화면에는 트랙 모양 아이콘만 있습니다.",
    "fix": "트랙 고르개에는 <b>글자가 없습니다.</b> 트랙 모양 그림으로 구별하며, 차례로 포물선 · 경사로 · 쌍언덕 · 고리입니다.",
    "confidence": "certain"
  },
  {
    "id": "energy-skate-park",
    "where": "controls[3].desc",
    "severity": "medium",
    "kind": "mission",
    "quote": "미리 만들어진 트랙 네 가지입니다. 이름이 영어로 나옵니다 — 포물선 · 경사로 · 쌍언덕 · 고리입니다.",
    "problem": "이름이 화면에 나오지 않습니다. 트랙 모양 아이콘 네 개뿐입니다.",
    "fix": "미리 만들어진 트랙 네 가지입니다. 글자 없이 트랙 모양 그림으로 나오며, 차례로 포물선 · 경사로 · 쌍언덕 · 고리입니다.",
    "confidence": "certain"
  },
  {
    "id": "life-3",
    "where": "missions[10]",
    "severity": "medium",
    "kind": "mission",
    "quote": "오른쪽 <b>Experiment Mode</b>를 <b>By time period</b>로 바꾸고",
    "problem": "Experiment Mode 와 By time period 는 a11y.concentrationPanel 아래 이름으로 스크린리더 전용이라 화면에 없습니다. 화면에는 농도 패널 아래 아이콘 단추 두 개만 있습니다. 이어지는 빙하시대·1750·1950·2020 은 실제로 나오므로 맞습니다.",
    "fix": "오른쪽 농도 상자 아래 <b>아이콘 단추 두 개</b> 중 <b>시계 그림</b>(시대별)으로 바꾸고",
    "confidence": "certain"
  },
  {
    "id": "greenhouse-effect",
    "where": "gotchas[5]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Experiment Mode</b>와 온도 단위 이름이 영어로 나옵니다.",
    "problem": "Experiment Mode 는 영어로 나오는 것이 아니라 화면에 아예 없습니다(스크린리더 전용). 온도 단위 K, °C, °F 는 실제로 화면에 나옵니다.",
    "fix": "농도 방식 고르개에는 <b>글자가 없습니다</b> — 그림 두 개로 구별합니다. 온도 단위는 K · °C · °F 로 나옵니다.",
    "confidence": "certain"
  },
  {
    "id": "light-4",
    "where": "missions[1]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Particle Type</b>(입자 종류)이 <b>Photons</b>(광자)인지 확인하고",
    "problem": "Particle Type 은 a11y.sceneRadioButtonGroup.accessibleName 으로 화면에 없습니다. 다만 선택지 Photons, Electrons, Neutrons, Helium Atoms 는 왼쪽 아래에 영어 글자로 실제로 나옵니다.",
    "fix": "왼쪽 아래 입자 고르개가 <b>Photons</b>(광자)인지 확인하고",
    "confidence": "certain"
  },
  {
    "id": "light-4",
    "where": "missions[6]",
    "severity": "medium",
    "kind": "mission",
    "quote": "<b>Detection Mode</b>(검출 방식)를 <b>Hits</b>(맞은 자리)로 바꾸세요.",
    "problem": "Detection Mode 는 a11y.detectionModeRadioButtons.accessibleName 으로 화면에 없습니다. Hits 는 실제로 나옵니다.",
    "fix": "검출 방식을 <b>Hits</b>(맞은 자리)로 바꾸세요.",
    "confidence": "certain"
  },
  {
    "id": "light-4",
    "where": "missions[10]",
    "severity": "low",
    "kind": "mission",
    "quote": "<b>Particle Type</b>을 <b>Electrons</b>(전자)나 <b>Helium Atoms</b>(헬륨 원자)로 바꿔 보세요.",
    "problem": "Particle Type 이라는 글자는 화면에 없습니다. 선택지 이름은 실제로 나옵니다.",
    "fix": "왼쪽 아래 입자 고르개를 <b>Electrons</b>(전자)나 <b>Helium Atoms</b>(헬륨 원자)로 바꿔 보세요.",
    "confidence": "certain"
  },
  {
    "id": "number-pairs",
    "where": "controls[6].name",
    "severity": "low",
    "kind": "mission",
    "quote": "Representation Type (아래 가운데) — 물건 모양",
    "problem": "Representation Type 은 a11y.representationType.accessibleName 으로 스크린리더 전용이라 화면에 없습니다. 고르개 자체는 아래 가운데가 맞습니다.",
    "fix": "물건 모양 고르개 (아래 가운데 — 글자 없이 그림만)",
    "confidence": "certain"
  },
  {
    "id": "photoelectric-effect",
    "where": "controls[6].name",
    "severity": "low",
    "kind": "mission",
    "quote": "Representation — Grounded · Circuit (표현 방식)",
    "problem": "Representation 과 Circuit 은 a11y.representationRadioButtonGroup 아래 이름으로 스크린리더 전용이라 화면에 없습니다. 이 실험은 원래 영어로 열리지만 이 두 이름만은 어느 언어로도 나오지 않습니다.",
    "fix": "표현 방식 고르개 (글자 없이 그림 두 개 — 접지 그림 / 회로 그림)",
    "confidence": "certain"
  },
  {
    "id": "quantum-bound-states",
    "where": "controls[7].name",
    "severity": "low",
    "kind": "mission",
    "quote": "Hide Curves (곡선 감추기) · Restart · Pause",
    "problem": "Hide Curves 는 a11y.curvesVisibleToggleButton.accessibleNameOn 으로 스크린리더 전용이라 화면에 없습니다. 눈 모양 아이콘 단추입니다.",
    "fix": "곡선 감추기 (눈 모양 아이콘 단추) · Restart · Pause",
    "confidence": "certain"
  },
  {
    "id": "throw-1",
    "where": "real",
    "severity": "medium",
    "kind": "fact",
    "quote": "멀리뛰기 선수의 도약 각도가 45°보다 낮은 것도 공기저항 때문입니다.",
    "problem": "원인이 다릅니다. 멀리뛰기 도약각이 낮은(실제 18~22°) 이유는 공기저항이 아니라 사람의 몸이 낼 수 있는 연직 속도의 한계 때문입니다. 크게 솟구치려면 발을 오래 딛어야 하고 그러면 조주로 얻은 수평 속도를 잃습니다. 이 거리에서 공기저항은 무시할 수준입니다. 같은 문단의 포탄·골프공 설명은 맞습니다.",
    "fix": "멀리뛰기 선수의 도약 각도가 20° 안팎으로 훨씬 낮은 것은 다른 이유입니다. 크게 솟구치려면 발을 오래 딛어야 하는데, 그러면 달려온 속도를 잃기 때문이죠.",
    "confidence": "certain"
  },
  {
    "id": "wave-4",
    "where": "explain.body",
    "severity": "medium",
    "kind": "fact",
    "quote": "기본 파동(n=1)에 그 절반 파장(n=2), 3분의 1 파장(n=3)… 을 <strong>알맞은 크기로</strong> 더하면",
    "problem": "사각파는 홀수 배음만 씁니다. Waveform.ts 의 SQUARE 가 amplitudes.push( n % 2 === 0 ? 0 : 4/(n*PI) ) 로 짝수 항을 정확히 0으로 둡니다. 학습자는 바로 앞 미션 5에서 파형을 사각형으로 골랐고, 그 순간 화면의 A2·A4·A6 손잡이가 전부 0으로 내려간 것을 봤습니다. 설명이 화면과 어긋납니다.",
    "fix": "기본 파동(n=1)에 3분의 1 파장(n=3), 5분의 1 파장(n=5)… <strong>홀수 번째만</strong> 알맞은 크기로 더하면",
    "confidence": "certain"
  },
  {
    "id": "matter-3",
    "where": "real",
    "severity": "medium",
    "kind": "fact",
    "quote": "같은 원자로 되어 있어도 모양이 다르면 전혀 다른 물질이 됩니다 — 1960년대 탈리도마이드 사고가 거울상 분자 때문이었습니다.",
    "problem": "널리 퍼진 서술이지만 사실과 어긋납니다. 탈리도마이드는 체내에서 두 거울상이 서로 뒤바뀌어(라세미화) 안전한 쪽만 골라 투여했어도 사고를 막지 못했습니다. 거울상 분자 때문이라고 못박으면 광학이성질체만 분리하면 안전하다는 잘못된 결론을 심습니다. 또 이 레슨의 주제는 VSEPR 로 정해지는 결합 각도인데 거울상 이성질체는 다른 종류의 모양이라 예시로도 어긋납니다.",
    "fix": "같은 원자로 되어 있어도 <b>붙은 순서와 각도</b>가 다르면 전혀 다른 물질이 됩니다 — 약이 몸속 단백질과 맞물릴 수 있느냐가 여기서 갈립니다.",
    "confidence": "likely"
  },
  {
    "id": "wave-4",
    "where": "explain.body",
    "severity": "low",
    "kind": "fact",
    "quote": "하모닉스를 늘릴수록 그 물결이 작아지지만 완전히 사라지지는 않습니다.",
    "problem": "깁스 현상에서 모서리 근처 넘침의 높이는 약 9%로 그대로 남고, 물결이 차지하는 폭만 좁아집니다. 작아진다는 높이도 줄어든다는 뜻으로 읽힙니다.",
    "fix": "하모닉스를 늘릴수록 그 물결이 모서리 쪽으로 좁아지지만 완전히 사라지지는 않습니다.",
    "confidence": "likely"
  },
  {
    "id": "wave-2",
    "where": "explain.body",
    "severity": "low",
    "kind": "fact",
    "quote": "이 성질을 <strong>등시성</strong>이라고 합니다. 흔들림의 크기와 상관없이 주기가 일정하다는 뜻이죠.",
    "problem": "바로 뒤에 갈릴레오의 진자 일화가 붙는데, 용수철-추는 진폭과 무관하게 정확히 등시성이지만 진자는 작은 각에서만 그렇습니다. 진자도 언제나 등시성이라는 오해를 심을 수 있습니다.",
    "fix": "이 성질을 <strong>등시성</strong>이라고 합니다. 흔들림의 크기와 상관없이 주기가 일정하다는 뜻이죠. 진자는 작게 흔들리는 동안만 그렇습니다.",
    "confidence": "likely"
  },
  {
    "id": "wave-3",
    "where": "real",
    "severity": "low",
    "kind": "fact",
    "quote": "소리, 빛, 라디오 전파, 와이파이 — 전부 '물질은 그대로, 흔들림만 이동'입니다.",
    "problem": "빛·라디오 전파·와이파이는 매질이 아예 없습니다. 물질은 그대로라고 묶으면 매질이 있는 것처럼 읽혀, 04편(빛의 정체)에서 다시 풀어야 할 오해가 생깁니다.",
    "fix": "소리와 지진파는 '물질은 그대로, 흔들림만 이동'입니다. 빛과 라디오 전파, 와이파이는 옮겨 줄 물질조차 필요 없는데, 그 이야기는 04편에서 합니다.",
    "confidence": "likely"
  },
  {
    "id": "ratio-2",
    "where": "explain.body",
    "severity": "medium",
    "kind": "crossref",
    "quote": "12편(그래프)에서 화면 해상도를 두 배로 키워도 화면 모양이 안 변한다고 했던 것과 같은 이야기죠.",
    "problem": "화면 해상도(1920×1080 → 3840×2160) 예시는 10편(분수) 2편의 real 에 있습니다. 12편(그래프)에는 해상도 이야기가 없습니다.",
    "fix": "10편(분수) 2편에서 화면 해상도를 두 배로 키워도 화면 모양이 안 변한다고 했던 것과 같은 이야기죠.",
    "confidence": "certain"
  },
  {
    "id": "life-3",
    "where": "quiz[2].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "<b>구름</b>이 하는 일은?",
    "problem": "정답이 하나가 아닙니다. 실제 구름은 햇빛을 되돌려 식히기도 하고(낮은 구름) 적외선을 붙잡아 데우기도 합니다(높은 구름). 오답으로 둔 [0] 적외선을 붙잡아 데운다도 맞는 말입니다. 같은 레슨 explain.body 가 데우는 것과 식히는 것이 함께 움직인다고 이미 인정하고 있어 안에서도 어긋납니다.",
    "fix": "<b>이 실험에서</b> 구름이 하는 일은?",
    "confidence": "certain"
  },
  {
    "id": "quantum-1",
    "where": "quiz[2].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "<b>중첩</b>을 가장 정확히 설명한 것은?",
    "problem": "②를 그대로 되묻습니다. 정답 '앞도 뒤도 아닌 상태이고 관측할 때 정해진다'는 ②의 정답과 사실상 같은 문장이고, 오답 '빠르게 오가는 상태'와 '관측자가 모르는 상태'도 ②의 오답 두 개와 같습니다. 확인 문항 세 개 중 하나가 낭비됩니다.",
    "fix": "중첩을 다른 각도에서 확인하는 문항으로 바꾸기를 권합니다. 예: '중첩 상태의 α와 β가 확률보다 더 많은 정보를 담고 있다는 것은 어디서 드러나나요?' → 측정 횟수를 늘릴 때 / 두 틈 실험의 줄무늬에서 / 동전을 덮어 둘 때 (정답 두 번째)",
    "confidence": "certain"
  },
  {
    "id": "atom-6",
    "where": "quiz[2].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "핵에서 튀어나온 전자는 어디에 있던 것인가요?",
    "problem": "②를 그대로 되묻습니다. 정답 '붕괴하는 순간 만들어졌다'는 ②의 정답과 같고, 오답 '전자껍질'과 '핵 안에 보관되어 있었다'도 ②의 오답과 같습니다.",
    "fix": "레슨의 다른 지점을 묻는 것이 좋겠습니다. 예: 'β⁻ 붕괴 전후로 전하의 합이 맞아떨어지는 이유는?' → 중성자(0)가 양성자(+1)와 전자(−1)로 갈렸으니까 / 전자가 밖에서 들어왔으니까 / 전하는 보존되지 않으니까 (정답 첫 번째)",
    "confidence": "certain"
  },
  {
    "id": "space-1",
    "where": "quiz[0].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "궤도를 도는 물체에 <b>중력이 사라지면</b>?",
    "problem": "②와 같은 것을 묻습니다. ②가 달이 지구를 도는 중에 중력이 갑자기 사라진 상황이고 정답이 '그 순간의 방향으로 곧게 날아간다'인데, 이 문항은 같은 상황을 일반화한 것뿐이고 정답도 '곧게 날아간다'로 같습니다. 오답도 멈춘다·떨어진다로 겹칩니다.",
    "fix": "레슨의 다른 지점으로 바꾸기를 권합니다. 예: '달이 지구로 떨어지지 않는 이유는?' → 중력이 달까지 닿지 않아서 / 옆으로 가는 속도가 있어 계속 비껴 가서 / 달이 너무 가벼워서 (정답 두 번째)",
    "confidence": "certain"
  },
  {
    "id": "light-1",
    "where": "quiz[0].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "렌즈의 <b>일부만</b> 가리면 상은?",
    "problem": "②와 같은 것을 묻습니다. ②가 렌즈의 절반을 가린 상황이고 정답이 '상 전체가 어두워질 뿐 모양은 그대로다'인데, 이 문항은 절반을 일부로 바꾼 것뿐이고 정답도 '전체가 어두워진다'로 같습니다.",
    "fix": "레슨의 다른 지점으로 바꾸기를 권합니다. 예: '주된 광선 세 개만 그려 상을 찾는 작도법이 뜻하는 것은?' → 실제로 광선이 셋뿐이다 / 작도를 쉽게 하려는 요령이다 / 렌즈가 세 부분으로 나뉘어 있다 (정답 두 번째)",
    "confidence": "certain"
  },
  {
    "id": "wave-4",
    "where": "quiz[0].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "사각파를 만들 때 하모닉스를 <b>늘리면</b>?",
    "problem": "②와 같은 것을 묻습니다. ②의 정답이 '만들 수 있다 — 많이 더할수록 사각파에 가까워진다'인데 이 문항의 정답도 '점점 더 사각파에 가까워진다'로 같습니다.",
    "fix": "화면에서 본 다른 것을 묻는 편이 좋겠습니다. 예: '파형을 사각형으로 골랐을 때 짝수 번째 손잡이(A2·A4)는 어떻게 되나요?' → 0이 된다 / 홀수 번째와 같아진다 / 가장 커진다 (정답 첫 번째)",
    "confidence": "likely"
  },
  {
    "id": "space-2",
    "where": "quiz[0].q",
    "severity": "medium",
    "kind": "quiz",
    "quote": "지구가 태양을 당기는 힘은?",
    "problem": "②와 같은 것을 묻습니다. ②가 두 힘을 견주는 물음이고 정답이 '크기가 같다 — 방향만 반대다'인데, 이 문항의 정답도 '태양이 지구를 당기는 힘과 같다'로 같습니다.",
    "fix": "레슨의 다른 지점으로 바꾸기를 권합니다. 예: '태양과 지구의 질량 중심은 어디에 있나요?' → 두 천체의 한가운데 / 태양 내부 / 지구 내부 (정답 두 번째)",
    "confidence": "likely"
  },
  {
    "id": "mix-4",
    "where": "quiz[0].q",
    "severity": "low",
    "kind": "quiz",
    "quote": "빵 2 + 치즈 1 규칙에서 빵 <b>7</b>장, 치즈 <b>5</b>장이면 샌드위치는?",
    "problem": "숫자를 바꿔 한계 반응물이 빵으로 뒤바뀌는 좋은 전이 문항인데, 정답이 ②와 똑같이 3개라 계산하지 않고 앞의 답을 옮겨 적어도 맞습니다.",
    "fix": "빵 2 + 치즈 1 규칙에서 빵 <b>9</b>장, 치즈 <b>5</b>장이면 샌드위치는? (정답 4개, 선택지는 4개·5개·9개)",
    "confidence": "certain"
  },
  {
    "id": "courses.json",
    "where": "courses[0].minutes",
    "severity": "medium",
    "kind": "difficulty",
    "quote": "\"minutes\": 52",
    "problem": "코스 01의 minutes 가 52 인데 레슨 4편의 min 합은 14 + 16 + 12 + 18 = 60 입니다. 나머지 13개 코스는 전부 일치합니다.",
    "fix": "\"minutes\": 60",
    "confidence": "certain"
  },
  {
    "id": "throw-1",
    "where": "missions[9]",
    "severity": "medium",
    "kind": "difficulty",
    "quote": "각을 <b>15° · 30° · 45° · 60° · 75°</b>로 바꿔 가며 <b>범위</b>(날아간 거리)를 적어 보세요.",
    "problem": "각도 설정에서 발사, 착지 대기, 값 기록까지 한 번에 30~45초입니다. 이 미션과 다음 미션(공기저항 켜고 같은 각들 반복)이 합쳐 발사 10회를 요구해 6~8분이 듭니다. 레슨 배정이 14분이고 미션이 11개인데 이 둘이 절반을 먹습니다.",
    "fix": "각을 <b>30° · 45° · 60°</b>로 바꿔 가며 <b>범위</b>(날아간 거리)를 적어 보세요.",
    "confidence": "likely"
  },
  {
    "id": "throw-1",
    "where": "missions[10]",
    "severity": "low",
    "kind": "difficulty",
    "quote": "이제 <b>공기저항</b>을 켜고 같은 각들을 다시 해 보세요.",
    "problem": "앞 미션과 합쳐 발사 10회가 되어 배정 시간을 넘깁니다.",
    "fix": "이제 <b>공기저항</b>을 켜고 <b>30°</b>와 <b>60°</b>만 다시 해 보세요.",
    "confidence": "likely"
  },
  {
    "id": "static-3",
    "where": "missions[3]",
    "severity": "low",
    "kind": "wording",
    "quote": "이번엔 <b>전하 1</b>만 두 배로 올리세요.",
    "problem": "전하 1의 기본값이 −4 μC(음수)라 두 배로 올리세요가 −4 에서 −2 로 읽힐 수 있습니다.",
    "fix": "이번엔 <b>전하 1</b>의 크기만 두 배로 하세요(−4 → −8 μC).",
    "confidence": "likely"
  },
  {
    "id": "reactants-products-and-leftovers",
    "where": "controls[1].name",
    "severity": "low",
    "kind": "mission",
    "quote": "\"반응\" 전 (왼쪽 아래)",
    "problem": "반응 전 상자는 화면 왼쪽 가운데입니다(실측 x184~590, y135~476). 화면 아래에는 반응물 범례가 있습니다.",
    "fix": "\"반응\" 전 (왼쪽 가운데 큰 상자)",
    "confidence": "certain"
  },
  {
    "id": "reactants-products-and-leftovers",
    "where": "controls[2].name",
    "severity": "low",
    "kind": "mission",
    "quote": "\"반응\" 후 (오른쪽 아래)",
    "problem": "반응 후 상자는 화면 오른쪽 가운데입니다(실측 x685~1092, y135~476).",
    "fix": "\"반응\" 후 (오른쪽 가운데 큰 상자)",
    "confidence": "certain"
  },
  {
    "id": "quantum-measurement",
    "where": "controls[4].name",
    "severity": "low",
    "kind": "mission",
    "quote": "검측기 (오른쪽 · 위)",
    "problem": "검측기 두 개는 화면 가로 한가운데 쪽에 있습니다. 수직의 편광검측기가 위 가운데(x537~628), 수평의 편광검측기가 가운데(x612~703)입니다. 오른쪽은 아닙니다.",
    "fix": "검측기 (가운데 — 수직은 위, 수평은 아래)",
    "confidence": "certain"
  },
  {
    "id": "greenhouse-effect",
    "where": "gotchas[6]",
    "severity": "low",
    "kind": "wording",
    "quote": "<b>층 모형</b> 화면은 이 레슨의 범위를 넘습니다.",
    "problem": "5-1 표에 없는 새 오역입니다. 층 모형 화면의 surfaceAlbedo 가 표면 아베도로 나옵니다. 알베도의 오타입니다. 레슨 범위 밖이라 급하지는 않지만 표에 추가해 두시면 좋겠습니다.",
    "fix": "<b>층 모형</b> 화면은 이 레슨의 범위를 넘습니다. (그 화면의 <b>표면 아베도</b>는 <b>표면 알베도</b>의 오타입니다.)",
    "confidence": "certain"
  },
  {
    "id": "fourier-making-waves",
    "where": "gotchas[0]",
    "severity": "low",
    "kind": "wording",
    "quote": "표기가 일반적이지 않을 뿐 같은 것입니다.",
    "problem": "푸우리에는 표기 차이가 아니라 철자 오류입니다(푸리에). 또 제목 말고도 화면 안에 세 곳 더 나옵니다 — 푸우리에 급수(오른쪽 위), 푸우리에 요소, 푸우리에 요소의 진폭(파동 패킷 화면).",
    "fix": "<b>푸리에</b>의 오타이고, 화면 안 <b>푸우리에 급수</b>에도 같은 오타가 있습니다.",
    "confidence": "certain"
  },
  {
    "id": "coulombs-law",
    "where": "gotchas (새 항목 추가)",
    "severity": "low",
    "kind": "wording",
    "quote": "",
    "problem": "5-1 표에 없는 새 오역입니다. 힘 값 고르개의 소숫점 표시법은 소수점 표시법의 오타입니다(inverse-square-law-common 의 decimalNotation). 화면 오른쪽 아래에 나옵니다.",
    "fix": "힘 값의 <b>소숫점 표시법</b>은 <b>소수점</b>의 오타입니다.",
    "confidence": "certain"
  },
  {
    "id": "wave-on-a-string",
    "where": "gotchas (새 항목 추가)",
    "severity": "low",
    "kind": "wording",
    "quote": "",
    "problem": "5-1 표에 없는 새 오역입니다. damping 이 감폭으로 번역되어 있는데 한국 교육과정 용어는 감쇠입니다. wave-3 미션 2·12 가 화면을 따라 감폭을 그대로 쓰고 있어 방침으로는 맞지만, 뜻을 한 줄 달아 주면 좋겠습니다.",
    "fix": "<b>감폭</b>은 <b>감쇠</b>(흔들림이 잦아드는 정도)라는 뜻입니다.",
    "confidence": "certain"
  },
  {
    "id": "charges-and-fields",
    "where": "gotchas (새 항목 추가)",
    "severity": "low",
    "kind": "wording",
    "quote": "",
    "problem": "5-1 표에 없는 새 오역입니다. grid 가 망으로 번역되어 있습니다(격자/모눈). 사용법 조작[3]이 망은 바닥에 격자를 깝니다로 뜻을 이미 풀어 주고 있어 실사용에는 문제가 없지만, 오역 목록에는 넣어 두시면 좋겠습니다.",
    "fix": "<b>망</b>은 <b>격자</b>(Grid)의 번역입니다.",
    "confidence": "certain"
  }
]
```

---

## 12. 전수 확인 요약

| 항목 | 범위 | 결과 |
|---|---|---|
| ② 정답 인덱스 | 61 / 61 | **오류 0** |
| ⑦ 정답 인덱스 | 179 / 179 | **오류 0** |
| `explain.body` 사실 | 61 / 61 | 2건 (throw-1은 `real`) |
| `real` 수치·사실 | 61 / 61 | 2건 |
| 미션 | 600 / 600 (조작 이름·위치는 61종 실제 구동 대조) | 위치·조작 오류 7건, 화면에 없는 이름 11건 |
| 사용법 `controls` 외 | 430 / 430 | 위치·조작 오류 11건, 화면에 없는 이름 11건 |
| 상호 참조 | 30여 곳 전부 | 1건 |
| ②↔⑦ 중복 | 61 / 61 | 6건 + 낮은 순위 1건 |
| 코스 메타데이터 | 14 / 14 | 1건 |
| 5-1 오역 표 | 13 / 13 확인 | 전부 실재. 추가 6건 발견 |
| 5-2 제목 덮어쓰기 9종 | 9 / 9 | 전부 타당 |
| 5-3 영어 전용 6종 | 6 / 6 | 전부 실재 (번역 0 %) |

문제가 없어 보고하지 않은 곳이 대부분입니다. 특히 **정답 인덱스 240문항과 수치·연도·상수는
한 건도 틀리지 않았습니다.**
