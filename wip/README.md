# wip/ — 번역 작업 폴더

배포본에 실리지 않는 곳입니다. `tools/build.py` 는 `site/` 아래만 `dist/` 로
복사하므로, 여기 있는 파일은 어떤 경로로도 공개되지 않습니다.

> 의뢰서(`docs/I18N-BRIEF.md`)는 처음에 `site/content/_wip/` 를 권했지만,
> 그 자리는 빌드가 통째로 복사해 가는 곳이라 **번역 중인 원고가 그대로 배포**됩니다.
> 그래서 저장소 루트의 이 폴더로 옮겼습니다. (`site/` 안에 `_wip` 이 생기더라도
> 빌드가 걸러 내도록 안전장치를 하나 더 두었습니다.)

## 무엇이 어디에

```
wip/<lang>/lessons.json     작업 중인 원고. 61편이 다 차면 site/content/<lang>/ 로 옮기고 커밋
wip/<lang>/guides.json      작업 중인 사용법
wip/<lang>/courses.json     코스. 작아서 보통 한 번에 끝납니다
wip/labels/<lang>/          화면 글자 사전 — 생성물이라 git 에 넣지 않습니다
```

**반쯤 번역된 파일을 `site/content/<lang>/` 에 두지 마세요.** 폴백이 파일 단위라
안내 문구가 사라진 채 한국어와 그 언어가 섞여 나옵니다 (의뢰서 §1-4).

## 화면 글자 사전 쓰는 법

```bash
python tools/labels.py          # en · es · ja 전부 다시 뽑기
```

`wip/labels/<lang>/<repo>.json` 한 장에 세 가지가 들어 있습니다.

| 자리 | 뜻 |
|---|---|
| `opensIn` | 그 시뮬레이션이 실제로 열리는 언어. `en` 이면 그 언어 번역이 아예 없습니다 |
| `screen` | **화면에 실제로 찍히는 글자 전부.** 미션·사용법은 여기서 그대로 인용합니다 |
| `fallback` | `screen` 중 번역이 빠져 영어로 찍히는 자리. 번역이 있는 시뮬에도 있습니다 |
| `hidden` | `a11y.*` — 스크린리더 전용. **어느 언어로도 화면에 안 나옵니다. 인용 금지** |

`_shared.json` 은 joist · scenery-phet · sun · vegas 의 공통 화면 요소입니다
(되돌리기 버튼, 재생 속도, 화면 이름 따위).

## 검사

```bash
node tools/parity.mjs           # ko 와 뼈대가 같은지 (wip/ 도 같이 봅니다)
node tools/lint.mjs             # 태그 · 조판
```

`parity.mjs` 는 `wip/` 의 미완성 파일을 진행률로만 보고, 있는 부분은 전부 검사합니다.
작업 중에도 계속 돌리세요.
