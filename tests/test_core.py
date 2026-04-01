"""
Unit tests for DropShipping AI Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestProductResearchAgent:
    """Tests for Product Research Agent."""
    
    @pytest.mark.asyncio
    async def test_generate_mock_products(self):
        """Test mock product generation."""
        from backend.agents.product_research import ProductResearchAgent
        
        agent = ProductResearchAgent(mock_mode=True)
        products = await agent.research_products(limit=5)
        
        assert len(products) == 5
        assert all("name" in p for p in products)
        assert all("category" in p for p in products)
        assert all("cost_price" in p for p in products)
    
    @pytest.mark.asyncio
    async def test_analyze_product(self):
        """Test product analysis."""
        from backend.agents.product_research import ProductResearchAgent
        
        agent = ProductResearchAgent()
        product_data = {
            "name": "Test Product",
            "cost_price": 25.0,
            "rating": 4.5,
            "estimated_orders": 1000
        }
        
        analyzed = await agent.analyze_product(product_data)
        
        assert "profitability_score" in analyzed
        assert "trend_indicator" in analyzed
        assert analyzed["profitability_score"] > 0


class TestDemandPredictor:
    """Tests for Demand Prediction Model."""
    
    def test_generate_training_data(self):
        """Test training data generation."""
        from backend.models.demand_prediction import DemandPredictor
        
        predictor = DemandPredictor()
        X, y = predictor._generate_training_data(100)
        
        assert len(X) == 100
        assert len(y) == 100
        assert all(0 <= v <= 1 for v in y)
    
    def test_train_model(self):
        """Test model training."""
        from backend.models.demand_prediction import DemandPredictor
        
        predictor = DemandPredictor()
        result = predictor.train(n_samples=100)
        
        assert result is not None
        assert predictor.is_trained
    
    def test_mock_predict(self):
        """Test mock prediction."""
        from backend.models.demand_prediction import DemandPredictor
        
        predictor = DemandPredictor()
        features = {
            "rating": 4.5,
            "review_count": 500,
            "price": 30,
            "supplier_rating": 4.5
        }
        
        result = predictor._mock_predict(features)
        
        assert "demand_score" in result
        assert "confidence" in result
        assert 0 <= result["demand_score"] <= 1
    
    def test_predict_with_features(self):
        """Test prediction with features."""
        from backend.models.demand_prediction import DemandPredictor
        
        predictor = DemandPredictor()
        predictor.train(n_samples=100)
        
        features = {
            "category": "Electronics",
            "price": 25.0,
            "rating": 4.5,
            "review_count": 500,
            "competitor_count": 20,
            "supplier_rating": 4.5,
            "shipping_days": 14
        }
        
        result = predictor.predict(features)
        
        assert "demand_score" in result
        assert "factors" in result


class TestPricingOptimizationAgent:
    """Tests for Pricing Optimization Agent."""
    
    def test_cost_plus_pricing(self):
        """Test cost-plus pricing strategy."""
        from backend.agents.pricing_optimization import PricingOptimizationAgent
        
        agent = PricingOptimizationAgent(target_margin=30.0)
        
        result = agent._cost_plus_pricing(20.0, 30.0)
        
        assert result["optimal_price"] == 26.0
        assert result["margin_percent"] == 30.0
        assert result["estimated_profit"] == 6.0
    
    def test_competitive_pricing(self):
        """Test competitive pricing strategy."""
        from backend.agents.pricing_optimization import PricingOptimizationAgent
        
        agent = PricingOptimizationAgent()
        
        result = agent._competitive_pricing(
            cost_price=20.0,
            competitor_prices=[25.0, 30.0, 35.0],
            demand_score=0.7
        )
        
        assert result["optimal_price"] > 20.0
        assert "competitor_analysis" in result
    
    def test_optimize_price(self):
        """Test main optimize price function."""
        from backend.agents.pricing_optimization import PricingOptimizationAgent
        
        agent = PricingOptimizationAgent(target_margin=25.0)
        
        result = agent.optimize_price(
            cost_price=20.0,
            competitor_prices=[25.0, 30.0],
            demand_score=0.6
        )
        
        assert "optimal_price" in result
        assert "margin_percent" in result
        assert "recommendations" in result
        assert result["optimal_price"] > 20.0
    
    def test_batch_optimization(self):
        """Test batch price optimization."""
        from backend.agents.pricing_optimization import PricingOptimizationAgent
        
        agent = PricingOptimizationAgent()
        
        products = [
            {"id": 1, "name": "Product 1", "cost_price": 20.0, "demand_score": 0.7, "competitor_prices": [25.0, 30.0]},
            {"id": 2, "name": "Product 2", "cost_price": 15.0, "demand_score": 0.5, "competitor_prices": [20.0, 25.0]}
        ]
        
        results = agent.optimize_batch(products)
        
        assert len(results) == 2
        assert all("optimal_price" in r for r in results)


class TestSupplierService:
    """Tests for Supplier Service."""
    
    @pytest.mark.asyncio
    async def test_get_supplier(self):
        """Test getting supplier info."""
        from backend.services.supplier_service import get_supplier_service
        
        service = get_supplier_service()
        supplier = await service.get_supplier("SUP-001")
        
        assert supplier is not None
        assert supplier["supplier_id"] == "SUP-001"
        assert "name" in supplier
        assert "rating" in supplier
    
    @pytest.mark.asyncio
    async def test_check_stock(self):
        """Test stock checking."""
        from backend.services.supplier_service import get_supplier_service
        
        service = get_supplier_service()
        result = await service.check_stock("PROD-001", 10)
        
        assert "available" in result
        assert result["available"] is True
    
    @pytest.mark.asyncio
    async def test_place_order(self):
        """Test placing order."""
        from backend.services.supplier_service import get_supplier_service
        
        service = get_supplier_service()
        result = await service.place_order("PROD-001", 5)
        
        assert result["success"] is True
        assert "order_id" in result
        assert "total_cost" in result


class TestStoreService:
    """Tests for Store Service."""
    
    @pytest.mark.asyncio
    async def test_create_product(self):
        """Test creating store product."""
        from backend.services.store_service import get_store_service
        
        service = get_store_service()
        
        result = await service.create_product(
            title="Test Product",
            description="Test Description",
            price=29.99
        )
        
        assert result["success"] is True
        assert "store_product_id" in result
        assert result["status"] == "draft"
    
    @pytest.mark.asyncio
    async def test_publish_product(self):
        """Test publishing product."""
        from backend.services.store_service import get_store_service
        
        service = get_store_service()
        
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        store_id = create_result["store_product_id"]
        publish_result = await service.publish_product(store_id)
        
        assert publish_result["success"] is True
        assert publish_result["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_update_price(self):
        """Test updating product price."""
        from backend.services.store_service import get_store_service
        
        service = get_store_service()
        
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        store_id = create_result["store_product_id"]
        update_result = await service.update_price(store_id, 39.99)
        
        assert update_result["success"] is True
        assert update_result["new_price"] == 39.99
    
    @pytest.mark.asyncio
    async def test_list_products(self):
        """Test listing store products."""
        from backend.services.store_service import get_store_service
        
        service = get_store_service()
        
        await service.create_product("Product 1", "Desc 1", 19.99)
        await service.create_product("Product 2", "Desc 2", 29.99)
        
        products = await service.list_products()
        
        assert len(products) >= 2


class TestAIDecisionAgent:
    """Tests for AI Decision Agent."""
    
    @pytest.mark.asyncio
    async def test_calculate_selection_score(self):
        """Test selection score calculation."""
        from backend.agents.ai_decision_agent import AIDecisionAgent
        
        agent = AIDecisionAgent()
        
        product = {
            "demand_score": 0.8,
            "rating": 4.5,
            "estimated_orders": 1000,
            "cost_price": 25.0
        }
        
        score = agent._calculate_selection_score(product)
        
        assert 0 <= score <= 1
    
    @pytest.mark.asyncio
    async def test_make_decision(self):
        """Test making agent decision."""
        from backend.agents.ai_decision_agent import AIDecisionAgent, AgentAction
        
        agent = AIDecisionAgent()
        
        decision = agent._make_decision(
            action=AgentAction.SELECT,
            reason="High demand score",
            confidence=0.9
        )
        
        assert decision.action == AgentAction.SELECT
        assert decision.confidence == 0.9
    
    @pytest.mark.asyncio
    async def test_get_performance_metrics(self):
        """Test getting performance metrics."""
        from backend.agents.ai_decision_agent import AIDecisionAgent
        
        agent = AIDecisionAgent()
        
        metrics = agent.get_performance_metrics()
        
        assert "products_analyzed" in metrics
        assert "products_selected" in metrics
        assert "decision_breakdown" in metrics


class TestAnalyticsService:
    """Tests for Analytics Service."""
    
    @pytest.mark.asyncio
    async def test_get_default_metrics(self):
        """Test getting default metrics."""
        from backend.services.analytics_service import AnalyticsService
        
        service = AnalyticsService()
        metrics = service._get_default_metrics()
        
        assert metrics["total_revenue"] == 0.0
        assert metrics["total_sales"] == 0
        assert metrics["published_products"] == 0
    
    @pytest.mark.asyncio
    async def test_record_sale(self):
        """Test recording a sale."""
        from backend.models.database import init_db, get_session
        from backend.models.database import Product
        from backend.services.analytics_service import AnalyticsService
        
        await init_db("sqlite+aiosqlite:///:memory:")
        
        service = AnalyticsService()
        
        session = await get_session()
        product = Product(
            name="Test Product",
            cost_price=20.0,
            selling_price=40.0,
            category="Test"
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        await session.close()
        
        sale_id = await service.record_sale(
            product_id=product.id,
            quantity=2,
            unit_price=40.0,
            cost_price=20.0
        )
        
        assert sale_id > 0


class TestAPISchemas:
    """Tests for API Schemas."""
    
    def test_product_create_schema(self):
        """Test ProductCreate schema."""
        from backend.models.schemas import ProductCreate
        
        product = ProductCreate(
            name="Test Product",
            description="Test Description",
            category="Electronics",
            cost_price=25.99
        )
        
        assert product.name == "Test Product"
        assert product.category == "Electronics"
    
    def test_predict_demand_request(self):
        """Test PredictDemandRequest schema."""
        from backend.models.schemas import PredictDemandRequest
        
        request = PredictDemandRequest(
            category="Electronics",
            price=29.99,
            rating=4.5,
            review_count=500,
            competitor_count=20,
            supplier_rating=4.5,
            shipping_days=14
        )
        
        assert request.category == "Electronics"
        assert request.price == 29.99
    
    def test_optimize_price_request(self):
        """Test OptimizePriceRequest schema."""
        from backend.models.schemas import OptimizePriceRequest
        
        request = OptimizePriceRequest(
            cost_price=20.0,
            competitor_prices=[25.0, 30.0],
            demand_score=0.7,
            target_margin=30.0
        )
        
        assert request.cost_price == 20.0
        assert len(request.competitor_prices) == 2


class TestDatabaseModels:
    """Tests for Database Models."""
    
    @pytest.mark.asyncio
    async def test_product_model(self):
        """Test Product model."""
        from backend.models.database import Product
        from datetime import datetime
        
        product = Product(
            name="Test Product",
            category="Electronics",
            cost_price=25.99,
            selling_price=49.99,
            rating=4.5
        )
        
        assert product.name == "Test Product"
        assert product.is_active is True
        assert product.is_published is False
    
    @pytest.mark.asyncio
    async def test_sale_model(self):
        """Test Sale model."""
        from backend.models.database import Sale
        
        sale = Sale(
            product_id=1,
            quantity=2,
            unit_price=49.99,
            total_price=99.98,
            cost_price=51.98,
            profit=48.0
        )
        
        assert sale.product_id == 1
        assert sale.quantity == 2
        assert sale.profit == 48.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])