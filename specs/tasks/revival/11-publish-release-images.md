# Task 11: Publish Release images

**Owner:** agent · **Phase:** 2 · **Scope:** S

**Description:** In `release.yml`, add a build job that runs only when release-please creates a Release and pushes `:X.Y.Z` (multi-arch, SBOM, provenance) from the release tag. Building inside the same workflow avoids relying on tag events from a token that can't trigger workflows. Write `docs/release.md` covering the release PR, version rules and image tags.

**Acceptance criteria:**
- [ ] Merging the release PR creates the `vX.Y.Z` tag, a GitHub Release, and the `:X.Y.Z` image.
- [ ] No `latest` tag is pushed.
- [ ] `docs/release.md` describes the flow end to end.

**Verification:**
- [ ] `uvx zizmor .github/` still passes.
- [ ] Manual check: `docker pull ghcr.io/mighty-muffin/httpenv-app:X.Y.Z` works for the first Release.

**Dependencies:** 02, 10

**Files likely touched:**
- `.github/workflows/release.yml`
- `docs/release.md`
