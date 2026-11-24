# Task 13: Read the Exposed Value from Infisical with a cache

**Owner:** agent · **Phase:** 3 · **Scope:** M · **Highest technical risk: start early**

**Description:** Add a module that reads `EXPOSED_VALUE` through the Infisical Python SDK with Universal Auth (ADR-0002). Configuration comes from environment variables: client ID, client secret, project ID, Environment slug. It keeps an in-process cache with a ~60s TTL, records the time of the last successful fetch, and on a failed refresh returns the last value marked stale. It exposes the value, `rotated_at` (the secret's last-updated time from Infisical; check the SDK's field names), the stale flag and the last-success time. No endpoint changes in this task.

**Acceptance criteria:**
- [ ] With Infisical mocked: the first call fetches, a second call within the TTL doesn't, and a call after the TTL refetches.
- [ ] A failed refresh returns the last value with stale set. With no prior success it raises a clear "never fetched" error.
- [ ] The Infisical SDK is a runtime dependency in `pyproject.toml` and `uv.lock`.

**Verification:**
- [ ] `uv run pytest tests/test_exposed_value.py` passes.
- [ ] `uv run ruff check` and `make coverage` (at or above 70%) pass.

**Dependencies:** 01

**Files likely touched:**
- `app/exposed_value.py`
- `tests/test_exposed_value.py`
- `pyproject.toml`
- `uv.lock`
