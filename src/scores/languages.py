"""Scoring language info."""

from pandas import DataFrame


def main(df: DataFrame):
    """Draft function for scoring languages used within dataset.

    Args:
        df: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    df_score = df[["iso3", "level"]].copy()
    df_score["languages"] = df["language_count"] > 0
    return df_score
