# 문서 조직 규약 (Doc Organization Convention)

생태계 전체 문서 정리의 기준. 신규 문서 작성·정리·자동화 잡 생성 시 따를 것.

---

## 1. Canonical 디자인 시스템

- **단일 출처**: `project-oxi/.github/DESIGN.md` (v1.0).
- 이유: `.github/`는 GitHub 원격에 푸시되어 org-profile/CONTRIBUTING 등이 참조하므로 GitHub-facing canonical이 자연스럽다.
- **레포별 DESIGN.md 전문 카피 금지** — 드리프트 위험. 대신 `DESIGN-REF.md` 포인터 사용.

## 2. DESIGN-REF.md 포인터 (레포별)

각 레포에 `DESIGN-REF.md` 배치 (루트 또는 `docs/`). 형식:
- 제목 + `> Pointer file` 표시
- canonical 경로 + 버전/날짜 (`project-oxi/.github/DESIGN.md`)
- **이 레포의 역할/특이사항** (예: primary reference, migration status, OKLCH 토큰 출처)
- 기존 좋은 예시: `oximemo/.omp/DESIGN-REF.md` (레포별 role + migration status 포함)
- 동일 주제의 구 `DESIGN.md`/`UNIFIED-DESIGN.md` 전문 카피는 → `docs/archive/` 로 이동.

## 3. 레포별 docs/ 구조

- `docs/INDEX.md` — 해당 레포 문서 목록 (**필수**, 모든 docs/ 트리에 작성)
- 기존 하위 디렉터리(`rfcs/` `designs/` `audits/` `proposals/` 등)는 유지 — 구조가 이미 합리적.
- `docs/archive/` — superseded/구버전 문서.
- `docs/archive/transient/` — `progress.md`, `.release-prep-status.md`, `*handoff*`/`HANDOVER*` 등 임시·상태 문서.

## 4. 아카이브 정책

- **버전 스프롤 해소**: 동일 주제의 여러 버전(예: `DESIGN_IMPROVEMENTS{,_V2,_REVIEW}.md`) → 최신 1개만 `docs/`에, 나머지 `docs/archive/`.
- **판단 기준**: canonical과 동일 주제의 per-repo 카피는 diff로 비교 — >95% 동일 → 포인터로 교체 + 원본 archive; 실질적 다름(working fork) → 유지하되 헤더에 canonical 안내 추가.
- **worktree 복제본**(`.worktrees/...`)은 건드리지 않음 — git worktree artifact, 정식 문서 아님.

## 5. 커밋 정책

- doc 변경은 명확한 커밋 메시지로 커밋 (`docs: ...`).
- **dirty 레포에서 `git add -A` 금지** — doc 파일만 선택적 `git add <path>` (사용자 진행 중 작업과 분리).
- **푸시 금지** — 사용자 리뷰 후 수행 (자동화 잡 포함).

## 6. 임시/상태 문서

- `progress.md`, `.release-prep-status.md`, `.oxi-fixraf-*.md`, `*handoff*`/`HANDOVER*` → `docs/archive/transient/`로 이동 (삭제 아님).
- `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `README.md` → **유지** (정식 문서).
