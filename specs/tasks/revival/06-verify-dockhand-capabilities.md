# Task 06: Verify Dockhand can run the planned stacks

**Owner:** human · **Phase:** 1 · **Scope:** XS · **Risk spike**

**Description:** ADR-0004 assumes Dockhand features that weren't checked against your instance. Before any deploy work, confirm in your Dockhand that a git stack can: use a compose file at a sub-path of a public repo (`deploy/staging/compose.yml`); sync on a `*/5 * * * *` schedule without a webhook; take per-stack environment variables passed into `${VAR}` substitution; and run two stacks from the same repo. Record the Dockhand version and anything that differs in `docs/deployment.md` (or in a note on this task if that file doesn't exist yet).

**Acceptance criteria:**
- [ ] All four capabilities confirmed, or each gap written down with a proposed workaround.
- [ ] Dockhand version recorded.

**Verification:**
- [ ] Manual check: a throwaway git stack pointing at a sub-path compose file syncs on schedule and sees a stack env var.

**Dependencies:** None

**Files likely touched:**
- `docs/deployment.md` (or a note on this task)
