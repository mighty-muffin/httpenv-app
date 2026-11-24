# Task 07: Create the Renovate GitHub App

**Owner:** human · **Phase:** 2 · **Scope:** XS

**Description:** Create a GitHub App for self-hosted Renovate (and for release-please, see Open questions in `plan.md`), installed on `mighty-muffin/httpenv-app` only. Permissions: contents, pull requests, issues, workflows and checks read/write; metadata and packages read. Store `RENOVATE_APP_ID` and `RENOVATE_APP_PRIVATE_KEY` as Actions secrets.

**Acceptance criteria:**
- [ ] The App is installed on this repo only.
- [ ] Both secrets exist in the repo's Actions secrets.

**Verification:**
- [ ] `gh secret list` shows `RENOVATE_APP_ID` and `RENOVATE_APP_PRIVATE_KEY`.

**Dependencies:** None

**Files likely touched:** none
