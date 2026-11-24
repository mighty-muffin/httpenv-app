# Task 04: Replace the remote pin check with zizmor

**Owner:** agent · **Phase:** 1 · **Scope:** S

**Description:** Replace `repo.yml`'s `reusable-ensure-pin-actions.yml` job with an inlined job that runs zizmor over `.github/` and uploads SARIF to code scanning. Add a zizmor config that ignores only the findings caused by Planted Leaks (the `vault` action), each with a comment pointing at ADR-0001. Fix every other finding. Start `docs/planted-leaks.md` with the full list of Planted Leaks and the scanners expected to flag each one.

**Acceptance criteria:**
- [ ] `repo.yml` no longer references `mighty-muffin/.github`.
- [ ] zizmor reports no findings except the documented Planted Leak ignores.
- [ ] `docs/planted-leaks.md` lists every Planted Leak (token in `app/main.py`, `/policeducode`, `vault` action) and says each value is fake or dead.

**Verification:**
- [ ] `uvx zizmor .github/` exits 0.
- [ ] Manual check: a `workflow_dispatch` run of `CI - Repository` uploads results to the Security tab.

**Dependencies:** 01, 02, 03

**Files likely touched:**
- `.github/workflows/repo.yml`
- `.github/zizmor.yml`
- `docs/planted-leaks.md`
