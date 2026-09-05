# Current Handoff

- Canonical repo: `/Users/aim/Documents/Projects/The-Penthouse-main-auth`.
- Status: local worktree exists at `2bea709` and is dirty; do not reset, pull, deploy, or merge it as part of routine work.
- Last verified evidence: local API health was the required precondition for Fara acceptance; the September Fara runner remained blocked when API health was not `{"status":"ok","db":"reachable"}`. Public ingress and Unraid release state require fresh proof.
- Open gates: inspect the current diff; prove API, web, and Postgres listeners plus `/api/v1/health`; run browser acceptance; decide separately before deploying.
- Next action: recover the local stack and capture browser/runtime proof before changing or promoting anything.
