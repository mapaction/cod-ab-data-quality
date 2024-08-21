"""Main entry point for the script."""

from logging import getLogger

from pandas import read_csv
from tqdm import tqdm

from ..config import tables
from ..utils import get_metadata

logger = getLogger(__name__)


def main():
    """Main function deaft, to be updated with actual functionality."""
    logger.info("starting")
    metadata = get_metadata()
    checks = read_csv(tables / "checks.csv")
    if checks.empty:
        raise RuntimeError()
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso3"])
    logger.info("finished")


if __name__ == "__main__":
    main()
