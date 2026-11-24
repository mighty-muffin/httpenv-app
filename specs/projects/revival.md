# Revival: spec

- **Intent**: [specs/intents/revival.md](../intents/revival.md)
- **Vocabulary**: [GLOSSARY.md](../../GLOSSARY.md). Capitalised terms below (Environment, Exposed Value, Rotation, Release, Promotion, Planted Leak, Test Bed) are defined there.
- **Decisions**: [ADR-0001](../../docs/adr/0001-planted-leaks-in-a-public-repo.md) Planted Leaks · [ADR-0002](../../docs/adr/0002-fetch-exposed-value-from-infisical-at-runtime.md) runtime fetch · [ADR-0003](../../docs/adr/0003-health-depends-on-infisical.md) health · [ADR-0004](../../docs/adr/0004-gitops-deploy-with-dockhand-git-sync.md) GitOps deploy
- **Status**: agreed in a design grilling session on 2026-11-24. Not yet broken into tasks.

## Objective

Turn httpenv-app into a stable Test Bed for an AI SDLC. It stays a tiny FastAPI service that serves one Exposed Value, now held in Infisical and rotated on a schedule. Around it: self-contained CI, self-hosted Renovate across every ecosystem, automated semantic-version Releases, and GitOps deploys to two Environments (Staging and Production). The service stays simple. What matters is that the foundation is stable and every step is observable.

## Non-goals

- Rotating anything other than the Exposed Value: machine-identity client secrets, the tunnel token and the Renovate App key are left for a later spec.
- Automatic rollback.
- Making the Dockhand host, reverse proxy, Cloudflare account or Uptime Kuma configuration part of this repo. They are documented, not managed.
- Removing Planted Leaks (ADR-0001).

## 1. Application

### Endpoints

| Path            | Behaviour |
| --------------- | --------- |
| `/`             | Unchanged greeting. |
| `/bye`          | Unchanged farewell. |
| `/external`     | Unchanged (still uses the Planted Leak token fallback). |
| `/policeducode` | Serves the Exposed Value as JSON: `{"value", "environment", "rotated_at", "version", "stale"}`, with `Cache-Control: no-store`. |
| `/healthcheck`  | Unhealthy (non-2xx) when no Infisical fetch has ever succeeded, or the last success is more than 5 minutes old. Otherwise `{"status": "OK"}`. |

- `value`: the Environment's `EXPOSED_VALUE` from Infisical.
- `environment`: `staging` or `production`, from config.
- `rotated_at`: the secret's last-updated timestamp in Infisical.
- `version`: the running Release version (from package metadata, or `main`/sha for Staging builds).
- `stale`: `true` when the cached value is older than the cache TTL because refreshes are failing.

### Reading the Exposed Value (ADR-0002)

- Authenticate to Infisical Cloud with the Infisical Python SDK and a Universal Auth machine identity. The credentials come from environment variables, along with the Infisical project ID and Environment slug.
- Fetch at request time with a ~60s in-process cache. On a failed refresh, keep serving the last value with `stale: true`. If nothing was ever fetched, `/policeducode` returns 503.
- Never read the Exposed Value from an environment variable or `.env` file.

### Planted Leaks (ADR-0001)

Keep the hard-coded token in `app/main.py`, `/policeducode`, and the `vault` composite action as decoys. Every planted value must be fake or dead. List each one in `docs/planted-leaks.md`.

### Acceptance

- Unit tests cover these cases with Infisical mocked: fresh value, stale value served while refreshes fail, 503 before the first fetch, health flipping after 5 minutes stale, and the `no-store` header.
- `uv run pytest` and `ruff check` pass, and coverage stays at or above 70%.

## 2. Infisical

- **Project**: `httpenv-app` on Infisical Cloud, with environments `staging` and `prod`, each holding its own `EXPOSED_VALUE`.
- **Identities** (three):
  - `httpenv-staging-reader`: read-only on `staging`.
  - `httpenv-prod-reader`: read-only on `prod`.
  - `httpenv-rotator`: write access on both, used only by `rotate.yml`.
