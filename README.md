# techintel-leader-follower

UAV swarm / leader-follower focused example of techintel: the open literature on
unmanned aircraft that position, navigate and synchronise off one another, with
emphasis on optical links (infrared, visible light, ultraviolet / solar-blind,
LED beacons).

Same pipeline and app as `techintel-jamming`, re-run on a different OpenAlex corpus.

## Run the app

Python 3.11 (pandas is pinned to 2.0.0).

```
uv venv --python 3.11 .venv
uv pip install -p .venv/bin/python -r requirements.txt
.venv/bin/streamlit run leaderfollower2d.py
```

The app needs `.streamlit/secrets.toml` (not committed) with two keys:

```
OPENAI_API_KEY = "..."
MAPBOX_TOKEN = "..."
```

Click a paper or a pink topic centroid in the scatter plot to get the write-up,
the ranked countries / affiliations / authors / journals, and the affiliation map.

## Corpus

Union of three Boolean OpenAlex Works searches over title + abstract, published
after 2000, all countries, deduplicated by paper id:

| Tag | Query |
|---|---|
| A, optical swarm PNT | UAV × swarm / formation × infrared / visible light / ultraviolet / beacon × positioning |
| C, leader-follower | UAV × "leader-follower" |
| D, relative localization | UAV × swarm / formation × relative / mutual / cooperative localization or navigation |

The exact strings are in `QUERIES` in the notebook.

## Data pipeline

Two steps, in two environments:

1. `leader_follower.ipynb`, pipeline environment (`requirements-pipeline.txt`, Python 3.12):

   OpenAlex Boolean Works search → abstract reconstruction → YAKE keywords →
   flair sentence embeddings (`all-MiniLM-L6-v2`) → UMAP (2D) → HDBSCAN clusters →
   paper/author/affiliation triples → topic centroids → source and affiliation-geo dicts.

   ```
   jupyter nbconvert --to notebook --execute --inplace leader_follower.ipynb
   ```

   The raw pull is cached in `cache/works_raw.pkl`; delete it to pull afresh.
   Set `OPENALEX_API_KEY` to use an OpenAlex key (keyless requests share a small
   daily budget per IP address).

2. `resave_pickles.py`, app environment: pandas pickles do not load across the
   pandas 3 → 2.0.0 gap, so the notebook writes JSON-lines into `cache/` and this
   script writes the pickles the app reads.

   ```
   .venv/bin/python resave_pickles.py
   ```

Outputs (loaded by `leaderfollower2d.py`):
`leaderfollowercentroids2d.pkl.gz`, `leaderfollowerdfinfo2d.pkl.gz`,
`leaderfollowerdftriple2d.pkl.gz`, `updatesource_page_dict.pkl`, `updateaffil_geo_dict.pkl`.
