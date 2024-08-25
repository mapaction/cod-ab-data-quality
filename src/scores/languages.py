"""Scoring language info."""

from random import random

from pandas import DataFrame


def main(df: DataFrame):
    """Scores languages used within dataset.

    Args:
        df: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    df["languages"] = [random() for _ in df.index]
    return df
