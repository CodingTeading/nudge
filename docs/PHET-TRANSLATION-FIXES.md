# PhET 번역 수정 제출 목록

세 언어 원고를 쓰면서 찾은 **PhET 번역 자체의 오역**입니다. 지금은 우리 원고가
`gotchas` 에 "이건 ○○의 오역입니다" 한 줄을 달아 **우회**하고 있는데, 원본이 고쳐지면
그 줄들을 지울 수 있습니다.

- 작성일: 2026-08-23
- 근거: PhET 포크 `C:/projects/phet` 의 `babel/<repo>/<repo>-strings_<lang>.json`
- 대조: 같은 키의 영어 원문 `<repo>/<repo>-strings_en.json`
- 확인: 전부 실제 babel 값과 대조했습니다 (키 · 현재 값 일치)

| 언어 | 낱말 뜻 오역 | 문자열 파손 | 계 |
|---|---:|---:|---:|
| 한국어 | 22 | 12 | 34 |
| 일본어 | 15 | 0 | 15 |
| 스페인어 | 7 | 4 | 11 |
| | | | **60** |

**낱말 뜻 오역**은 아래 첫 묶음, **문자열 파손**(줄 겹침 · 안 지워진 영어 ·
붙여넣기 사고)은 "2차" 묶음입니다. 뒤엣것은 `python tools/label-quality.py` 가 찾습니다.

## 어디에 올리나

<https://phet.colorado.edu/translate> 의 번역 도구입니다. **PhET 계정이 필요합니다.**
GitHub PR 로는 받지 않습니다 — `phetsims/babel` 은 그 도구가 쓰는 저장소입니다.

도구는 **언어와 시뮬레이션을 하나씩 골라** 문자열 표를 보여 줍니다. 그래서 아래를
**시뮬레이션 단위로** 묶어 두었습니다. 한 페이지에서 고칠 것을 한 번에 끝내세요.

**딸린 저장소**(`solar-system-common` · `inverse-square-law-common` ·
`density-buoyancy-common`)의 문자열은 그 저장소를 쓰는 시뮬레이션 페이지에 함께
나옵니다. 한 번 고치면 그 저장소를 쓰는 **모든 시뮬레이션에 반영**됩니다.

> **자리표시자 없음.** 44건 가운데 `{{value}}` · `{0}` 같은 자리표시자가 든 문자열은
> 하나도 없습니다. 그대로 바꿔 넣으면 됩니다.

---

# 한국어 — 22곳

## A. `Custom` — 12곳 전부 오역입니다

같은 낱말이 12개 시뮬레이션에서 제각각으로, 그리고 **전부 틀리게** 옮겨져 있습니다.
`Custom` 은 "관례·관습·관행"(전해 내려오는 방식)이 아니라 **값을 직접 정한다**는 뜻입니다.
`고객`은 customer 와 혼동한 것이고, `관레`는 그 위에 오타까지 얹혔습니다.

일본어(`カスタム`)와 스페인어(`Personalizado`)는 전부 맞게 되어 있습니다 — **한국어만**
그렇습니다.

붙여 넣을 글은 12곳 모두 **`사용자 지정`** 으로 통일하기를 제안합니다.

| 시뮬레이션 (도구에서 열 페이지) | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Bending Light | `custom` | 관행 | `사용자 지정` |
| Collision Lab | `custom` | 관레 | `사용자 지정` |
| Density / Buoyancy ※ | `gravity.custom` | 관례 | `사용자 지정` |
| Density / Buoyancy ※ | `material.custom` | 관례 | `사용자 지정` |
| Energy Skate Park | `physicalControls.custom` | 관례 | `사용자 지정` |
| Least-Squares Regression | `custom.graphTitle` | 고객 | `사용자 지정` |
| Masses and Springs | `body.custom` | 관습 | `사용자 지정` |
| My Solar System | `mode.custom` | 관례 | `사용자 지정` |
| Pendulum Lab | `custom` | 관습 | `사용자 지정` |
| Projectile Motion | `custom` | 관습 | `사용자 지정` |
| Quantum Measurement | `custom` | 관례 | `사용자 지정` |
| Reactants, Products and Leftovers | `custom` | 관습 | `사용자 지정` |

※ `density-buoyancy-common` 은 딸린 저장소입니다. Density 나 Buoyancy 페이지를 열면
그 저장소의 문자열이 함께 나오고, 한 번 고치면 둘 다 반영됩니다.

## B. 시뮬레이션별 오역 — 10곳

