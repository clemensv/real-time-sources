"""Public package surface for the botfinder analysis pipeline.

The package starts from an anchor Bluesky handle, acquires follower and
firehose data, computes per-account bot scores, and then builds downstream
artifacts such as co-follow graphs, cross-follow measurements, and HTML
dossiers. This module re-exports the primary dataclasses and orchestration
functions that notebooks, scripts, and the CLI use.
"""

from .config import Config
from .scoring import BotScore, compute_bot_score, compute_network_statistics
from .acquire import AcquiredData, acquire_all
from .pipeline import AnalysisResult, run_analysis, run_full_pipeline, FullResult

__all__ = [
    "Config",
    "BotScore",
    "compute_bot_score",
    "compute_network_statistics",
    "AcquiredData",
    "acquire_all",
    "AnalysisResult",
    "run_analysis",
    "run_full_pipeline",
    "FullResult",
]

__version__ = "0.1.0"
