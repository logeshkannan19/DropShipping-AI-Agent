"""Script to train the demand prediction model."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.models.demand_prediction import train_model


def main():
    """Train the demand prediction model."""
    print("Training demand prediction model...")
    result = train_model()
    print(f"Training result: {result}")
    
    if "rmse" in result:
        print(f"\nModel trained successfully!")
        print(f"  RMSE: {result['rmse']:.4f}")
        print(f"  MAE: {result['mae']:.4f}")
        print(f"  R²: {result['r2']:.4f}")


if __name__ == "__main__":
    main()
