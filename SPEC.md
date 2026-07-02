# Claude 연동 가이드 포탈 — 설계 스펙 (2026-07-02)

분리돼 있던 Claude 연동 전파교육 가이드들을 하나의 정보 포탈로 통합한다.

## 확정 결정
- **구조**: 하이브리드 = 공유 셸(디자인시스템·네비) + 토픽별 가이드 모듈
- **빌드**: 정적 멀티페이지 + 공유 CSS (빌드 파이프라인 없음, GitHub Pages)
- **v1 범위(C안)**: 셸 + 허브 + 가이드 1개(디스코드) 완전 이식 → 패턴 확정 후 나머지 점진 추가
- **호스팅**: GitHub Pages 공개, repo `jakeon32/claude-guide-portal`
- **로컬 소스**: `C:\ComfyUI_windows_portable\claude-guide-portal\`

## 제약 (제이크 지시)
- **기본 테마 = 라이트.** 라이트/다크 토글 지원(허브 포함), 최초 진입 라이트.
- **아이브로우(eyebrow/kicker 라벨) 금지** — 제목 그룹은 heading + sub만.
- **이모지 전면 금지** — UI·콘텐츠 어디에도 이모지 안 씀. 아이콘은 인라인 SVG 또는 ComfyUI 이미지.
- **필요 이미지는 ComfyUI 생성**(ZIT `z_image_turbo` 또는 Krea 2.0). 스톡/외부/이모지 대체 금지.
- 진행하며 반복 개선.

## 구조
```
claude-guide-portal/
  index.html          포탈 허브 (히어로 + 가이드 카드 그리드)
  shared.css          공유 디자인시스템 (토큰 + 컴포넌트)
  shared.js           테마 토글 · 네비 · 진행 표시
  guides/
    discord.html      ① 템플릿 모듈 (기존 8단계 콘텐츠 이식)
    (remote / vibe / figma .html — 이후 추가)
  assets/             ComfyUI 생성 이미지
  .nojekyll
  SPEC.md
```

## 디자인 시스템 (shared.css)
- 기존 가이드에서 추출한 공통 토큰: 폰트(Space Grotesk / Pretendard / JetBrains Mono), `--bg/surface/text/muted/border`, space·radius·text 스케일, 라이트/다크(`[data-theme]`).
- **기본값 라이트**: `<html>` 초기 `data-theme="light"`, 토글로 dark. localStorage 저장.
- **토픽 액센트 스와핑**: `[data-topic="discord"]` → Claude 테라코타 + Discord blurple, `="remote"` → Tailscale/Sunshine/Moonlight, `="vibe"`, `="figma"` … 각 페이지가 자기 액센트만 지정. 허브 셸은 중립(Claude 테라코타).
- 공통 컴포넌트: 상단 고정 네비, 푸터, 가이드카드, 스텝, 콜아웃, 코드블록.
- **디자인 원칙 적용**(`design-principles.md`): 반복 카드=그림자 대신 border / 제목그룹 근접성(위 64·아래 32) / 섹션 패딩 규칙 / 제목↔단순텍스트 경계 구분선 / 그림자는 떠야하는 요소만.
- **한글 안전장치**: 모든 제목 `word-break:keep-all` + `text-wrap:balance` (+`overflow-wrap:anywhere`).
- **아이콘**: 이모지 금지 → 인라인 SVG 또는 ComfyUI 이미지.

## 포탈 허브 (index.html)
- 히어로: 타이틀 "Claude 연동 가이드" + 한 줄 설명(전파교육 포탈), 테마 토글. (아이브로우 없음)
- 가이드 카드 그리드: 디스코드 · 원격제어 · 바이브코딩 3장 + "Figma(예정)" 플레이스홀더. 카드 = 토픽 액센트 + 아이콘(SVG/ComfyUI) + 제목 + 1줄 설명 + "가이드 열기". 반복 카드라 border 구분(그림자 X).
- 상단 고정 네비(포탈명 + 가이드 바로가기 + 테마토글).

## 템플릿 모듈 (guides/discord.html)
- 기존 `guides\claude-discord-연동가이드.html` 8단계 콘텐츠를 셸(shared.css + 네비 + `data-topic="discord"`)로 이식.
- 상단 "← 포탈" 복귀 링크 + 스크롤 진행 표시. 이 모듈로 패턴 확정 → 나머지 복제.

## 이미지 (ComfyUI)
- 허브 히어로/카드 일러스트 등 필요 이미지는 ComfyUI(ZIT 또는 Krea2)로 생성 → `assets/`.
- 기존 원격제어 가이드의 `generate_guide_images.py` 패턴 참고.

## 배포
- 새 repo `jakeon32/claude-guide-portal` 생성 → `.nojekyll` → jakeon32 계정 push → GitHub Pages.
- 기존 3개 사이트는 당분간 유지, 이식 완료분부터 포탈 내부로 대체.

## v1 완료 기준
- 라이트 기본 테마 허브 + shared.css + 디스코드 모듈이 로컬에서 정상 렌더(테마 토글·네비·카드 동작), GitHub Pages 배포 후 접속 확인.
- 이후: remote / vibe / figma 모듈을 같은 틀로 하나씩 추가(제이크와 반복 개선).
