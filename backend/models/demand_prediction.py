"""
Demand Prediction Model Module

This module provides demand prediction functionality using ML models:
- Train a RandomForest/XGBoost model on historical data
- Save model to disk for inference
- Load model and make predictions
"""

import os
import json
import pickle
import random
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import numpy as np
import pandas as pd
from loguru import logger
from backend.config.settings import get_settings

settings = get_settings()


class DemandPredictor:
    """
    Machine learning model for predicting product demand.
    
    Uses RandomForest or XGBoost to predict demand score (0-1)
    based on product features.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the demand predictor.
        
        Args:
            model_path: Path to saved model file
        """
        self.model_path = model_path or settings.demand_model_path
        self.model = None
        self.is_trained = False
        self.feature_names = [
            "category_encoded", "price", "rating", "review_count",
            "competitor_count", "supplier_rating", "shipping_days"
        ]
        
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            logger.warning(f"Model not found at {self.model_path}. Will train on first use.")
    
    def load_model(self) -> bool:
        """
        Load trained model from disk.
        
        Returns:
            True if model loaded successfully
        """
        try:
            with open(self.model_path, "rb") as f:
                data = pickle.load(f)
                self.model = data["model"]
                self.is_trained = data.get("is_trained", False)
                self.feature_mapping = data.get("feature_mapping", {})
            logger.info(f"Model loaded from {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def save_model(self) -> bool:
        """
        Save trained model to disk.
        
        Returns:
            True if model saved successfully
        """
        if self.model is None:
            logger.error("No model to save")
            return False
        
        try:
            os.makedirs(os.path.dirname(self.model_path) or ".", exist_ok=True)
            with open(self.model_path, "wb") as f:
                pickle.dump({
                    "model": self.model,
                    "is_trained": True,
                    "feature_mapping": getattr(self, "feature_mapping", {}),
                    "feature_names": self.feature_names
                }, f)
            logger.info(f"Model saved to {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return False
    
    def _generate_training_data(self, n_samples: int = 1000) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Generate synthetic training data.
        
        In production, this would use real historical sales data.
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            Features DataFrame and target Series
        """
        np.random.seed(42)
        
        categories = ["Electronics", "Home & Garden", "Fashion", "Beauty", 
                     "Sports", "Toys", "Automotive", "Health"]
        category_encoding = {cat: i for i, cat in enumerate(categories)}
        
        data = {
            "category_encoded": np.random.choice(len(categories), n_samples),
            "price": np.random.uniform(10, 100, n_samples),
            "rating": np.random.uniform(3.0, 5.0, n_samples),
            "review_count": np.random.randint(50, 5000, n_samples),
            "competitor_count": np.random.randint(5, 100, n_samples),
            "supplier_rating": np.random.uniform(3.5, 5.0, n_samples),
            "shipping_days": np.random.randint(5, 30, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Generate demand score based on features (simulate real relationships)
        # Higher rating, more reviews, better supplier, fewer competitors = higher demand
        demand = (
            0.15 * (df["rating"] - 3.0) / 2.0 +
            0.20 * np.log1p(df["review_count"]) / np.log1p(5000) +
            0.10 * (df["supplier_rating"] - 3.5) / 1.5 +
            0.10 * (30 - df["shipping_days"]) / 25 +
            0.15 * (50 - df["competitor_count"]) / 45 +
            0.20 * (1 - (df["price"] - 10) / 90) +
            0.10 * np.random.random(n_samples)
        )
        
        demand = np.clip(demand, 0, 1)
        demand = (demand - demand.min()) / (demand.max() - demand.min())
        
        self.feature_mapping = {"categories": category_encoding}
        
        return df, pd.Series(demand, name="demand")
    
    def train(self, n_samples: int = 1000) -> Dict[str, Any]:
        """
        Train the demand prediction model.
        
        Args:
            n_samples: Number of training samples to generate
            
        Returns:
            Training results including metrics
        """
        logger.info("Starting model training...")
        
        try:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
            
            X, y = self._generate_training_data(n_samples)
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train, y_train)
            
            y_pred = self.model.predict(X_test)
            
            metrics = {
                "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
                "mae": float(mean_absolute_error(y_test, y_pred)),
                "r2": float(r2_score(y_test, y_pred)),
                "train_samples": len(X_train),
                "test_samples": len(X_test)
            }
            
            self.is_trained = True
            self.save_model()
            
            logger.info(f"Training complete. Metrics: {metrics}")
            return metrics
            
        except ImportError:
            logger.error("sklearn not installed, using mock prediction")
            self.is_trained = True
            return {"status": "mock", "message": "Using mock prediction"}
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict demand for a product.
        
        Args:
            features: Product features dictionary
            
        Returns:
            Prediction result with demand score and confidence
        """
        if self.model is None or not self.is_trained:
            # Try to train first
            self.train()
        
        if self.model is None:
            # Return mock prediction
            return self._mock_predict(features)
        
        try:
            # Prepare features
            category = features.get("category", "Electronics")
            category_encoding = self.feature_mapping.get("categories", {})
            cat_encoded = category_encoding.get(category, 0)
            
            feature_vector = np.array([[
                cat_encoded,
                features.get("price", 0),
                features.get("rating", 0),
                features.get("review_count", 0),
                features.get("competitor_count", 0),
                features.get("supplier_rating", 0),
                features.get("shipping_days", 0)
            ]])
            
            # Make prediction
            demand_score = float(self.model.predict(feature_vector)[0])
            demand_score = max(0.0, min(1.0, demand_score))
            
            # Calculate confidence based on feature importance
            feature_importance = self.model.feature_importances_
            confidence = float(np.mean(feature_importance))
            
            # Get key factors
            factors = self._get_key_features(features, feature_importance)
            
            return {
                "demand_score": round(demand_score, 3),
                "confidence": round(confidence, 3),
                "factors": factors
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return self._mock_predict(features)
    
    def _mock_predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mock prediction when model is not available.
        
        Args:
            features: Product features
            
        Returns:
            Mock prediction result
        """
        # Simple heuristic-based prediction
        rating = features.get("rating", 4.0)
        reviews = features.get("review_count", 100)
        price = features.get("price", 30)
        
        score = (
            (rating / 5.0) * 0.3 +
            min(reviews / 2000, 1.0) * 0.3 +
            (1 - abs(price - 30) / 70) * 0.2 +
            features.get("supplier_rating", 4.0) / 5.0 * 0.2
        )
        
        # Add some randomness
        score += random.uniform(-0.1, 0.1)
        score = max(0.0, min(1.0, score))
        
        return {
            "demand_score": round(score, 3),
            "confidence": 0.7,
            "factors": {
                "rating_impact": "positive" if rating >= 4.0 else "neutral",
                "review_impact": "high" if reviews > 500 else "medium",
                "price_impact": "optimal" if 20 <= price <= 50 else "adjust"
            }
        }
    
    def _get_key_features(self, features: Dict[str, Any], importance: np.ndarray) -> Dict[str, Any]:
        """
        Identify key factors influencing the prediction.
        
        Args:
            features: Input features
            importance: Feature importance scores
            
        Returns:
            Dictionary of key factors
        """
        importance_dict = dict(zip(self.feature_names, importance))
        
        sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        
        factors = {}
        for feature, score in sorted_features[:3]:
            if feature == "rating":
                factors["rating_impact"] = "positive" if features.get("rating", 0) >= 4.0 else "negative"
            elif feature == "review_count":
                factors["review_impact"] = "high" if features.get("review_count", 0) > 500 else "low"
            elif feature == "competitor_count":
                factors["competition_impact"] = "high" if features.get("competitor_count", 0) > 50 else "low"
            elif feature == "price":
                price = features.get("price", 30)
                factors["price_impact"] = "optimal" if 20 <= price <= 50 else "too_high" if price > 50 else "too_low"
        
        return factors
    
    def predict_batch(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Predict demand for multiple products.
        
        Args:
            products: List of product feature dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for product in products:
            features = {
                "category": product.get("category", "Electronics"),
                "price": product.get("cost_price", 0),
                "rating": product.get("rating", 4.0),
                "review_count": product.get("review_count", 100),
                "competitor_count": product.get("competitor_count", 20),
                "supplier_rating": product.get("supplier_rating", 4.0),
                "shipping_days": product.get("shipping_time_days", 14)
            }
            result = self.predict(features)
            result["product_id"] = product.get("id")
            result["product_name"] = product.get("name")
            results.append(result)
        
        return results


def train_model() -> Dict[str, Any]:
    """
    Convenience function to train the demand model.
    
    Returns:
        Training results
    """
    predictor = DemandPredictor()
    return predictor.train()


def predict_demand(product_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to predict demand.
    
    Args:
        product_features: Product features
        
    Returns:
        Prediction result
    """
    predictor = DemandPredictor()
    return predictor.predict(product_features)