# Task 17: Add the Production stack with cloudflared

**Owner:** agent · **Phase:** 4 · **Scope:** S

**Description:** Add `deploy/production/compose.yml`: the app image pinned to the first Release `:X.Y.Z`, `environment: production`, prod reader credentials via `${VAR}`, a healthcheck, and no published ports. Add a `cloudflared` service (image pinned by digest) using `${TUNNEL_TOKEN}` on a private network shared with the app. Add `deploy/production/.env.example`. Extend `docs/deployment.md` with the Production stack, the Promotion flow and rollback by revert.

**Acceptance criteria:**
- [ ] The app image is pinned to an exact Release, and cloudflared is pinned by digest.
- [ ] Neither service publishes a host port.
- [ ] `docs/deployment.md` explains Promotion and rollback.

**Verification:**
- [ ] `docker compose -f deploy/production/compose.yml --env-file deploy/production/.env.example config` succeeds.

**Dependencies:** 11, 16

**Files likely touched:**
- `deploy/production/compose.yml`
- `deploy/production/.env.example`
- `docs/deployment.md`
