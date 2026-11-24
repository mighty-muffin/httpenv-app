# Workflows

Every GitHub Actions workflow in this repository is self-contained: jobs are defined inline in `.github/workflows/`, and third-party actions are pinned to a commit SHA with a version comment. Shared logic is duplicated across workflows on purpose rather than pulled from a reusable workflow in another repository.

> Migration in progress: the Docker build jobs still call `mighty-muffin/.github`'s `reusable-docker-build.yml`, and `repo.yml` still calls `reusable-ensure-pin-actions.yml`. Tasks 02 and 04 in `specs/tasks/revival/` inline them.

## Overview

| Workflow | File | Triggers | Jobs |
| -------- | ---- | -------- | ---- |
| CI - PR | `pr.yml` | Pull requests to `main` (except README-only changes), manual | `unit-test` → `docker-build-push` |
| CI - Branches | `branch.yml` | Pushes to `dev`, `feat/*`, `fix/*`, `rel/*` (except README-only changes), manual | `unit-test` → `docker-build-push` (build only) |
| CI - Main | `main.yml` | Pushes to `main` (except README-only changes), manual | `hello-world` → `unit-test` → `docker-build-push` |
| CI - Cron | `cron.yml` | Every 6 hours, manual | `vault` → `unit-test` → `docker-build-push` (build only) |
| CI - Repository | `repo.yml` | Weekly (Sunday 00:00 UTC), manual | `pinned-actions` |

Each workflow cancels its own in-progress run when a newer run starts on the same ref.

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

`main.yml` runs the `hello` composite action and `cron.yml` runs the `vault` composite action from `.github/actions/`. The `vault` action is a Planted Leak: see ADR-0001 (`docs/adr/0001-planted-leaks-in-a-public-repo.md`) before changing it.

### `docker-build-push`

Builds the container image after `unit-test` passes. Only `main.yml` pushes to GHCR.

### `pinned-actions`

Checks that workflow actions are pinned to commit SHAs.
