from pandas import DataFrame

from src.config import EPSG_WGS84


def score_bounds(checks: DataFrame, scores: DataFrame) -> DataFrame:
    """Gives a perfect score if all bounds are exactly the same.

    Partial scores are given by the fraction of remaining layers that all share the same
    bounds.

    Args:
        checks: checks DataFrame.
        scores: scores DataFrame.

    Returns:
        DataFrame with added column for bounds score.
    """
    bounds = ["geom_min_x", "geom_min_y", "geom_max_x", "geom_max_y"]
    summary = checks.copy()
    summary["bounds"] = checks[bounds].map(str).agg(",".join, axis=1)
    group = summary[["iso3", "bounds"]].groupby("iso3").agg(["count", "nunique"])
    group.columns = group.columns.get_level_values(1)
    group["geometry_bounds"] = (group["count"] - group["nunique"] + 1) / group["count"]
    return scores.merge(group["geometry_bounds"], on="iso3")


def score_areas(checks: DataFrame, scores: DataFrame) -> DataFrame:
    """Gives a perfect score if all areas are exactly the same.

    Partial scores are given by the fraction of remaining layers that all share the same
    area.

    Args:
        checks: checks DataFrame.
        scores: scores DataFrame.

    Returns:
        DataFrame with added column for area score.
    """
    group = checks[["iso3", "geom_area_km"]].groupby("iso3").agg(["count", "nunique"])
    group.columns = group.columns.get_level_values(1)
    group["geometry_area"] = (group["count"] - group["nunique"] + 1) / group["count"]
    return scores.merge(group["geometry_area"], on="iso3")


def main(checks: DataFrame) -> DataFrame:
    """Creates scores based on geometry.

    - geometry_valid: scores based on whether each layer has valid geometry.
    - geometry_hierarchy: scores based on whether each layer nests perfectly to parents.
    - geometry_bounds: scores based on whether each layer has the same bounds.
    - geometry_areas: scores based on whether each layer has the same area.

    Args:
        checks: checks DataFrame.

    Returns:
        DataFrame with columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["geometry_valid"] = (
        checks["geom_not_empty"]
        & checks["geom_is_polygon"]
        & checks["geom_is_xy"]
        & checks["geom_is_valid"]
        & checks["geom_proj"].eq(EPSG_WGS84)
        & checks["geom_overlaps_self"].eq(0)
    )
    scores["geometry_hierarchy"] = checks["geom_overlaps_parent"].eq(0)
    scores = score_bounds(checks, scores)
    return score_areas(checks, scores)
