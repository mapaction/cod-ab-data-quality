"""Download functions using GDAL, runs faster than HTTPX."""

from logging import getLogger
from pathlib import Path
from re import compile
from subprocess import DEVNULL, run
from urllib.parse import urlencode

from tenacity import retry, stop_after_attempt, wait_fixed

from src.config import ATTEMPT, WAIT, boundaries

logger = getLogger(__name__)


def ogr2ogr(idx: int, url: str, filename: str, records: int | None):
    """Uses OGR2OGR to download ESRI JSON from an ArcGIS server to local GeoPackage.

    The query parameter "f" (format) is set to return JSON (default is HTML), "where" is
    a required parameter with the value "1=1" to return all features, "outFields" is set
    to "*" specifying to return all fields (default is only first field),
    "orderByFields" is required for pagination to ensure that features are always
    ordered the same way and duplicates are not returned when paginating, and finally
    "resultRecordCount" is used to specify how many records to paginate through each
    time.

    OGR2OGR is set to overwrite the existing file if it exists (default is to throw an
    error). "-nln" sets the name of the layer to be the same as the filename (default is
    the name of the source layer, in this case "ESRIJSON"). The output option ("-oo")
    "FEATURE_SERVER_PAGING" is set to "YES" instructing the command to paginate through
    the server and not stop with the first query result.

    Args:
        idx: Index the layer is available at on the ArcGIS Feature Service.
        url: Base URL of an ArcGIS Feature Service.
        filename: Name of the downloaded layer.
        records: The number of records to fetch from the server per request during
        pagination.

    Returns:
        A subprocess completed process, including a returncode stating whether the run
        was successfun or not.
    """
    query: dict = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "orderByFields": "OBJECTID",
    }
    if records is not None:
        query["resultRecordCount"] = records
    dst_dataset = boundaries / f"{filename}.gpkg"
    src_dataset = f"{url}/{idx}/query?{urlencode(query)}"
    return run(
        [
            "ogr2ogr",
            "-overwrite",
            *["-nln", filename],
            *["-oo", "FEATURE_SERVER_PAGING=YES"],
            *[dst_dataset, src_dataset],
        ],
        stderr=DEVNULL,
    )


def is_polygon(file: Path):
    """Uses OGR to check whether a downloaded file is a valid polygon.

    During the download process, the ArcGIS server may return empty geometry. This check
    ensures data has been downloaded correctly.

    Args:
        file: Path of a OGR readable file.

    Returns:
        True if the file is detected as a valid polygon, otherwise false.
    """
    regex = compile(r"\((Multi Polygon|Polygon)\)")
    result = run(["ogrinfo", file], capture_output=True)
    return bool(regex.search(result.stdout.decode("utf-8")))


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def download(iso3: str, lvl: int, idx: int, url: str):
    """Downloads ESRI JSON from an ArcGIS Feature Server and saves as GeoPackage.

    First, attempts to download ESRI JSON paginating through the layer with the value
    set by "maxRecordCount" (default behavior when "resultRecordCount" is unspecified).
    This request may fail due to memory issues on the server.

    Then, starting with "1000" and reducing by factors of "10", try to paginate through
    the layer. "1000" is a value that will succeed for most layers, however layers with
    excessively large geometries will require smaller sets of records to avoid
    overloading the server's memory. When all records have been obtained through
    pagination, save the result.

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
    for records in [None, 1000, 100, 10, 1]:
        result = ogr2ogr(idx, url, filename, records)
        if result.returncode == 0:
            break
    if not is_polygon(boundaries / f"{filename}.gpkg"):
        raise RuntimeError(filename)
