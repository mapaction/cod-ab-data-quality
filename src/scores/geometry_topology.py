from pandas import DataFrame

from src.config import SLIVER_GAP_AREA_KM, SLIVER_GAP_THINNESS


def main(checks: DataFrame) -> DataFrame:
    """Creates scores based on geometry topology.

    Args:
        checks: checks DataFrame.

    Returns:
        DataFrame with columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["geometry_topology"] = (
        (
            checks["geom_gap_area_km"].isna()
            | checks["geom_gap_area_km"].gt(SLIVER_GAP_AREA_KM)
            | checks["geom_gap_thinness"].isna()
            | checks["geom_gap_thinness"].gt(SLIVER_GAP_THINNESS)
        )
        & checks["geom_overlaps_self"].eq(0)
        & checks["geom_not_within_parent"].eq(0)
        & checks["geom_within_name_mismatch"].eq(0)
        & checks["geom_within_pcode_mismatch"].eq(0)
    )
    return scores
