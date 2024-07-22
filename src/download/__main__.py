import logging
import subprocess

from tqdm import tqdm

from .utils import get_metadata, is_polygon, outputs

logger = logging.getLogger(__name__)


def run(idx: int, url: str, filename: str, records: int | None):
    record_count = f"&resultRecordCount={records}" if records is not None else ""
    return subprocess.run(
        [
            "ogr2ogr",
            "-overwrite",
            *["--config", "OGR_GEOJSON_MAX_OBJ_SIZE", "0"],
            *["-mapFieldType", "DateTime=Date"],
            *["-nln", filename],
            *["-oo", "FEATURE_SERVER_PAGING=YES"],
            outputs / f"{filename}.gpkg",
            f"{url}/{idx}/query?where=1=1&outFields=*&f=json{record_count}",
        ],
        stderr=subprocess.DEVNULL,
    )


def download(iso3: str, lvl: int, idx: int, url: str):
    filename = f"{iso3}_adm{lvl}".lower()
    success = False
    for records in [None, 1000, 100, 10, 1]:
        result = run(idx, url, filename, records)
        if result.returncode == 0:
            success = True
            break
    if success:
        if not is_polygon(outputs / f"{filename}.gpkg"):
            (outputs / f"{filename}.gpkg").unlink()
            logger.info(f"NOT POLYGON: {filename}")
    else:
        logger.info(f"NOT DOWNLOADED: {filename}")


if __name__ == "__main__":
    logger.info("starting")
    outputs.mkdir(parents=True, exist_ok=True)
    metadata = get_metadata()
    pbar = tqdm(metadata)
    for row in pbar:
        iso3 = row["iso3"]
        lvl = row["admin_level"]
        idx = row[f"itos_index_{lvl}"]
        pbar.set_postfix_str(f"{iso3}_ADM{lvl}")
        download(iso3, lvl, idx, row["itos_url"])
    logger.info("finished")
