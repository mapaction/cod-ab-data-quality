"""Main entry point for the script."""

from logging import getLogger

from pandas import read_csv

from ..config import tables
from . import dates, languages, output

logger = getLogger(__name__)


def main():
    """Main function draft, to be updated with actual functionality."""
    logger.info("starting")
    df = read_csv(tables / "checks.csv")
    for check in (languages, dates):
        df = check.main(df)
    output.main(df)
    logger.info("finished")


if __name__ == "__main__":
    main()
