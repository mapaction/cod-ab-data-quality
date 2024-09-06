from typing import Any

from pandas import Timestamp


def join_hdx_metadata(hdx: dict) -> dict[str, Any]:
    """Returns new properties for contry config from HDX.

    Args:
        hdx: HDX metadata from https://data.humdata.org/api/3/action/package_show.

    Returns:
        Country config supplemented with extra properties.
    """
    return {
        "hdx_date": Timestamp(hdx["dataset_date"][1:11]),
        "hdx_update": Timestamp(hdx["last_modified"][:10]),
        "hdx_source_1": hdx["dataset_source"],
        "hdx_source_2": hdx["organization"]["title"],
        "hdx_license": hdx["license_title"],
        "hdx_url": f"https://data.humdata.org/dataset/{hdx["name"]}",
    }


def join_itos_metadata(itos: dict) -> dict[str, Any]:
    """Returns new properties for contry config from ITOS.

    Args:
        itos: ITOS Metadata from https://codgis.itos.uga.edu/arcgis/rest/services.

    Returns:
        Country config supplemented with extra properties.
    """
    return {
        "itos_url": itos["url"],
        "itos_service": itos["directory"],
        "itos_level": list(itos["indexes"].keys())[-1],
        "itos_index_0": itos["indexes"].get(0),
        "itos_index_1": itos["indexes"].get(1),
        "itos_index_2": itos["indexes"].get(2),
        "itos_index_3": itos["indexes"].get(3),
        "itos_index_4": itos["indexes"].get(4),
    }
