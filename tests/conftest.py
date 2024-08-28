"""Test configuration file."""

from pathlib import Path

import pytest
from geopandas import GeoDataFrame, read_file


@pytest.fixture(scope="session")
def iso3():
    """Fixture to load test data."""
    return "MDG"


@pytest.fixture(scope="session")
def gdfs() -> list[GeoDataFrame]:
    """Fixture to load test data."""
    data = []
    test_data_dir = Path("tests/test_data")
    for file_path in sorted(test_data_dir.glob("*.gpkg")):
        data.append(read_file(file_path))
    return data
