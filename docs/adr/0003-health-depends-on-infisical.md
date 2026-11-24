# Health depends on Infisical, with a 5-minute stale window

`/healthcheck` reports unhealthy when the last successful fetch of the Exposed Value from Infisical is more than 5 minutes old (or when no fetch has ever succeeded). We want an Infisical outage to be visible as an unhealthy container, not hidden behind a liveness check that is always green. The 5-minute window keeps a single network blip from flipping health. During an outage, `/policeducode` keeps serving the last known value marked `"stale": true`, and returns 503 only if nothing was ever fetched.

## Consequences

- An Infisical Cloud outage turns both Environments unhealthy at once. Anything that acts on container health (deploy tooling, rollback) must not mistake that for a bad Release.
