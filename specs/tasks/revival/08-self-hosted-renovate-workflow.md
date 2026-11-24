# Task 08: Run Renovate self-hosted from renovate.yml

**Owner:** agent · **Phase:** 2 · **Scope:** M

**Description:** Add `renovate.yml` running `renovatebot/github-action` on a schedule and on `workflow_dispatch`, authenticated with a token minted from the Renovate App (`actions/create-github-app-token`). Update `.github/renovate.json` so it covers github-actions (with SHA pinning), Dockerfile, docker-compose (including `deploy/**/compose.yml`), pre-commit and Python/uv, keeps lock-file maintenance, and auto-merges patch, digest, pin, pre-commit and lock-file updates once required checks pass. Minor and major updates stay manual.

**Acceptance criteria:**
- [ ] A manual run of `renovate.yml` opens or updates the Dependency Dashboard and at least one PR.
- [ ] Renovate PRs trigger `CI - PR` (they're authored by the App, not `GITHUB_TOKEN`).
- [ ] `docs/dependencies.md` explains the runner, ecosystems and auto-merge rules.

**Verification:**
- [ ] `npx --yes --package renovate -- renovate-config-validator .github/renovate.json` passes.
- [ ] Manual check: a patch-level Renovate PR merges itself after its checks pass.

**Dependencies:** 05, 07

**Files likely touched:**
- `.github/workflows/renovate.yml`
- `.github/renovate.json`
- `docs/dependencies.md`
