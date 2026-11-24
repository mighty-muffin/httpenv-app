# Task 10: Switch to release-please

**Owner:** agent · **Phase:** 2 · **Scope:** M

**Description:** Add `release.yml` running `googleapis/release-please-action` on pushes to main, with the Python release type, managing `pyproject.toml` `project.version` and `CHANGELOG.md`. Use an App token so the release PR triggers `CI - PR` (see Open questions in `plan.md`). Remove `python-semantic-release` from the dev dependencies and `[tool.semantic_release]` from `pyproject.toml`, and refresh `uv.lock`. The commitizen hook stays.

**Acceptance criteria:**
- [ ] After a `feat:` or `fix:` merge, release-please opens or updates a release PR with the version bump and changelog.
- [ ] The release PR runs the required checks.
- [ ] `python-semantic-release` no longer appears in `pyproject.toml` or `uv.lock`.

**Verification:**
- [ ] `uv sync --frozen` and `uv run pytest` pass.
- [ ] `uvx check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/release.yml` passes.
- [ ] Manual check: the release PR appears and is mergeable once its checks are green.

**Dependencies:** 05, 07

**Files likely touched:**
- `.github/workflows/release.yml`
- `release-please-config.json`
- `.release-please-manifest.json`
- `pyproject.toml`
- `uv.lock`
