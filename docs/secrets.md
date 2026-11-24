# Secrets

The service serves one secret, the Exposed Value. It lives in Infisical and the service reads it at runtime ([ADR-0002](adr/0002-fetch-exposed-value-from-infisical-at-runtime.md)). It is never read from an environment variable or a `.env` file.

## Infisical layout

| Thing       | Value |
| ----------- | ----- |
| Host        | Infisical Cloud, `https://app.infisical.com` |
| Project     | `httpenv-app` |
| Environments | `staging`, `prod` |
| Secret      | `EXPOSED_VALUE` at path `/`, one per environment |

Three Universal Auth machine identities:

| Identity                 | Access              | Used by |
| ------------------------ | ------------------- | ------- |
| `httpenv-staging-reader` | read on `staging`   | the Staging stack, and local development |
| `httpenv-prod-reader`    | read on `prod`      | the Production stack |
| `httpenv-rotator`        | write on both       | `rotate.yml` only; its credentials are GitHub Actions secrets |

Reader credentials never go into GitHub.

## Configuration

| Variable                  | Required | Meaning |
| ------------------------- | -------- | ------- |
| `INFISICAL_CLIENT_ID`     | yes      | the reader identity's client ID |
| `INFISICAL_CLIENT_SECRET` | yes      | the reader identity's client secret |
| `INFISICAL_PROJECT_ID`    | yes      | the `httpenv-app` project ID |
| `INFISICAL_ENVIRONMENT`   | yes      | the Infisical environment slug: `staging` or `prod` |
| `INFISICAL_HOST`          | no       | defaults to `https://app.infisical.com` |
| `APP_ENVIRONMENT`         | no       | the Environment name shown in responses: `staging` or `production`. Defaults to `local` |
| `APP_VERSION`             | no       | the version shown in responses. Defaults to the version in `pyproject.toml` |

`app/main.py` loads a `.env` file at startup, so these can live there locally. `.env` is git-ignored.

## How the service reads it

`/policeducode` returns:

```json
{"value": "...", "environment": "staging", "rotated_at": "2026-11-24T12:00:00Z", "version": "0.1.0", "stale": false}
```

with `Cache-Control: no-store`.

- The value is cached in-process for 60 seconds.
- `rotated_at` is when the secret was last updated in Infisical.
- If a refresh fails, the last value is served with `"stale": true`.
- If no fetch has ever succeeded, the endpoint returns 503.
- `/healthcheck` returns 503 when no fetch has ever succeeded, or the last success is more than 5 minutes old ([ADR-0003](adr/0003-health-depends-on-infisical.md)). When the 60-second cache has expired it refreshes the value itself, so an idle service still notices an outage.
- A missing required variable makes the endpoint return 500 and names the missing variables in the server log.

## Running locally against Staging

1. Create a client secret for `httpenv-staging-reader` in the Infisical dashboard (Access Control → Identities → the identity → Universal Auth). Keep it out of the repo.
2. Create `.env` in the repo root:

   ```sh
   INFISICAL_CLIENT_ID=<staging reader client ID>
   INFISICAL_CLIENT_SECRET=<staging reader client secret>
   INFISICAL_PROJECT_ID=<httpenv-app project ID>
   INFISICAL_ENVIRONMENT=staging
   APP_ENVIRONMENT=local
   ```

3. Run the server and ask for the value:

   ```sh
   uv run uvicorn app.main:app --port 8080
   curl -i localhost:8080/policeducode
   ```

   The response shows the current Staging value and `"stale": false`.

Tests never call Infisical: they swap in a fake SDK client (`tests/fakes.py`).
