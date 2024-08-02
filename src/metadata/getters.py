from re import compile

from .utils import client_get


def get_hdx_metadata(iso3: str):
    id = f"cod-ab-{iso3.lower()}"
    url = f"https://data.humdata.org/api/3/action/package_show?id={id}"
    return client_get(url).json().get("result")


def get_service_url(path: str, iso3: str):
    base = "https://codgis.itos.uga.edu/arcgis/rest/services"
    return f"{base}/{path}/{iso3}_pcode/FeatureServer?f=json"


def get_service(iso3: str):
    path = "COD_External"
    url = get_service_url(path, iso3)
    service = client_get(url).json()
    if "error" in service:
        path = "COD_NO_GEOM_CHECK"
        url = get_service_url(path, iso3)
        service = client_get(url).json()
        if "error" in service:
            service = None
    return service, path, url.split("?")[0]


def get_layer_indexes(service: dict):
    p = compile(r"Admin")
    layers = [x for x in service["layers"] if p.search(x["name"])]
    layers = [x for x in layers if x["geometryType"] == "esriGeometryPolygon"]
    indexes = {}
    idx = 0
    for layer in layers:
        lvl = int(layer["name"][-1])
        idx = layer["id"]
        indexes[lvl] = idx
    return indexes


def get_itos_metadata(iso3: str):
    service, path, url = get_service(iso3)
    if service is None:
        return None
    indexes = get_layer_indexes(service)
    result = {"url": url, "path": path, "indexes": indexes}
    return result
