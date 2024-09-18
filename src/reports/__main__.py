from logging import getLogger
from multiprocessing import Pool

from src.config import tables_dir
from src.utils import get_metadata, read_csv

from .report import create_report

logger = getLogger(__name__)


def main() -> None:
    """_summary_."""
    logger.info("Starting")
    metadata = get_metadata()
    checks = read_csv(tables_dir / "checks.csv")
    scores = read_csv(tables_dir / "scores.csv")
    results = []
    with Pool() as pool:
        for row in metadata:
            iso3 = row["iso3"]
            levels = row["itos_level"]
            if levels is not None:
                checks_iso3 = checks[checks["iso3"] == iso3].to_dict("records")
                scores_iso3 = scores[scores["iso3"] == iso3].to_dict("records")[0]
                result = pool.apply_async(
                    create_report,
                    args=[iso3, levels, row, checks_iso3, scores_iso3],
                )
                results.append(result)
        pool.close()
        pool.join()
    for result in results:
        result.get()
    logger.info("Finished")


if __name__ == "__main__":
    main()
