"""Scoring date info."""

from datetime import UTC, datetime

from dateutil.relativedelta import relativedelta
from pandas import DataFrame


def main(df: DataFrame):
    """Draft function for scoring date values within dataset.

    Args:
        df: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    df_score = df[["iso3", "level"]].copy()
    df_score["dates"] = df["update_1"] > datetime.now(tz=UTC) - relativedelta(years=3)
    return df_score
