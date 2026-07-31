# Contributing to project-oxi

Thank you for your interest in contributing. This guide covers all repositories under the **project-oxi** organization (oxicode, oxibrowser, oxios, oxinot, oxipage, oxiline, oxicleaner). Per-project exceptions are noted in each repo's own `CONTRIBUTING.md`.

## Code of conduct

All participation is governed by [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md). By signing off on any commit, you agree to abide by it. Enforcement contact: **a7garden@icloud.com**.

## Reporting security vulnerabilities

**Do NOT file a public issue for security bugs.** Email **a7garden@icloud.com** with a description and reproduction. See [`SECURITY.md`](./SECURITY.md) for the full policy, response SLAs, and supported versions.

---

## Development setup

### Toolchain

All Rust projects are pinned to **Rust 1.96** via `rust-toolchain.toml`:

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.96"
components = ["rustfmt", "clippy"]
```

Projects at `rust-version = "1.85"` (oxiline) or `stable` (oxinot) may lag the floor — check their own `rust-toolchain.toml`.

### Pre-commit hooks

After cloning:

```bash
pip install pre-commit
pre-commit install
```

The hooks run `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, YAML/TOML lint, large-file scan, and a private-key guard. Bypassing with `--no-verify` requires a written justification in the PR description.

### Build & test

```bash
cargo fmt --all -- --check
cargo clippy --workspace -- -D warnings
cargo test --workspace
```

For projects with a frontend (web/desktop):

```bash
cd web && bun install && bun run build   # oxipage
cd apps/desktop && bun run build        # oxinot, oxiline
```

---

## Pull request workflow

### 1. Open a draft PR early

Open a draft PR as soon as you push your first commit. Early review catches direction issues before you spend time polishing.

### 2. Commit messages — Conventional Commits

PR titles (which become merge commits) MUST follow Conventional Commits:

```
<type>(<scope>): <subject>

Types:    feat | fix | docs | refactor | perf | test | chore | ci | build | style | revert
Scope:    optional, project-specific (core | cli | tui | webapi | cdp | docs | ui | capture)
Subject:  imperative mood, lowercase, no period, ≤72 chars
Examples: feat(tui): add streaming indicator
          fix(core): resolve panic on empty input
          docs: update AGENTS.md tooling section
```

Commits inside the PR can be any style — they will be squashed.

### 3. Labels

Apply at least one `area:*` label and one `type:*` label from `.github/labels.yml` of the target repo.

### 4. Issue link

Reference the issue in the PR body using `Fixes #123`, `Closes #123`, or `Refs #123`. PR-gate CI warns when missing.

### 5. CHANGELOG entry

Every PR that changes behavior MUST add an entry under `## [Unreleased]` in the target repo's `CHANGELOG.md`. Format: Keep a Changelog 1.1.0 (see any repo's `CHANGELOG.md` for examples):

```markdown
## [Unreleased]

### Added
- **component-name** — short description of the user-visible capability

### Fixed
- **component-name** — short description of the bug and its resolution
```

### 6. Size limits

- **< 2000 lines** preferred. CI warns above this.
- **> 4000 lines** is blocked — split the PR.

### 7. Pass all CI gates

CI runs `cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo test --workspace` on every push. PRs cannot merge with failing checks. To run the same locally:

```bash
cargo fmt --all -- --check && \
  cargo clippy --workspace -- -D warnings && \
  cargo test --workspace
```

### 8. PR template checklist

Use the [pull request template](./PULL_REQUEST_TEMPLATE.md) — fill in Summary, Motivation, Changes, Testing (with command output), and Breaking Changes.

---

## Design decisions

If your change affects user-visible behavior, CLI flags, data model, or design tokens, update the relevant `doc/` file in the target repo. For projects under the unified design system (oxinot, oxipage, oxios, oxiline, oxibrowser), also update [`DESIGN.md`](./DESIGN.md) in this `.github` repo.

---

## Licensing

By submitting a contribution, you agree to license your work under the same terms as the target repository:

- **MIT** — oxicode, oxibrowser, oxios, oxipage, oxiline, oxicleaner
- **MIT OR Apache-2.0** — oxinot

See each repo's `LICENSE` / `LICENSE.md` file for the exact text.

---

## Communication

- **Bug reports & features**: GitHub Issues on the target repository
- **Security**: a7garden@icloud.com (do not file public issues)
- **General questions**: GitHub Discussions on the target repository

No Discord, Slack, or other chat channels. Use the issue tracker.