# Security policy

## Supported scope

Security fixes target the current default branch. While OATHDO remains pre-release/alpha, repository visibility or green CI alone must not be interpreted as a production-readiness guarantee.

## Reporting a vulnerability

Do not publish vulnerabilities, credentials, personal data, non-public URLs, or exploit details in a public issue or pull request.

Prefer GitHub Private Vulnerability Reporting when it is enabled for this repository. If no private reporting channel is available, create only a minimal public request for a private contact path and omit sensitive details.

A useful report includes:

- affected revision and component;
- attack prerequisites;
- minimal reproduction;
- security impact;
- expected safe behavior;
- proposed mitigation, if known.

## Security baseline

- never commit secrets or production data;
- enforce privileged decisions and authorization server-side;
- use least privilege and deny-by-default boundaries;
- validate untrusted input and bound resource consumption;
- preserve audit evidence without recording secrets;
- missing or unverifiable evidence must not mean success;
- revoke or rotate exposed credentials;
- do not weaken governance rules, required checks, or authority policy to make a test pass.

## Cockpit boundary

The local cockpit is an observability surface, not an authority surface. It binds to loopback by default, exposes read-only HTTP routes, and must not be extended with repository mutation, approval, merge, secret, or token capabilities without a separately governed security/architecture decision.

No response or remediation SLA is guaranteed during the pre-release phase.
