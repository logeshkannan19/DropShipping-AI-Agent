"""Unit tests for Product Research Agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio

from backend.agents.product_research import ProductResearchAgent


class TestProductResearchAgent:
    """Test cases for ProductResearchAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance."""
        return ProductResearchAgent(mock_mode=True)

    @pytest.mark.asyncio
    async def test_research_products_mock_mode(self, agent):
        """Test product research in mock mode."""
        products = await agent.research_products(limit=10)
        
        assert len(products) == 10
        assert all("name" in p for p in products)
        assert all("category" in p for p in products)
        assert all("cost_price" in p for p in products)
        assert all("rating" in p for p in products)
        assert all("estimated_orders" in p for p in products)

    @pytest.mark.asyncio
    async def test_research_products_limit(self, agent):
        """Test that limit is respected."""
        products = await agent.research_products(limit=5)
        assert len(products) == 5

    @pytest.mark.asyncio
    async def test_analyze_product(self, agent):
        """Test product analysis."""
        product = {
            "name": "Test Product",
            "cost_price": 15.99,
            "rating": 4.5,
            "estimated_orders": 1500
        }
        
        analyzed = await agent.analyze_product(product)
        
        assert "profitability_score" in analyzed
        assert "trend_indicator" in analyzed
        assert analyzed["trend_indicator"] == "up"

    @pytest.mark.asyncio
    async def test_analyze_product_low_orders(self, agent):
        """Test product analysis with low orders."""
        product = {
            "name": "Low Orders Product",
            "cost_price": 50.99,
            "rating": 3.5,
            "estimated_orders": 500
        }
        
        analyzed = await agent.analyze_product(product)
        
        assert "profitability_score" in analyzed
        assert analyzed["profitability_score"] < 0.6

    def test_categories_available(self, agent):
        """Test that categories are defined."""
        assert len(agent.categories) > 0
        assert "Electronics" in agent.categories
        assert "Sports" in agent.categories

    @pytest.mark.asyncio
    async def test_research_real_mode_fallback(self):
        """Test that real mode falls back to mock."""
        agent = ProductResearchAgent(mock_mode=False)
        products = await agent.research_products(limit=5)
        
        assert len(products) == 5
        assert all("name" in p for p in products)

    def test_agent_initialization(self):
        """Test agent initialization."""
        agent1 = ProductResearchAgent(mock_mode=True)
        assert agent1.mock_mode == True
        
        agent2 = ProductResearchAgent(mock_mode=False)
        assert agent2.mock_mode == False

    @pytest.mark.asyncio
    async def test_product_data_structure(self, agent):
        """Test that product data has all required fields."""
        products = await agent.research_products(limit=3)
        
        required_fields = [
            "name", "description", "category", "cost_price",
            "rating", "review_count", "estimated_orders",
            "supplier_id", "supplier_rating", "shipping_time_days",
            "stock_quantity", "source"
        ]
        
        for product in products:
            for field in required_fields:
                assert field in product, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_price_variance(self, agent):
        """Test that mock products have price variance."""
        products = await agent.research_products(limit=10)
        
        prices = [p["cost_price"] for p in products]
        assert len(set(prices)) > 1

    @pytest.mark.asyncio
    async def test_rating_in_valid_range(self, agent):
        """Test that ratings are in valid range."""
        products = await agent.research_products(limit=20)
        
        for product in products:
            assert 1.0 <= product["rating"] <= 5.0
