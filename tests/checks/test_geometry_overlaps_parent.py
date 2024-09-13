from geopandas import GeoDataFrame

from checks.geometry_overlaps_parent import main


def test_mdg_geometry_overlaps_parent(iso3: str, gdfs: list[GeoDataFrame]) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 1,
            "geom_parent_overlaps": 0,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "geom_parent_overlaps": 0,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "geom_parent_overlaps": 0,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "geom_parent_overlaps": 82,
        },
    ]
    assert actual == expected
