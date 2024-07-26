from datetime import date
from re import compile

from .utils import client_get


def get_hdx_metadata(iso3: str):
    id = f"cod-ab-{iso3.lower()}"
    url = f"https://data.humdata.org/api/3/action/package_show?id={id}"
    return client_get(url).json().get("result")


def get_service_url(path: str, iso3: str):
    base = "https://codgis.itos.uga.edu/arcgis/rest/services"
    return f"{base}/{path}/{iso3}_pcode/FeatureServer?f=json"


def get_layer_url(path: str, iso3: str, idx: int):
    base = "https://codgis.itos.uga.edu/arcgis/rest/services"
    query = "f=json&where=1=1&outFields=*&resultRecordCount=1&returnGeometry=false"
    return f"{base}/{path}/{iso3}_pcode/FeatureServer/{idx}/query?{query}"


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


def get_layer(service: dict, path: str, iso3: str):
    p = compile(r"Admin")
    layers = [x for x in service["layers"] if p.search(x["name"])]
    layers = [x for x in layers if x["geometryType"] == "esriGeometryPolygon"]
    indexes = {}
    idx = 0
    for layer in layers:
        lvl = int(layer["name"][-1])
        idx = layer["id"]
        indexes[lvl] = idx
    url = get_layer_url(path, iso3, idx)
    r = client_get(url).json()
    attrs = r["features"][0]["attributes"]
    return attrs, indexes, lvl


def get_languages(attrs: dict, lvl: int):
    keys = list(attrs.keys())
    p = compile(rf"^ADM{lvl}_\w{{2}}$")
    langs = [x.split("_")[1].lower() for x in keys if p.search(x)]
    langs = list(dict.fromkeys(langs))
    return langs


def get_itos_metadata(iso3: str):
    service, path, url = get_service(iso3)
    if service is None:
        return None
    attrs, indexes, lvl = get_layer(service, path, iso3)
    langs = get_languages(attrs, lvl)
    result = {"url": url, "path": path, "langs": langs, "indexes": indexes}
    if attrs.get("date") is None:
        result["date"] = None
        result["update"] = None
        return result
    result["date"] = date.fromtimestamp(attrs["date"] / 1000)
    result["update"] = date.fromtimestamp(attrs["validOn"] / 1000)
    return result
