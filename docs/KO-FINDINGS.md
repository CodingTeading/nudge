# 번역 중 발견한 한국어 원고 문제

영어판을 옮기면서 한국어 원고에 남아 있는 것을 발견하면 여기 적습니다.
고치지는 않았습니다 — 한국어 원고는 배포 중이고, 손대려면 따로 판단이 필요합니다.

`docs/I18N-BRIEF.md` §10-5 가 요청한 목록입니다.

---

## 1. 화면에 없는 이름(`a11y.*`)을 인용한 자리 — 20곳 (코스 04 까지)

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

`photoelectric-effect` 와 `quantum-wave-interference` 는 한국어 번역이 없어 화면이
영어로 나옵니다. 그래서 한국어 원고가 영어 이름을 인용하는 것 자체는 맞습니다 —
문제는 **인용한 영어 이름 중 일부가 화면에 없는 이름**이라는 점입니다.

같은 문서가 다른 자리에서는 "글자 없이 그림으로 구별합니다"라고 써 두어(예:
`guides/photoelectric-effect/controls[7].name`), **한 항목 안에서 앞뒤가 어긋나는
곳도 있습니다** — 이름표에는 "글자 없이 그림 두 개"라고 해 놓고 팁에서 `Circuit`
이라고 부릅니다.

영어판은 전부 그림이나 위치로 가리키게 썼습니다.

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
