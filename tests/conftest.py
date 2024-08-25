import os
import re

from geopandas import GeoDataFrame, read_file
from pytest import fixture

ADMIN_REGEX = r"_adm(\d)_"
TEST_DATA_DIR = "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"


def get_admin_level_from_file_path(string: str) -> int:
    """Extracts the admin level from the test data filepath."""
    match = re.search(ADMIN_REGEX, string)
    return int(match.group(1))


@fixture(scope="session")
def gdfs() -> list[GeoDataFrame]:
    """Fixture to load test data"""
    data = []
    shapefile_paths = [
        os.path.join(TEST_DATA_DIR, f)
        for f in os.listdir(TEST_DATA_DIR)
        if f.endswith(".shp") and re.search(ADMIN_REGEX, f)
    ]
    shapefile_paths.sort(key=get_admin_level_from_file_path)
    for shapefile_path in shapefile_paths:
        gdf = read_file(shapefile_path)
        data.append(gdf)
    return data
