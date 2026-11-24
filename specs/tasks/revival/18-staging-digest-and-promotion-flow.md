# Task 18: Wire the Staging digest flow and Promotion rules

**Owner:** agent · **Phase:** 4 · **Scope:** S

**Description:** In `main.yml`, add `deploy/**` to `paths-ignore` (the loop guard from ADR-0004) and, after `:main` is pushed, trigger `renovate.yml` with `workflow_dispatch`. In `.github/renovate.json`, add rules so that the `:main` digest in `deploy/staging/compose.yml` auto-merges, and the app image version in `deploy/production/compose.yml` becomes a Promotion PR that is never auto-merged (labelled `promotion`). `pr.yml` must not ignore `deploy/**`.

**Acceptance criteria:**
- [ ] A merge to main produces a Staging digest PR that merges itself, and that merge doesn't trigger a new image build.
- [ ] A new Release produces a Promotion PR that waits for a human.
- [ ] `docs/dependencies.md` and `docs/deployment.md` describe both flows.

**Verification:**
- [ ] `npx --yes --package renovate -- renovate-config-validator .github/renovate.json` passes.
- [ ] Manual check: watch two consecutive merges and confirm no build loop (no `CI - Main` run for the digest-bump commit).

**Dependencies:** 08, 16, 17

**Files likely touched:**
- `.github/workflows/main.yml`
- `.github/renovate.json`
- `docs/dependencies.md`
- `docs/deployment.md`
