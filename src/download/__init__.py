from logging import INFO, WARNING, basicConfig, getLogger
from os import environ
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
getLogger("httpx").setLevel(WARNING)
getLogger("pyogrio._io").setLevel(WARNING)

environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
environ["OGR_ORGANIZE_POLYGONS"] = "ONLY_CCW"

ATTEMPT = 5
WAIT = 10
TIMEOUT = 600

cwd = Path(__file__).parent
outputs = cwd / "../../data/boundaries"
