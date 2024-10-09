from pandas import DataFrame

from src.config import EPSG_WGS84


def main(checks: DataFrame) -> DataFrame:
    """Creates scores based on valid geometry.

    Args:
        checks: checks DataFrame.

    Returns:
        DataFrame with columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["geometry_valid"] = (
        (
            checks["level"].eq(0) & checks["geom_count"].eq(1)
            | checks["level"].gt(0) & checks["geom_count"].gt(0)
        )
        & checks["geom_empty"].eq(0)
        & checks["geom_not_polygon"].eq(0)
        & checks["geom_has_z"].eq(0)
        & checks["geom_invalid"].eq(0)
        & checks["geom_proj"].eq(EPSG_WGS84)
        & checks["geom_min_x"].ge(-180)
        & checks["geom_min_y"].ge(-90)
        & checks["geom_max_x"].le(180)
        & checks["geom_max_y"].le(90)
    )
    return scores
