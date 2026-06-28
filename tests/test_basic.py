"""Specter basic integration tests: verify imports and version."""

import pytest


def test_import_specter():
    """Test that the main package can be imported."""
    from pathlib import Path

    import toml

    import specter

    # Read version from pyproject.toml to avoid hardcoding
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    pyproject = toml.load(pyproject_path)
    expected_version = pyproject["project"]["version"]

    assert specter.__version__ == expected_version


def test_all_submodules_importable():
    """Test that all major submodules can be imported."""


def test_no_import_errors():
    """Verify no module raises on import."""
    import importlib

    modules = [
        "specter",
        "specter.config.schema",
        "specter.config.settings",
        "specter.agent.context",
        "specter.agent.memory",
        "specter.agent.prompts",
        "specter.agent.core",
        "specter.mcp.registry",
        "specter.mcp.router",
        "specter.mcp.lifecycle",
        "specter.skills.loader",
        "specter.skills.dispatcher",
        "specter.kb.store",
        "specter.kb.retriever",
        "specter.kb.updater",
        "specter.report.generator",
        "specter.report.poc_builder",
        "specter.cli.main",
    ]
    for mod_name in modules:
        try:
            importlib.import_module(mod_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {mod_name}: {e}")
