import pytest
from geopandas import GeoDataFrame

from src.checks.geometry import main


@pytest.mark.slow
def test_mdg_geometry(iso3: str, gdfs: list[GeoDataFrame]) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 0,
            "geom_not_empty": True,
            "geom_is_polygon": True,
            "geom_is_xy": True,
            "geom_is_valid": True,
            "geom_invalid_reason": "",
            "geom_proj": 4326,
            "geom_min_x": 43.176924,
            "geom_min_y": -25.605753,
            "geom_max_x": 50.484852,
            "geom_max_y": -11.951388,
            "geom_area_km": 592192.582884,
        },
        {
            "iso3": "MDG",
            "level": 1,
            "geom_not_empty": True,
            "geom_is_polygon": True,
            "geom_is_xy": True,
            "geom_is_valid": True,
            "geom_invalid_reason": "",
            "geom_proj": 4326,
            "geom_min_x": 43.176924,
            "geom_min_y": -25.605753,
            "geom_max_x": 50.484852,
            "geom_max_y": -11.951388,
            "geom_area_km": 592192.582884,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "geom_not_empty": True,
            "geom_is_polygon": True,
            "geom_is_xy": True,
            "geom_is_valid": True,
            "geom_invalid_reason": "",
            "geom_proj": 4326,
            "geom_min_x": 43.176924,
            "geom_min_y": -25.605753,
            "geom_max_x": 50.484852,
            "geom_max_y": -11.951388,
            "geom_area_km": 592192.582884,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "geom_not_empty": True,
            "geom_is_polygon": True,
            "geom_is_xy": True,
            "geom_is_valid": True,
            "geom_invalid_reason": "",
            "geom_proj": 4326,
            "geom_min_x": 43.176924,
            "geom_min_y": -25.605753,
            "geom_max_x": 50.484852,
            "geom_max_y": -11.951388,
            "geom_area_km": 592192.582884,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "geom_not_empty": True,
            "geom_is_polygon": True,
            "geom_is_xy": True,
            "geom_is_valid": False,
            "geom_invalid_reason": "Ring Self-intersection",
            "geom_proj": 4326,
            "geom_min_x": 43.176924,
            "geom_min_y": -25.605753,
            "geom_max_x": 50.484852,
            "geom_max_y": -11.951388,
            "geom_area_km": 592192.582884,
        },
    ]
    assert actual == expected
