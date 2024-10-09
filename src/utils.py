from argparse import ArgumentParser, Namespace
from collections.abc import Hashable
from os import getenv
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from httpx import Client, Response
from pandas import DataFrame, to_datetime
from tenacity import retry, stop_after_attempt, wait_fixed

from .config import ATTEMPT, WAIT, tables_dir


def parse_args(argv: list[str] | None = None) -> Namespace:
    """Parses command line arguments.

    Args:
        argv: sys.argv. Defaults to None.

    Returns:
        argparse Namespace.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--iso3",
        help="Comma separated list of ISO3 codes used by commands.",
    )
    parser.add_argument(
        "--checks-include",
        help="Comma separated checks to include.",
    )
    parser.add_argument(
        "--checks-exclude",
        help="Comma separated checks to exclude.",
    )
    return parser.parse_args(argv)


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def client_get(url: str, timeout: int, params: dict | None = None) -> Response:
    """HTTP GET with retries, waiting, and longer timeouts.

    Args:
        url: A valid URL.
        timeout: Amount in seconds to wait between retries.
        params: Optional URL query parameters included in the request.

    Returns:
        HTTP response.
    """
    with Client(http2=True, timeout=timeout) as client:
        return client.get(url, params=params)


def read_csv(file_path: Path | str, *, datetime_to_date: bool = False) -> DataFrame:
    """Pandas read CSV with columns converted to the best possible dtypes.

    Args:
        file_path: CSV file path to read.
        datetime_to_date: Convert datetime to date, needed for export to Excel.

    Returns:
        Pandas DataFrame with converted dtypes.
    """
    df_csv = pd.read_csv(file_path).convert_dtypes()
    for col in df_csv.select_dtypes(include=["string"]):
        try:
            df_csv[col] = to_datetime(df_csv[col], format="ISO8601")
            if datetime_to_date:
                df_csv[col] = df_csv[col].dt.date
        except ValueError:
            pass
    return df_csv


def get_iso3() -> list[str]:
    """Gets a list of ISO-3 values from an environment variable or argparser.

    Returns:
        List of ISO-3 values cleaned of potential human error.
    """
    args = parse_args()
    iso3_list = getenv("ISO3", "").split(",")
    if args.iso3:
        iso3_list = args.iso3.split(",")
    return [x.strip().upper() for x in iso3_list if x.strip() != ""]


def get_checks_filter() -> tuple[list[str], list[str]]:
    """Gets a list of checks from an environment variable or argparser.

    Returns:
        List of checks values cleaned of potential human error.
    """
    args = parse_args()
    checks_include = getenv("CHECKS_INCLUDE", "").split(",")
    checks_exclude = getenv("CHECKS_EXCLUDE", "").split(",")
    if args.checks_include:
        checks_include = args.checks_include.split(",")
    if args.checks_exclude:
        checks_exclude = args.checks_exclude.split(",")
    checks_include = [x.strip().lower() for x in checks_include if x.strip() != ""]
    checks_exclude = [x.strip().lower() for x in checks_exclude if x.strip() != ""]
    return checks_include, checks_exclude


def get_metadata() -> list[dict[Hashable, Any]]:
    """Load the metadata table and create a list with every COD admin layer to download.

    For example, returns entries for AFG_ADM0, AFG_ADM1, AFG_ADM2, AGO_ADM0, etc.

    Returns:
        List containing the following information to download each COD: ISO-3 code,
        admin level, URL and layer index of the COD on the ArcGIS server.
    """
    metadata = read_csv(tables_dir / "metadata.csv")
    records = metadata.to_dict("records")
    iso3_list = get_iso3()
    if len(iso3_list):
        records = [x for x in records if x["iso3"] in iso3_list]
    return records


def get_epsg_ease(min_lat: float, max_lat: float) -> Literal[6931, 6932, 6933]:
    """Gets the code for appropriate Equal-Area Scalable Earth grid based on latitude.

    Args:
        min_lat: Minimum latitude of geometry from bounds.
        max_lat: Maximum latitude of geometry from bounds.

    Returns:
        EPSG for global EASE grid if area touches neither or both poles, otherwise a
        north or south grid if the area touches either of those zones.
    """
    latitude_poles = 80
    latitude_equator = 0
    epsg_ease_north = 6931
    epsg_ease_south = 6932
    epsg_ease_global = 6933
    if max_lat >= latitude_poles and min_lat >= latitude_equator:
        return epsg_ease_north
    if min_lat <= -latitude_poles and max_lat <= latitude_equator:
        return epsg_ease_south
    return epsg_ease_global


def is_empty(string: str) -> bool:
    """Checks if string is empty.

    Args:
        string: Any valid string.

    Returns:
        True if string is only whitespace.
    """
    return str(string).strip() == ""
