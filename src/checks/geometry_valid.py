from geopandas import GeoDataFrame

from src.config import (
    EPSG_WGS84,
    GEOJSON_PRECISION,
    METERS_PER_KM,
    POLYGON,
    VALID_GEOMETRY,
    CheckReturnList,
)
from src.utils import get_epsg_ease


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check properties associated with geometry.

    The first section of checks look at validity criteria:
    - geom_count: Count of geometries.
    - geom_empty: Count of empty geometries.
    - geom_not_polygon: Count of geometries which are not a Polygon or MultiPolygons.
    - geom_has_z: Count of geometries with a Z dimension (are 3D).
    - geom_is_valid: Count of invalid geometries.
    - geom_invalid_reason: Explains why geometries are invalid.

    The next section looks at projection and bounds:
    - geom_proj: Gives the EPSG code of the dataset's projection.
    - geom_{min|max}_{x|y}: Gives the bounding box in decimal degrees.

    Finally, areas are calculated:
    - geom_area_km: The sum area of individual geometries.

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
                round(x, GEOJSON_PRECISION)
                for x in gdf.geometry.to_crs(EPSG_WGS84).total_bounds
            ]
            epsg_ease = get_epsg_ease(min_y, max_y)
            area = int(gdf.geometry.to_crs(epsg_ease).area.sum())
            invalid_reason = ", ".join(
                {
                    reason.split("[")[0]
                    for reason in gdf.geometry.is_valid_reason()
                    if reason != VALID_GEOMETRY
                },
            )
            row |= {
                "geom_count": len(gdf.index),
                "geom_empty": len(
                    gdf[gdf.geometry.is_empty | gdf.geometry.isna()].index,
                ),
                "geom_not_polygon": len(
                    gdf[~gdf.geometry.geom_type.str.contains(POLYGON)].index,
                ),
                "geom_has_z": len(gdf[gdf.geometry.has_z].index),
                "geom_invalid": len(gdf[~gdf.geometry.is_valid].index),
                "geom_invalid_reason": invalid_reason,
                "geom_proj": gdf.geometry.crs.to_epsg(),
                "geom_min_x": min_x,
                "geom_min_y": min_y,
                "geom_max_x": max_x,
                "geom_max_y": max_y,
                "geom_area_km": area / METERS_PER_KM,
            }
            if "AREA_SQKM" in gdf.columns:
                row["geom_area_km_attr"] = gdf["AREA_SQKM"].sum()
        check_results.append(row)
    return check_results
