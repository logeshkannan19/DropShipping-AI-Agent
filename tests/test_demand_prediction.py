"""Unit tests for Demand Prediction Model."""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from backend.models.demand_prediction import DemandPredictor


class TestDemandPredictor:
    """Test cases for DemandPredictor."""

    @pytest.fixture
    def predictor(self):
        """Create predictor instance with test model path."""
        return DemandPredictor(model_path="./data/test_demand_model.pkl")

    @pytest.fixture
    def sample_features(self):
        """Sample features for prediction."""
        return {
            "category": "Electronics",
            "price": 35.99,
            "rating": 4.5,
            "review_count": 200,
            "competitor_count": 25,
            "supplier_rating": 4.7,
            "shipping_days": 12
        }

    def test_predictor_initialization(self, predictor):
        """Test predictor initialization."""
        assert predictor.feature_names is not None
        assert len(predictor.feature_names) > 0

    def test_generate_training_data(self, predictor):
        """Test training data generation."""
        df, target = predictor._generate_training_data(n_samples=100)
        
        assert len(df) == 100
        assert len(target) == 100
        assert all(0 <= t <= 1 for t in target)

    def test_predict_without_model(self, predictor, sample_features):
        """Test prediction when model is not available."""
        result = predictor._mock_predict(sample_features)
        
        assert "demand_score" in result
        assert "confidence" in result
        assert 0 <= result["demand_score"] <= 1
        assert 0 <= result["confidence"] <= 1

    def test_predict_with_features(self, predictor, sample_features):
        """Test prediction with all features."""
        result = predictor.predict(sample_features)
        
        assert "demand_score" in result
        assert "confidence" in result
        assert 0 <= result["demand_score"] <= 1

    def test_predict_batch(self, predictor):
        """Test batch prediction."""
        products = [
            {"id": 1, "name": "Product 1", "cost_price": 30.0, "category": "Electronics"},
            {"id": 2, "name": "Product 2", "cost_price": 25.0, "category": "Fashion"},
        ]
        
        results = predictor.predict_batch(products)
        
        assert len(results) == 2
        assert all("demand_score" in r for r in results)
        assert all("product_id" in r for r in results)

    def test_demand_score_bounds(self, predictor):
        """Test that demand scores are bounded."""
        features_list = [
            {
                "category": "Electronics",
                "price": 10.0,
                "rating": 5.0,
                "review_count": 5000,
                "competitor_count": 5,
                "supplier_rating": 5.0,
                "shipping_days": 5
            },
            {
                "category": "Toys",
                "price": 100.0,
                "rating": 1.0,
                "review_count": 0,
                "competitor_count": 100,
                "supplier_rating": 3.5,
                "shipping_days": 30
            }
        ]
        
        for features in features_list:
            result = predictor.predict(features)
            assert 0 <= result["demand_score"] <= 1

    def test_category_encoding(self, predictor):
        """Test category encoding in prediction."""
        categories = ["Electronics", "Fashion", "Sports"]
        
        for cat in categories:
            features = {
                "category": cat,
                "price": 30.0,
                "rating": 4.0,
                "review_count": 100,
                "competitor_count": 20,
                "supplier_rating": 4.0,
                "shipping_days": 14
            }
            result = predictor.predict(features)
            assert "demand_score" in result

    def test_training_data_shape(self, predictor):
        """Test training data has correct shape."""
        df, target = predictor._generate_training_data(n_samples=500)
        
        expected_features = 7
        assert df.shape[1] == expected_features
        assert len(target) == 500

    def test_train_returns_metrics(self, predictor):
        """Test that training returns metrics."""
        metrics = predictor.train(n_samples=100)
        
        assert isinstance(metrics, dict)
        assert "rmse" in metrics or "status" in metrics

    def test_mock_predict_factors(self, predictor, sample_features):
        """Test that mock prediction returns factors."""
        result = predictor._mock_predict(sample_features)
        
        assert "factors" in result
        assert isinstance(result["factors"], dict)

    def test_predict_with_missing_features(self, predictor):
        """Test prediction with missing optional features."""
        features = {
            "category": "Electronics",
            "price": 30.0
        }
        
        result = predictor.predict(features)
        
        assert "demand_score" in result
        assert 0 <= result["demand_score"] <= 1

    def test_demand_score_variance(self, predictor):
        """Test that different inputs produce different scores."""
        features1 = {
            "category": "Electronics",
            "price": 100.0,
            "rating": 5.0,
            "review_count": 5000,
            "competitor_count": 5,
            "supplier_rating": 5.0,
            "shipping_days": 5
        }
        
        features2 = {
            "category": "Toys",
            "price": 10.0,
            "rating": 1.0,
            "review_count": 0,
            "competitor_count": 100,
            "supplier_rating": 3.5,
            "shipping_days": 30
        }
        
        result1 = predictor.predict(features1)
        result2 = predictor.predict(features2)
        
        assert result1["demand_score"] != result2["demand_score"]
