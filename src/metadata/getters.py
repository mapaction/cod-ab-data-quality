from re import compile
from typing import Any, Literal

from src.config import TIMEOUT
from src.utils import client_get


def get_hdx_metadata(iso3: str) -> dict[str, Any]:
    """Get HDX metadata associated with a COD on HDX.

    This is useful for accessing information such as what license does this data fall
    under, which organization contributed this data, what is the source of the data,
    etc.

    Args:
        iso3: A valid ISO 3166-1 alpha-3 code.

    Returns:
        A complete package of metadata describing the COD resource on HDX.
    """
    url = "https://data.humdata.org/api/3/action/package_show"
    params = {"id": f"cod-ab-{iso3.lower()}"}
    result: dict = client_get(url, TIMEOUT, params).json().get("result")
    return result


def get_service_url(directory: str, iso3: str) -> str:
    """Gets the URL of a COD's ArcGIS Feature Service from ITOS.

    Args:
        directory: Either COD_External or COD_NO_GEOM_CHECK.
        iso3: A valid ISO 3166-1 alpha-3 code.

    Returns:
        The URL for a COD's ArcGIS Feature Service.
    """
    base = "https://codgis.itos.uga.edu/arcgis/rest/services"
    return f"{base}/{directory}/{iso3}_pcode/FeatureServer"


def get_service(
    iso3: str,
) -> tuple[Any | None, Literal["COD_NO_GEOM_CHECK", "COD_External"], str]:
    """Gets key metadata about a COD from the ITOS ArcGIS server.

    Args:
        iso3: A valid ISO 3166-1 alpha-3 code.

    Returns:
        Metadata about a COD, including the list of layers available for a location,
        which service directory it belongs to, and the URL of the service.
    """
    params = {"f": "json"}
    directory = "COD_External"
    url = get_service_url(directory, iso3)
    service = client_get(url, TIMEOUT, params).json()
    if "error" in service:
        directory = "COD_NO_GEOM_CHECK"
        url = get_service_url(directory, iso3)
        service = client_get(url, TIMEOUT, params).json()
        if "error" in service:
            service = {"layers": None}
    return service["layers"], directory, url.split("?")[0]


def get_layer_indexes(layers: list[dict[str, Any]]) -> dict[str, Any]:
    """A list of layer indexes containing admin polygons for the COD's Feature Service.

    The Feature Service for a COD will contain many layers identified by their index
    location (0, 1, 2, 3, etc). Admin Layers are labeled as "Admin0", "Admin1", etc.
    Sometimes index 0 corresponds to "Admin0", but this is not always the case. This
    function searches for every layer containing "Admin" and its corresponding index.

    Args:
        layers: List of layers from an ArcGIS Feature Service.

    Returns:
        A dict where each key represents the admin level, and each value the index
        location it can be accessed from.
    """
    p = compile(r"Admin")
    layers = [x for x in layers if p.search(x["name"])]
    layers = [x for x in layers if x["geometryType"] == "esriGeometryPolygon"]
    indexes = {}
    idx = 0
    for layer in layers:
        lvl = int(layer["name"][-1])
        idx = layer["id"]
        indexes[lvl] = idx
    return indexes


def get_itos_metadata(iso3: str) -> dict[str, Any] | None:
    """Gets COD metadata from the ITOS ArcGIS server if it exists there.

    Args:
        iso3: A valid ISO 3166-1 alpha-3 code.

    Returns:
        Metadata that can be used to download CODs from the ITOS ArcGIS server.
    """
    layers, directory, url = get_service(iso3)
    if layers is None:
        return None
    indexes = get_layer_indexes(layers)
    return {"url": url, "directory": directory, "indexes": indexes}
