from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Scores columns used within dataset.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["table_names"] = (
        checks["name_column_levels"].eq(checks["level"] + 1)
        & checks["name_column_count"].ge(
            checks["language_count"] * (checks["level"] + 1),
        )
        & checks["name_cell_empty"].eq(0)
    )
    return scores
