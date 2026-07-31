"""Public project links for the ``about`` command.

The GitHub URL is read from the installed package metadata (i.e. the
``[project.urls]`` entries) so it stays in sync with ``pyproject.toml``, with a
hardcoded fallback for running uninstalled from source. The PyPI URL is derived
from the distribution name.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, metadata

from sleepydatapeek.core.version import DIST_NAME, getVersion

_GITHUB_FALLBACK = "https://github.com/anthonybench/datapeek"


def pypiUrl() -> str:
    """Return the public PyPI project URL."""

    return f"https://pypi.org/project/{DIST_NAME}/"


def githubUrl() -> str:
    """Return the public GitHub URL from package metadata, or a fallback."""

    try:
        entries = metadata(DIST_NAME).get_all("Project-URL") or []
    except PackageNotFoundError:
        return _GITHUB_FALLBACK

    labelled: dict[str, str] = {}
    for entry in entries:  # each entry looks like "Source, https://github.com/…"
        label, _, url = entry.partition(",")
        labelled[label.strip().lower()] = url.strip()

    for key in ("source", "homepage", "repository"):
        if "github.com" in labelled.get(key, ""):
            return labelled[key]
    for url in labelled.values():
        if "github.com" in url:
            return url
    return _GITHUB_FALLBACK


def printAbout() -> None:
    """Print the project's version and public PyPI + GitHub links."""

    print(f"{DIST_NAME} {getVersion()}")
    print(f"PyPI:   {pypiUrl()}")
    print(f"GitHub: {githubUrl()}")
