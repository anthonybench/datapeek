"""Tests for the ``about`` command."""

from __future__ import annotations

from typer.testing import CliRunner

from sleepydatapeek.main import app

runner = CliRunner()


def testAboutPrintsPublicLinks() -> None:
    """`about` prints the PyPI and GitHub URLs."""

    result = runner.invoke(app, ["about"])

    assert result.exit_code == 0
    assert "https://pypi.org/project/sleepydatapeek/" in result.output
    assert "github.com/anthonybench/datapeek" in result.output