### Models of the Hydrogen Atom

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Transitions | `transitions` | 트랜지스터 | `전이` |
| Radial Distance | `radialDistance` | 원주상 거리 | `반지름 방향 거리` |
| Excite Electron | `exciteElectron` | 여기 된 전자 | `전자 들뜨게 하기` |

`Transitions` 를 transistor(반도체 소자)로 읽었습니다. 전자가 에너지 준위 사이를
옮겨 가는 일을 뜻합니다. `Radial` 은 원주(둘레) 방향이 아니라 중심에서 바깥으로
재는 방향입니다. `Excite Electron` 은 누르는 단추라 명령형이어야 합니다.

### Fourier: Making Waves

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Fourier Components | `fourierComponents` | 푸우리에 요소 | `푸리에 성분` |
| Amplitudes of Fourier Components | `amplitudesOfFourierComponents` | 푸우리에 요소의 진폭 | `푸리에 성분의 진폭` |

인명 표기가 `푸우리에`로 되어 있습니다. 국립국어원 외래어 표기는 `푸리에`입니다.

### Ratio and Proportion

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Ratio and Proportion | `ratio-and-proportion.title` | 비울과 비 | `비와 비율` |

제목의 `비울`은 `비율`의 오타입니다.

### Greenhouse Effect

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Surface Albedo | `surfaceAlbedo` | 표면 아베도 | `표면 알베도` |

### Wave on a String

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Damping | `damping` | 감폭 | `감쇠` |

`damping` 의 표준 용어는 감쇠입니다.

### My Solar System — 딸린 저장소 `solar-system-common`

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Some force vectors are too small to display. | `offscaleMessage` | 읿부 힘벡터는 표시하기에 너무 작음 | `일부 힘 벡터는 너무 작아 표시할 수 없습니다.` |

`읿부`는 `일부`의 오타입니다. 이 저장소는 **My Solar System · Kepler's Laws ·
Gravity and Orbits** 가 함께 씁니다 — 한 번 고치면 셋 다 반영됩니다.

### Coulomb's Law — 딸린 저장소 `inverse-square-law-common`

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Decimal Notation | `decimalNotation` | 소숫점 표시법 | `소수점 표기법` |

`소숫점`은 `소수점`의 오기입니다. 이 저장소는 **Coulomb's Law · Gravity Force Lab** 이
함께 씁니다.

---

# 일본어 — 15곳

## Rutherford Scattering

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Electron Energy Level | `electronEnergyLevel` | 電気エネルギーレベル | `電子エネルギー準位` |

電**子**를 電**気**로 옮겼습니다. 전자와 전기는 다릅니다. `Level` 도 물리 용어로는
`準位` 입니다.

## Build a Nucleus

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Age of the Universe | `ageOfTheUniverse` | 地球の年齢 | `宇宙の年齢` |

반감기 눈금의 맨 오른쪽 값입니다. 우주의 나이(약 138억 년)를 지구의 나이(약 46억 년)로
옮겨 놓아 눈금의 크기 감각이 어긋납니다.

## Gas Properties

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Sample Period | `samplePeriod` | 仕事率 | `サンプル周期` |
| Scale | `scale` | 規模を表示 | `目盛りを表示` |

`Sample Period` 는 충돌 계수기가 **몇 초 동안 세는지**를 정하는 값인데 `仕事率`(일률,
power)로 옮겨져 있습니다. `Scale` 은 확산 화면의 **길이를 재는 자**입니다.

## Beer's Law Lab

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Copper(II) sulfate | `copperSulfate` | 硫化銅 | `硫酸銅(II)` |

**다른 물질입니다.** 硫化銅는 황화구리(copper sulfide)이고, 원문은 황산구리입니다.

## Reactants, Products and Leftovers

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Reactants | `reactants` | 反応 | `反応物` |
| Products | `products` | 生産 | `生成物` |

둘 다 **물질**의 이름인데 사건(反応)과 행위(生産)로 옮겨져 있습니다.

## Graphing Quadratics — 5곳

| 영어 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Axis of Symmetry | `axisOfSymmetry` | 対象軸 | `対称軸` |
| Focus | `focus` | 中心 | `焦点` |
| Focus & Directrix | `screen.focusAndDirectrix` | 中心と準線 | `焦点と準線` |
| Quadratic Terms | `quadraticTerms` | 二次方程式 | `二次の項` |
| Graphing Quadratics | `graphing-quadratics.title` | 二次方程式のグラフ | `二次関数のグラフ` |

