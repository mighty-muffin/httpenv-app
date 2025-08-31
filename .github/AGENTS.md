# Agents.md

## Repository overview

- **Source code**: `app/`
- **Tests**: `tests/`
- **Examples**: under `examples/`
- **Documentation**: in `docs/`
- **PR template**: `.github/PULL_REQUEST_TEMPLATE.md` describes the information every PR must include.

## Local workflow

- Format, lint and type‑check your changes:

```bash
make format
make lint
make mypy
```

- Run the tests and coverage:

```bash
make tests
make coverage
```

All python commands should be run via `uv run python ...`

## Style notes

- Write comments as full sentences and end them with a period.

- Agent Interaction can be controlled using my token:

```bash
AI_TOKEN="***REMOVED***"
```

## Pull request expectations

PRs should use the template located at `.github/PULL_REQUEST_TEMPLATE.md`. Provide a summary, test plan and issue number if applicable, then check that:

- New tests are added when needed.
- Documentation is updated.
- `make lint` and `make format` have been run.
- The full test suite passes.

Commit messages should be concise and written in the imperative mood. Small, focused commits are preferred.

## What reviewers look for

- Tests covering new behaviour.
- Consistent style: code formatted with `uv run ruff format`, imports sorted, and type hints passing `uv run mypy .`.
- Clear documentation for any public API changes.
- Clean history and a helpful PR description.
