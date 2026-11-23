from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "usgs_waterdata_core"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
for source in Path(__file__).resolve().parents[1].glob("*producer/*/src"):
    sys.path.insert(0, str(source))