`対象`과 `対称`은 발음이 같은 다른 낱말입니다. 포물선에 `中心`은 없습니다 —
`Focus` 는 초점입니다. 그리는 것은 방정식이 아니라 함수입니다.

## 제목이 원제와 무관하거나 서로 뒤바뀐 것 — 3곳

| 시뮬레이션 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Function Builder | `function-builder.title` | マジックスコープ | `関数を作ろう` |
| Build a Fraction | `build-a-fraction.title` | 分数の計算 | `分数を作ろう` |
| Fraction Matcher | `fraction-matcher.title` | 分数を作ろう | `分数のマッチング` |

`マジックスコープ`("매직 스코프")는 번역이 아니라 **제목과 무관한 다른 문자열**이
들어간 것으로 보입니다.

> **뒤의 둘은 같이 올리세요.** 지금 `Fraction Matcher` 가 쓰고 있는 이름
> (`分数を作ろう`)을 `Build a Fraction` 에 주는 것이라, 한쪽만 반영되면 **두 시뮬레이션이
> 같은 이름을 갖게 됩니다.** 둘 다 같은 회차에 제출하세요.

---

# 스페인어 — 7곳

전부 악센트·철자입니다. 뜻은 통하지만 학습자가 화면에서 글자를 찾을 때 걸립니다.

| 시뮬레이션 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Faraday's Electromagnetic Lab | `loopArea` | Área **se** la espira | `Área de la espira` |
| Coulomb's Law ※ | `scientificNotation` | Notación cientifica | `Notación científica` |
| Blackbody Spectrum | `graphValues` | valores del gr**à**fico | `valores del gráfico` |
| Graphing Quadratics | `vertex` | Vertice␣ | `Vértice` |
| Graphing Quadratics | `axisOfSymmetry` | Eje de Simetria␣ | `Eje de Simetría` |
| Center and Variability | `sortData` | Orde**nt**ar Datos | `Ordenar Datos` |
| Projectile Motion | `cannonball` | Bala de cañ**on** | `Bala de cañón` |

※ `scientificNotation` 은 딸린 저장소 `inverse-square-law-common` 입니다 —
Coulomb's Law · Gravity Force Lab 에 함께 반영됩니다.

**`␣` 는 줄 바꿈 없는 공백(U+00A0)입니다.** `vertex` 와 `axisOfSymmetry` 의 지금 값
끝에 붙어 있습니다. 위의 "붙여 넣을 글"에는 없으니 **그대로 붙여 넣으면 함께 지워집니다.**

`loopArea` 는 영어 원문이 `Loop Area:` 로 콜론까지 포함하는데, 한국어(`루프 영역`)도
콜론 없이 되어 있습니다. 기존 방식을 따라 콜론 없이 제안합니다.

---

# 2차 — 줄 나뉜 문자열·붙여넣기 사고에서 나온 것 (2026-08-23)

`python tools/label-quality.py` 로 61종 + 딸린 저장소를 훑어 나온 것입니다.
앞의 목록이 **낱말 뜻**의 오역이라면, 이쪽은 **문자열이 물리적으로 망가진** 것들입니다.

## 한국어 — 12곳 더

### 줄마다 따로 옮기다 낱말이 겹친 것 — 2곳

원문이 `Remove
Wall` 처럼 **두 줄짜리 단추**인데, 줄마다 따로 옮기면서 첫 줄에
전체 뜻을 넣고 둘째 줄에 또 옮겨 **같은 말이 두 번** 찍힙니다.

| 시뮬레이션 | key | 지금 (화면에 보이는 것) | 붙여 넣을 글 |
|---|---|---|---|
| Balloons and Static Electricity | `removeWall` | `벽 제거` ⏎ `제거` → **"벽 제거 제거"** | `벽` ⏎ `제거` |
| Balloons and Static Electricity | `addWall` | `벽 더하기` ⏎ `추가` → **"벽 더하기 추가"** | `벽` ⏎ `추가` |

일본어(`壁を非表示にする` 한 줄)와 스페인어(`Eliminar` ⏎ `muro`)는 맞게 되어 있습니다.

### 번역 도구의 화면 글자가 통째로 섞여 들어간 것 — 2곳

한국어 값 안에 번역 도구의 **`다른 초안 보기`** 가 그대로 붙어 있고, 같은 문장이
대여섯 번 되풀이됩니다. 원문 83자가 **471자**가 되었습니다.

