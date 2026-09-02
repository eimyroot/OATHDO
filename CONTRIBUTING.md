# Contributing to OATHDO

Changes should be small, reviewable, tested, evidence-aware, and reversible.

## Workflow

1. Reference or create a related issue for material changes.
2. Create a narrowly scoped branch from the repository's current default branch.
3. Implement the smallest complete change that resolves the declared problem.
4. Add or update tests and documentation where the behavior or contract changes.
5. Run the repository verification commands.
6. Open a pull request that states rationale, affected scope, evidence, risk, and rollback.

## Pull request standard

A pull request should state:

- what changed and why;
- what is intentionally out of scope;
- verification commands and observed results;
- security, compatibility, data, and operational risks;
- rollback or safe-disable procedure;
- governance approvals required by the affected change class.

Do not commit secrets, personal data, local databases, runtime state, or claims that have not been verified. A green check proves only the scope that the check actually evaluates.

## Verification

```bash
./scripts/bootstrap_local.sh
./scripts/verify.sh
python3 scripts/cockpit.py --root . --check
```

If a change affects authority, enforcement, workflows, rulesets, or canonical governance documents, treat it as a control-plane change and preserve the required independent review path.
