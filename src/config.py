from argparse import ArgumentParser
from logging import ERROR, INFO, WARNING, basicConfig, getLogger
from os import environ, getenv
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv(override=True)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
getLogger("fontTools").setLevel(ERROR)
getLogger("httpx").setLevel(WARNING)
getLogger("numexpr.utils").setLevel(WARNING)
getLogger("pyogrio._io").setLevel(WARNING)

environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
environ["OGR_ORGANIZE_POLYGONS"] = "ONLY_CCW"

parser = ArgumentParser()
parser.add_argument(
    "--iso3",
    help="Comma separated list of ISO3 codes used by commands.",
)
parser.add_argument(
    "--checks-include",
    help="Comma separated checks to include.",
)
parser.add_argument(
    "--checks-exclude",
    help="Comma separated checks to exclude.",
)
args = parser.parse_args()

ATTEMPT = int(getenv("ATTEMPT", "5"))
WAIT = int(getenv("WAIT", "10"))
TIMEOUT = int(getenv("TIMEOUT", "60"))
TIMEOUT_DOWNLOAD = int(getenv("TIMEOUT_DOWNLOAD", "600"))
ADMIN_LEVELS = int(getenv("ADMIN_LEVELS", "5"))

EPSG_WGS84 = 4326
GEOJSON_PRECISION = 6
METERS_PER_KM = 1_000_000
PLOTLY_SIMPLIFY = 0.000_01
POLYGON = "Polygon"
VALID_GEOMETRY = "Valid Geometry"

# NOTE: Could do more with this type, as iso3 and levels keys are required.
type CheckReturnList = list[dict[str, Any]]

cwd = Path(__file__).parent
boundaries_dir = cwd / "../data/boundaries"
boundaries_dir.mkdir(parents=True, exist_ok=True)
images_dir = cwd / "../data/images"
images_dir.mkdir(parents=True, exist_ok=True)
reports_dir = cwd / "../data/reports"
reports_dir.mkdir(parents=True, exist_ok=True)
tables_dir = cwd / "../data/tables"
tables_dir.mkdir(parents=True, exist_ok=True)

metadata_columns = [
    "iso3",
    "iso2",
    "name",
    "itos_url",
    "itos_service",
    "itos_level",
    *[f"itos_index_{level}" for level in range(ADMIN_LEVELS + 1)],
    "hdx_url",
    "hdx_date",
    "hdx_update",
    "hdx_source_1",
    "hdx_source_2",
    "hdx_license",
]
