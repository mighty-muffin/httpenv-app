# httpenv-app

A tiny HTTP service that serves one value managed in a secrets manager. It exists as the Test Bed for an AI-driven software delivery lifecycle: simple on purpose, with a stable foundation.

## Language

**Test Bed**:
This project's role: the repository on which AI SDLC agents and practices are exercised before being trusted elsewhere.
_Avoid_: Canary, sandbox, playground

**Environment**:
A running deployment of the service. There are exactly two: Staging and Production.
_Avoid_: Env (when meaning a deployment), stage

**Staging**:
The Environment reachable only from the home network, at a `*.local.mighty-muffin.io` hostname.
_Avoid_: Local, dev, test

**Production**:
The Environment reachable from the public internet at `env.mighty-muffin.io`, through a Cloudflare Tunnel.
_Avoid_: Live, public

**Release**:
A semantically versioned, immutable build of the service, cut from main.
_Avoid_: Deploy, build, tag

**Promotion**:
The reviewed change that points Production at a newer Release. Staging always runs the latest main and is never promoted.
_Avoid_: Deploy, rollout, release

**Exposed Value**:
The single, non-sensitive value the service serves over HTTP, held in the secrets manager so its changes are observable from outside.
_Avoid_: Secret, environment variable, token

**Rotation**:
Replacing the Exposed Value of one Environment with a freshly generated value.
_Avoid_: Refresh, renewal

**Planted Leak**:
A deliberately committed, always-invalid fake credential or leaky code path that exists to check whether scanners and reviewers catch it.
_Avoid_: Vulnerability, real leak, bug
