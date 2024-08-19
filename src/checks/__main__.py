"""Main entry point for the script."""

from logging import getLogger

from geopandas import GeoDataFrame, read_file
from pandas import DataFrame
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from ..config import boundaries, tables
from ..utils import get_metadata
from . import dates, languages

logger = getLogger(__name__)


def main():
    """Main function."""
    logger.info("starting")
    metadata = get_metadata()
    checks = [[dates, []], [languages, []]]
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
        for check, result in checks:
            check.main(result, iso3, gdfs)
    results = None
    for _, result in checks:
        df = DataFrame(result)
        if results is None:
            results = df
        else:
            results = results.merge(df, on=["iso3", "level"], how="outer")
    if results is not None:
        dest = tables / "checks.csv"
        results.to_csv(dest, encoding="utf-8-sig", index=False)
    logger.info("finished")


if __name__ == "__main__":
    main()