| 시뮬레이션 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Center and Variability | `rangeDescription` | 같은 문장 ×6 + `다른 초안 보기` ×5 (471자) | `<strong>범위</strong>는 최소 데이터 포인트와 최대 데이터 포인트 사이의 거리입니다.` |
| Center and Variability | `iqrDescription` | 같은 문장 ×5 + `다른 초안 보기` ×4 (371자) | `<strong>사분위수 범위(IQR)</strong>는 데이터의 중간 50%입니다.` |

같은 실험의 `madDescription` 은 멀쩡합니다 — 그 한 줄을 본보기로 삼으면 됩니다.

### 영어가 지워지지 않고 남은 것 — 5곳

| 시뮬레이션 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Gas Properties | `oopsTemperatureOpen` | 이런! ⏎ **T**그릇이 열려 있으면 ⏎ 온도를 일정하게 유지하지 못합니다. | `이런!<br><br>그릇이 열려 있으면<br>온도를 일정하게 유지할 수 없습니다.` |
| Gas Properties | `oopsPressureLarge` | 이런! ⏎ 부피가 너무 크면 **constant.** ⏎ 압력을 … | `이런!<br><br>압력을 일정하게 유지할 수 없습니다.<br>부피가 너무 커집니다.` |
| Gas Properties | `oopsPressureSmall` | 이런! ⏎ 부피가 너무 **적으면 constant.** ⏎ 압력을 … | `이런!<br><br>압력을 일정하게 유지할 수 없습니다.<br>부피가 너무 작아집니다.` |
| Quantum Measurement | `propagationIntoPage` | 전파 ⏎ **(into page)** | `전파<br>(지면 안쪽으로)` |
| Fourier: Making Waves | `sawtoothWithCosines` | **cosines**는 … 톱날파도를 … **sines**로 바꾸시오. | `톱날파는 비대칭이라 코사인만으로는 만들 수 없습니다.<br>사인으로 바꿉니다.` |

`oopsPressureLarge` · `oopsPressureSmall` 은 영어가 남은 것에 더해 **인과가 뒤집혀**
있습니다. 원문은 "압력을 일정하게 유지할 수 없다 — 부피가 너무 커지기 때문"인데
한국어는 "부피가 너무 크면 압력을 유지 못한다"로 읽힙니다.
`적으면`도 부피에는 `작으면`이 맞습니다.

`sawtoothWithCosines` 의 `톱날파도`는 같은 실험의 파형 이름(`톱날파`)과도 어긋납니다.

### 그 밖 — 3곳

| 시뮬레이션 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Gas Properties | `oopsPressureEmpty` | … 유지 못합니다**..** (마침표 둘) | `이런!<br><br>그릇이 비어 있으면<br>압력을 일정하게 유지할 수 없습니다.` |
| Equality Explorer | `level1Description` | `<b>Level 1</b>  1단계 방정식 **equations**` | `<b>Level 1</b>  1단계 방정식` |
| Equality Explorer | `level2Description` | `<b>Level 2</b>  음의 계수를 포함한 1단계 방정식 **coefficients**` | `<b>Level 2</b>  음의 계수를 포함한 1단계 방정식` |

> `Level` 자체가 다섯 수준 모두 영어로 남아 있습니다(`레벨`이 아니라). 뜻은 통하므로
> 위에서는 **남은 찌꺼기만** 지우는 최소 수정으로 적었습니다.

## 스페인어 — 4곳 더

| 시뮬레이션 | key | 지금 | 붙여 넣을 글 |
|---|---|---|---|
| Faraday's Electromagnetic Lab | `currentSource` | `Fuente <br>` — **Current 가 통째로 빠짐** | `Fuente de<br>corriente` |
| Equality Explorer | `leftSideFull` | `!Oops!` … `esta lleno` | `¡Ups!<br><br>El lado izquierdo de la balanza está lleno.` |
| Equality Explorer | `rightSideFull` | `!Oops!` … `esta lleno` | `¡Ups!<br><br>El lado derecho de la balanza está lleno.` |
| Equality Explorer | `numberTooBig` | `!Oops!` + U+00A0 | `¡Ups!<br><br>Eso hará un número que es<br>muy grande para la simulación.<br><br>¡Intenta una operación diferente!` |

`currentSource` 가 가장 급합니다 — 화면에 **`Fuente`(원)** 만 찍혀 무엇의 원인지
알 수 없습니다. `!Oops!` 는 여는 부호가 `¡` 가 아니고, `esta` 는 `está` 의 악센트가
빠졌습니다. 같은 PhET 스페인어가 `gas-properties` 에서는 `¡Ups!` 를 쓰고 있으니
그쪽에 맞췄습니다.

