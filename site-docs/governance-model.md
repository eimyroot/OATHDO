# Governance model

## Change flow

```text
Repository change
  → deterministic classification
  → decision matrix
  → operation plan
  → validation
  → authority verification
  → governance gate
  → controlled execution where explicitly authorized
  → registry, graph, and audit evidence
```

The exact capabilities available at any point in time are defined by canonical repository state and policy, not by presentation-layer claims.

## Authority

1. Repository files and Git history are canonical.
2. Chat transcripts, exports, ZIP files, and dashboards are snapshots or derived views.
3. Deterministic policy defines allowed operation classes.
4. An LLM cannot approve its own output or substitute for required human authority.
5. Accepted decisions are superseded explicitly rather than silently overwritten.
6. Validation or authority failure must not be converted into a canonical write.

## Write policy

| Class | Meaning |
|---|---|
| `automatic` | Structured mutable project state allowed by policy |
| `append-only` | Chronological register corrected through new entries |
| `approval-required` | Canonical change requires the configured authority |
| `immutable` | Accepted evidence is not rewritten |
| `generated` | Derived output is rebuilt from canonical sources |

## Cockpit boundary

The local cockpit is a read-only observability surface. Its role is to make control-plane structure and repository state visible. It is intentionally separated from the deterministic kernel and must not become an implicit authorization or mutation path.

Detailed normative rules remain in the canonical repository documents.
