# 번역 중 발견한 한국어 원고 문제

영어판·일본어판을 옮기면서 한국어 원고에 남아 있는 것을 발견하면 여기 적습니다.
고치지는 않았습니다 — 한국어 원고는 배포 중이고, 손대려면 따로 판단이 필요합니다.
(딱 하나, **없는 화면을 설명하던 곳**만 세 언어에서 함께 뺐습니다 — §4 참고.)

`docs/I18N-BRIEF.md` §10-5 가 요청한 목록입니다.

---

## 1. 화면에 없는 이름(`a11y.*`)을 인용한 자리 — 영어판 작업에서 (코스 13 까지)

검수에서 미션 22곳을 고쳤지만, **사용법의 `tip` 과 `name`, 설명 본문, 그리고 미션
몇 곳에는 아직 남아 있습니다.** 전부 아이콘만 있거나 이름표가 없는 조작의 접근성
이름이라 어느 언어로도 화면에 그려지지 않습니다.

| 인용한 이름 | 나오는 자리 | 실제 |
|---|---|---|
| `Projected onto x y axes` | `lessons/throw-4/explain.body`, `guides/vector-addition/controls[4].tip` | `a11y.projectionRadioButton` — 성분 상자의 오른쪽 아래 **그림** 단추 |
| `Polar` | `guides/vector-addition/controls[6].tip` | a11y 전용. 오른쪽 아래 **부채꼴 그림** 단추 |
| `Double Well` · `Loop` | `guides/energy-skate-park/controls[3].tip` · `[4].tip` | `a11y.trackSelectionRadioButtonGroup.*` |
| `Clear Thermal Energy` | `guides/energy-skate-park/controls[9].name` | `a11y.…clearThermalButton` |
| `Erase · Pause · Step Forward` | `guides/projectile-motion/controls[9].name` | scenery-phet 의 `a11y.eraserButton` · `a11y.playPauseButton` · `a11y.stepForwardButton` |
| `Step Forward` | `lessons/wave-3/missions[5]`, `guides/wave-on-a-string/controls[7]`, `guides/masses-and-springs/controls[7]` | 위와 같음 |
| `Target Material` | `lessons/light-3/missions[0]` · `[7]`, `guides/photoelectric-effect/controls[2].name` · `steps[0]` | `a11y.materialsComboBox.accessibleName` — 콤보 상자에 **이름표가 없습니다** |
| `Circuit` | `guides/photoelectric-effect/controls[7].tip` | `a11y.representationRadioButtonGroup.circuitRadioButton` |
| `Pause · Step Forward` | `guides/photoelectric-effect/controls[8].name` | 위의 scenery-phet a11y |
| `Detection Mode` · `Particle Type` | `guides/quantum-wave-interference/controls[3].name` · `[4].name` | `a11y.detectionModeRadioButtons` 등. 라디오 묶음에 **제목이 없습니다** |
| `Clear Hits` · `Take Snapshot` | `guides/quantum-wave-interference/controls[7].name` | `a11y.detectorScreenButtons.*` |
| `Fast` | `guides/quantum-wave-interference/controls[8].name` · `steps[4]` | 화면 라벨은 `Particle Speed` 뿐입니다 |
| `Pause · Reset All` | `guides/natural-selection/controls[7].name` | scenery-phet a11y. 되돌리기는 오른쪽 아래 **노란 원**입니다 |
| `Heads` · `Tails` | `lessons/quantum-1/missions[1]`, `guides/quantum-coin-toss/controls[0].desc` | `a11y.coinsScreen.coinStates.*` — 동전 면은 **그림**입니다 |
| `Start Measurement` | `lessons/quantum-1/missions[8]` | `a11y.coinsScreen.startMeasurement`. 단추에 찍히는 글자는 **`Start`** 뿐입니다 |
| `Potential` | `guides/quantum-bound-states/controls[0].name` · `steps[0]` · `steps[6]` | 가두는 모양 콤보 상자에 **제목이 없습니다** |
| `Step Forward` | `guides/quantum-measurement/controls[7].name` | scenery-phet a11y |

`photoelectric-effect` 와 `quantum-wave-interference` 는 한국어 번역이 없어 화면이
영어로 나옵니다. 그래서 한국어 원고가 영어 이름을 인용하는 것 자체는 맞습니다 —
문제는 **인용한 영어 이름 중 일부가 화면에 없는 이름**이라는 점입니다.

같은 문서가 다른 자리에서는 "글자 없이 그림으로 구별합니다"라고 써 두어(예:
`guides/photoelectric-effect/controls[7].name`), **한 항목 안에서 앞뒤가 어긋나는
곳도 있습니다** — 이름표에는 "글자 없이 그림 두 개"라고 해 놓고 팁에서 `Circuit`
이라고 부릅니다.

영어판은 전부 그림이나 위치로 가리키게 썼습니다.

## 1-2. 오역된 화면 이름을 그대로 믿고 설명이 어긋난 곳 — 1곳

`guides/mean-share-and-balance/screens[1]`

PhET 한국어가 `Distribute` 를 **`분산`** 으로 옮겼습니다. 통계의 분산(variance)과
같은 낱말이라, 한국어 원고가 그 화면을 **"값들이 평균에서 얼마나 떨어져 있는지
봅니다"** 라고 설명하고 있습니다. 실제로 그 화면이 하는 일은 **초코바를 사람들에게
나누어 1인당 평균을 보는 것**입니다 — 분산과 무관합니다.

a11y 인용과 달리 이건 **내용이 틀린 것**이라 한국어 사용자가 실제로 오해합니다.
영어판에는 옮기지 않고 화면이 하는 일을 그대로 썼습니다.


## 1-3. 화면에 없는 이름 — 일본어 작업에서 추가로 찾은 것 17곳

