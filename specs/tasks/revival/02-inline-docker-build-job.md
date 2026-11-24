# Task 02: Inline the Docker build job with the new image tags

**Owner:** agent · **Phase:** 1 · **Scope:** M

**Description:** Replace every `reusable-docker-build.yml` job with an inlined build job: QEMU, buildx, GHCR login, docker/metadata-action, build-push with GHA cache, SBOM and provenance, for `linux/amd64,linux/arm64`. Apply the tag scheme from the spec: a push to main pushes `:main` and `:sha-<short>`; PR, branch and cron builds never push; no `latest` tag anywhere. Drop the PR-comment feature of the old reusable workflow. Grant `packages: write` only to the job that pushes.

**Acceptance criteria:**
- [ ] No workflow references `reusable-docker-build.yml`.
- [ ] Only `main.yml` pushes images, tagged exactly `:main` and `:sha-<short>`.
- [ ] `docs/workflows.md` documents the tag scheme.

**Verification:**
- [ ] `docker buildx build -f Dockerfile . -t httpenv-app` succeeds locally.
- [ ] `uvx check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml` passes.
- [ ] Manual check: after merge, `ghcr.io/mighty-muffin/httpenv-app` shows `main` and `sha-<short>` and no new `latest`.

**Dependencies:** 01

**Files likely touched:**
- `.github/workflows/pr.yml`
- `.github/workflows/branch.yml`
- `.github/workflows/main.yml`
- `.github/workflows/cron.yml`
- `docs/workflows.md`
