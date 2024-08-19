"""Main entry point for the script."""

from logging import getLogger

from pandas import read_csv

from ..config import tables

logger = getLogger(__name__)


def main():
    """Main function."""
    logger.info("starting")
    checks = read_csv(tables / "checks.csv")
    if checks.empty:
        raise RuntimeError()
    logger.info("finished")


if __name__ == "__main__":
    main()
