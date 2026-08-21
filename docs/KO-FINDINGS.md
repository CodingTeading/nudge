# 번역 중 발견한 한국어 원고 문제

영어판을 옮기면서 한국어 원고에 남아 있는 것을 발견하면 여기 적습니다.
고치지는 않았습니다 — 한국어 원고는 배포 중이고, 손대려면 따로 판단이 필요합니다.

`docs/I18N-BRIEF.md` §10-5 가 요청한 목록입니다.

---

## 1. 화면에 없는 이름(`a11y.*`)을 인용한 자리 — 10곳

검수에서 미션 22곳을 고쳤지만, **사용법의 `tip` 과 `name`, 설명 본문, 그리고 미션
한 곳에는 아직 남아 있습니다.** `Step Forward` 는 세 곳에 반복해 나옵니다. 전부 아이콘만 있는 단추의 접근성 이름이라 어느 언어로도 화면에
그려지지 않습니다.

| 자리 | 인용한 이름 | 실제 |
|---|---|---|
| `lessons/throw-4/explain.body` | `Projected onto x y axes` | `a11y.projectionRadioButton.accessibleName` — 성분 상자의 오른쪽 아래 **그림** 단추 |
| `guides/vector-addition/controls[4].tip` | `Projected onto x y axes` | 위와 같음 |
| `guides/vector-addition/controls[6].tip` | `Polar` | a11y 전용. 오른쪽 아래 **부채꼴 그림** 단추 |
| `guides/energy-skate-park/controls[3].tip` | `Double Well` | `a11y.trackSelectionRadioButtonGroup.doubleWellRadioButton.accessibleName` |
| `guides/energy-skate-park/controls[4].tip` | `Loop` | 위와 같은 그룹의 a11y 이름 |
| `guides/energy-skate-park/controls[9].name` | `Clear Thermal Energy` | `a11y.energyBarGraphAccordionBox.clearThermalButton.accessibleName` |
| `guides/projectile-motion/controls[9].name` | `Erase · Pause · Step Forward` | scenery-phet 의 `a11y.eraserButton` · `a11y.playPauseButton` · `a11y.stepForwardButton` |
| `lessons/wave-3/missions[5]` | `Step Forward` | `a11y.stepForwardButton.accessibleName` — 일시정지 옆 **아이콘** |
| `guides/wave-on-a-string/controls[7].name` · `.tip` | `Step Forward` | 위와 같음 |
| `guides/masses-and-springs/controls[7].name` | `Step Forward` | 위와 같음 |

같은 자리에서 한국어 원고가 이미 "글자 없이 그림으로 구별합니다"라고 써 둔 곳도
많습니다(예: `guides/vector-addition/gotchas[0]`). 그래서 **한 문서 안에서 앞뒤가
어긋납니다** — 단추에 글자가 없다고 해 놓고 그 단추를 영어 이름으로 부릅니다.

영어판은 전부 그림으로 가리키게 썼습니다.

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

## 3. 공유 이미지 서체 — 일본어

`tools/font-check.py` 결과, Pretendard 에 한자가 없습니다(표본 757자 중 491자).
일본어 OG 를 굽기 전에 CJK 서체를 얹어야 합니다. 영어·스페인어는 문제 없습니다.
