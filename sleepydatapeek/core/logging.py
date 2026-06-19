"""Shared logging setup for sleepydatapeek."""

import logging


def configureLogging() -> None:
    """Configure application logging once.

    Returns:
        None.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    # WeasyPrint logs every rendering step at INFO; quiet it to keep CLI output clean.
    logging.getLogger("weasyprint").setLevel(logging.WARNING)
    logging.getLogger("fontTools").setLevel(logging.WARNING)
