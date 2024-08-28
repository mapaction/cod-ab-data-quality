"""Creating the final Excel output of the project."""

from datetime import date

from pandas import DataFrame, ExcelWriter
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from src.config import tables
from src.utils import read_csv


def format_between(format: Format, min: float, max: float):
    """Returns a configuration used for conditional formatting between values in Excel.

    Args:
        min: Minimum value for conditional formatting to apply to.
        max: Maximum value for conditional formatting to apply to.
        format: What formatting to apply when the two conditions above are true.

    Returns:
        Configuration for Excel conditional formatting.
    """
    return {
        "type": "cell",
        "criteria": "between",
        "minimum": min,
        "maximum": max,
        "format": format,
    }


def style(last_row: int, last_col: int, workbook: Workbook, worksheet: Worksheet):
    """Apply red / amber / green styling to excel values that fall between value ranges.

    - Decimals are formatted as percentages.
    - Red formatting is applied for values: 0-33%
    - Yellow formatting is applied for values: 33-66%
    - Green formatting is applied for values: 66-100%

    Args:
        last_row: Index of last row in Excel (0-indexed).
        last_col: Index of last column in Excel (0-indexed).
        workbook: Excel workbook instance.
        worksheet: Excel worksheet instance.
    """
    first_row = 1
    first_col = 1
    format_percent = workbook.add_format({"num_format": "0%"})
    format_rd = workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
    format_yl = workbook.add_format({"bg_color": "#FFEB9C", "font_color": "#9C6500"})
    format_gn = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
    between_rd = format_between(format_rd, 0, 0.333)
    between_yl = format_between(format_yl, 0.333, 0.666)
    between_gn = format_between(format_gn, 0.666, 1)
    worksheet.autofit()
    worksheet.set_column(first_col, last_col, None, format_percent)
    worksheet.conditional_format(first_row, first_col, last_row, last_col, between_rd)
    worksheet.conditional_format(first_row, first_col, last_row, last_col, between_yl)
    worksheet.conditional_format(first_row, first_col, last_row, last_col, between_gn)


def aggregate(df: DataFrame):
    """Summarize scores by averaging scores from each admin level.

    Args:
        df: Resulting DataFrame created by scoring functions.

    Returns:
        Dataframe grouped and averaged by ISO3.
    """
    df = df.drop(columns=["level"])
    df = df.groupby("iso3").mean()
    df["score"] = df.mean(axis=1)
    df = df.sort_values(by=["score"])
    return df


def main(df: DataFrame):
    """Aggregates scores and outputs to an Excel workbook with red/amber/green coloring.

    1. Groups and averages the scores generated in this module and outputs as a CSV.

    2. Applied styling to the dataset generated in step 1 and saves as Excel.

    3. Adds all CSVs generated in previous modules to the Excel workbook.

    4. Adds a final sheet specifying which date the workbook was generated on.

    Args:
        df: checks DataFrame.
    """
    df = aggregate(df)
    df.to_csv(tables / "scores.csv", encoding="utf-8-sig")
    with ExcelWriter(tables / "cod_ab_data_quality.xlsx") as writer:
        df.to_excel(writer, sheet_name="scores")
        if isinstance(writer.book, Workbook):
            style(len(df.index), len(df.columns), writer.book, writer.sheets["scores"])
        for sheet in ["checks", "metadata"]:
            df1 = read_csv(tables / f"{sheet}.csv", datetime_to_date=True)
            df1.to_excel(writer, sheet_name=sheet, index=False)
            writer.sheets[sheet].autofit()
        df_date = DataFrame([{"date": date.today()}])
        df_date.to_excel(writer, sheet_name="date", index=False)
        writer.sheets["date"].autofit()
