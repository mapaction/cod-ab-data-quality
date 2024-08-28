"""Project configuration."""

from argparse import ArgumentParser
from logging import INFO, WARNING, basicConfig, getLogger
from os import environ, getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
getLogger("httpx").setLevel(WARNING)
getLogger("numexpr.utils").setLevel(WARNING)
getLogger("pyogrio._io").setLevel(WARNING)

environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
environ["OGR_ORGANIZE_POLYGONS"] = "ONLY_CCW"

parser = ArgumentParser()
parser.add_argument(
    "--iso3", help="Comma separated list of ISO3 codes used by commands."
)
args = parser.parse_args()

ATTEMPT = int(getenv("ATTEMPT", "5"))
WAIT = int(getenv("WAIT", "10"))
TIMEOUT = int(getenv("TIMEOUT", "60"))
TIMEOUT_DOWNLOAD = int(getenv("TIMEOUT_DOWNLOAD", "600"))

cwd = Path(__file__).parent
tables = cwd / "../data/tables"
tables.mkdir(parents=True, exist_ok=True)
boundaries = cwd / "../data/boundaries"
boundaries.mkdir(parents=True, exist_ok=True)

metadata_columns = [
    "iso3",
    "iso2",
    "name",
    "itos_url",
    "itos_service",
    "itos_level",
    "itos_index_0",
    "itos_index_1",
    "itos_index_2",
    "itos_index_3",
    "itos_index_4",
    "hdx_url",
    "hdx_date",
    "hdx_update",
    "hdx_source_1",
    "hdx_source_2",
    "hdx_license",
]
