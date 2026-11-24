# Task 16: Add the Staging stack

**Owner:** agent · **Phase:** 4 · **Scope:** S

**Description:** Add `deploy/staging/compose.yml`: the app image pinned as `ghcr.io/mighty-muffin/httpenv-app:main@sha256:<current digest>`, `environment: staging`, Infisical reader credentials and project ID via `${VAR}`, a `/healthcheck` healthcheck with a start period of about 60s, and no published ports. It joins your existing reverse proxy's external network, with whatever labels or config that proxy needs for `httpenv.local.mighty-muffin.io` (confirm which proxy with the human). Add `deploy/staging/.env.example` listing variable names only. Start `docs/deployment.md`.

**Acceptance criteria:**
- [ ] The compose file pins an image digest and contains no secret values.
- [ ] `.env.example` lists every variable the stack needs.
- [ ] `docs/deployment.md` describes the Staging stack and its Dockhand settings.

**Verification:**
- [ ] `docker compose -f deploy/staging/compose.yml --env-file deploy/staging/.env.example config` succeeds.
- [ ] `uvx zizmor .github/` and CI still pass, and `main.yml` doesn't build for this deploy-only change once task 18 lands.

**Dependencies:** 02, 14, 15

**Files likely touched:**
- `deploy/staging/compose.yml`
- `deploy/staging/.env.example`
- `docs/deployment.md`
