from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Creates scores based on geometry area.

    Args:
        checks: checks DataFrame.

    Returns:
        DataFrame with columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    group = checks[["iso3", "geom_area_km"]].groupby("iso3").agg(["count", "nunique"])
    group.columns = group.columns.get_level_values(1)
    group["geometry_area"] = (group["count"] - group["nunique"] + 1) / group["count"]
    return scores.merge(group["geometry_area"], on="iso3")
