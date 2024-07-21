import logging
from datetime import date

import httpx
import pandas as pd
from tenacity import retry, stop_after_attempt
from tqdm import tqdm

from .utils import columns, cwd, get_config, join_hdx_metadata, join_itos_metadata


@retry(stop=stop_after_attempt(5))
def get_hdx_metadata(iso_3: str):
    id = f"cod-ab-{iso_3.lower()}"
    url = f"https://data.humdata.org/api/3/action/package_show?id={id}"
    with httpx.Client(http2=True, timeout=60) as client:
        return client.get(url).json().get("result")


@retry(stop=stop_after_attempt(5))
def get_itos_metadata(iso_3: str, lvl: int | None, idx: int | None):
    if lvl is None:
        return None
    idx = idx + lvl if idx is not None else lvl
    path = "COD_External"
    query = "where=1=1&outFields=date,validon&f=json&resultRecordCount=1&returnGeometry=false"
    url = f"https://codgis.itos.uga.edu/arcgis/rest/services/{path}/{iso_3}_pcode/FeatureServer/{idx}/query?{query}"
    with httpx.Client(http2=True, timeout=60) as client:
        result = client.get(url).json()
        if "error" in result:
            path = "COD_NO_GEOM_CHECK"
            url = f"https://codgis.itos.uga.edu/arcgis/rest/services/{path}/{iso_3}_pcode/FeatureServer/{idx}/query?{query}"
            result = client.get(url).json()
            if "error" in result:
                return None
    attrbutes = result["features"][0]["attributes"]
    itos_url = url.split("FeatureServer")[0] + "FeatureServer"
    if result["geometryType"] != "esriGeometryPolygon" or attrbutes["date"] is None:
        return {"url": itos_url, "date": None, "update": None}
    itos_date = date.fromtimestamp(attrbutes["date"] / 1000)
    itos_update = date.fromtimestamp(attrbutes["validOn"] / 1000)
    return {"url": itos_url, "date": itos_date, "update": itos_update}


def get_metadata():
    metadata = get_config()
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso_3"])
        hdx = get_hdx_metadata(row["iso_3"])
        if hdx is not None:
            row = join_hdx_metadata(row, hdx)
        itos = get_itos_metadata(row["iso_3"], row["admin_level"], row["itos_index"])
        if itos is not None:
            row = join_itos_metadata(row, itos)
    return metadata


def save_metadata(metadata):
    df = pd.DataFrame(metadata)
    df = df[df["hdx_date"].notna()]
    df = df[columns]
    dest = cwd / "../../data/metadata.csv"
    df.to_csv(dest, encoding="utf-8-sig", float_format="%.0f", index=False)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("starting")
    metadata = get_metadata()
    save_metadata(metadata)
    logger.info("finished")