- **Rotation**: `.github/workflows/rotate.yml` runs on `cron: '0 */6 * * *'` and `workflow_dispatch`. For each Environment, it generates a random value and writes it through the Infisical API with the rotator identity. It then polls `https://env.mighty-muffin.io/policeducode` for up to 3 minutes until the new value shows, and fails the run if it doesn't. Staging is rotated but not checked, because GitHub-hosted runners can't reach the LAN.
- The rotator credentials are GitHub Actions secrets. The reader credentials never go into GitHub.

### Acceptance

- After a manual `rotate.yml` run, PROD's `/policeducode` shows the new value and a newer `rotated_at` within 3 minutes, without a restart.

## 3. CI and workflows (all local)

- **No reusable workflows.** Inline the jobs from `mighty-muffin/.github` (`reusable-python-uv`, `reusable-docker-build`, `reusable-ensure-pin-actions`) into this repo's workflows.
- **Keep the existing layout and triggers.** `branch.yml` (pushes to dev/feat/fix/rel), `main.yml`, `pr.yml`, `cron.yml` (every 6h) and `repo.yml` (weekly) all stay.
- **New single-purpose workflows**: `release.yml`, `renovate.yml`, `rotate.yml`.
- **Local composite actions**: change references from `mighty-muffin/httpenv-app/.github/actions/<x>@main` to `./.github/actions/<x>`, which needs a checkout step.
- **`repo.yml`**: runs zizmor instead of the remote pinned-actions check.
- **Pinning**: every third-party action is pinned to a commit SHA with a version comment, and Renovate keeps the pins current.
- **Build loop guard**: `main.yml` adds `deploy/**` to `paths-ignore`, so the Staging digest bumps don't trigger new image builds (ADR-0004).
- **Required checks**: `pr.yml` must run its required checks on every PR, including PRs that only touch `deploy/`. Don't add `paths-ignore` for `deploy/**` in `pr.yml`.

### Container images

Published to `ghcr.io/mighty-muffin/httpenv-app` for `linux/amd64` and `linux/arm64`, with SBOM and provenance:

| Event             | Tags pushed |
| ----------------- | ----------- |
| Push to main      | `:main`, `:sha-<short>` |
| Release published | `:X.Y.Z` |
| PR / branch / cron | Build only, never pushed |

No `latest` tag.

### Branch protection

A ruleset on `main`: changes only through PRs, required status checks from `pr.yml`, no force-push and no deletion. Repo admins can bypass.

## 4. Releases

- **release-please** on `main`, in `release.yml`. It keeps a release PR open that bumps `pyproject.toml` `project.version` and updates `CHANGELOG.md`. Merging that PR creates the `vX.Y.Z` tag and GitHub Release, which triggers the image build and push for `:X.Y.Z`.
- Remove `python-semantic-release` from the dev dependencies and delete `[tool.semantic_release]` from `pyproject.toml`.
- The commitizen commit-msg hook stays as the Conventional Commits gate.
- If release-please's default token can't trigger downstream workflows, use the Renovate GitHub App, or a dedicated App, to mint the token.

## 5. Dependencies (Renovate, self-hosted)

- **Runner**: `.github/workflows/renovate.yml` runs `renovatebot/github-action` on a schedule, on `workflow_dispatch`, and when triggered by `main.yml` after `:main` is pushed. It authenticates with a dedicated GitHub App (app ID and private key as Actions secrets).
- **Ecosystems**: github-actions, Dockerfile, docker-compose (including `deploy/**/compose.yml`), pre-commit, and Python/uv (`pyproject.toml` + `uv.lock`). Keep lock-file maintenance.
- **Auto-merge** (once required checks pass): patch, digest, pin, pre-commit and lock-file updates, and the Staging `:main` digest bump.
- **Manual**: minor and major updates, and the Production Promotion PR.
- **Uninstall from this repo**: the hosted Mend Renovate app and pre-commit.ci.
- **Config**: `.github/renovate.json` holds the repo config. Self-hosted runner options live in the workflow.

