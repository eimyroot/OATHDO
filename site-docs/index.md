# OATHDO

**OATHDO** is a deterministic documentation governor for projects operated by humans and AI agents. It connects repository changes with the documentation, decisions, approvals, policy checks, and audit evidence that should accompany them.

!!! important "Presentation layer"
    This documentation site is a derived presentation layer. Canonical truth remains the OATHDO repository files and Git history. Building the site does not mutate canonical governance content and does not imply publication.

!!! note "CLI compatibility"
    The product and repository are named OATHDO. The Python package and CLI remain named `goverdocs` in the current compatibility line.

## What the system provides

- deterministic change classification;
- a decision matrix and documentation-operation planning;
- validation of metadata, relationships, supersession, and local links;
- registries, a relationship graph, and audit receipts;
- explicit approval and authority boundaries;
- exact-head GitHub governance enforcement;
- reproducible distribution artifacts;
- a read-only local operator cockpit.

## Local cockpit

```bash
./RUN_COCKPIT.command
```

Default endpoint: `http://127.0.0.1:8765/`.

The cockpit observes repository state only. It does not expose write, approval, merge, credential, or governance-bypass capability.

## Safety boundary

OATHDO does not treat an LLM proposal as human authority. Canonical writes remain subject to the repository's policy and enforcement model.

## Current state

OATHDO is alpha-stage. The exact milestone and verification status are maintained in the repository's canonical [`PROJECT_STATE.md`](https://github.com/eimyroot/OATHDO/blob/main/PROJECT_STATE.md) and governed evidence.

Continue to [Getting started](getting-started.md) or the [Governance model](governance-model.md).
