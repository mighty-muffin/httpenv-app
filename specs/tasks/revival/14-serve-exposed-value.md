# Task 14: Serve the Exposed Value on /policeducode

**Owner:** agent · **Phase:** 3 · **Scope:** S

**Description:** Change `/policeducode` to return JSON `{"value", "environment", "rotated_at", "version", "stale"}` from the reader (task 13), with `Cache-Control: no-store`, and 503 when nothing has ever been fetched. `environment` comes from config, and `version` from package metadata (or the image's build arg for `:main` builds). The endpoint is a Planted Leak path (ADR-0001): keep its name. Update `.env.example` with the new variable names and no values. Start `docs/secrets.md` covering the Infisical layout and local development.

**Acceptance criteria:**
- [ ] The response has all five fields and the `no-store` header.
- [ ] 503 before the first successful fetch, and a stale value marked `"stale": true` during an outage.
- [ ] `docs/secrets.md` explains how to run locally with the staging reader identity.

**Verification:**
- [ ] `uv run pytest` passes, with new cases in `tests/test_main.py`.
- [ ] Manual check: `uv run uvicorn app.main:app --port 8080` with staging reader credentials, then `curl -i localhost:8080/policeducode` shows the real staging value.

**Dependencies:** 13

**Files likely touched:**
- `app/main.py`
- `tests/test_main.py`
- `.env.example`
- `docs/secrets.md`
