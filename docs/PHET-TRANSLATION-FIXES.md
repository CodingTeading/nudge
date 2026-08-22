# PhET 번역 수정 제출 목록

세 언어 원고를 쓰면서 찾은 **PhET 번역 자체의 오역**입니다. 지금은 우리 원고가
`gotchas` 에 "이건 ○○의 오역입니다" 한 줄을 달아 **우회**하고 있는데, 원본이 고쳐지면
그 줄들을 지울 수 있습니다.

- 작성일: 2026-08-23
- 근거: PhET 포크 `C:/projects/phet` 의 `babel/<repo>/<repo>-strings_<lang>.json`
- 대조: 같은 키의 영어 원문 `<repo>/<repo>-strings_en.json`

## 어디에 올리나

PhET 번역은 <https://phet.colorado.edu/translate> 의 번역 도구로 제출합니다.
**PhET 계정이 필요하고, 언어별 담당자가 검토한 뒤 반영됩니다.** GitHub PR 로는
받지 않습니다 (`phetsims/babel` 은 도구가 쓰는 저장소입니다).

아래 표의 **key** 를 번역 도구에서 찾아 **제안** 값으로 바꾸면 됩니다.
같은 문자열이 여러 시뮬레이션에 나오는 경우, 키가 딸린 저장소(`inverse-square-law-common`
같은)에 있으면 **그 저장소 하나만 고치면 전부 따라옵니다.**

---

## 한국어 — 11곳

| 저장소 | key | 지금 | 제안 | 왜 |
|---|---|---|---|---|
| `models-of-the-hydrogen-atom` | `transitions` | 트랜지스터 | **전이** | Transitions 를 transistor 로 읽었습니다. 반도체 소자와 무관합니다 |
| `models-of-the-hydrogen-atom` | `radialDistance` | 원주상 거리 | **반지름 방향 거리** | Radial 은 '원주상'이 아니라 중심에서 바깥으로 재는 방향입니다 |
| `models-of-the-hydrogen-atom` | `exciteElectron` | 여기 된 전자 | **전자 들뜨게 하기** | 원문이 명령형(Excite)인데 과거분사로 옮겼습니다 |
| `fourier-making-waves` | `fourierComponents` | 푸우리에 요소 | **푸리에 성분** | 인명 표기 오류 (Fourier → 푸리에) |
| `fourier-making-waves` | `amplitudesOfFourierComponents` | 푸우리에 요소의 진폭 | **푸리에 성분의 진폭** | 위와 같음 |
| `ratio-and-proportion` | `ratio-and-proportion.title` | 비울과 비 | **비와 비율** | '비율'의 오타 |
| `greenhouse-effect` | `surfaceAlbedo` | 표면 아베도 | **표면 알베도** | albedo 표기 오류 |
| `quantum-measurement` | `custom` | 관례 | **직접 정하기** | Custom 을 custom(관례)으로 읽었습니다. 값을 직접 넣는 자리입니다 |
| `wave-on-a-string` | `damping` | 감폭 | **감쇠** | damping 의 표준 용어는 감쇠입니다 |
| `solar-system-common` | `offscaleMessage` | 읿부 힘벡터는 표시하기에 너무 작음 | **일부 힘 벡터는 너무 작아 표시할 수 없습니다** | '읿부'는 '일부'의 오타 |
| `inverse-square-law-common` | `decimalNotation` | 소숫점 표시법 | **소수점 표기법** | '소숫점'은 '소수점'의 오기 |

> 뒤의 둘은 **딸린 저장소**라 여러 시뮬레이션에 한꺼번에 반영됩니다 —
> `solar-system-common` 은 `my-solar-system` · `keplers-laws` · `gravity-and-orbits`,
> `inverse-square-law-common` 은 `coulombs-law` · `gravity-force-lab`.

---

## 일본어 — 12곳

