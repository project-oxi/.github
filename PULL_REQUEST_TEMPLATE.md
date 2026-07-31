## Summary

<!-- One-paragraph description of what this PR does. -->

## Motivation

<!-- Why is this change needed? Link the issue: Fixes #123, Closes #123, or Refs #123. -->

## Changes

<!-- List the user-visible or structural changes. Group by component. -->

-

## Testing

<!-- Run these locally and paste the output (or "all pass" if unchanged). -->

- [ ] `cargo fmt --all -- --check` passes
- [ ] `cargo clippy --workspace -- -D warnings` passes
- [ ] `cargo test --workspace` passes
- [ ] For web/desktop projects: `bun run build` passes
- [ ] `cargo audit` reports no new advisories (if dependencies changed)

### Test output

```
<!-- paste output here -->
```

## Design Documentation

<!-- Required if your PR affects CLI flags, data model, public APIs, or design tokens. -->

- [ ] `CHANGELOG.md` entry added under `## [Unreleased]`
- [ ] `doc/` updated (if applicable)
- [ ] `DESIGN.md` in `project-oxi/.github` updated (if design tokens changed)


## Breaking Changes

<!-- Mark one. -->

- [ ] No breaking changes
- [ ] Breaking changes documented below

```
<!-- Describe migration path for breaking changes. -->
```

## Checklist

- [ ] PR title follows Conventional Commits (`<type>(<scope>): <subject>`)
- [ ] At least one `area:*` label applied
- [ ] At least one `type:*` label applied
- [ ] Linked to an issue (`Fixes #123` etc.)
- [ ] PR < 2000 lines; split if larger
- [ ] No new dependencies, or rationale for any additions