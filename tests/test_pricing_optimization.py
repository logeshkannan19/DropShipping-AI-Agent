"""Unit tests for Pricing Optimization Agent."""

import pytest
from backend.agents.pricing_optimization import (
    PricingOptimizationAgent,
    PricingStrategy,
    optimize_price
)


class TestPricingOptimizationAgent:
    """Test cases for PricingOptimizationAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance."""
        return PricingOptimizationAgent(target_margin=30.0)

    @pytest.fixture
    def sample_cost(self):
        """Sample cost price."""
        return 25.99

    @pytest.fixture
    def sample_competitor_prices(self):
        """Sample competitor prices."""
        return [45.99, 49.99, 42.99, 47.99]

    def test_agent_initialization(self, agent):
        """Test agent initialization."""
        assert agent.target_margin == 30.0
        assert isinstance(agent.price_history, dict)

    def test_cost_plus_pricing(self, agent, sample_cost):
        """Test cost-plus pricing strategy."""
        result = agent._cost_plus_pricing(sample_cost, 30.0)
        
        assert "optimal_price" in result
        assert "margin_percent" in result
        assert "estimated_profit" in result
        assert result["margin_percent"] == 30.0
        assert result["optimal_price"] > sample_cost
        assert result["estimated_profit"] > 0

    def test_competitive_pricing_with_competitors(self, agent, sample_cost, sample_competitor_prices):
        """Test competitive pricing with competitor prices."""
        result = agent._competitive_pricing(
            sample_cost,
            sample_competitor_prices,
            demand_score=0.7
        )
        
        assert "optimal_price" in result
        assert "competitor_analysis" in result
        assert result["competitor_analysis"]["min"] == min(sample_competitor_prices)
        assert result["competitor_analysis"]["max"] == max(sample_competitor_prices)
        assert result["competitor_analysis"]["avg"] == sum(sample_competitor_prices) / len(sample_competitor_prices)

    def test_competitive_pricing_without_competitors(self, agent, sample_cost):
        """Test competitive pricing falls back to cost-plus."""
        result = agent._competitive_pricing(
            sample_cost,
            competitor_prices=[],
            demand_score=0.5
        )
        
        assert "optimal_price" in result
        assert result["optimal_price"] >= sample_cost * 1.15

    def test_premium_pricing(self, agent, sample_cost):
        """Test premium pricing for high-demand products."""
        result = agent._premium_pricing(
            sample_cost,
            margin=30.0,
            demand_score=0.9
        )
        
        assert "optimal_price" in result
        assert result["optimal_price"] > sample_cost
        assert result["margin_percent"] > 30.0

    def test_penetration_pricing(self, agent, sample_cost, sample_competitor_prices):
        """Test penetration pricing strategy."""
        result = agent._penetration_pricing(
            sample_cost,
            competitor_prices=sample_competitor_prices
        )
        
        assert "optimal_price" in result
        assert result["optimal_price"] < min(sample_competitor_prices)
        assert result["optimal_price"] >= sample_cost * 1.1

    def test_dynamic_pricing(self, agent, sample_cost, sample_competitor_prices):
        """Test dynamic pricing strategy."""
        result = agent._dynamic_pricing(
            sample_cost,
            competitor_prices=sample_competitor_prices,
            demand_score=0.8
        )
        
        assert "optimal_price" in result
        assert result["optimal_price"] > sample_cost

    def test_optimize_price_auto_strategy(self, agent, sample_cost, sample_competitor_prices):
        """Test auto strategy selection."""
        result = agent.optimize_price(
            cost_price=sample_cost,
            competitor_prices=sample_competitor_prices,
            demand_score=0.75,
            strategy="auto"
        )
        
        assert "optimal_price" in result
        assert "strategy" in result
        assert "recommendations" in result

    def test_optimize_price_with_specific_strategy(self, agent, sample_cost, sample_competitor_prices):
        """Test specific strategy selection."""
        for strategy in PricingStrategy:
            result = agent.optimize_price(
                cost_price=sample_cost,
                competitor_prices=sample_competitor_prices,
                demand_score=0.5,
                strategy=strategy.value
            )
            
            assert result["strategy"] == strategy.value

    def test_strategy_selection_high_demand(self, agent):
        """Test strategy selection for high demand."""
        strategy = agent._select_strategy(
            demand_score=0.8,
            competitor_prices=[50.0, 60.0, 55.0]
        )
        
        assert strategy in [PricingStrategy.PREMIUM, PricingStrategy.COMPETITIVE]

    def test_strategy_selection_low_demand(self, agent):
        """Test strategy selection for low demand."""
        strategy = agent._select_strategy(
            demand_score=0.3,
            competitor_prices=[40.0, 45.0]
        )
        
        assert strategy == PricingStrategy.PENETRATION

    def test_generate_recommendations(self, agent):
        """Test recommendation generation."""
        recommendations = agent._generate_recommendations(
            cost_price=25.99,
            optimal_price=45.99,
            demand_score=0.8,
            competitor_prices=[40.0, 45.0, 50.0]
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) >= 0

    def test_generate_recommendations_low_margin(self, agent):
        """Test recommendations for low margin."""
        recommendations = agent._generate_recommendations(
            cost_price=25.99,
            optimal_price=28.99,
            demand_score=0.5,
            competitor_prices=[30.0, 32.0]
        )
        
        assert any("negotiating" in rec.lower() for rec in recommendations)

    def test_optimize_batch(self, agent):
        """Test batch optimization."""
        products = [
            {"id": 1, "name": "Product 1", "cost_price": 20.0, "competitor_prices": [35.0], "demand_score": 0.7},
            {"id": 2, "name": "Product 2", "cost_price": 15.0, "competitor_prices": [30.0], "demand_score": 0.5},
        ]
        
        results = agent.optimize_batch(products)
        
        assert len(results) == 2
        assert all("optimal_price" in r for r in results)
        assert results[0]["product_id"] == 1
        assert results[1]["product_id"] == 2

    def test_convenience_function(self, sample_cost, sample_competitor_prices):
        """Test convenience function."""
        result = optimize_price(
            cost_price=sample_cost,
            competitor_prices=sample_competitor_prices,
            demand_score=0.6,
            target_margin=25.0
        )
        
        assert "optimal_price" in result
        assert result["optimal_price"] > sample_cost

    def test_price_calculation_accuracy(self, agent):
        """Test price calculation accuracy."""
        cost = 100.0
        margin = 30.0
        
        result = agent._cost_plus_pricing(cost, margin)
        
        expected_price = cost * (1 + margin / 100)
        assert abs(result["optimal_price"] - expected_price) < 0.01

    def test_simulate_rl_pricing(self, agent, sample_cost):
        """Test RL pricing simulation."""
        result = agent.simulate_rl_pricing(
            cost_price=sample_cost,
            current_price=50.0,
            sales_count=100,
            demand_score=0.7,
            iterations=50
        )
        
        assert "recommended_price" in result
        assert "expected_improvement" in result
        assert result["recommended_price"] >= sample_cost
