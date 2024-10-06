from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Scores columns used within dataset.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level", "language_count"]].copy()
    scores["columns_required"] = (
        checks["levels_with_data"].eq(checks["level"] + 1)
        & checks["levels_with_name"].eq(checks["level"] + 1)
        & checks["levels_with_pcode"].eq(checks["level"] + 1)
        & checks["name_count"].eq(checks["language_count"] * (checks["level"] + 1))
    )
    return scores.drop(columns=["language_count"])
