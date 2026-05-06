"""botfinder — Bluesky bot-network detection around an anchor account."""

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
