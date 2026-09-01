# Installation

## Requirements

- Python 3.11, 3.12, or 3.13
- Git
- POSIX shell for the bootstrap helper

## Clean install

```bash
git clone https://github.com/eimyroot/OATHDO.git
cd OATHDO
./scripts/bootstrap_local.sh
```

The bootstrap creates a repository-local `.venv` and installs the development environment needed by OATHDO's verification workflow.

Verify the install:

```bash
.venv/bin/goverdocs --version
.venv/bin/goverdocs health --root .
./scripts/verify.sh
```

## Run the cockpit

The cockpit itself uses only the Python standard library and can be started without installing Node.js or a frontend toolchain:

```bash
./RUN_COCKPIT.command
```

Or directly:

```bash
python3 scripts/cockpit.py --root .
```

Default endpoint:

```text
http://127.0.0.1:8765/
```

For a non-interactive smoke check:

```bash
python3 scripts/cockpit.py --root . --check
```

The server refuses non-loopback binding unless `--allow-remote` is explicitly supplied.

## Uninstall / rollback

OATHDO does not require system-wide installation for the repository workflow. Remove the cloned directory to remove the local installation. For code changes, use normal Git branch/revert workflows rather than overwriting canonical history.
