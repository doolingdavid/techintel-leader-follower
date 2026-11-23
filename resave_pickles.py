"""Turn the pipeline's JSON-lines exports into the pickles the app loads.

The pipeline notebook runs on a newer pandas than the app, and pandas pickles
do not load across that gap. Run this with the APP environment (Python 3.11,
pandas 2.0.0 from requirements.txt), after executing leader_follower.ipynb:

    .venv/bin/python resave_pickles.py
"""
import json

import pandas as pd

NAMES = [
    "leaderfollowercentroids2d",
    "leaderfollowerdftriple2d",
    "leaderfollowerdfinfo2d",
]

for name in NAMES:
    df = pd.read_json(f"cache/{name}.jsonl", orient="records", lines=True,
                      dtype=False, convert_dates=False)
    with open(f"cache/{name}.dtypes.json") as f:
        dtypes = json.load(f)
    # restore column order and the numeric dtypes the pipeline had
    df = df[list(dtypes)]
    for col, dt in dtypes.items():
        if dt.startswith(("int", "float")) and col != "__index__":
            df[col] = df[col].astype(dt)
    df = df.set_index("__index__")
    df.index.name = "cluster" if name.endswith("centroids2d") else None
    if name.endswith("dfinfo2d"):
        df.index.name = "id"
    df.to_pickle(f"{name}.pkl.gz")
    print(f"{name}.pkl.gz", df.shape, "pandas", pd.__version__)
