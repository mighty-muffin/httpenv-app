# Task 01: Inline the Python test job

**Owner:** agent · **Phase:** 1 · **Scope:** M

**Description:** Replace every `uses: mighty-muffin/.github/.github/workflows/reusable-python-uv.yml@main` job with an equivalent job defined in the workflow itself: checkout, setup-uv (cache on `uv.lock`), setup-python from `.python-version`, `uv sync --frozen`, `ruff check`, `uv run pytest`, `uv cache prune --ci`. Pin every action to a commit SHA with a version comment (copy the pins the reusable workflow already uses). Keep each workflow's triggers, concurrency and job names unchanged so later required checks stay stable.

**Acceptance criteria:**
- [ ] No workflow in `.github/workflows/` references `reusable-python-uv.yml`.
- [ ] The inlined job runs ruff and pytest and fails the workflow when either fails.
- [ ] `docs/workflows.md` exists and lists each workflow, its triggers and its jobs.

**Verification:**
- [ ] `grep -r reusable-python-uv .github/workflows` returns nothing.
- [ ] `uvx check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml` passes.
- [ ] Manual check: the PR's `CI - PR` run shows the test job green.

**Dependencies:** None

**Files likely touched:**
- `.github/workflows/pr.yml`
- `.github/workflows/branch.yml`
- `.github/workflows/main.yml`
- `.github/workflows/cron.yml`
- `docs/workflows.md`
