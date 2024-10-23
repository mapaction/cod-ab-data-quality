from logging import getLogger
from typing import Any

from hdx.location.country import Country
from pandas import DataFrame
from tqdm import tqdm

from src.config import metadata_columns, tables_dir
from src.utils import get_iso3

from .getters import get_hdx_metadata, get_itos_metadata
from .join import join_hdx_metadata, join_itos_metadata

logger = getLogger(__name__)


def get_metadata() -> list[dict[str, Any]]:
    """Gets metadata for all 249 ISO 3166 country codes.

    Iterates through each location in HDX countries and adds metadata about those
    locations from HDX and ITOS.

    Returns:
        A list of country config dicts from HDX countries with additional metadata from
        HDX and ITOS.
    """
    metadata = [
        {
            "iso3": iso3,
            "iso2": Country.get_iso2_from_iso3(iso3),
            "name": Country.get_country_name_from_iso3(iso3),
        }
        for iso3 in Country.countriesdata()["countries"]
        if iso3 is not None
    ]
    iso3_list = get_iso3()
    if len(iso3_list):
        metadata = [x for x in metadata if x["iso3"] in iso3_list]
    metadata.sort(key=lambda x: x["iso3"])
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso3"])
        hdx = get_hdx_metadata(row["iso3"])
        if hdx is not None:
            row.update(join_hdx_metadata(hdx))
        itos = get_itos_metadata(row["iso3"])
        if itos is not None:
            row.update(join_itos_metadata(itos))
    return metadata


def save_metadata(metadata: list[dict]) -> None:
    """Saves country metadata as a CSV.

    Although the complete list of country codes contains 249 items, not all of these
    are relevant. Any location that doesn't have a matching URL from either HDX or ITOS
    if filtered out from the list, resulting in 164 locations as of 2024.

    Args:
        metadata: A list of country config dicts.
    """
    output = DataFrame.from_records(metadata).convert_dtypes()
    output = output[output["hdx_url"].notna() | output["itos_url"].notna()]
    output = output[metadata_columns]
    output.to_csv(tables_dir / "metadata.csv", index=False, encoding="utf-8-sig")


def main() -> None:
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
