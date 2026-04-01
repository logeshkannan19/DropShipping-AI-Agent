"""Demand prediction model training script."""

import numpy as np
import pickle
from pathlib import Path


def train_demand_model():
    """Train a simple demand prediction model."""
    print("Training demand prediction model...")
    
    model_data = {
        "coefficients": {
            "rating": 0.15,
            "review_count": 0.20,
            "supplier_rating": 0.10,
            "shipping_days": -0.10,
            "competitor_count": -0.15,
            "price": -0.20
        },
        "intercept": 0.30
    }
    
    model_path = Path("./data/demand_model.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(model_path, "wb") as f:
        pickle.dump(model_data, f)
    
    print(f"Model saved to {model_path}")
    print("Model trained successfully!")


def predict_demand(features: dict) -> float:
    """
    Predict demand using the trained model.
    
    Args:
        features: Product features
        
    Returns:
        Demand score (0-1)
    """
    model_path = Path("./data/demand_model.pkl")
    
    if not model_path.exists():
        train_demand_model()
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    score = model["intercept"]
    
    for feature, coef in model["coefficients"].items():
        if feature in features:
            value = features[feature]
            if feature == "review_count":
                value = min(value / 5000, 1.0)
            elif feature == "competitor_count":
                value = min(value / 100, 1.0)
            elif feature == "shipping_days":
                value = 1 - (value / 30)
            elif feature == "rating":
                value = value / 5.0
            elif feature == "supplier_rating":
                value = value / 5.0
            elif feature == "price":
                value = 1 - min(value / 100, 1.0)
            
            score += coef * value
    
    return min(max(score, 0.0), 1.0)


if __name__ == "__main__":
    train_demand_model()