| 저장소 | key | 지금 | 제안 | 왜 |
|---|---|---|---|---|
| `rutherford-scattering` | `electronEnergyLevel` | 電気エネルギーレベル | **電子エネルギー準位** | 電**子**를 電**気**로. 전자와 전기는 다릅니다 |
| `build-a-nucleus` | `ageOfTheUniverse` | 地球の年齢 | **宇宙の年齢** | 우주의 나이를 지구의 나이로 옮겼습니다 |
| `gas-properties` | `samplePeriod` | 仕事率 | **サンプル周期** | Sample Period 를 '일률(power)'로. 충돌을 세는 시간 길이입니다 |
| `gas-properties` | `scale` | 規模を表示 | **目盛りを表示** | Scale 이 '규모'가 아니라 길이를 재는 자입니다 |
| `beers-law-lab` | `copperSulfate` | 硫化銅 | **硫酸銅(II)** | 원문은 Copper(II) sulfate — 황산구리입니다. 硫化銅은 황화구리로 다른 물질입니다 |
| `reactants-products-and-leftovers` | `reactants` | 反応 | **反応物** | Reactants 는 반응이 아니라 반응하는 물질입니다 |
| `reactants-products-and-leftovers` | `products` | 生産 | **生成物** | Products 는 생산이 아니라 생겨난 물질입니다 |
| `graphing-quadratics` | `axisOfSymmetry` | 対象軸 | **対称軸** | 同音 오타 (対象 ↔ 対称) |
| `graphing-quadratics` | `focus` | 中心 | **焦点** | 포물선에 중심은 없습니다. Focus 는 초점입니다 |
| `graphing-quadratics` | `screen.focusAndDirectrix` | 中心と準線 | **焦点と準線** | 위와 같음 |
| `graphing-quadratics` | `quadraticTerms` | 二次方程式 | **二次の項** | Quadratic Terms 는 식 전체가 아니라 항입니다 |
| `graphing-quadratics` | `graphing-quadratics.title` | 二次方程式のグラフ | **二次関数のグラフ** | 그리는 것은 방정식이 아니라 함수입니다 |

### 제목이 원제와 어긋나는 것 — 2곳

이 둘은 **서로의 뜻을 가리키고** 있어 같은 코스 안에서 학습자가 혼동합니다.

| 저장소 | key | 지금 | 제안 |
|---|---|---|---|
| `function-builder` | `function-builder.title` | マジックスコープ | **関数を作ろう** |
| `build-a-fraction` | `build-a-fraction.title` | 分数の計算 | **分数を作ろう** |
| `fraction-matcher` | `fraction-matcher.title` | 分数を作ろう | **分数のマッチング** |

> `function-builder` 의 `マジックスコープ`("매직 스코프")는 번역이라기보다 **제목과
> 무관한 다른 문자열**이 들어간 것으로 보입니다.

---

## 스페인어 — 7곳

전부 악센트·철자 오류입니다. 뜻은 통하지만 학습자가 화면에서 글자를 찾을 때 걸립니다.

| 저장소 | key | 지금 | 제안 | 왜 |
|---|---|---|---|---|
| `faradays-electromagnetic-lab` | `loopArea` | Área **se** la espira | Área **de** la espira | `de` 가 `se` 로 |
| `inverse-square-law-common` | `scientificNotation` | Notación cientifica | Notación cient**í**fica | í 빠짐 |
| `blackbody-spectrum` | `graphValues` | valores del gr**à**fico | valores del gr**á**fico | 악센트 방향 반대 |
| `graphing-quadratics` | `vertex` | Vertice | V**é**rtice | é 빠짐 |
| `graphing-quadratics` | `axisOfSymmetry` | Eje de Simetria | Eje de Simetr**í**a | í 빠짐 |
| `center-and-variability` | `sortData` | Orde**nt**ar Datos | Orde**n**ar Datos | t 가 하나 더 |
| `projectile-motion` | `cannonball` | Bala de cañ**on** | Bala de cañ**ón** | ó 빠짐 |

`graphing-quadratics` 의 스페인어 `vertex` · `axisOfSymmetry` 값 끝에는 **줄 바꿈 없는
공백(U+00A0)** 도 붙어 있습니다. 함께 지우면 좋습니다.

---

## 제출한 뒤 우리 쪽에서 할 일

반영이 확인되면:

1. `python tools/labels.py` 를 다시 돌려 사전을 갱신합니다.
2. `node tools/lint.mjs` 의 [9] 검사가 바뀐 글자를 잡아 줍니다 — 원고가 옛 오역을
   인용하고 있으면 그때 걸립니다.
3. 해당 사용법의 `gotchas` 에서 "이건 ○○의 오역입니다" 줄을 지웁니다.
4. `docs/KO-FINDINGS.md` · `docs/JA-FINDINGS.md` · `docs/ES-FINDINGS.md` 의 해당 줄에
   반영 날짜를 적습니다.

한국어 `ratio-and-proportion.title` 처럼 `site/content/sim-titles.json` 이 덮어쓰고 있는
것은, 원본이 고쳐지면 **덮어쓰기를 지워야** 합니다. 안 그러면 옛 교정본이 계속 나갑니다.
