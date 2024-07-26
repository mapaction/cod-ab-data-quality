from logging import INFO, WARNING, basicConfig, getLogger
from os import environ, getenv
from pathlib import Path

from dotenv import load_dotenv
from httpx import Client
from pandas import read_csv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv(override=True)
basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
getLogger("httpx").setLevel(WARNING)
getLogger("pyogrio._io").setLevel(WARNING)

environ["OGR_ORGANIZE_POLYGONS"] = "ONLY_CCW"

ATTEMPT = 5
WAIT = 10
TIMEOUT = 600

cwd = Path(__file__).parent
outputs = cwd / "../../data/itos"


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def client_get(url: str):
    with Client(http2=True, timeout=TIMEOUT) as client:
        return client.get(url)


def clean_list(items: list):
    return [item.strip().upper() for item in items if item.strip() != ""]


def get_iso3():
    return clean_list(getenv("ISO3", "").split(","))


def get_metadata():
    dtypes = {
        "itos_level": "Int8",
        "itos_index_0": "Int8",
        "itos_index_1": "Int8",
        "itos_index_2": "Int8",
        "itos_index_3": "Int8",
        "itos_index_4": "Int8",
    }
    df = read_csv(cwd / "../../data/metadata.csv", dtype=dtypes)
    records = df.to_dict("records")
    iso3_list = get_iso3()
    if len(iso3_list):
        records = [x for x in records if x["iso3"] in iso3_list]
    result = []
    for record in records:
        for level in range(5):
            if record[f"itos_index_{level}"] is not None:
                result.append({**record, "admin_level": level})
    return result
