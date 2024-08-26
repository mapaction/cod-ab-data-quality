"""Main entry point for the script."""

from logging import getLogger

from geopandas import GeoDataFrame, read_file
from pandas import DataFrame
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from src.config import boundaries, tables
from src.utils import get_metadata

from . import dates, languages

logger = getLogger(__name__)


def main():
    """Summarizes and describes the data contained within downloaded boundaries.

    1. Create an iterable with each item containing the following (check_function,
    results_list).

    2. Iterate through ISO3 values, creating a list of GeoDataFrames containing admin
    levels 0-n.

    3. Iterate through the check functions, passing to them the results list for that
    check as well as boundary data needed for checking.

    4. When all checks have run against the ISO3's GeoDataFrames, they are released from
    memory and a new ISO3 is loaded in.

    4. After all the checks have been performed for all ISO3 values, join the check
    tables together by ISO3 and admin level.

    5. Output the final result as a single table: "data/tables/checks.csv".
    """
    logger.info("starting")
    metadata = get_metadata()
    checks = ((dates, []), (languages, []))
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso3"])
        iso3 = row["iso3"]
        levels = row["itos_level"]
        if levels is None:
            levels = -1
        gdfs = []
        for level in range(levels + 1):
            file = boundaries / f"{iso3.lower()}_adm{level}.gpkg"
            try:
                gdf = read_file(file, use_arrow=True)
            except DataSourceError:
                gdf = GeoDataFrame()
            gdfs.append(gdf)
        for function, results in checks:
            rows = function.main(iso3, gdfs)
            results.extend(rows)
    output_table = None
    for _, results in checks:
        df = DataFrame(results)
        if output_table is None:
            output_table = df
        else:
            output_table = output_table.merge(df, on=["iso3", "level"], how="outer")
    if output_table is not None:
        dest = tables / "checks.csv"
        output_table.to_csv(dest, encoding="utf-8-sig", index=False)
    logger.info("finished")


if __name__ == "__main__":
    main()
