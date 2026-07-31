# Security Policy

## Supported Versions

| Project | Latest stable | Receiving security fixes |
|---------|---------------|---------------------------|
| **oxicode** | current `main` + latest release | ✅ |
| **oxios** | current `main` + latest release | ✅ |
| **oxibrowser** | current `main` + latest release | ✅ |
| **oxinot** | current `main` + latest release | ✅ |
| **oxipage** | current `main` + latest release | ✅ |
| **oxiline** | pre-release | ✅ (best effort) |
| **oxicleaner** | current `main` | ✅ (best effort) |
| Older releases (n-1, n-2) | — | ❌ no backports |

Each repository's `CHANGELOG.md` and tags are the source of truth for what is "latest." We do not maintain security branches for older minor versions.

## Reporting a Vulnerability

**Do NOT file a public GitHub issue for security vulnerabilities.**

Email **a7garden@icloud.com** with:

1. **Description** — what the vulnerability is and which component is affected (e.g. `oxicode`, `oxibrowser-core`, `oxios-supervisor`).
2. **Reproduction** — minimal steps, code snippet, or proof-of-concept. A failing test or `cargo run` command is ideal.
3. **Impact** — what an attacker can achieve (information disclosure, RCE, privilege escalation, credential exposure, etc.).
4. **Affected versions** — commit SHA, tag, or release range.
5. **Suggested fix** — optional but welcome. We will credit you in the advisory.

### Response targets

| Phase | Target |
|-------|--------|
| Initial acknowledgement | **48 hours** |
| Triage + severity assessment | **7 days** |
| Patch released | **30 days** for high/critical, **90 days** for low/medium |

We follow [coordinated disclosure](https://docs.github.com/en/code-security/security-advisories/guidance-on-coordinated-disclosure-of-security-vulnerabilities): we ask that you give us a reasonable window before public disclosure.

## Security Tooling

Each Rust repo **should** run the following in CI:

- **`cargo audit`** — RustSec Advisory Database scan on every push
- **`cargo deny`** — license + ban-list + supply-chain check

Both must pass for a PR to merge.

## Security-Sensitive Areas

These components handle credentials, user data, or agent execution paths and warrant extra scrutiny:

- **oxicode** — multi-provider LLM API keys, session JSONL persistence
- **oxios** — agent supervisor (fork/exec/wait/kill), MCP/A2A protocol handlers, Merkle audit trail, RBAC access manager
- **oxibrowser** — TLS stack, JS engine (boa_engine), stealth fingerprinting
- **oxinot** — capture overlay, on-disk note encryption (when enabled), FTS index
- **oxipage** — local Axum console on `127.0.0.1` (no auth by design — do not expose to network)

If your PR touches any of these, request a security review by emailing **a7garden@icloud.com**.

