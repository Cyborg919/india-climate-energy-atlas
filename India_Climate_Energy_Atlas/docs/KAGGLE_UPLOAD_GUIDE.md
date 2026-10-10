# Kaggle upload guide

## Recommended upload target
For a runnable research presentation, upload `notebooks/India_Climate_Energy_Atlas_Kaggle.ipynb` as a Kaggle Notebook rather than uploading the ZIP and expecting it to run automatically.

## Before running
1. Enable Internet in the notebook settings.
2. Run every cell from top to bottom.
3. Confirm that the data retrieval cell prints a row count and the observed year range.
4. Inspect `earth_atlas_outputs/` and download the CSV/provenance outputs if you want to publish them as a separate dataset.

## If you want to upload the ZIP as a dataset
The ZIP is a source bundle containing code and documentation. It is not a precomputed dataset and it will not execute merely by uploading it. The standalone notebook inside `notebooks/` is the intended runnable artifact.

## Scientific integrity
Do not publish conclusions until the notebook has run successfully in the target environment. Do not present correlations as causal effects. If the World Bank API is unreachable, retry later rather than inserting made-up observations.
