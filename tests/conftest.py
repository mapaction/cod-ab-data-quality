"""Test configuration file."""

from pathlib import Path

from geopandas import GeoDataFrame, read_file
from pytest import fixture


@fixture(scope="session")
def gdfs() -> list[GeoDataFrame]:
    """Fixture to load test data."""
    data = []
    test_data_dir = Path("tests/test_data")
    for file_path in sorted(test_data_dir.glob("*.gpkg")):
        data.append(read_file(file_path))
    return data
