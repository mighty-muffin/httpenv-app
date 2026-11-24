# Implementation plan: Revival

## Overview

This plan breaks [specs/projects/revival.md](../../projects/revival.md) into 22 tasks, one file each in this folder. Terms follow [GLOSSARY.md](../../../GLOSSARY.md). Each task has an **Owner**:

- **agent** tasks can be picked up by an AI agent (triage label `ready-for-agent`).
- **human** tasks need accounts or homelab access only you have (`ready-for-human`).

Tasks live here as markdown, not as GitHub issues. If you publish them later, keep one issue per file and carry the dependencies over as GitHub "blocked by" links.

## Architecture decisions

These are settled elsewhere; this plan doesn't re-open them:

- [ADR-0001](../../../docs/adr/0001-planted-leaks-in-a-public-repo.md): Planted Leaks stay, and every planted value is fake or dead.
- [ADR-0002](../../../docs/adr/0002-fetch-exposed-value-from-infisical-at-runtime.md): the Exposed Value is fetched from Infisical at runtime with a ~60s cache.
- [ADR-0003](../../../docs/adr/0003-health-depends-on-infisical.md): health fails after 5 minutes without a successful fetch.
- [ADR-0004](../../../docs/adr/0004-gitops-deploy-with-dockhand-git-sync.md): Dockhand git-sync deploys. Staging's digest is bumped by Renovate, and Production moves only through Promotion PRs.
- **Docs ship with their slice.** Each task writes or extends the `docs/` page for what it builds. Task 22 only adds the README and architecture overview and checks the set is complete.

## Task list

### Phase 1: Local CI foundation

- [ ] [01](01-inline-python-ci-job.md) Inline the Python test job: agent, M
- [ ] [02](02-inline-docker-build-job.md) Inline the Docker build job with the new image tags: agent, M (after 01)
- [ ] [03](03-reference-composite-actions-locally.md) Reference composite actions locally: agent, XS (after 01)
- [ ] [04](04-zizmor-workflow-audit.md) Replace the remote pin check with zizmor: agent, S (after 01–03)
- [ ] [05](05-protect-main-ruleset.md) Protect main with a ruleset: agent with admin, S (after 01, 02)
- [ ] [06](06-verify-dockhand-capabilities.md) Verify Dockhand can run the planned stacks: **human, risk spike**, can start right away

### Checkpoint A: Foundation

- [ ] No workflow references `mighty-muffin/.github` or a remote composite action.
- [ ] `uvx zizmor .github/` is clean apart from the documented Planted Leak ignores.
- [ ] A PR to main can't merge without the required checks passing.
- [ ] Dockhand's capabilities are confirmed, or ADR-0004 is revisited before Phase 4.
- [ ] Review with the human before continuing.

### Phase 2: Dependencies and Releases

- [ ] [07](07-create-renovate-github-app.md) Create the Renovate GitHub App: **human**, XS
- [ ] [08](08-self-hosted-renovate-workflow.md) Run Renovate self-hosted from renovate.yml: agent, M (after 05, 07)
- [ ] [09](09-uninstall-hosted-apps.md) Uninstall the hosted Renovate and pre-commit.ci apps: **human**, XS (after 08)
- [ ] [10](10-switch-to-release-please.md) Switch to release-please: agent, M (after 05, 07)
- [ ] [11](11-publish-release-images.md) Publish Release images: agent, S (after 02, 10)

### Phase 3: Exposed Value (can run in parallel with Phase 2)

- [ ] [12](12-set-up-infisical.md) Set up the Infisical project and identities: **human**, XS
- [ ] [13](13-exposed-value-reader.md) Read the Exposed Value from Infisical with a cache: agent, M (after 01). **Highest technical risk, so start early.**
- [ ] [14](14-serve-exposed-value.md) Serve the Exposed Value on /policeducode: agent, S (after 13)
- [ ] [15](15-health-reflects-infisical.md) Make /healthcheck reflect Infisical freshness: agent, S (after 13, parallel with 14)

### Checkpoint B: Releases and the service

