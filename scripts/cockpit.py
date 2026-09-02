from __future__ import annotations

import argparse
import json
import subprocess
import tomllib
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}

CONTROL_PLANE = {
    "Decision matrix": "automation/documentation_decision_matrix.yaml",
    "Documentation policy": "automation/documentation_policy.yaml",
    "Authority policy": "policies/AUTHORITY_POLICY.yaml",
    "Authority bindings": "policies/AUTHORITY_BINDINGS.yaml",
    "Governance gate workflow": ".github/workflows/governance-gate.yml",
    "Quality workflow": ".github/workflows/quality.yml",
    "CodeQL workflow": ".github/workflows/codeql.yml",
    "Document registry": "manifests/DOCUMENT_REGISTRY.yaml",
    "Relationship graph": "manifests/RELATIONSHIP_GRAPH.json",
    "Evidence store": "evidence",
}


def _git_value(root: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = completed.stdout.strip()
    return value or None


def _count(root: Path, pattern: str) -> int:
    return sum(1 for path in root.glob(pattern) if path.is_file())


def _version(root: Path) -> str:
    try:
        data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        return str(data["project"]["version"])
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        return "unknown"


def collect_status(root: Path) -> dict[str, Any]:
    root = root.resolve()
    checks = [
        {"name": label, "path": rel_path, "present": (root / rel_path).exists()}
        for label, rel_path in CONTROL_PLANE.items()
    ]
    present = sum(1 for item in checks if item["present"])

    return {
        "product": "OATHDO",
        "version": _version(root),
        "mode": "read-only local control surface",
        "repository": str(root),
        "git": {
            "branch": _git_value(root, "branch", "--show-current") or "detached/unknown",
            "head": _git_value(root, "rev-parse", "--short=12", "HEAD") or "unknown",
            "dirty": bool(_git_value(root, "status", "--porcelain")),
        },
        "inventory": {
            "python_modules": _count(root, "src/goverdocs/*.py"),
            "tests": _count(root, "tests/test_*.py"),
            "schemas": _count(root, "schemas/*.json"),
            "policies": _count(root, "policies/*"),
            "governance_docs": _count(root, "docs/governance/*.md"),
            "workflows": _count(root, ".github/workflows/*.yml"),
        },
        "control_plane": {"present": present, "total": len(checks), "checks": checks},
        "boundaries": [
            "Cockpit is read-only and does not mutate canonical repository state.",
            "Server binds to loopback by default; remote binding requires --allow-remote.",
            "No credentials, tokens, GitHub writes, approvals, or governance bypasses are exposed.",
            "Canonical truth remains repository files, Git history, policies, and evidence.",
        ],
    }


def _load_html(root: Path) -> bytes:
    return (root / "cockpit" / "index.html").read_bytes()


def make_handler(root: Path) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "OATHDOCockpit/1"

        def _headers(self, status: HTTPStatus, content_type: str, length: int) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                "connect-src 'self'; object-src 'none'; base-uri 'none'; "
                "frame-ancestors 'none'; form-action 'none'",
            )
            self.end_headers()

        def _send(self, status: HTTPStatus, content_type: str, body: bytes) -> None:
            self._headers(status, content_type, len(body))
            if self.command != "HEAD":
                self.wfile.write(body)

        def do_HEAD(self) -> None:  # noqa: N802
            self.do_GET()

        def do_GET(self) -> None:  # noqa: N802
            if self.path in {"/", "/index.html"}:
                try:
                    body = _load_html(root)
                except OSError:
                    self._send(HTTPStatus.INTERNAL_SERVER_ERROR, "text/plain; charset=utf-8", b"cockpit asset missing\n")
                    return
                self._send(HTTPStatus.OK, "text/html; charset=utf-8", body)
                return

            if self.path == "/api/status":
                body = json.dumps(collect_status(root), sort_keys=True, indent=2).encode("utf-8")
                self._send(HTTPStatus.OK, "application/json; charset=utf-8", body)
                return

            if self.path == "/healthz":
                self._send(HTTPStatus.OK, "application/json; charset=utf-8", b'{"status":"ok"}\n')
                return

            self._send(HTTPStatus.NOT_FOUND, "text/plain; charset=utf-8", b"not found\n")

        def do_POST(self) -> None:  # noqa: N802
            self._send(HTTPStatus.METHOD_NOT_ALLOWED, "text/plain; charset=utf-8", b"read-only cockpit\n")

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def _validate_host(host: str, allow_remote: bool) -> None:
    if host not in LOOPBACK_HOSTS and not allow_remote:
        raise ValueError(
            "Refusing non-loopback bind without --allow-remote. "
            "The cockpit is designed as a local read-only control surface."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the OATHDO read-only local cockpit.")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--allow-remote", action="store_true")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--check", action="store_true", help="Print cockpit status as JSON and exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()

    if not (root / "pyproject.toml").is_file() or not (root / "cockpit" / "index.html").is_file():
        raise SystemExit(f"Not an OATHDO repository root: {root}")

    if args.check:
        print(json.dumps(collect_status(root), sort_keys=True, indent=2))
        return 0

    try:
        _validate_host(args.host, args.allow_remote)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    server = ThreadingHTTPServer((args.host, args.port), make_handler(root))
    url = f"http://{args.host}:{args.port}/"
    print(f"OATHDO_COCKPIT={url}")
    print("MODE=READ_ONLY")
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
