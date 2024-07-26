from json import dumps
from logging import getLogger
from time import sleep

from geopandas import read_file

from .utils import WAIT, client_get, outputs

logger = getLogger(__name__)


def get_query(url: str, idx: int, records=None, offset=None):
    query = "f=json&where=1=1&outFields=*&orderByFields=OBJECTID"
    q_record = f"&resultRecordCount={records}" if records is not None else ""
    q_offset = f"&resultOffset={offset}" if offset is not None else ""
    return f"{url}/{idx}/query?{query}{q_record}{q_offset}"


def get_query_count(url: str, idx: int):
    return f"{url}/{idx}/query?f=json&where=1=1&returnCountOnly=true"


def save_file(text: str, filename: str):
    gdf = read_file(text, use_arrow=True)
    gdf = gdf.drop(columns=["OBJECTID"], errors="ignore")
    gdf.to_file(outputs / f"{filename}.gpkg")


def download(iso3: str, lvl: int, idx: int, url: str):
    filename = f"{iso3}_adm{lvl}".lower()
    query = get_query(url, idx)
    esri_text = client_get(query).text
    if not esri_text.startswith('{"error":'):
        save_file(esri_text, filename)
    else:
        query_count = get_query_count(url, idx)
        count = client_get(query_count).json()["count"]
        for records in [1000, 100, 10, 1]:
            result = None
            for offset in range(0, count, records):
                query = get_query(url, idx, records, offset)
                esri_json = client_get(query).json()
                if "error" in esri_json:
                    sleep(WAIT)
                    break
                else:
                    if result is None:
                        result = esri_json
                    else:
                        result["features"].extend(esri_json["features"])
            if result is not None:
                save_file(dumps(result), filename)
                break
