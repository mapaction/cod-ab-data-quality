import re
from pathlib import Path

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
    test_data_dir = Path("tests/test_data")
    for file_path in sorted(test_data_dir.glob("*.gpkg")):
        data.append(read_file(file_path))
    return data
