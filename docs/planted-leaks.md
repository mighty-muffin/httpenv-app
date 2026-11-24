# Planted Leaks

A **Planted Leak** is a deliberately committed, always-invalid fake credential or leaky code path. It exists to check whether scanners and reviewers, human or AI, catch it. They stay in the repository on purpose: read ADR-0001 (`docs/adr/0001-planted-leaks-in-a-public-repo.md`) before changing any of them.

## Rules

1. **Every planted value must be fake, revoked, or a canary token.** Nothing listed here may ever grant real access, because the repository is public and Production is on the internet.
2. **Don't "fix" a Planted Leak.** Removing or changing one is a deliberate, reviewed decision that updates this page.
3. **Dismiss, don't delete.** When a scanner flags a Planted Leak, dismiss the finding as "used in tests" (or ignore it in the scanner's config with a comment pointing here). Don't remove the leak.
4. **A new Planted Leak** must use a value that has never been valid, and must be added to the table below.

## Inventory

| # | Planted Leak | Where | What leaks | Expected to be caught by | Value status |
| - | ------------ | ----- | ---------- | ------------------------ | ------------ |
| 1 | Hard-coded GitHub token | `app/main.py`: `GH_TOKEN` fallback (`ghp_QbIm…ByjC`) | A GitHub personal access token in source | ggshield, GitHub secret scanning, gitleaks, AI review | Dead (confirmed 2026-11-24) |
| 2 | `/policeducode` endpoint | `app/main.py` | A value served publicly under a "secret" name. Today it serves `SECRET` (fallback `123456`). Per the revival spec it will serve only the non-sensitive Exposed Value. | Snyk Code (information exposure), AI review | Fallback `123456` is fake |
| 3 | `vault` composite action, run every 6h by `CI - Cron` | `.github/actions/vault/action.yml` | Prints `secrets.SECRET_SECRET` letter-spaced, which bypasses GitHub's log masking. Writes it and `vars.SECRET_VAR1`/`vars.SECRET_VAR2` into `.env` and uploads that as the `.env_file` artifact, which any signed-in GitHub user can download on a public repo. It also interpolates the inputs straight into shell (template injection). | zizmor (`template-injection`), AI review, GitHub's masking | **Unconfirmed.** `SECRET_VAR1`/`SECRET_VAR2` look like an AWS access key pair. Confirm they are a canary or dead, or replace them with ones that are. |

## Scanner configuration

| Scanner | Where Planted Leaks are ignored |
| ------- | ------------------------------- |
| zizmor | `.github/zizmor.yml`: `template-injection` at the four `vault` action lines. Entries match basename and line, so editing the action makes the findings resurface on purpose. |

## Not classified yet

- `Dockerfile` sets `ENV SECRET="some other value"`, which bakes a "secret" into image layers. That's bait for image scanners (Trivy, Docker Scout) if planted, or leftover config if not. Decide which and either move it into the inventory or remove it.