61종 전체를 기계로 훑었습니다. 방법은 이렇습니다 — 한국어 원고의
`controls[].name` 과 `<b>…</b>` 인용에서 **영어처럼 보이는 토막**을 뽑아,
`wip/labels/en/<repo>.json` 의 `screen`·`common`(그리고 `_shared.json`)에
그 글자가 실제로 있는지 대조했습니다. 화학식·수식 같은 우리 표기는 걸러 냈습니다.

§1 의 표에 없던 것만 적습니다.

| 시뮬레이션 | 인용한 이름 | 나오는 자리 | 실제 |
|---|---|---|---|
| `gravity-and-orbits` | `Zoom` | `controls[6].name` | `a11y.zoom` — 확대·축소는 **돋보기 아이콘** |
| `states-of-matter` | `Step Forward` | `controls[7].name` | scenery-phet `a11y.stepForwardButton` |
| `greenhouse-effect` | `Step Forward` | `controls[8].name` | 위와 같음 |
| `quantum-bound-states` | `Restart` | `controls[7].name` | `a11y.restartButton.*` |
| `mean-share-and-balance` | `Info` | `controls[7].name` | `a11y.info` — **i 아이콘** |
| `membrane-transport` | `Erase All Solutes` | `controls[5].name` · `steps[2]` · `gotchas[5]` | `a11y.eraseSolutesButton.accessibleName` |
| `unit-rates` | `Erase` | `controls[5].name` | scenery-phet `a11y.eraserButton` — **지우개 아이콘** |
| `equality-explorer` | `Erase` | `controls[5].name` | 위와 같음 |
| `function-builder` | `Erase` | `controls[3].name` | 위와 같음 |
| `function-builder` | `Page 1 · 2 · 3` | `controls[1].name` | 문자열 자체가 없습니다 — 회전 목록의 **점 표시**입니다 |
| `center-and-variability` | `Erase Current Data` | `controls[7].name` | `a11y.eraseButton.accessibleName` |
| `number-pairs` | `Total Number` | `controls[0].name`, `lessons/num-3/missions[1]` | 화면에 찍히는 건 **`Total`** 뿐입니다 |
| `number-pairs` | `Swap Addends` | `controls[3].name`, `lessons/num-3/missions[5]` | `a11y.controls.commutativeButton.accessibleName` |
| `number-pairs` | `Hide Left / Right Counting Area` | `controls[4].name`, `lessons/num-3/missions[8]` | `a11y.controls.addendVisibleButton.accessibleNameOnPattern` |
| `number-pairs` | `Organize` | `controls[5].name` | `a11y.controls.tenFrameButton.accessibleName` |
| `number-pairs` | `No Voice Found` | `controls[8].tip` | `a11y.controls.speechSynthesis.noVoiceAccessibleName` |
| `quantum-coin-toss` | `Coin Bias / State` | `controls[1].name` | 화면은 **`Coin Bias (State)`** — 슬래시가 아니라 괄호입니다 |

`number-pairs` 는 **한 실험에서만 다섯 곳**입니다. 이 실험은 조작 단추가 거의 다
아이콘이라, 이름을 붙이려면 `a11y` 를 볼 수밖에 없었던 것으로 보입니다.

`Erase` 계열이 네 곳입니다(§1 의 `projectile-motion` 까지 하면 다섯). scenery-phet 의
지우개 단추는 어느 실험에서나 **글자 없는 아이콘**이라, 한 번 정해 두면 다 같이
고칠 수 있습니다.

일본어판은 전부 그림이나 위치로 가리키게 썼습니다 — 예: "지우개 그림 단추".

## 2. 번역이 "있는" 시뮬레이션도 일부는 영어로 나옵니다

`sim-locales.json` 은 파일이 있는지만 봅니다. 파일이 있어도 문자열 단위로 빠진 것은
영어로 그려집니다.

| 언어 | 통째로 영어 | 번역이 있는데 일부만 영어 |
|---|---:|---:|
| ko | 6 / 61 | (미측정 — `tools/labels.py` 에 ko 를 더하면 나옵니다) |
| es | 5 / 61 | 12 |
| ja | 18 / 61 | 33 |

한국어판에도 같은 틈이 있을 가능성이 높습니다. 확인하려면 `tools/labels.py` 의
`LANGS` 에 `'ko'` 를 더해 돌리고 `fallback` 이 큰 시뮬레이션부터 보세요.

## 3. 공유 이미지 서체 — 일본어 ✅ 해결

Pretendard 에 한자가 없어 일본어 카드가 두부(□)로 찍히던 문제입니다.
Noto Sans JP(OFL)를 `tools/fonts/` 에 넣고 `make-og.py` 의 서체 사슬에 이었습니다.
`python tools/font-check.py` 가 네 언어 모두 통과합니다.

---

## 4. 없는 화면을 설명하던 곳 — 2곳 (고쳤습니다)

일본어 작업에서 발견한 것으로, 이것만은 **세 언어(ko · en · es)에서 함께 뺐습니다.**
번역 문제가 아니라 사실이 틀린 것이라 그대로 둘 수 없었습니다.

| 시뮬레이션 | 원고가 적어 둔 화면 | 실제 |
|---|---|---|
| `number-play` | 10 · 20 · 게임 · **실험** | Ten · Twenty · Game (셋) |
| `number-compare` | 비교하기 · **실험** | Compare (하나) |

61종 전수로 화면 수를 대조했고 나머지는 맞습니다. 반대로 **있는 화면을 원고가
빼먹은 것**이 3종 있는데, 레슨에서 안 쓰는 화면이라 그대로 두었습니다 —
`projectile-motion`(Stats) · `greenhouse-effect`(Micro) · `quantum-bound-states`(Superposition).
