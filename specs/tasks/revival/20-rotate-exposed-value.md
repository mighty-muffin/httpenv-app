# Task 20: Rotate the Exposed Value every 6 hours

**Owner:** agent · **Phase:** 4 · **Scope:** M

**Description:** Add `rotate.yml` on `cron: '0 */6 * * *'` and `workflow_dispatch`. It logs in as `httpenv-rotator` (Infisical CLI or API) and, for `staging` then `prod`, writes a freshly generated random value to `EXPOSED_VALUE` without printing it. It then polls `https://env.mighty-muffin.io/policeducode` every 10s for up to 3 minutes until `value` matches the new prod value, and fails the run otherwise. Staging is rotated but not checked. Minimal permissions, pinned actions. Extend `docs/secrets.md` with Rotation.

**Acceptance criteria:**
- [ ] A manual run rotates both Environments, and PROD shows the new value and a newer `rotated_at` within 3 minutes, with no restart.
- [ ] The new value never appears in logs (masked with `::add-mask::` before use).
- [ ] The run fails when PROD doesn't converge.

**Verification:**
- [ ] `uvx zizmor .github/` passes.
- [ ] Manual check: `workflow_dispatch` run is green, and the curl output before and after shows different values.

**Dependencies:** 12, 19

**Files likely touched:**
- `.github/workflows/rotate.yml`
- `docs/secrets.md`
