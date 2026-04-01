"""
Pricing Optimization Agent Module

This module handles pricing strategy and optimization:
- Rule-based pricing: price = cost + margin + competitor adjustment
- Optional reinforcement learning placeholder
- AI-enhanced pricing decisions
"""

import random
from typing import List, Dict, Optional, Any
from enum import Enum
from loguru import logger
from backend.config.settings import get_settings

settings = get_settings()


class PricingStrategy(str, Enum):
    """Pricing strategy types."""
    COST_PLUS = "cost_plus"
    COMPETITIVE = "competitive"
    PREMIUM = "premium"
    PENETRATION = "penetration"
    DYNAMIC = "dynamic"


class PricingOptimizationAgent:
    """
    Agent responsible for optimizing product prices.
    
    Implements multiple pricing strategies and can use AI
    for enhanced decision making.
    """
    
    def __init__(self, target_margin: float = 30.0):
        """
        Initialize the pricing optimization agent.
        
        Args:
            target_margin: Default target profit margin percentage
        """
        self.target_margin = target_margin
        self.price_history = {}
        logger.info(f"PricingOptimizationAgent initialized with target margin: {target_margin}%")
    
    def optimize_price(
        self,
        cost_price: float,
        competitor_prices: List[float],
        demand_score: float,
        target_margin: float = None,
        strategy: str = "auto"
    ) -> Dict[str, Any]:
        """
        Calculate optimal price for a product.
        
        Args:
            cost_price: Cost price from supplier
            competitor_prices: List of competitor prices
            demand_score: Predicted demand score (0-1)
            target_margin: Target profit margin percentage
            strategy: Pricing strategy to use
            
        Returns:
            Optimization result with price and metadata
        """
        margin = target_margin or self.target_margin
        
        if strategy == "auto":
            strategy = self._select_strategy(demand_score, competitor_prices)
        
        logger.info(f"Optimizing price with strategy: {strategy}")
        
        if strategy == PricingStrategy.COST_PLUS:
            result = self._cost_plus_pricing(cost_price, margin)
        elif strategy == PricingStrategy.COMPETITIVE:
            result = self._competitive_pricing(cost_price, competitor_prices, demand_score)
        elif strategy == PricingStrategy.PREMIUM:
            result = self._premium_pricing(cost_price, margin, demand_score)
        elif strategy == PricingStrategy.PENETRATION:
            result = self._penetration_pricing(cost_price, competitor_prices)
        elif strategy == PricingStrategy.DYNAMIC:
            result = self._dynamic_pricing(cost_price, competitor_prices, demand_score)
        else:
            result = self._cost_plus_pricing(cost_price, margin)
        
        result["strategy"] = strategy.value
        result["recommendations"] = self._generate_recommendations(
            cost_price, result["optimal_price"], demand_score, competitor_prices
        )
        
        return result
    
    def _select_strategy(self, demand_score: float, competitor_prices: List[float]) -> PricingStrategy:
        """
        Automatically select best pricing strategy based on context.
        
        Args:
            demand_score: Predicted demand
            competitor_prices: Competitor prices
            
        Returns:
            Selected pricing strategy
        """
        if demand_score > 0.7 and len(competitor_prices) > 0:
            avg_competitor = sum(competitor_prices) / len(competitor_prices)
            if avg_competitor > 50:
                return PricingStrategy.PREMIUM
            return PricingStrategy.COMPETITIVE
        elif demand_score > 0.5:
            return PricingStrategy.COST_PLUS
        else:
            return PricingStrategy.PENETRATION
    
    def _cost_plus_pricing(self, cost_price: float, margin: float) -> Dict[str, Any]:
        """
        Calculate price using cost-plus method.
        
        Args:
            cost_price: Cost price
            margin: Target margin percentage
            
        Returns:
            Pricing result
        """
        optimal_price = cost_price * (1 + margin / 100)
        profit = optimal_price - cost_price
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": margin,
            "estimated_profit": round(profit, 2),
            "pricing_method": "cost_plus"
        }
    
    def _competitive_pricing(
        self,
        cost_price: float,
        competitor_prices: List[float],
        demand_score: float
    ) -> Dict[str, Any]:
        """
        Calculate price based on competitor analysis.
        
        Args:
            cost_price: Cost price
            competitor_prices: Competitor prices
            demand_score: Demand score
            
        Returns:
            Pricing result
        """
        if not competitor_prices:
            return self._cost_plus_pricing(cost_price, self.target_margin)
        
        min_price = min(competitor_prices)
        max_price = max(competitor_prices)
        avg_price = sum(competitor_prices) / len(competitor_prices)
        
        # Adjust based on demand
        demand_factor = 0.9 if demand_score < 0.5 else 1.0 if demand_score < 0.7 else 1.1
        
        # Price at slightly below average for competitiveness
        optimal_price = avg_price * 0.95 * demand_factor
        
        # Ensure we don't go below cost
        optimal_price = max(optimal_price, cost_price * 1.15)
        
        margin = ((optimal_price - cost_price) / optimal_price) * 100
        profit = optimal_price - cost_price
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin, 1),
            "estimated_profit": round(profit, 2),
            "pricing_method": "competitive",
            "competitor_analysis": {
                "min": round(min_price, 2),
                "max": round(max_price, 2),
                "avg": round(avg_price, 2)
            }
        }
    
    def _premium_pricing(
        self,
        cost_price: float,
        margin: float,
        demand_score: float
    ) -> Dict[str, Any]:
        """
        Calculate premium pricing for high-demand products.
        
        Args:
            cost_price: Cost price
            margin: Base margin
            demand_score: Demand score
            
        Returns:
            Pricing result
        """
        # Higher margin for high demand
        premium_margin = margin * (1 + demand_score * 0.5)
        
        optimal_price = cost_price * (1 + premium_margin / 100)
        profit = optimal_price - cost_price
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(premium_margin, 1),
            "estimated_profit": round(profit, 2),
            "pricing_method": "premium"
        }
    
    def _penetration_pricing(
        self,
        cost_price: float,
        competitor_prices: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate penetration pricing to gain market share.
        
        Args:
            cost_price: Cost price
            competitor_prices: Competitor prices
            
        Returns:
            Pricing result
        """
        if not competitor_prices:
            min_competitor = cost_price * 1.1
        else:
            min_competitor = min(competitor_prices)
        
        # Price lower than competitors
        optimal_price = min_competitor * 0.85
        optimal_price = max(optimal_price, cost_price * 1.1)  # Ensure minimum profit
        
        margin = ((optimal_price - cost_price) / optimal_price) * 100
        profit = optimal_price - cost_price
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin, 1),
            "estimated_profit": round(profit, 2),
            "pricing_method": "penetration"
        }
    
    def _dynamic_pricing(
        self,
        cost_price: float,
        competitor_prices: List[float],
        demand_score: float
    ) -> Dict[str, Any]:
        """
        Dynamic pricing based on multiple factors.
        
        Args:
            cost_price: Cost price
            competitor_prices: Competitor prices
            demand_score: Demand score
            
        Returns:
            Pricing result
        """
        base_price = cost_price * (1 + self.target_margin / 100)
        
        if competitor_prices:
            avg_competitor = sum(competitor_prices) / len(competitor_prices)
            competitor_factor = avg_competitor / base_price if base_price > 0 else 1
        else:
            competitor_factor = 1
        
        # Adjust for demand
        demand_factor = 0.8 + (demand_score * 0.4)
        
        optimal_price = base_price * competitor_factor * demand_factor
        optimal_price = max(optimal_price, cost_price * 1.1)
        
        margin = ((optimal_price - cost_price) / optimal_price) * 100
        profit = optimal_price - cost_price
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin, 1),
            "estimated_profit": round(profit, 2),
            "pricing_method": "dynamic"
        }
    
    def _generate_recommendations(
        self,
        cost_price: float,
        optimal_price: float,
        demand_score: float,
        competitor_prices: List[float]
    ) -> List[str]:
        """
        Generate pricing recommendations.
        
        Args:
            cost_price: Cost price
            optimal_price: Calculated optimal price
            demand_score: Demand score
            competitor_prices: Competitor prices
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        margin = ((optimal_price - cost_price) / optimal_price) * 100
        
        if margin < 15:
            recommendations.append("Consider negotiating better supplier pricing")
        elif margin > 50:
            recommendations.append("Room to lower price for better competitiveness")
        
        if demand_score > 0.7:
            recommendations.append("High demand justifies premium pricing")
        elif demand_score < 0.4:
            recommendations.append("Consider promotional pricing to boost sales")
        
        if competitor_prices:
            avg_competitor = sum(competitor_prices) / len(competitor_prices)
            if optimal_price > avg_competitor * 1.1:
                recommendations.append("Price is above average competitor - consider reducing")
            elif optimal_price < avg_competitor * 0.9:
                recommendations.append("Price is competitive but may leave money on table")
        
        if optimal_price < cost_price:
            recommendations.append("ERROR: Price below cost! Adjust pricing strategy")
        
        return recommendations
    
    def optimize_batch(
        self,
        products: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Optimize prices for multiple products.
        
        Args:
            products: List of product data with cost_price, competitor_prices, demand_score
            
        Returns:
            List of optimization results
        """
        results = []
        for product in products:
            result = self.optimize_price(
                cost_price=product.get("cost_price", 0),
                competitor_prices=product.get("competitor_prices", []),
                demand_score=product.get("demand_score", 0.5),
                target_margin=product.get("target_margin")
            )
            result["product_id"] = product.get("id")
            result["product_name"] = product.get("name")
            results.append(result)
        
        return results
    
    def simulate_rl_pricing(
        self,
        cost_price: float,
        current_price: float,
        sales_count: int,
        demand_score: float,
        iterations: int = 100
    ) -> Dict[str, Any]:
        """
        Placeholder for reinforcement learning pricing.
        
        In production, this would use RL to learn optimal pricing
        based on historical sales data.
        
        Args:
            cost_price: Product cost
            current_price: Current selling price
            sales_count: Number of sales
            demand_score: Demand score
            iterations: Number of simulation iterations
            
        Returns:
            Simulation results
        """
        logger.info("Running RL pricing simulation (placeholder)")
        
        # Simple multi-armed bandit simulation
        price_points = [current_price * 0.8, current_price, current_price * 1.2]
        rewards = []
        
        for price in price_points:
            # Simulated reward based on demand and price
            if price < cost_price:
                reward = 0
            else:
                margin = (price - cost_price) / price
                expected_sales = sales_count * (1 - abs(price - current_price) / current_price)
                reward = margin * expected_sales * demand_score
            rewards.append(reward)
        
        best_idx = rewards.index(max(rewards))
        
        return {
            "recommended_price": round(price_points[best_idx], 2),
            "expected_improvement": round((rewards[best_idx] - rewards[1]) / max(rewards[1], 1) * 100, 1),
            "simulation_iterations": iterations,
            "note": "This is a placeholder for actual RL implementation"
        }


def optimize_price(
    cost_price: float,
    competitor_prices: List[float],
    demand_score: float,
    target_margin: float = 30.0
) -> Dict[str, Any]:
    """
    Convenience function to optimize price.
    
    Args:
        cost_price: Product cost
        competitor_prices: Competitor prices
        demand_score: Demand prediction
        target_margin: Target margin
        
    Returns:
        Optimization result
    """
    agent = PricingOptimizationAgent(target_margin)
    return agent.optimize_price(cost_price, competitor_prices, demand_score, target_margin)