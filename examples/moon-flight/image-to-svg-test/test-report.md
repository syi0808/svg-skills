# Moon Flight · Image to SVG 테스트

## 범위와 입력

- 실행일: 2026-08-28.
- 사용 스킬: `image-to-svg`.
- 변환 입력: 상위 폴더의 `preview.png` — 768×768 RGBA PNG.
- 입력 SHA-256: `0757842b718231ec76f14ae09d3edeec2e4f1f6bebc372de2ae8f2812c447321`.
- 변환 중 기존 `artwork.svg`, `normalized.svg`, 원본 `scene.json`은 읽거나 복사하지 않았다.
- PNG를 직접 보고 색상, 연결 영역의 경계, 일부 행의 픽셀 위치를 측정하여 도형을 작성했다.
- 기존 `preview-small.png`는 작성 이후 96×96 축소 결과를 비교하는 데만 사용했다.
- 같은 대화에서 수행한 수동 워크플로 테스트이며, 독립 평가자에 의한 블라인드 테스트는 아니다.

## 변환 방식과 산출물

자동 트레이서 없이 의미 있는 부품을 재구성했다. 원본의 1:1 비율, 여백,
13개 주요 색상, 모서리 투명도를 유지했다. 이미지 생성, 외부 API, 추가 설치는
사용하지 않았고 원본 PNG의 체크섬이 작업 후에도 동일함을 확인했다.

- [converted.svg](converted.svg): 3,827바이트, 그리기 요소 29개, 그룹 5개.
- [scene.json](scene.json): 로켓, 화염, 창, 달, 분화구, 별, 궤적의 편집용 ID와 관계.
- [preview.png](preview.png), [preview-small.png](preview-small.png): 768px / 96px 렌더링.
- [comparison.html](comparison.html): 원본과 결과를 나란히 배치한 로컬 비교 페이지.
- [validation.json](validation.json): 구조와 장면 매핑 검증 결과.
- [comparison.json](comparison.json), [comparison-small.json](comparison-small.json): 픽셀 비교 기록.

공개용 `validation.json`의 입력 경로는 개인 작업 경로 대신 프로젝트 루트 기준
상대 경로로 정리했다. 검증 결과와 측정값은 변경하지 않았다.

문자는 없는 이미지이므로 글꼴 의존성이 없다. 곡선은 짧은 Bézier 경로로,
원형 요소와 프레임은 기본 도형으로 유지했다. 달 뒤에 가려진 궤적 연결 형태는
원본에서 복구할 수 없으므로 보이는 위쪽 두 획과 아래쪽 점선을 별도 경로로 묶었다.

## 검증 결과

| 검사 | 결과 |
| --- | --- |
| SVG XML, namespace, viewBox, 경로와 참조 | 통과, 오류 0 / 경고 0 |
| 장면 ID, 태그, 부모 관계, 그리기 순서 | 통과 |
| 비트맵, data URL, 외부 참조, 스크립트, foreignObject | 없음 |
| 렌더링 | `rsvg-convert 2.59.2`, 768×768 / 96×96 성공 |
| 직접 시각 확인 | 원본과 결과 PNG를 전체 크기 및 96px에서 확인 |
| 투명 모서리 | 밝은/어두운 배경에서 결과 확인; 두 크기 모두 alpha RMSE 0 |
| 원본 보존 | 입력 PNG 체크섬 일치, 기존 산출물 수정 없음 |

첫 렌더에서 프레임 모서리 곡률, 달 음영 폭, 궤적 위치 차이를 발견했다.
모서리 반경을 72에서 67.2로 보정하고 음영 곡선 및 위쪽 궤적을 조정한 뒤
다시 검증·렌더링·시각 확인했다.

| 렌더 | 정규화 RGB RMSE | Alpha RMSE |
| --- | ---: | ---: |
| 첫 재구성, 768px | 0.035991 | 0.027294 |
| 모서리·음영 보정, 768px | 0.024282 | 0 |
| 최종, 768px | 0.023551 | 0 |
| 최종, 96px | 0.011209 | 0 |

