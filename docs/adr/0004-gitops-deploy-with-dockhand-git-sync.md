# Deploy with Dockhand git-sync, not CI pushes

Both Environments run on one home host as Dockhand git stacks that poll this repository's `main` branch every 5 minutes: `deploy/staging/compose.yml` and `deploy/production/compose.yml`. CI never reaches into the home network, and there is no self-hosted GitHub runner, because GitHub advises against self-hosted runners on public repositories (a fork's pull request can run code on the host). Git is the record of what runs where. Staging pins `:main@sha256:…`, which Renovate bumps and auto-merges after each main build. Production pins an exact Release, and Renovate's Promotion PR bumps it after human review. Rolling back means reverting the commit in git. There is no automatic rollback: per ADR-0003, an Infisical outage makes every container unhealthy, and a health-driven rollback would blame the Release.

## Consequences

- The main image build must ignore pushes that only touch `deploy/**`. Otherwise every Staging digest bump would trigger a new build and a new bump, in an endless loop.
- PR checks must still run on deploy-only PRs. Required checks that never report would block Renovate's auto-merge.
- Host secrets (Infisical machine-identity credentials, the Cloudflare Tunnel token) live in Dockhand's per-stack environment variables, never in git.
- A deploy can take up to ~5 minutes after a merge (the polling interval). A webhook was rejected because it would expose Dockhand to the internet.
