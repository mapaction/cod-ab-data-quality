from logging import getLogger
from multiprocessing import Pool
from typing import Any

from geopandas import GeoDataFrame, read_file
from pandas import DataFrame
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from src.config import MULTIPROCESSING, boundaries_dir, tables_dir
from src.utils import get_checks_filter, get_metadata

from . import (
    dates,
    geometry_gaps,
    geometry_overlaps_self,
    geometry_valid,
    geometry_within_parent,
    languages,
    table_names,
    table_pcodes,
)

logger = getLogger(__name__)


def filter_checks(checks: list[Any]) -> list[Any]:
    """Filters checks performed by environment variable or argparser.

    Args:
        checks: List of checks to perform.

    Returns:
        Filtered list of checks.
    """
    checks_include, checks_exclude = get_checks_filter()
    if checks_include:
        checks = [x for x in checks if x[0].__name__.split(".")[-1] in checks_include]
    if checks_exclude:
        checks = [
            x for x in checks if x[0].__name__.split(".")[-1] not in checks_exclude
        ]
    return checks


def create_output(checks: list) -> None:
    """Create CSV from registered checks.

    Args:
        checks: Registered checks.
    """
    output = None
    for _, results in checks:
        if MULTIPROCESSING:
            rows = [row for result in results for row in result.get()]
        else:
            rows = [row for result in results for row in result]
        partial = DataFrame(rows).convert_dtypes()
        if output is None:
            output = partial
        else:
            output = output.merge(partial, on=["iso3", "level"], how="outer")
    if output is not None:
        dest = tables_dir / "checks.csv"
        output.to_csv(dest, encoding="utf-8-sig", index=False)


def main() -> None:
    """Summarizes and describes the data contained within downloaded boundaries.

    1. Create an iterable with each item containing the following (check_function,
    results_list).

    2. Iterate through ISO3 values, creating a list of GeoDataFrames containing admin
    levels 0-n.

    3. Iterate through the check functions, passing to them the results list for that
    check as well as boundary data needed for checking.

    4. When all checks have run against the ISO3's GeoDataFrames, they are released from
    memory and a new ISO3 is loaded in.

    5. After all the checks have been performed for all ISO3 values, join the check
    tables together by ISO3 and admin level.

    6. Output the final result as a single table: "data/tables/checks.csv".
    """
    logger.info("Starting")

    # NOTE: Register checks here.
    checks = [
        (geometry_valid, []),
        (geometry_gaps, []),
        (geometry_overlaps_self, []),
        (geometry_within_parent, []),
        (table_pcodes, []),
        (table_names, []),
        (dates, []),
        (languages, []),
    ]

    checks = filter_checks(checks)
    metadata = get_metadata()
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso3"])
        iso3 = row["iso3"]
        levels = row["itos_level"]
        if levels is None:
            levels = -1
        gdfs = []
        for level in range(levels + 1):
            file = boundaries_dir / f"{iso3.lower()}_adm{level}.gpkg"
            try:
                gdf = read_file(file, use_arrow=True)
            except DataSourceError:
                gdf = GeoDataFrame()
            gdfs.append(gdf)
        if MULTIPROCESSING:
            with Pool() as pool:
                for function, results in checks:
                    result = pool.apply_async(function.main, args=[iso3, gdfs])
                    results.append(result)
                pool.close()
                pool.join()
        else:
            for function, results in checks:
                result = function.main(iso3, gdfs)
                results.append(result)
    create_output(checks)
    logger.info("Finished")


if __name__ == "__main__":
    main()
