"""Scripts package."""

from backend.scripts.seed_data import seed_demo_data
from backend.scripts.train_model import train_demand_model

__all__ = [
    "seed_demo_data",
    "train_demand_model",
]
