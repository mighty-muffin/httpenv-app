# Fetch the Exposed Value from Infisical at runtime

Despite the project's name ("httpenv"), the service does not read the Exposed Value from an environment variable. It authenticates to Infisical Cloud with a read-only machine identity scoped to its Environment and fetches `EXPOSED_VALUE` at request time, with a ~60-second in-process cache. We chose this over injecting the value as an environment variable at container start (`infisical run` or an env file) so that a Rotation becomes visible within about a minute, with no restart or redeploy. The only bootstrap secrets on the host are the machine identity's credentials.

## Considered Options

- **Env var injected at start**: matches the name, but every Rotation needs a container restart, which couples Rotation to deployment.
- **Infisical Agent rendering a file**: no restart, but adds a sidecar container per Environment.
