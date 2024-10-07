from pandas import DataFrame, Series

from src.config import EPSG_WGS84, SLIVER_GAP_AREA_KM, SLIVER_GAP_THINNESS


def score_validity(checks: DataFrame) -> Series:
    """Gives a perfect score if all validity conditions are true.

    Args:
        checks: checks DataFrame.

    Returns:
        Data Series for validity score.
    """
    return (
        checks["geom_count"].gt(0)
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


def score_topology(checks: DataFrame) -> Series:
    """Gives a perfect score if all topology conditions are true.

    Args:
        checks: checks DataFrame.

    Returns:
        Data Series for topology score.
    """
    return (
        (
            checks["geom_gap_area_km"].isna()
            | checks["geom_gap_area_km"].gt(SLIVER_GAP_AREA_KM)
            | checks["geom_gap_thinness"].isna()
            | checks["geom_gap_thinness"].gt(SLIVER_GAP_THINNESS)
        )
        & checks["geom_overlaps_self"].eq(0)
        & checks["geom_not_within_parent"].eq(0)
        & (
            checks["geom_not_within_pcode"].isna()
            | checks["geom_not_within_pcode"].eq(0)
        )
    )


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
    - geometry_hierarchy: scores based on whether layer has valid topology.
    - geometry_areas: scores based on whether each layer has the same area.

    Args:
        checks: checks DataFrame.

    Returns:
        DataFrame with columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["geometry_valid"] = score_validity(checks)
    scores["geometry_topology"] = score_topology(checks)
    return score_areas(checks, scores)
