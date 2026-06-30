from autoscreen.pipeline import ScreeningPipeline
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

pipeline = ScreeningPipeline()

# pipeline.train("CHEMBL2094253")

pipeline.screen(
    target_id="CHEMBL2094253",
    limit=1000,
)