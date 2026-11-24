# Task 21: Add the Uptime Kuma monitors

**Owner:** human · **Phase:** 4 · **Scope:** XS

**Description:** In your existing Uptime Kuma, add HTTP monitors for `/healthcheck` on Staging and Production, plus a keyword monitor for `"stale":false` on Production's `/policeducode`, with your usual notification channel. The monitor list must match `docs/deployment.md`.

**Acceptance criteria:**
- [ ] All three monitors are up and green.
- [ ] Making the Staging reader credentials invalid in Dockhand turns the Staging monitor red within about 6 minutes. Restore them afterwards.

**Verification:**
- [ ] Manual check: the test notification arrives.

**Dependencies:** 19

**Files likely touched:** none
