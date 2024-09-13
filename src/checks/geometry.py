from geopandas import GeoDataFrame

from src.config import EPSG_WGS84, CheckReturnList
from src.utils import get_epsg_ease

METERS_PER_KM = 1_000_000
PRECISION = 6


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check properties associated with geometry.

    The first section of checks look at validity criteria:
    - geom_is_polygon: Checks if all geometries are Polygon or MultiPolygons.
    - geom_is_xy: Checks that a geometry doesn't contain Z dimension (is 3D).
    - geom_is_valid: Checks that a geometry is valid.
    - geom_invalid_reason: Explains why a polygon is invalid.

    The next section looks at projection and bounds:
    - geom_proj: Gives the EPSG code of the dataset's projection.
    - geom_{min|max}_{x|y}: Gives the bounding box in decimal degrees.

    Finally, areas are calculated:
    - geom_area_km: The sum of individual geometries. Counts overlaped areas twice.
    - geom_area_km_dissolved: The sum of dissolved geometries. This resolves overlaps.
    - geom_area_km_overlap: The area of overlapping polygons. Values <= 1e-6 may be
        false positives. Please rely on `geom_overlaps` for more accurate metrics.

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
            min_x, min_y, max_x, max_y = [
                round(x, PRECISION)
                for x in gdf.geometry.to_crs(EPSG_WGS84).total_bounds
            ]
            epsg_ease = get_epsg_ease(min_y, max_y)
            valid = gdf.copy()
            valid.geometry = valid.geometry.make_valid()
            area = int(valid.geometry.to_crs(epsg_ease).area.sum())
            area_dissolved = int(valid.dissolve().to_crs(epsg_ease).area.sum())
            invalid_reason = ", ".join(
                {
                    reason.split("[")[0]
                    for reason in gdf.geometry.is_valid_reason()
                    if reason != "Valid Geometry"
                },
            )
            row |= {
                "geom_is_polygon": gdf.geometry.geom_type.str.contains("Polygon").all(),
                "geom_is_xy": not gdf.geometry.has_z.any(),
                "geom_is_valid": gdf.geometry.is_valid.all(),
                "geom_invalid_reason": invalid_reason,
                "geom_proj": gdf.geometry.crs.to_epsg(),
                "geom_min_x": min_x,
                "geom_min_y": min_y,
                "geom_max_x": max_x,
                "geom_max_y": max_y,
                "geom_area_km": area / METERS_PER_KM,
                "geom_area_km_dissolved": area_dissolved / METERS_PER_KM,
                "geom_area_km_overlap": (area - area_dissolved) / METERS_PER_KM,
            }
        check_results.append(row)
    return check_results
