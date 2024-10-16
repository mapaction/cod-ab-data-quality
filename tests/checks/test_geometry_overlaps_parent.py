import pytest
from geopandas import GeoDataFrame

from src.checks.geometry_overlaps_parent import main


@pytest.mark.slow
def test_mdg_geometry_overlaps_parent(iso3: str, gdfs: list[GeoDataFrame]) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 1,
            "geom_overlaps_parent": 0,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "geom_overlaps_parent": 0,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "geom_overlaps_parent": 0,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "geom_overlaps_parent": 82,
        },
    ]
    assert actual == expected
