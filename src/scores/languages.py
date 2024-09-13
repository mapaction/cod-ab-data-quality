from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Draft function for scoring languages used within dataset.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["languages"] = checks["language_count"] > 0
    return scores
