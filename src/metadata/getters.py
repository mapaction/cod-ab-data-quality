import re
from datetime import date

import httpx
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(5))
def get_hdx_metadata(iso3: str):
    id = f"cod-ab-{iso3.lower()}"
    url = f"https://data.humdata.org/api/3/action/package_show?id={id}"
    with httpx.Client(http2=True, timeout=60) as client:
        return client.get(url).json().get("result")


def get_service_url(path: str, iso3: str):
    base = "https://codgis.itos.uga.edu/arcgis/rest/services"
    return f"{base}/{path}/{iso3}_pcode/FeatureServer?f=json"


def get_layer_url(path: str, iso_3: str, idx: int):
    base = "https://codgis.itos.uga.edu/arcgis/rest/services"
    query = "where=1=1&outFields=*&f=json&resultRecordCount=1&returnGeometry=false"
    return f"{base}/{path}/{iso_3}_pcode/FeatureServer/{idx}/query?{query}"


def get_layer(service: dict, path: str, iso3: str, client: httpx.Client):
    p = re.compile(r"Admin")
    layers = list(filter(lambda x: p.search(x["name"]), service["layers"]))
    layers = list(filter(lambda x: x["geometryType"] == "esriGeometryPolygon", layers))
    layer_map = {}
    idx = 0
    for layer in layers:
        lvl = int(layer["name"][-1])
        idx = layer["id"]
        layer_map[lvl] = idx
    url = get_layer_url(path, iso3, idx)
    return layer_map, lvl, client.get(url).json()


def get_languages(attrbutes: dict, lvl: int):
    keys = list(attrbutes.keys())
    p = re.compile(rf"^ADM{lvl}_\w{{2}}$")
    langs = list(filter(lambda x: p.search(x), keys))
    langs = list(map(lambda x: x.split("_")[1].lower(), langs))
    langs = list(dict.fromkeys(langs))
    return langs


@retry(stop=stop_after_attempt(5))
def get_itos_metadata(iso3: str):
    with httpx.Client(http2=True, timeout=60) as client:
        path = "COD_External"
        url = get_service_url(path, iso3)
        service = client.get(url).json()
        if "error" in service:
            path = "COD_NO_GEOM_CHECK"
            url = get_service_url(path, iso3)
            service = client.get(url).json()
            if "error" in service:
                return None
        layers, lvl, layer = get_layer(service, path, iso3, client)
    attrs = layer["features"][0]["attributes"]
    langs = get_languages(attrs, lvl)
    itos_url = url.split("?")[0]
    result = {"url": itos_url, "path": path, "langs": langs, "layers": layers}
    if attrs.get("date") is None:
        result["date"] = None
        result["update"] = None
        return result
    result["date"] = date.fromtimestamp(attrs["date"] / 1000)
    result["update"] = date.fromtimestamp(attrs["validOn"] / 1000)
    return result