## 6. Deployment (ADR-0004)

Both Environments run on one home host as Dockhand git stacks from this public repo's `main` branch, with scheduled sync every 5 minutes. There is no webhook and no inbound exposure.

| Stack                | Compose file                     | Image                              | Ingress |
| -------------------- | -------------------------------- | ---------------------------------- | ------- |
| `httpenv-staging`    | `deploy/staging/compose.yml`     | `…:main@sha256:<digest>`, auto-bumped | Joins the existing LAN reverse proxy's network as `httpenv.local.mighty-muffin.io`, with no published port |
| `httpenv-production` | `deploy/production/compose.yml`  | `…:X.Y.Z`, bumped by the Promotion PR | A `cloudflared` service in the same stack routes `env.mighty-muffin.io`, with no published port |

- **Secrets**: Infisical reader credentials (per stack) and `TUNNEL_TOKEN` (production) are Dockhand per-stack environment variables, passed in with `${VAR}` substitution. Commit only `deploy/*/.env.example` with the names.
- **Staging flow**: merge to main → `main.yml` pushes `:main` → triggers `renovate.yml` → digest PR → auto-merge → Dockhand sync.
- **Promotion flow**: release-please PR merged → `:X.Y.Z` pushed → Renovate opens the Promotion PR on `deploy/production/compose.yml` → a human reviews and merges → Dockhand sync.
- **Rollback**: revert the commit in git (the Promotion PR, or the digest bump). No automatic rollback.
- **Compose healthchecks** call `/healthcheck` with a start period of about 60s.
- **Monitoring**: add monitors for `/healthcheck` on both Environments to your existing Uptime Kuma, plus a keyword monitor for `"stale":false` on PROD's `/policeducode`. List them in `docs/deployment.md`. Configuring Uptime Kuma itself is out of scope.

### Acceptance

- A merge to main reaches Staging without manual action. Expect about 5 minutes for Dockhand's sync, plus Renovate and CI time.
- A Release reaches Production only after the Promotion PR is merged.
- Reverting a Promotion PR brings back the previous Release within one sync interval.

## 7. Documentation

- **`README.md`**: one screen. What the project is, how to run it locally (uv, then Docker), and links to `docs/`. The `.sample.env` instructions are replaced by `.env.example` and the Infisical setup.
- **`docs/`**:
  - `architecture.md`: overview and diagram.
  - `secrets.md`: Infisical layout and Rotation.
  - `dependencies.md`: Renovate.
  - `release.md`
  - `deployment.md`: Environments, Dockhand stacks, Promotion, rollback, Uptime Kuma monitors.
  - `workflows.md`
  - `planted-leaks.md`
  - plus the existing `docs/agents/` and `docs/adr/`.
- **`specs/`**: keeps `intents/`, `projects/`, `research/`, `tasks/` for agent work.

## Suggested delivery order

These are vertical slices, each one shippable and leaving `main` green. Break them into tasks under `specs/tasks/` when you're ready.

1. Local CI: inline workflows, local composite actions, zizmor, `main` ruleset.
2. Self-hosted Renovate: App, `renovate.yml`, uninstall the hosted apps.
3. release-please and the image tagging scheme.
4. Infisical runtime fetch, the new `/policeducode`, health semantics.
5. `rotate.yml` with the PROD check.
6. `deploy/` stacks, Dockhand setup, Staging digest flow, Promotion flow.
7. Uptime Kuma monitors.
8. README and `docs/`.

## Risks and things to check during implementation

- **Dockhand behaviour isn't verified here.** Sub-path compose files, per-stack env vars and scheduled sync are assumed from its feature list. Confirm them against your instance before slice 6.
- **The release-please token** may need to be an App token, so that tag/release events trigger the image workflow.
- **Renovate auto-merge** needs the App to have permission to merge and the required checks to report on its PRs.
- **The Staging digest loop:** watch the first few cycles to confirm the `paths-ignore` guard works.
