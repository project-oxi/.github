# ADR: 전역 OMP AGENTS.md (2026-08-04)

**상태:** 채택됨
**위치:** `~/.omp/agent/AGENTS.md` (이 PC, user `won`)

## 배경

- 전역 AGENTS.md가 존재하지 않았음 (`~/.dotfiles`, `~/.omp`, `~/.config` 어디에도 없음).
- 사용자 요청: 이 PC에서 사용하는 코딩 에이전트(OMP/Pi)의 전역 규칙 파일 신설.
- 참고 근거:
  - Vercel eval (Next.js): AGENTS.md 방식이 skills 대비 median 완료 28.64% 빠르고 출력 토큰 16.58% 적음. skills는 56%의 테스트에서 호출조차 안 됨 ([hada.io #26262](https://news.hada.io/topic?id=26262)).
  - [drona23/claude-token-efficient](https://github.com/drona23/claude-token-efficient): 전역 규칙 파일은 매 턴 입력 토큰을 소모하므로 "커지면 절약보다 비용" — lean 유지 원칙.
  - agents.md 공식: "simple, open format… README for agents".

## 결정

1. **위치**: `~/.omp/agent/AGENTS.md`.
   - 실증 테스트(마커 5곳 배치 후 신규 세션에서 검색) 결과, `~/.omp/agent/AGENTS.md`만 user-level 컨텍스트 파일로 로드됨. `~/.omp/`, `~/.pi/`, `~/.config/omp/`, `~/` 루트는 무시됨.
2. **내용 원칙**:
   - **Always 규칙만** 수록. Ask-first/Never 계열은 SKILL로 분리 (토큰 지속 비용 최소화).
   - Lean 크기 (~30줄 / 758B) 유지. 확장은 매 턴 토큰 비용이므로 신중히.
   - 구체적 실패 모드 중심 (drona23의 "scope rules to your actual failure modes").
3. **수록 항목**: 톤·언어 / 도구 규율(bash grep·ls·find 금지, todo 단독 금지) / superpowers 보존 / 절대 금지 영역(`~/.codexbar`, `~/.npki_pkcs11.cnf`, `~/.omp`, `~/.oxi*`, `~/.mini-agent`, 심볼릭 링크 캐시) / 디자인 캐노니컬 포인터(`.github/DESIGN.md` 우선).

## 검증

- 신규 `omp -p` 세션(throwaway cwd)에서 `# 전역 에이전트 규칙` 헤딩 로드 확인 → YES.

## 결과 / 후속

- 파일이 너무 커지면(~100줄 초과) 프로젝트별 AGENTS.md로 분산 고려.
- dotfiles 추적 여부는 별도 결정 사항 (현재 `~/.omp/agent/`는 dotfiles 미추적).
