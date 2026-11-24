# Task 12: Set up the Infisical project and identities

**Owner:** human · **Phase:** 3 · **Scope:** XS

**Description:** In Infisical Cloud, create the project `httpenv-app` with environments `staging` and `prod`, each with an initial `EXPOSED_VALUE`. Create three Universal Auth machine identities: `httpenv-staging-reader` (read on `staging`), `httpenv-prod-reader` (read on `prod`), `httpenv-rotator` (write on both). Store the rotator's client ID and secret, and the project ID, as Actions secrets. Keep the reader credentials for Dockhand (task 19) and for local development; never put them in GitHub.

**Acceptance criteria:**
- [ ] Both environments hold `EXPOSED_VALUE`.
- [ ] Each identity can do only what's listed above.
- [ ] `INFISICAL_ROTATOR_CLIENT_ID`, `INFISICAL_ROTATOR_CLIENT_SECRET` and `INFISICAL_PROJECT_ID` exist as Actions secrets.

**Verification:**
- [ ] Manual check: logging in as `httpenv-staging-reader` with the Infisical CLI can read `staging` and is refused on `prod`.

**Dependencies:** None

**Files likely touched:** none
