from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/cockpit.py"


def _module():
    spec = importlib.util.spec_from_file_location("oathdo_cockpit", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cockpit_safe_defaults() -> None:
    module = _module()
    args = module.build_parser().parse_args([])
    assert args.host == "127.0.0.1"
    assert args.port == 8765
    assert args.allow_remote is False


def test_cockpit_refuses_remote_bind_without_explicit_opt_in() -> None:
    module = _module()
    with pytest.raises(ValueError, match="Refusing non-loopback bind"):
        module._validate_host("0.0.0.0", False)
    module._validate_host("0.0.0.0", True)


def test_collect_status_reports_read_only_control_plane(tmp_path: Path) -> None:
    module = _module()
    (tmp_path / "src/goverdocs").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "schemas").mkdir()
    (tmp_path / "policies").mkdir()
    (tmp_path / "docs/governance").mkdir(parents=True)
    (tmp_path / ".github/workflows").mkdir(parents=True)
    (tmp_path / "automation").mkdir()
    (tmp_path / "manifests").mkdir()
    (tmp_path / "evidence").mkdir()
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "goverdocs"\nversion = "0.1.0"\n', encoding="utf-8")
    for relative in module.CONTROL_PLANE.values():
        path = tmp_path / relative
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("test\n", encoding="utf-8")
        else:
            path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "src/goverdocs/kernel.py").write_text("", encoding="utf-8")
    (tmp_path / "tests/test_kernel.py").write_text("", encoding="utf-8")
    (tmp_path / "schemas/example.json").write_text("{}", encoding="utf-8")
    (tmp_path / "docs/governance/example.md").write_text("# test\n", encoding="utf-8")
    status = module.collect_status(tmp_path)
    assert status["product"] == "OATHDO"
    assert status["version"] == "0.1.0"
    assert status["mode"] == "read-only local control surface"
    assert status["control_plane"]["present"] == status["control_plane"]["total"]
    assert status["inventory"]["python_modules"] == 1
    assert status["inventory"]["tests"] == 1
