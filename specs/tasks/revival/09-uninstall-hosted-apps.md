# Task 09: Uninstall the hosted Renovate and pre-commit.ci apps

**Owner:** human · **Phase:** 2 · **Scope:** XS

**Description:** Once self-hosted Renovate has run successfully, remove this repo from the Mend Renovate app and from pre-commit.ci, and close their open PRs that self-hosted Renovate now duplicates.

**Acceptance criteria:**
- [ ] Neither app has access to this repo.
- [ ] No open PRs from `app/renovate` or `app/pre-commit-ci`.

**Verification:**
- [ ] `gh pr list --author app/renovate` and `gh pr list --author app/pre-commit-ci` return nothing.

**Dependencies:** 08

**Files likely touched:** none
