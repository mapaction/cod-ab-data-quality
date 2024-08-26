"""Functions for adding properties to existing dictionaries."""

from datetime import datetime as dt


def join_hdx_metadata(row: dict, hdx: dict):
    """Adds new properties to contry config from HDX.

    Args:
        row: Country config from https://vocabulary.unocha.org/json/beta-v4/countries.json.
        hdx: HDX metadata from https://data.humdata.org/api/3/action/package_show.

    Returns:
        Country config supplemented with extra properties.
    """
    row["hdx_date"] = dt.fromisoformat(hdx["dataset_date"][1:11])
    row["hdx_update"] = dt.fromisoformat(hdx["last_modified"][:10])
    row["hdx_source_1"] = hdx["dataset_source"]
    row["hdx_source_2"] = hdx["organization"]["title"]
    row["hdx_license"] = hdx["license_title"]
    row["hdx_url"] = f"https://data.humdata.org/dataset/cod-ab-{row['iso3'].lower()}"
    return row


def join_itos_metadata(row: dict, itos: dict):
    """Adds new properties to contry config from ITOS.

    Args:
        row: Country config from https://vocabulary.unocha.org/json/beta-v4/countries.json.
        itos: ITOS Metadata from https://codgis.itos.uga.edu/arcgis/rest/services.

    Returns:
        Country config supplemented with extra properties.
    """
    row["itos_url"] = itos["url"]
    row["itos_service"] = itos["directory"]
    row["itos_level"] = list(itos["indexes"].keys())[-1]
    for n in range(5):
        row[f"itos_index_{n}"] = itos["indexes"].get(n)
    return row
