from logging import getLogger
from shutil import which

from tqdm import tqdm

from . import httpx, ogr2ogr
from .utils import get_metadata, outputs

logger = getLogger(__name__)

if __name__ == "__main__":
    logger.info("starting")
    outputs.mkdir(parents=True, exist_ok=True)
    download = ogr2ogr.download if which("ogr2ogr") else httpx.download
    metadata = get_metadata()
    pbar = tqdm(metadata)
    for row in pbar:
        iso3 = row["iso3"]
        lvl = row["admin_level"]
        idx = row[f"itos_index_{lvl}"]
        pbar.set_postfix_str(f"{iso3}_ADM{lvl}")
        download(iso3, lvl, idx, row["itos_url"])
    logger.info("finished")
