import logging
import re
import subprocess
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

cwd = Path(__file__).parent
outputs = cwd / "../../data/itos"


def is_polygon(file):
    regex = re.compile(r"\((Multi Polygon|Polygon)\)")
    result = subprocess.run(["ogrinfo", file], capture_output=True)
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
    df = pd.read_csv(cwd / "../../data/metadata.csv", dtype=dtypes)
    records = df.to_dict("records")
    result = []
    for record in records:
        for level in range(5):
            if record[f"itos_index_{level}"] is not None:
                result.append({**record, "admin_level": level})
    return result
