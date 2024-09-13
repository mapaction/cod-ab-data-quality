from logging import getLogger

from geopandas import GeoDataFrame, read_file
from pandas import DataFrame
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from src.config import boundaries_dir, tables_dir
from src.utils import get_metadata

from . import (
    dates,
    geometry,
    geometry_overlaps,
    languages,
    table_data_completeness,
    table_data_formatting_has_data,
    table_data_formatting_heirarchical,
)

logger = getLogger(__name__)


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
    checks = (
        (geometry, []),
        (geometry_overlaps, []),
        (table_data_completeness, []),
        (dates, []),
        (languages, []),
        (table_data_formatting_has_data, []),
        (table_data_formatting_heirarchical, []),
    )

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
        for function, results in checks:
            rows = function.main(iso3, gdfs)
            results.extend(rows)
    output = None
    for _, results in checks:
        partial = DataFrame(results).convert_dtypes()
        if output is None:
            output = partial
        else:
            output = output.merge(partial, on=["iso3", "level"], how="outer")
    if output is not None:
        dest = tables_dir / "checks.csv"
        output.to_csv(dest, encoding="utf-8-sig", index=False)
    logger.info("Finished")


if __name__ == "__main__":
    main()
