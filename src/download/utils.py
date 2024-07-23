from logging import INFO, WARNING, basicConfig, getLogger
from os import getenv
from pathlib import Path
from re import compile
from subprocess import run

from dotenv import load_dotenv
from pandas import read_csv

load_dotenv(override=True)
basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
getLogger("httpx").setLevel(WARNING)

cwd = Path(__file__).parent
outputs = cwd / "../../data/itos"


def clean_list(items: list):
    return [item.strip().upper() for item in items if item.strip() != ""]


def get_iso3():
    return clean_list(getenv("ISO3", "").split(","))


def is_polygon(file):
    regex = compile(r"\((Multi Polygon|Polygon)\)")
    result = run(["ogrinfo", file], capture_output=True)
    return regex.search(result.stdout.decode("utf-8"))


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
