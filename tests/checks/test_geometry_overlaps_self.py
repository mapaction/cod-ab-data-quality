import pytest
from geopandas import GeoDataFrame

from src.checks.geometry_overlaps_self import main


@pytest.mark.slow
def test_mdg_geometry_overlaps_self(iso3: str, gdfs: list[GeoDataFrame]) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 0,
            "geom_overlaps_self": 0,
        },
        {
            "iso3": "MDG",
            "level": 1,
            "geom_overlaps_self": 0,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "geom_overlaps_self": 0,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "geom_overlaps_self": 0,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "geom_overlaps_self": 0,
        },
    ]
    assert actual == expected
