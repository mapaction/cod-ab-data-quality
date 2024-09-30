from dateutil.relativedelta import relativedelta
from pandas import DataFrame, Timestamp


def main(checks: DataFrame) -> DataFrame:
    """Draft function for scoring date values within dataset.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["dates"] = checks["update_1"] > Timestamp.now() - relativedelta(years=1)
    return scores
