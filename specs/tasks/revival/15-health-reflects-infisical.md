# Task 15: Make /healthcheck reflect Infisical freshness

**Owner:** agent · **Phase:** 3 · **Scope:** S

**Description:** Per ADR-0003, `/healthcheck` returns non-2xx when no fetch has ever succeeded or the last success is more than 5 minutes old, and `{"status": "OK"}` otherwise. Health must actively trigger a refresh when the cache has expired, so an idle service still notices an outage. Give the root `compose.yml` healthcheck a start period of about 60s.

**Acceptance criteria:**
- [ ] With the clock and Infisical mocked: healthy after a fetch, still healthy at 4m59s stale, unhealthy at 5m01s, unhealthy before any fetch.
- [ ] A healthcheck call after the TTL triggers a refresh attempt.

**Verification:**
- [ ] `uv run pytest tests/test_healthchecky.py` passes.
- [ ] Manual check: `docker compose up` with bad Infisical credentials shows the container going unhealthy after the start period plus 5 minutes.

**Dependencies:** 13

**Files likely touched:**
- `app/main.py`
- `tests/test_healthchecky.py`
- `compose.yml`
