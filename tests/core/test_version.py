"""Tests for version reporting and the -v/--version pre-scan."""

from __future__ import annotations

import sys

import pytest

import sleepydatapeek.main as main_module
from sleepydatapeek.core import version as version_module


def testWantsVersionDetectsFlagAnywhere() -> None:
    """-v/--version is detected even amid a full subcommand invocation."""

    assert version_module.wantsVersion(["--version"])
    assert version_module.wantsVersion(["-v"])
    assert version_module.wantsVersion(["summary", "data.csv", "--version"])
    assert not version_module.wantsVersion(["summary", "data.csv"])


def testIsNewerComparesReleases() -> None:
    """Semantic-ish comparison of dotted versions."""

    assert version_module.isNewer("2.4.0", "2.3.1")
    assert not version_module.isNewer("2.3.1", "2.3.1")
    assert not version_module.isNewer("2.3.0", "2.3.1")


def testPrintVersionQuietWhenCheckFails(capsys: pytest.CaptureFixture[str]) -> None:
    """A failed update check prints only the version line (graceful)."""

    version_module.printVersion(fetch_latest=lambda: None)

    out = capsys.readouterr().out
    assert version_module.DIST_NAME in out
    assert "newer version" not in out


def testPrintVersionFlagsNewerRelease(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A newer published version is surfaced with an upgrade hint."""

    monkeypatch.setattr(version_module, "getVersion", lambda: "1.0.0")
    version_module.printVersion(fetch_latest=lambda: "999.0.0")

    assert "newer version is available: 999.0.0" in capsys.readouterr().out


def testLatestVersionReturnsNoneOnNetworkFailure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Any error during the PyPI lookup yields None rather than raising."""

    def _boom(*args, **kwargs):
        raise OSError("no network")

    monkeypatch.setattr(version_module.urllib.request, "urlopen", _boom)
    assert version_module.latestVersion() is None


def testMainVersionShortCircuits(monkeypatch: pytest.MonkeyPatch) -> None:
    """--version among subcommand args prints version and never runs the app."""

    calls = {"app": False, "version": False}
    monkeypatch.setattr(main_module, "app", lambda: calls.__setitem__("app", True))
    monkeypatch.setattr(main_module, "printVersion", lambda: calls.__setitem__("version", True))
    monkeypatch.setattr(sys, "argv", ["sleepydatapeek", "summary", "data.csv", "--version"])

    main_module.main()

    assert calls == {"app": False, "version": True}


def testMainRunsAppWithoutVersion(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without the flag, the Typer app is invoked as usual."""

    calls = {"app": False, "version": False}
    monkeypatch.setattr(main_module, "app", lambda: calls.__setitem__("app", True))
    monkeypatch.setattr(main_module, "printVersion", lambda: calls.__setitem__("version", True))
    monkeypatch.setattr(sys, "argv", ["sleepydatapeek", "summary", "data.csv"])

    main_module.main()

    assert calls == {"app": True, "version": False}
