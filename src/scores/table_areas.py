from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Function for scoring the area column used within a dataset.

    Gives a perfect score if the AREA_SQKM column is detected and is less than 1% of
    the calculated value.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["area_sqkm"] = checks["geom_area_km_attr"].gt(0) & (
        checks[["geom_area_km", "geom_area_km_attr"]]
        .pct_change(axis=1, fill_method=None)["geom_area_km_attr"]
        .abs()
        .lt(0.01)
    )
    return scores
