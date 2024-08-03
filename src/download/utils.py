from os import getenv

from httpx import Client
from pandas import read_csv
from tenacity import retry, stop_after_attempt, wait_fixed

from . import ATTEMPT, TIMEOUT, WAIT, cwd


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def client_get(url: str):
    """HTTP GET with retries, waiting, and longer timeouts.

    Args:
        url: A valid URL.

    Returns:
        HTTP response.
    """
    with Client(http2=True, timeout=TIMEOUT) as client:
        return client.get(url)


def clean_list(items: list[str]):
    """Strips whitespace and uppercases a list of strings, removing empty strings.

    Args:
        items: A list of str

    Returns:
        A list of strings uppercased and with whitespace trimmed.
    """
    return [item.strip().upper() for item in items if item.strip() != ""]


def get_iso3():
    """Gets a list of ISO-3 values from an environment variable.

    Returns:
        List of ISO-3 values cleaned of potential human error.
    """
    return clean_list(getenv("ISO3", "").split(","))


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
    df = read_csv(cwd / "../../data/metadata.csv", dtype=dtypes)
    records = df.to_dict("records")
    iso3_list = get_iso3()
    if len(iso3_list):
        records = [x for x in records if x["iso3"] in iso3_list]
    result = []
    for record in records:
        for level in range(5):
            if record[f"itos_index_{level}"] is not None:
                result.append({**record, "admin_level": level})
    return result
