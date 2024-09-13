from typing import Any

from pandas import Timestamp

from src.config import ADMIN_LEVELS


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
        **{
            f"itos_index_{level}": itos["indexes"].get(level)
            for level in range(ADMIN_LEVELS + 1)
        },
    }
