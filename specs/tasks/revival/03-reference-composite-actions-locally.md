# Task 03: Reference composite actions locally

**Owner:** agent · **Phase:** 1 · **Scope:** XS

**Description:** Change `uses: mighty-muffin/httpenv-app/.github/actions/hello@main` and `.../vault@main` to `./.github/actions/hello` and `./.github/actions/vault`, adding a pinned checkout step before each. The `vault` action is a Planted Leak (ADR-0001): keep its behaviour exactly as it is.

**Acceptance criteria:**
- [ ] No workflow references `mighty-muffin/httpenv-app/.github/actions`.
- [ ] `hello` and `vault` jobs still run and behave as before.

**Verification:**
- [ ] `grep -r 'httpenv-app/.github/actions' .github/workflows` returns nothing.
- [ ] Manual check: a `workflow_dispatch` run of `CI - Cron` runs the vault job.

**Dependencies:** 01

**Files likely touched:**
- `.github/workflows/main.yml`
- `.github/workflows/cron.yml`
