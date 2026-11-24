# Planted Leaks are committed on purpose

This repository is public and deliberately contains Planted Leaks: a hard-coded GitHub token in `app/main.py`, the `/policeducode` endpoint, and the `vault` composite action that prints a secret past log masking and uploads `.env` as an artifact. They exist so the Test Bed can check that secret scanners (ggshield, Snyk, GitHub secret scanning) and AI reviewers catch them. Every planted credential is fake or already revoked, and `/policeducode` serves only the non-sensitive Exposed Value, so nothing real is ever reachable — not even from Production, which is public.

## Consequences

- Do not "fix" a Planted Leak. Remove or change one only through a deliberate, reviewed decision that updates `docs/planted-leaks.md`.
- A new Planted Leak must use a value that has never been valid.
- Scanner findings on Planted Leaks are expected; dismiss them as "used in tests", not by deleting the leak.
