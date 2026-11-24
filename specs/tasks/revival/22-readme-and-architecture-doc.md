# Task 22: Rewrite the README and add the architecture doc

**Owner:** agent · **Phase:** 5 · **Scope:** S

**Description:** Rewrite `README.md` as one screen: what the project is (a Test Bed serving an Exposed Value), how to run it locally with uv and then Docker, and links into `docs/`. Remove the `.sample.env` instructions. Add `docs/architecture.md` with an overview diagram (Infisical, the service, Dockhand stacks, Cloudflare Tunnel, Renovate, release-please, Uptime Kuma) linking to each component doc and the ADRs. Check that every doc listed in the spec exists and that terms match `GLOSSARY.md`.

**Acceptance criteria:**
- [ ] The README fits on one screen and has no stale instructions.
- [ ] `docs/` contains architecture, secrets, dependencies, release, deployment, workflows and planted-leaks.
- [ ] Every relative link in `README.md` and `docs/` resolves.

**Verification:**
- [ ] Manual check: follow the README from a fresh clone to a running local server.

**Dependencies:** 04, 11, 18, 20, 21

**Files likely touched:**
- `README.md`
- `docs/architecture.md`
