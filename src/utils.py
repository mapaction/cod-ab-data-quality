"""Miscellaneous utilities."""

from os import getenv
from typing import Any

from httpx import Client
from pandas import read_csv
from tenacity import retry, stop_after_attempt, wait_fixed

from .config import ATTEMPT, WAIT, args, tables

# A return type for the checks in /checks.
# Could do more with this type, as iso3 and levels keys are required.
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
    dtypes = {
        "itos_level": "Int8",
        "itos_index_0": "Int8",
        "itos_index_1": "Int8",
        "itos_index_2": "Int8",
        "itos_index_3": "Int8",
        "itos_index_4": "Int8",
    }
    df = read_csv(tables / "metadata.csv", dtype=dtypes)
    records = df.to_dict("records")
    iso3_list = get_iso3()
    if len(iso3_list):
        records = [x for x in records if x["iso3"] in iso3_list]
    return records
