# Task 05: Protect main with a ruleset

**Owner:** agent (needs repo admin) · **Phase:** 1 · **Scope:** S

**Description:** Add a ruleset for `main`: changes only through PRs, required status checks from `pr.yml` (test job and Docker build job, by their final names from tasks 01 and 02), no force-push, no deletion, repo admins may bypass. Keep the ruleset as JSON in the repo and apply it with `gh api`, so it can be reviewed and reapplied.

**Acceptance criteria:**
- [ ] `.github/rulesets/main.json` holds the ruleset and is applied to the repo.
- [ ] A direct push to `main` by a non-admin is rejected, and a PR with failing checks can't merge.
- [ ] `docs/workflows.md` lists the required checks and how to reapply the ruleset.

**Verification:**
- [ ] `gh api repos/mighty-muffin/httpenv-app/rulesets` shows the ruleset as active.
- [ ] Manual check: a PR shows the required checks as "Required".

**Dependencies:** 01, 02

**Files likely touched:**
- `.github/rulesets/main.json`
- `docs/workflows.md`