## 일본어 — 없음

이 유형에서 일본어는 걸린 것이 없습니다. 두 줄짜리 단추를 한 줄로 합치는 쪽을
택해(`壁を非表示にする`) 겹침이 생기지 않았습니다.


---

# 작업 순서 — 열어야 할 페이지

도구는 한 번에 **한 시뮬레이션**만 보여 줍니다. 아래 순서대로 열면 딸린 저장소를
먼저 끝내게 되어 되돌아갈 일이 없습니다.

## 한국어 — 17개 페이지

| # | 열 페이지 | 고칠 것 |
|---:|---|---|
| 1 | **My Solar System** | `mode.custom` → 사용자 지정 · `offscaleMessage`(딸린 저장소) → 일부 힘 벡터는 너무 작아 표시할 수 없습니다. |
| 2 | **Coulomb's Law** | `decimalNotation`(딸린 저장소) → 소수점 표기법 |
| 3 | **Density** (또는 Buoyancy) | `gravity.custom` · `material.custom` → 사용자 지정 |
| 4 | Models of the Hydrogen Atom | `transitions` → 전이 · `radialDistance` → 반지름 방향 거리 · `exciteElectron` → 전자 들뜨게 하기 |
| 5 | Fourier: Making Waves | `fourierComponents` → 푸리에 성분 · `amplitudesOfFourierComponents` → 푸리에 성분의 진폭 |
| 6 | Ratio and Proportion | `ratio-and-proportion.title` → 비와 비율 |
| 7 | Greenhouse Effect | `surfaceAlbedo` → 표면 알베도 |
| 8 | Wave on a String | `damping` → 감쇠 |
| 9 | Energy Skate Park | `physicalControls.custom` → 사용자 지정 |
| 10 | Masses and Springs | `body.custom` → 사용자 지정 |
| 11 | Projectile Motion | `custom` → 사용자 지정 |
| 12 | Quantum Measurement | `custom` → 사용자 지정 |
| 13 | Reactants, Products and Leftovers | `custom` → 사용자 지정 |
| 14 | Bending Light | `custom` → 사용자 지정 |
| 15 | Collision Lab | `custom` → 사용자 지정 |
| 16 | Pendulum Lab | `custom` → 사용자 지정 |
| 17 | Least-Squares Regression | `custom.graphTitle` → 사용자 지정 |

1~3 번을 먼저 하는 이유: 딸린 저장소라 여러 시뮬레이션에 한꺼번에 반영됩니다.
4~8 번이 우리 사이트가 실제로 쓰는 실험이라 급하면 여기까지만 해도 됩니다.

## 일본어 — 9개 페이지

| # | 열 페이지 | 고칠 것 |
|---:|---|---|
| 1 | Graphing Quadratics | `axisOfSymmetry` → 対称軸 · `focus` → 焦点 · `screen.focusAndDirectrix` → 焦点と準線 · `quadraticTerms` → 二次の項 · `graphing-quadratics.title` → 二次関数のグラフ |
| 2 | Rutherford Scattering | `electronEnergyLevel` → 電子エネルギー準位 |
| 3 | Build a Nucleus | `ageOfTheUniverse` → 宇宙の年齢 |
| 4 | Gas Properties | `samplePeriod` → サンプル周期 · `scale` → 目盛りを表示 |
| 5 | Beer's Law Lab | `copperSulfate` → 硫酸銅(II) |
| 6 | Reactants, Products and Leftovers | `reactants` → 反応物 · `products` → 生成物 |
| 7 | **Build a Fraction** | `build-a-fraction.title` → 分数を作ろう |
| 8 | **Fraction Matcher** | `fraction-matcher.title` → 分数のマッチング |
| 9 | Function Builder | `function-builder.title` → 関数を作ろう |

**7 과 8 은 반드시 같이 제출하세요.** 8 이 지금 쓰는 이름을 7 에 넘기는 것이라,
한쪽만 반영되면 두 시뮬레이션이 같은 이름을 갖게 됩니다.

## 스페인어 — 6개 페이지

