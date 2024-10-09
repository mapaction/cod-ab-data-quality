import pytest
from geopandas import GeoDataFrame

from src.checks.geometry_within_parent import main


@pytest.mark.slow
def test_mdg_geometry_within_parent(iso3: str, gdfs: list[GeoDataFrame]) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 0,
            "geom_not_within_parent": 0,
        },
        {
            "iso3": "MDG",
            "level": 1,
            "geom_not_within_parent": 2,
            "geom_not_within_pcode": 0,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "geom_not_within_parent": 0,
            "geom_not_within_pcode": 0,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "geom_not_within_parent": 0,
            "geom_not_within_pcode": 0,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "geom_not_within_parent": 87,
            "geom_not_within_pcode": 0,
        },
    ]
    assert actual == expected