RGB RMSE는 검정/흰색 배경 합성 비교 중 큰 값이다. 낮을수록 픽셀 차이가 작지만
유사도 백분율이나 의미적 정확도 점수는 아니다. 비교 도구의 `threshold`는
`null`이므로 `passed: true`는 별도의 충실도 합격 기준을 통과했다는 뜻이 아니다.
원본과 완전히 같은 이미지는 아니며 로켓 외곽과 음영, 달 음영 및 점선 배치에
작은 차이가 남아 있다. 96px에서는 주요 형태와 부품 구분이 유지된다.

로컬 HTML의 브라우저 열기가 URL 정책으로 차단되어 비교 페이지의 브라우저
표시는 검증하지 못했다. 우회하지 않고 PNG 파일을 직접 열어 시각 검토했으며,
밝은/어두운 배경 확인은 검증된 SVG를 로컬 렌더러로 각각 렌더링하여 수행했다.

## 재검증

프로젝트 루트에서 실행한다. 기존 PNG를 덮어쓰지 않도록 별도 임시 폴더를 사용한다.

```bash
CASE="examples/moon-flight/image-to-svg-test"
TOOLS="image-to-svg/scripts"
CHECK_DIR="$(mktemp -d)"
python3 "$TOOLS/validate_svg.py" "$CASE/converted.svg" --scene "$CASE/scene.json"
python3 "$TOOLS/render_svg.py" "$CASE/converted.svg" --output "$CHECK_DIR/preview.png" --width 768
python3 "$TOOLS/compare_render.py" examples/moon-flight/preview.png "$CHECK_DIR/preview.png"
python3 "$TOOLS/render_svg.py" "$CASE/converted.svg" --output "$CHECK_DIR/preview-small.png" --width 96
python3 "$TOOLS/compare_render.py" examples/moon-flight/preview-small.png "$CHECK_DIR/preview-small.png"
```

## 스킬에 대한 판단

이 평면 일러스트 사례에서는 원본 확인 → 의미 부품 재구성 → 검증 → 렌더링 비교
→ 집중 보정 흐름이 작동했다. 최초 변환 테스트는 기존 벡터 스킬의 도구를
재사용했다. 이후 스킬별 독립 실행 요구에 따라 같은 도구를 `image-to-svg/scripts`
내에 포함하고, 위 재검증 명령도 내장 도구를 사용하도록 변경했다.
사진, 복잡한 질감, 글자 포함 로고, 자동 트레이서는 이번에 테스트하지 않았으므로
일반적인 변환 품질까지 입증한 것은 아니다.

## 독립 실행 재검증

스킬별로 새 임시 폴더에 해당 스킬 하나만 복사하고, 작업 디렉터리와 `HOME`,
`CODEX_HOME`을 별도로 지정하여 실행했다. `PYTHONPATH`와 `PYTHONHOME`은 제거했고,
설치 디렉터리에 다른 스킬이나 공유 파일 링크가 없음을 확인했다.
이는 단독 설치 상태를 검사한 것이며 OS 수준의 파일 접근 격리는 아니다.

- `image-to-svg`: CLI 검사 28개 통과.
- `vector-illustration`: 같은 단독 설치 검사 28개 통과.
- 각 스킬의 문서 링크가 자체 폴더 안에서 해결되는지 확인했다.
- 검증·측정·정규화는 Python `-S`로 외부 패키지 없이 실행했다.
- 768px / 96px 렌더링이 기존 결과와 픽셀 단위로 일치했다(RGB 및 alpha RMSE 0).
- XML 정규화 후 렌더링도 정규화 전과 일치했다.
- 비트맵·외부 참조·잘못된 경로·잘못된 장면 매핑 거부를 확인했다.
- 출력 덮어쓰기 및 입력 파일 덮어쓰기 방지, 크기 불일치와 임계값 실패를 확인했다.

렌더링과 픽셀 비교는 설치된 `rsvg-convert` 및 Pillow를 사용했다. 스킬 간
의존성은 제거했지만 이 실행 환경 의존성까지 없앤 것은 아니다.