| # | 열 페이지 | 고칠 것 |
|---:|---|---|
| 1 | **Coulomb's Law** | `scientificNotation`(딸린 저장소) → Notación científica |
| 2 | Graphing Quadratics | `vertex` → Vértice · `axisOfSymmetry` → Eje de Simetría |
| 3 | Faraday's Electromagnetic Lab | `loopArea` → Área de la espira |
| 4 | Blackbody Spectrum | `graphValues` → valores del gráfico |
| 5 | Center and Variability | `sortData` → Ordenar Datos |
| 6 | Projectile Motion | `cannonball` → Bala de cañón |

---

# 붙여 넣을 글만 모은 것

키와 값만 탭으로 갈라 두었습니다. 도구에서 키로 찾아 값을 붙여 넣으세요.

## ko
```
bending-light                     custom                          사용자 지정
collision-lab                     custom                          사용자 지정
density-buoyancy-common           gravity.custom                  사용자 지정
density-buoyancy-common           material.custom                 사용자 지정
energy-skate-park                 physicalControls.custom         사용자 지정
least-squares-regression          custom.graphTitle               사용자 지정
masses-and-springs                body.custom                     사용자 지정
my-solar-system                   mode.custom                     사용자 지정
pendulum-lab                      custom                          사용자 지정
projectile-motion                 custom                          사용자 지정
quantum-measurement               custom                          사용자 지정
reactants-products-and-leftovers  custom                          사용자 지정
models-of-the-hydrogen-atom       transitions                     전이
models-of-the-hydrogen-atom       radialDistance                  반지름 방향 거리
models-of-the-hydrogen-atom       exciteElectron                  전자 들뜨게 하기
fourier-making-waves              fourierComponents               푸리에 성분
fourier-making-waves              amplitudesOfFourierComponents   푸리에 성분의 진폭
ratio-and-proportion              ratio-and-proportion.title      비와 비율
greenhouse-effect                 surfaceAlbedo                   표면 알베도
wave-on-a-string                  damping                         감쇠
solar-system-common               offscaleMessage                 일부 힘 벡터는 너무 작아 표시할 수 없습니다.
inverse-square-law-common         decimalNotation                 소수점 표기법
```

## ja
```
rutherford-scattering             electronEnergyLevel             電子エネルギー準位
build-a-nucleus                   ageOfTheUniverse                宇宙の年齢
gas-properties                    samplePeriod                    サンプル周期
gas-properties                    scale                           目盛りを表示
beers-law-lab                     copperSulfate                   硫酸銅(II)
reactants-products-and-leftovers  reactants                       反応物
reactants-products-and-leftovers  products                        生成物
graphing-quadratics               axisOfSymmetry                  対称軸
graphing-quadratics               focus                           焦点
graphing-quadratics               screen.focusAndDirectrix         焦点と準線
graphing-quadratics               quadraticTerms                  二次の項
graphing-quadratics               graphing-quadratics.title       二次関数のグラフ
function-builder                  function-builder.title          関数を作ろう
build-a-fraction                  build-a-fraction.title          分数を作ろう
fraction-matcher                  fraction-matcher.title          分数のマッチング
```

## es
```
faradays-electromagnetic-lab      loopArea                        Área de la espira
inverse-square-law-common         scientificNotation              Notación científica
blackbody-spectrum                graphValues                     valores del gráfico
graphing-quadratics               vertex                          Vértice
graphing-quadratics               axisOfSymmetry                  Eje de Simetría
center-and-variability            sortData                        Ordenar Datos
projectile-motion                 cannonball                      Bala de cañón
```

---

# 제출한 뒤 우리 쪽에서 할 일

1. `python tools/labels.py` — 화면 글자 사전을 다시 뽑습니다.
2. `node tools/lint.mjs` — [9] 검사가 **옛 오역을 인용한 원고 자리**를 잡아 줍니다.
3. 해당 사용법의 `gotchas` 에서 "이건 ○○의 오역입니다" 줄을 지웁니다.
4. `docs/KO-FINDINGS.md` · `docs/JA-FINDINGS.md` · `docs/ES-FINDINGS.md` 의 해당 줄에
   반영 날짜를 적습니다.

**`site/content/sim-titles.json` 을 잊지 마세요.** 한국어 `ratio-and-proportion` 은
지금 우리가 `비와 비율`로 덮어쓰고 있습니다. 원본이 고쳐지면 그 덮어쓰기를 **지워야**
합니다 — 안 그러면 나중에 PhET 쪽이 또 바뀌었을 때 우리 것이 계속 이깁니다.
일본어 제목 3종도 반영되면 `sim-titles.json` 의 `ja` 값을 새 제목으로 고쳐야 합니다.
