# AutoScreen

An autonomous ligand-based virtual screening pipeline built with Python.

## Features

- Retrieve bioactivity data from ChEMBL
- Generate molecular fingerprints using RDKit
- Train machine learning models
- Evaluate with cross-validation
- Screen DrugCentral compounds
- Rank potential lead compounds

## Tech Stack

- Python
- RDKit
- scikit-learn
- PostgreSQL
- SQLAlchemy

## Example

```python
from pipeline import ScreeningPipeline

pipeline = ScreeningPipeline()

pipeline.train("CHEMBL2094253")

results = pipeline.screen("CHEMBL2094253")
