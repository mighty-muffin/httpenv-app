# Task 19: Wire Dockhand, the reverse proxy and the Cloudflare Tunnel

**Owner:** human · **Phase:** 4 · **Scope:** S

**Description:** In Dockhand, create git stacks `httpenv-staging` (`deploy/staging/compose.yml`) and `httpenv-production` (`deploy/production/compose.yml`) from this repo's `main`, syncing every 5 minutes, with their per-stack environment variables (reader credentials, project ID, `TUNNEL_TOKEN`). In Cloudflare, create the tunnel and route `env.mighty-muffin.io` to the app service. Point `httpenv.local.mighty-muffin.io` at the reverse proxy in local DNS.

**Acceptance criteria:**
- [ ] `https://httpenv.local.mighty-muffin.io/policeducode` returns the staging value from the LAN only.
- [ ] `https://env.mighty-muffin.io/policeducode` returns the prod value from the internet, and Cloudflare doesn't cache it (`cf-cache-status` isn't `HIT`).
- [ ] Both containers report healthy in Dockhand.

**Verification:**
- [ ] Manual check: `curl -sI https://env.mighty-muffin.io/policeducode` from outside the LAN, and the same for Staging from inside it.

**Dependencies:** 06, 12, 16, 17

**Files likely touched:** none (any findings go into `docs/deployment.md` through a follow-up PR)
