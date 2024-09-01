"""Miscellaneous utilities."""

from os import getenv
from pathlib import Path
from typing import Any

import pandas as pd
from httpx import Client
from pandas import to_datetime
from tenacity import retry, stop_after_attempt, wait_fixed

from .config import ATTEMPT, WAIT, args, tables_dir

# TODO: Could do more with this type, as iso3 and levels keys are required.
type CheckReturnList = list[dict[str, Any]]


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def client_get(url: str, timeout: int, params: dict | None = None):
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


def read_csv(file_path: Path | str, datetime_to_date: bool = False):
    """Pandas read CSV with columns converted to the best possible dtypes.

    Args:
        file_path: CSV file path to read.
        datetime_to_date: Convert datetime to date, needed for export to Excel.

    Returns:
        Pandas DataFrame with converted dtypes.
    """
    df = pd.read_csv(file_path).convert_dtypes()
    for col in df.select_dtypes(include=["string"]):
        try:
            df[col] = to_datetime(df[col], format="ISO8601")
            if datetime_to_date:
                df[col] = df[col].dt.date
        except ValueError:
            pass
    return df


def get_iso3():
    """Gets a list of ISO-3 values from an environment variable or argparser.

    Returns:
        List of ISO-3 values cleaned of potential human error.
    """
    iso3_list = getenv("ISO3", "").split(",")
    if args.iso3:
        iso3_list = args.iso3.split(",")
    iso3_list_cleaned = [x.strip().upper() for x in iso3_list if x.strip() != ""]
    return iso3_list_cleaned


def get_metadata():
    """Load the metadata table and create a list with every COD admin layer to download.

    For example, returns entries for AFG_ADM0, AFG_ADM1, AFG_ADM2, AGO_ADM0, etc.

    Returns:
        List containing the following information to download each COD: ISO-3 code,
        admin level, URL and layer index of the COD on the ArcGIS server.
    """
    df = read_csv(tables_dir / "metadata.csv")
    records = df.to_dict("records")
    iso3_list = get_iso3()
    if len(iso3_list):
        records = [x for x in records if x["iso3"] in iso3_list]
    return records
