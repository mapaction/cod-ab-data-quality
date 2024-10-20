from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Scores columns used within dataset.

    Layers which have all required P-Code columns (ADM2_PCODE), with no empty cells,
    only alphanumeric characters, starting with a valid ISO-2 code, and hierarchical
    nesting codes.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["table_pcodes"] = (
        checks["pcode_column_levels"].eq(checks["level"] + 1)
        & checks["pcode_empty"].eq(0)
        & checks["pcode_not_iso2"].eq(0)
        & checks["pcode_not_alnum"].eq(0)
        & checks["pcode_lengths"].eq(1)
        & checks["pcode_duplicated"].eq(0)
        & checks["pcode_not_nested"].eq(0)
    )
    return scores
