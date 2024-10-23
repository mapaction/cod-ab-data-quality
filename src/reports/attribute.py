from logging import getLogger

from geopandas import read_file

from src.config import attributes_dir, boundaries_dir

logger = getLogger(__name__)


def create_csv(iso3: str, level: int) -> None:
    """Creates a CSV for an admin boundary.

    Args:
        iso3: ISO3 of admin boundary.
        level: Admin level of boundary.
    """
    file = boundaries_dir / f"{iso3.lower()}_adm{level}.gpkg"
    if file.exists():
        csv = attributes_dir / f"{iso3.lower()}_adm{level}.csv"
        gdf = read_file(file, use_arrow=True)
        gdf.drop(columns="geometry").to_csv(csv, index=False, encoding="utf-8-sig")
