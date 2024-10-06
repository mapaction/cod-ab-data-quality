from dateutil.relativedelta import relativedelta
from pandas import DataFrame, Timestamp


def main(checks: DataFrame) -> DataFrame:
    """Function for scoring date values within dataset.

    Gives a perfect score if there is only one date value for the "date" and "validOn"
    columns, as well as whether the "validOn" column is less than 1 year.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["dates"] = (
        checks["date_count"].eq(1)
        & checks["update_count"].eq(1)
        & checks["update_1"].gt(Timestamp.now() - relativedelta(years=1))
    )
    return scores
