from json import dump
from logging import getLogger

from geopandas import read_file
from pandas import to_datetime
from tenacity import retry, stop_after_attempt, wait_fixed

from . import ATTEMPT, WAIT, outputs
from .utils import client_get

logger = getLogger(__name__)


def get_query(url: str, idx: int, records: int | None, offset: int | None):
    """Builds a URL used for retrieving ESRI JSON from an ArcGIS Feature Service.

    The query parameter "f" (format) is set to return JSON (default is HTML), "where" is
    a required parameter with the value "1=1" to return all features, "outFields" is set
    to "*" specifying to return all fields (default is only first field), and
    "orderByFields" is required for pagination to ensure that features are always
    ordered the same way and duplicates are not returned when paginating. For layers
    where the number of features exceeds the "maxRecordCount" property, add
    "resultRecordCount" and "resultOffset" query parameters to paginate through results.

    Args:
        url: Base URL of an ArcGIS Feature Service.
        idx: Index of a feature service layer.
        records: The number of records to fetch from the server per request.
        offset: For pagination, skips the specified number of records and starts from
        the next record.

    Returns:
        URL which returns ESRI JSON.
    """
    query = "f=json&where=1=1&outFields=*&orderByFields=OBJECTID"
    q_record = f"&resultRecordCount={records}" if records is not None else ""
    q_offset = f"&resultOffset={offset}" if offset is not None else ""
    return f"{url}/{idx}/query?{query}{q_record}{q_offset}"


def get_query_count(url: str, idx: int):
    """Gets a URL containing the total number of features in a layer.

    The query parameter "f" (format) is set to return JSON (default is HTML), "where" is
    a required parameter with the value "1=1" to return all features, and
    "returnCountOnly" tells the server to return only a count property as a result
    rather than ESRI JSON.

    Args:
        url: Base URL of an ArcGIS Feature Service.
        idx: Index of a feature service layer.

    Returns:
        URL containing information on the total number of features in a layer.
    """
    return f"{url}/{idx}/query?f=json&where=1=1&returnCountOnly=true"


def save_file(data: dict, filename: str):
    """Saves ESRI JSON data as a GeoPackage, normalizing attributes.

    First, temporarily saves an ESRI JSON file to disk to free up memory.

    Use Geopandas to read the file using pyogrio engine with arrow for the most
    efficiency. Geopandas will ignore "OBJECTID" and create it's own "fid" field, so
    drop "OBJECTID" to remove duplicate id fields. In ArcGIS versions prior to ArcGIS
    Pro 2.3, Integer64, Date and Time field types are not supported. Pandas also does
    not support Date types, only DateTime. Since data is represented as dates within
    DateTime fields, set the timezone to UTC so that they are consistently interpreted.

    Finally, save the result as a GeoPackage to disk and delete the temporary ESRI JSON.

    Args:
        data: ESRI JSON represented as a dict.
        filename: File name of the output.
    """
    tmp = outputs / f"{filename}.json"
    with open(tmp, "w") as f:
        dump(data, f, separators=(",", ":"))
    gdf = read_file(tmp, use_arrow=True)
    gdf = gdf.drop(columns=["OBJECTID"], errors="ignore")
    for col in gdf.select_dtypes(include=["datetime"]):
        gdf[col] = to_datetime(gdf[col], utc=True)
    gdf.to_file(outputs / f"{filename}.gpkg")
    tmp.unlink(missing_ok=True)


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def download(iso3: str, lvl: int, idx: int, url: str):
    """Downloads ESRI JSON from an ArcGIS Feature Server and saves as GeoPackage.

    First, attempts to download ESRI JSON in a single request. This request may fail due
    to memory issues on the server, in which case the result will return the key
    "error". Additionally, if the number of features returned exceeds the
    "maxRecordCount" property, it will contain the key "exceededTransferLimit" in the
    result indicating that only part of the dataset has been downloaded.

    If either of the above errors are encountered, make a query to obtain the total
    number of records for a layer. Starting with "1000" and reducing by factors of "10",
    try to paginate through the layer with multiple requests. "1000" is a value that
    will succeed for most layers, however layers with excessively large geometries will
    require smaller sets of records to avoid overloading the server's memory. When all
    records have been obtained through pagination, save the result.

    If at the end of this loop, the function is unable to download a layer, it is likely
    that a network error has occured. The RuntimeError will trigger tenacity to retry
    the function again from the start.

    Args:
        iso3: A valid ISO 3166-1 alpha-3 code.
        lvl: Admin level of the layer.
        idx: Index the layer is available at on the ArcGIS Feature Service.
        url: Base URL of an ArcGIS Feature Service.

    Raises:
        RuntimeError: Raises an error with the filename of a layer unable to be
        downloaded.
    """
    filename = f"{iso3}_adm{lvl}".lower()
    query = get_query(url, idx, None, None)
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