- [ ] The first Release exists: tag, GitHub Release and `:X.Y.Z` image.
- [ ] Self-hosted Renovate has opened and auto-merged at least one low-risk PR, and the hosted apps are gone.
- [ ] Running locally with the staging reader identity serves the real staging value, and the container goes unhealthy with bad credentials.
- [ ] Review with the human before continuing.

### Phase 4: Deployment

- [ ] [16](16-staging-stack.md) Add the Staging stack: agent, S (after 02, 14, 15)
- [ ] [17](17-production-stack.md) Add the Production stack with cloudflared: agent, S (after 11, 16)
- [ ] [18](18-staging-digest-and-promotion-flow.md) Wire the Staging digest flow and Promotion rules: agent, S (after 08, 16, 17)
- [ ] [19](19-wire-dockhand-and-tunnel.md) Wire Dockhand, the reverse proxy and the Cloudflare Tunnel: **human**, S (after 06, 12, 16, 17)
- [ ] [20](20-rotate-exposed-value.md) Rotate the Exposed Value every 6 hours: agent, M (after 12, 19)
- [ ] [21](21-uptime-kuma-monitors.md) Add the Uptime Kuma monitors: **human**, XS (after 19)

### Checkpoint C: End to end

- [ ] A merge to main reaches Staging with no manual step and no build loop.
- [ ] A Release reaches Production only through a merged Promotion PR, and reverting it restores the previous Release.
- [ ] A manual `rotate.yml` run shows a new value on Production within 3 minutes.
- [ ] Uptime Kuma is green for both Environments.

### Phase 5: Documentation

- [ ] [22](22-readme-and-architecture-doc.md) Rewrite the README and add the architecture doc: agent, S (after 04, 11, 18, 20, 21)

### Checkpoint D: Complete

- [ ] Every acceptance criterion in the spec is met.
- [ ] Ready for review.

## Parallel work

- **Can start immediately, independently:** 01, 06, 07, 12.
- **After 01:** 13 can run alongside the rest of Phase 1 and Phase 2. It touches only `app/`, `tests/` and dependencies.
- **Must be sequential:** 01 → 02 → 05, because the required check names must be final before the ruleset. Tasks 16 → 17 → 18 share `deploy/` and `renovate.json`.
- **Conflict hotspots:** tasks 01–03 all edit the same four workflow files, so run them one after another. Tasks 08 and 18 both edit `.github/renovate.json`.

## Risks and mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Dockhand lacks sub-path stacks, scheduled sync or stack env vars | High | Task 06 spikes it first. If it fails, revisit ADR-0004 before Phase 4. |
| Release PRs opened with `GITHUB_TOKEN` don't trigger CI, so the release PR can never pass its required checks | High | Task 10 uses an App token. |
| Staging digest bump re-triggers the image build, looping forever | Med | Task 18 adds the `paths-ignore` guard and verifies two cycles. |
| Required checks don't report on deploy-only PRs, blocking auto-merge | Med | `pr.yml` never ignores `deploy/**` (task 18). |
| Infisical SDK field names (e.g. for `rotated_at`) differ from assumptions | Low | Task 13 checks them against the SDK and covers them with tests. |
| The rotation workflow leaks the new value in logs | Med | Task 20 masks it before use, and zizmor runs in CI. |
| Your uncommitted working-tree changes (`.env.example`, `.sample.env` deletion, `.github/linter/`) collide with tasks 14 and 22 | Low | Commit or drop them before Phase 3. |

## Open questions

- **First Release version.** `pyproject.toml` is at `0.1.0`. Should release-please's first Release be `0.2.0` (follow the commits) or `1.0.0` (declare the foundation stable)? Decide before task 10.
- **App token for release-please.** Reuse the Renovate App (simplest) or create a separate release App (narrower permissions)? Task 07 assumes reuse.
- **Reverse proxy for Staging.** Which proxy runs on the home host (Traefik labels or Caddy/nginx config)? Task 16 needs it.
- **Host architecture.** Is the Dockhand host amd64 or arm64? Images are built for both. This only matters if you want to drop one.
