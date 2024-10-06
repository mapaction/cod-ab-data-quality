from math import pi

from geopandas import GeoDataFrame, GeoSeries
from shapely import Polygon

from src.config import EPSG_EQUAL_AREA, METERS_PER_KM, CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check for the number of gaps between geometries.

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of check rows to be outputed as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        row = {"iso3": iso3, "level": admin_level}
        if gdf.active_geometry_name:
            valid = gdf.copy()
            valid.geometry = valid.geometry.make_valid()
            interiors = valid.dissolve().explode().interiors.tolist()
            polygons = [Polygon(x) for y in interiors for x in y]
            if len(polygons):
                geometry = GeoSeries(polygons, crs=gdf.crs).to_crs(EPSG_EQUAL_AREA)
                thinness = geometry.map(lambda x: (4 * pi * x.area) / (x.length**2))
                row |= {
                    "geom_gap_area_km": geometry.area.min() / METERS_PER_KM,
                    "geom_gap_thinness": thinness.min(),
                }
            check_results.append(row)
    return check_results
