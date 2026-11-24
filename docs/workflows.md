# Workflows

Every GitHub Actions workflow in this repository is self-contained: jobs are defined inline in `.github/workflows/`, and third-party actions are pinned to a commit SHA with a version comment. Shared logic is duplicated across workflows on purpose rather than pulled from a reusable workflow in another repository.

## Overview

| Workflow | File | Triggers | Jobs |
| -------- | ---- | -------- | ---- |
| CI - PR | `pr.yml` | Pull requests to `main` (except README-only changes), manual | `unit-test` → `docker-build-push` (build only) |
| CI - Branches | `branch.yml` | Pushes to `dev`, `feat/*`, `fix/*`, `rel/*` (except README-only changes), manual | `unit-test` → `docker-build-push` (build only, amd64) |
| CI - Main | `main.yml` | Pushes to `main` (except README-only changes), manual | `hello-world` → `unit-test` → `docker-build-push` (pushes) |
| CI - Cron | `cron.yml` | Every 6 hours, manual | `vault` → `unit-test` → `docker-build-push` (build only) |
| CI - Repository | `repo.yml` | Weekly (Sunday 00:00 UTC), manual | `zizmor` |

Each workflow cancels its own in-progress run when a newer run starts on the same ref.

## Permissions

Every workflow sets `permissions: {}` at the top, so the `GITHUB_TOKEN` has no access unless a job asks for it. Jobs request only what they need: `contents: read` to check out, `packages: write` for the `main.yml` image push, and `security-events: write` for the zizmor upload. A new job without a `permissions:` block gets nothing.

## Jobs

### `unit-test`: Run Unit Tests & Integration Tests

The same job in `pr.yml`, `branch.yml`, `main.yml` and `cron.yml`. It runs on `ubuntu-24.04` with read-only repository access:

1. Checkout, without persisting the token.
2. Install uv (version pinned in the workflow), with the uv cache keyed on `uv.lock`.
3. Install Python from `.python-version`.
4. `uv sync --all-extras --dev --frozen`: fails if `uv.lock` is out of date.
5. `uv run ruff check`: lint, using the ruff version locked in `uv.lock`.
6. `uv run pytest`.
7. `uv cache prune --ci`.

The job runs the same commands as local development (`make lint`, `make tests`). When you change it, change all four copies.

### `hello-world` and `vault`

`main.yml` runs the `hello` composite action and `cron.yml` runs the `vault` composite action from `.github/actions/`. Both are referenced with GitHub's self-repository syntax (`uses: $/.github/actions/<name>`), which resolves the action from this repository at the exact commit being run, with no checkout step. Use `$/` rather than `./` (needs a checkout) or `mighty-muffin/httpenv-app/...@main` (runs whatever is on `main`, not the commit under test). The `vault` action is a Planted Leak: see ADR-0001 (`docs/adr/0001-planted-leaks-in-a-public-repo.md`) before changing it.

### `docker-build-push`: Docker Build

Builds the container image from `Dockerfile` with Buildx after `unit-test` passes. **Only `main.yml` pushes**, and it's the only job with `packages: write`.

| Workflow | Platforms | Pushes | Tags |
| -------- | --------- | ------ | ---- |
| `pr.yml` | amd64, arm64 | no | none |
| `branch.yml` | amd64 | no | none |
| `cron.yml` | amd64, arm64 | no | none |
| `main.yml` | amd64, arm64 | yes, to `ghcr.io/mighty-muffin/httpenv-app` | `main`, `sha-<short>` |

Notes:

- `main.yml` pushes with SBOM and provenance attestations, and writes the GitHub Actions layer cache. The other builds only read that cache.
- There is no `latest` tag. Staging follows `main` and Production pins an exact Release version (`X.Y.Z`, published by the release workflow).
- Builds that don't push exist to catch Dockerfile breakage before merge (PR, branch) and drift in base images or dependencies (cron).

### `zizmor`: Audit Workflows (zizmor)

Runs [zizmor](https://docs.zizmor.sh/) over `.github/` (workflows and composite actions) with online audits, and uploads the results to the repository's **Security → Code scanning** tab under the `zizmor` category. It checks SHA pinning, template injection, excessive permissions, credential persistence and more. The zizmor version is pinned in the workflow.

Configuration lives in `.github/zizmor.yml`. The only ignores allowed are Planted Leaks, listed in `docs/planted-leaks.md`. Run it locally before pushing workflow changes:

```sh
GH_TOKEN=$(gh auth token) uvx zizmor .github/
```
