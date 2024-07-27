from json import dump
from logging import getLogger

from geopandas import read_file
from pandas import to_datetime

from .utils import client_get, outputs

logger = getLogger(__name__)


def get_query(url: str, idx: int, records=None, offset=None):
    query = "f=json&where=1=1&outFields=*&orderByFields=OBJECTID"
    q_record = f"&resultRecordCount={records}" if records is not None else ""
    q_offset = f"&resultOffset={offset}" if offset is not None else ""
    return f"{url}/{idx}/query?{query}{q_record}{q_offset}"


def get_query_count(url: str, idx: int):
    return f"{url}/{idx}/query?f=json&where=1=1&returnCountOnly=true"


def save_file(data: dict, filename: str):
    tmp = outputs / f"{filename}.json"
    with open(tmp, "w") as f:
        dump(data, f, separators=(",", ":"))
    gdf = read_file(tmp, use_arrow=True)
    gdf = gdf.drop(columns=["OBJECTID"], errors="ignore")
    for col in gdf.select_dtypes(include=["datetime"]):
        gdf[col] = to_datetime(gdf[col], utc=True)
    gdf.to_file(outputs / f"{filename}.gpkg")
    tmp.unlink(missing_ok=True)


def download(iso3: str, lvl: int, idx: int, url: str):
    filename = f"{iso3}_adm{lvl}".lower()
    query = get_query(url, idx)
    esri_json = client_get(query).json()
    if "error" not in esri_json and "exceededTransferLimit" not in esri_json:
        save_file(esri_json, filename)
    else:
        query_count = get_query_count(url, idx)
        count = client_get(query_count).json()["count"]
        for records in [1000, 100, 10, 1]:
            result = None
            for offset in range(0, count, records):
                query = get_query(url, idx, records, offset)
                esri_json = client_get(query).json()
                if "error" in esri_json:
                    break
                else:
                    if result is None:
                        result = esri_json
                    else:
                        result["features"].extend(esri_json["features"])
            if result is not None:
                save_file(result, filename)
                break
        if not (outputs / f"{filename}.gpkg").is_file():
            raise RuntimeError(filename)
