"""Scoring language info."""

from datetime import date

from pandas import DataFrame, ExcelWriter, read_csv
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from ..config import score_columns, tables


def get_config(min: float, max: float, format: Format):
    """_summary_.

    Args:
        min: _description_
        max: _description_
        format: _description_

    Returns:
        _description_
    """
    return {
        "type": "cell",
        "criteria": "between",
        "minimum": min,
        "maximum": max,
        "format": format,
    }


def style(last_row: int, last_col: int, workbook: Workbook, worksheet: Worksheet):
    """_summary_.

    Args:
        last_row: _description_
        last_col: _description_
        workbook: _description_
        worksheet: _description_
    """
    first_row = 1
    first_col = 1
    format_percent = workbook.add_format({"num_format": "0%"})
    format_rd = workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
    format_yl = workbook.add_format({"bg_color": "#FFEB9C", "font_color": "#9C6500"})
    format_gn = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
    config_rd = get_config(0, 0.333, format_rd)
    config_yl = get_config(0.333, 0.666, format_yl)
    config_gn = get_config(0.666, 1, format_gn)
    worksheet.autofit()
    worksheet.set_column(first_col, last_col, None, format_percent)
    worksheet.conditional_format(first_row, first_col, last_row, last_col, config_rd)
    worksheet.conditional_format(first_row, first_col, last_row, last_col, config_yl)
    worksheet.conditional_format(first_row, first_col, last_row, last_col, config_gn)


def aggregate(df: DataFrame):
    """_summary_.

    Args:
        df: _description_

    Returns:
        _description_
    """
    df = df[score_columns]
    df = df.groupby("iso3").mean()
    df["score"] = df.mean(axis=1)
    df = df.sort_values(by=["score"])
    return df


def main(df: DataFrame):
    """Scores languages used within dataset.

    Args:
        df: checks DataFrame.
    """
    df = aggregate(df)
    df.to_csv(tables / "scores.csv", encoding="utf-8-sig")
    with ExcelWriter(tables / "cod-ab-data-quality.xlsx") as writer:
        df.to_excel(writer, sheet_name="scores")
        if isinstance(writer.book, Workbook):
            style(len(df.index), len(df.columns), writer.book, writer.sheets["scores"])
        for sheet in ["checks", "metadata"]:
            df1 = read_csv(tables / f"{sheet}.csv")
            df1.to_excel(writer, sheet_name=sheet, index=False)
            writer.sheets[sheet].autofit()
        df_date = DataFrame([{"date": date.today()}])
        df_date.to_excel(writer, sheet_name="date", index=False)
        writer.sheets["date"].autofit()
