---
id: ARCH-0003
type: architecture
title: Governance Classifier and Matrix Reconciliation
status: proposed
owner: GOVERDOCS
created: 2026-08-23
updated: 2026-08-23
version: 1.0.0
canonical: true
managed_by: mixed
write_policy: approval-required
supersedes: null
superseded_by: null
related:
  - ARCH-0002
  - ADR-0005
source_refs:
  - ISSUE-85
  - PR-84
last_verified: null
review_due: 2026-09-23
---

# Governance Classifier and Matrix Reconciliation

## Problem

The canonical decision matrix declares `src/**` as a changed-path detector for
`architecture_change`, while the changeset classifier currently emits that event
only for `docs/architecture/**` and `**/architecture/**` paths.

The Gate compares classifier-owned detection domains with the matrix. A generic
source change can therefore match the matrix without producing the corresponding
classifier event, yielding `CLASSIFIER_MATRIX_DRIFT` and a `WARN` result.

## Architectural invariant

A changed-path declaration that belongs to a classifier-owned event must be
implemented by the classifier. The matrix may be broader for label, validator,
or external detection domains, but path and semantic domains explicitly owned by
the classifier must not disagree with runtime classification.

For `architecture_change`, the intended invariant is:

```text
matrix changed path: src/**
        ==
classifier path ownership: src/**
```

## Resolution

Add `src/**` to the classifier path patterns for `architecture_change` and keep
the existing matrix declaration unchanged. This is an alignment/tightening
change, not a governance relaxation.

The accompanying regression test must prove that a representative source path
such as `src/goverdocs/gate.py`:

1. emits `architecture_change`, and
2. produces no classifier/matrix drift for the matching matrix rule.

## Trust boundaries

This change does not alter:

- authority bindings or quorum rules,
- GitHub required-check names or rulesets,
- branch protection or merge permissions,
- evidence trust configuration,
- direct-main write restrictions,
- the distinction between `PASS`, `WARN`, and `BLOCKED`.

GOVERDOCS continues to evaluate pull requests from exact canonical base code.
The architecture document is changed together with the classifier because the
classifier behavior itself is an architecture-level governance responsibility
change and must be recorded as such.

## Verification

Acceptance requires fresh CI, exact-head governance evaluation, no unresolved
review threads, project-owner approval, independent review, and expected-head
server merge. PR #82 must be reevaluated after this repair lands on `main`.
