from logging import getLogger
from multiprocessing import Pool

from src.utils import get_metadata

from .attribute import create_csv
from .image import create_png

logger = getLogger(__name__)


def main() -> None:
    """Create a csv and image for each administrative boundary layer."""
    logger.info("Starting")
    metadata = get_metadata()
    results = []
    with Pool() as pool:
        for row in metadata:
            iso3 = row["iso3"]
            levels = row["itos_level"]
            if levels is None:
                levels = -1
            for level in range(levels + 1):
                result = pool.apply_async(create_png, args=[iso3, level])
                result = pool.apply_async(create_csv, args=[iso3, level])
                results.append(result)
        pool.close()
        pool.join()
    for result in results:
        result.get()
    logger.info("Finished")


if __name__ == "__main__":
    main()
