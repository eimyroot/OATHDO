# Getting started

## Requirements

- Python 3.11 through 3.13
- Git
- POSIX shell for the bootstrap helper

## Installation

```bash
git clone https://github.com/eimyroot/OATHDO.git
cd OATHDO
./scripts/bootstrap_local.sh
```

## CLI compatibility

The product and repository are named **OATHDO**. The Python package and CLI remain named `goverdocs` in the current compatibility line.

## First verification

```bash
.venv/bin/goverdocs --version
.venv/bin/goverdocs inspect --root .
.venv/bin/goverdocs validate --root .
.venv/bin/goverdocs health --root .
```

## Analyze a change

```bash
.venv/bin/goverdocs classify --root . --diff HEAD~1..HEAD
.venv/bin/goverdocs plan --root . --diff HEAD~1..HEAD
```

These commands analyze and plan. They do not autonomously rewrite canonical documentation.

## Run the local cockpit

```bash
./RUN_COCKPIT.command
```

For a terminal-only status check:

```bash
python3 scripts/cockpit.py --root . --check
```

## Build the documentation portal locally

```bash
python -m pip install -e '.[docs]'
mkdocs build --strict
```

Output is written to the ignored `site/` directory. Publication remains a separate explicit operation.
