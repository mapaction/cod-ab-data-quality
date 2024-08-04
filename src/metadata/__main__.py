from logging import getLogger

from pandas import DataFrame
from tqdm import tqdm

from . import columns, tables
from .getters import get_hdx_metadata, get_itos_metadata
from .utils import client_get, join_hdx_metadata, join_itos_metadata

logger = getLogger(__name__)


def get_metadata():
    """Gets metadata for all 249 ISO 3166 country codes.

    Iterates through each location in the OCHA Country and Territory name list and adds
    metadata about those locations from HDX and ITOS.

    Returns:
        A list of country config dicts from OCHA with additional metadata from
        HDX and ITOS.
    """
    url = "https://vocabulary.unocha.org/json/beta-v4/countries.json"
    metadata: list[dict] = client_get(url).json()["data"]
    metadata = [x for x in metadata if x["iso3"] is not None]
    metadata.sort(key=lambda x: x["iso3"])
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso3"])
        row["name"] = row["label"]["default"]
        hdx = get_hdx_metadata(row["iso3"])
        if hdx is not None:
            row = join_hdx_metadata(row, hdx)
        itos = get_itos_metadata(row["iso3"])
        if itos is not None:
            row = join_itos_metadata(row, itos)
    return metadata


def save_metadata(metadata: list[dict]):
    """Saves country metadata as a CSV.

    Although the complete list of country codes contains 249 items, not all of these
    are relevant. Any location that doesn't have a matching URL from either HDX or ITOS
    if filtered out from the list, resulting in 164 locations as of 2024.

    Args:
        metadata: A list of country config dicts.
    """
    df = DataFrame(metadata)
    df = df[df["hdx_url"].notna() | df["itos_url"].notna()]
    df = df[columns]
    dest = tables / "metadata.csv"
    df.to_csv(dest, encoding="utf-8-sig", float_format="%.0f", index=False)


def main():
    """Gets metadata for each Common Operational Dataset (COD).

    This is needed to generate a master list of all available COD datasets with
    all the parameters required to build a download URL for each layer.
    """
    logger.info("starting")
    metadata = get_metadata()
    save_metadata(metadata)
    logger.info("finished")


if __name__ == "__main__":
    main()
