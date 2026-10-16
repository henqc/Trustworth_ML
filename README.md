# Trustworth_ML

## How to run (from the repo root)
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Download `adult.data`, `adult.test`, `adult.names` from https://archive.ics.uci.edu/ml/machine-learning-databases/adult/ into `data/adult/`
4. `python src/manifest.py` (only once, before any training; it overwrites `manifests/splits.json`, so skip it if the manifest exists)
5. `python src/data.py` (data/split/model self-check)
6. `python src/explain.py` (sampler/surrogate self-check)
7. `python src/first_start.py` (recover the known linear predictor, then the pilot: writes `results/first_start.csv`, `results/pilot.csv`, `results/pilot_summary.md`)
