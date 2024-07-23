from logging import getLogger
from subprocess import DEVNULL, run
from time import sleep

from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm import tqdm

from .utils import ATTEMPT, WAIT, get_metadata, is_polygon, outputs

logger = getLogger(__name__)


def ogr2ogr(idx: int, url: str, filename: str, records: int | None):
    record_count = f"&resultRecordCount={records}" if records is not None else ""
    return run(
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
        stderr=DEVNULL,
    )


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def download(iso3: str, lvl: int, idx: int, url: str):
    filename = f"{iso3}_adm{lvl}".lower()
    success = False
    for records in [None, 1000, 100, 10, 1]:
        result = ogr2ogr(idx, url, filename, records)
        if result.returncode == 0:
            success = True
            break
        else:
            sleep(WAIT)
    if success:
        if not is_polygon(outputs / f"{filename}.gpkg"):
            (outputs / f"{filename}.gpkg").unlink()
            logger.info(f"NOT POLYGON: {filename}")
    else:
        raise Exception


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
