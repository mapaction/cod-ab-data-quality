"""Scoring date info."""

from random import random

from pandas import DataFrame


def main(df: DataFrame):
    """Scores date values within dataset.

    Args:
        df: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    df["dates"] = [random() for _ in df.index]
    return df
