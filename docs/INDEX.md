# Oxi 생태계 문서 인덱스

> **내부 문서 허브.** 생태계 전체 산재 문서의 단일 진입점.
> 위치: `project-oxi/.github/docs/` — git-tracked, GitHub 원격 동기화됨.

---

## Canonical 디자인 시스템

- **[`../DESIGN.md`](../DESIGN.md)** — Oxi 통합 디자인 시스템 **v1.0** (단일 출처). 모든 앱이 따름.
  나이틀리 인테그리티 잡이 컨포먼스 체크 기준으로 사용.

## 허브 구조

| 경로 | 내용 |
|---|---|
| `architecture/` | 생태계 아키텍처 — 레포 관계도, 데이터 흐름, 의존성 |
| `decisions/` | ADR — 중요 설계 결정 기록 (OKLCH 채택, `.dark` 트리거, 네이밍 리네임 등) |
| `design/` | 디자인 시스템 보조 노트 (canonical은 `../DESIGN.md`) |
| `reports/` | 수동/감사 리포트 보관 (나이틀리 잡은 현재 `/tmp`에만 작성; 영속화는 추후 옵션) |
| `conventions/` | 문서·커밋 규약 — [`DOC-ORGANIZATION.md`](conventions/DOC-ORGANIZATION.md) |

## 레포별 문서

각 레포는 자체 `docs/` + `INDEX.md` + `DESIGN-REF.md` 포인터를 가진다 (포인터가 canonical을 가리킴).

| 레포 (로컬) | 레포명 | 문서 위치 |
|---|---|---|
| `oxi/` | oxiCode | `docs/` |
| `oximemo/` | oxiMemo | `docs/` + `doc/` |
| `oxipage/` | oxiBuilder | `docs/` + `doc/` |
| `oxios/` | oxios | `docs/` + `web/` |
| `oxibrowser/` | oxiBrowser | `docs/` |

## 자동화

- **나이틀리 인테그리티 잡**: `project-oxi/.omp/auto-task-nightly-integrity.md` → `/tmp/oxi-reports/`.

## 네이밍 히스토리

`oxi`→oxiCode · `oxiNot`→oxiMemo · `oxiPage`→oxiBuilder (GitHub 레포명 변경 2026-08-02; 로컬 경로는 일부 구명칭 유지).
