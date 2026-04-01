"""Pricing Optimization Agent Module."""

from enum import Enum
from typing import List, Dict, Any, Optional


class PricingStrategy(str, Enum):
    """Pricing strategy types."""
    
    COST_PLUS = "cost_plus"
    COMPETITIVE = "competitive"
    PREMIUM = "premium"
    PENETRATION = "penetration"
    DYNAMIC = "dynamic"


class PricingAgent:
    """
    Agent for optimizing product prices.
    
    Implements multiple pricing strategies based on cost,
    competition, and demand.
    """
    
    def __init__(self, target_margin: float = 0.30):
        """
        Initialize the pricing agent.
        
        Args:
            target_margin: Default target profit margin (0.0 - 1.0)
        """
        self.target_margin = target_margin
        self.min_margin = 0.15
        self.max_margin = 0.60
    
    def optimize_price(
        self,
        cost_price: float,
        competitor_prices: List[float],
        demand_score: float,
        strategy: str = "auto"
    ) -> Dict[str, Any]:
        """
        Calculate optimal price for a product.
        
        Args:
            cost_price: Cost price from supplier
            competitor_prices: List of competitor prices
            demand_score: Predicted demand score (0-1)
            strategy: Pricing strategy to use
            
        Returns:
            Optimization result with price and metadata
        """
        if strategy == "auto":
            strategy = self._select_strategy(demand_score, competitor_prices)
        
        if strategy == PricingStrategy.COST_PLUS:
            return self._cost_plus_pricing(cost_price)
        elif strategy == PricingStrategy.COMPETITIVE:
            return self._competitive_pricing(cost_price, competitor_prices, demand_score)
        elif strategy == PricingStrategy.PREMIUM:
            return self._premium_pricing(cost_price, demand_score)
        elif strategy == PricingStrategy.PENETRATION:
            return self._penetration_pricing(cost_price, competitor_prices)
        else:
            return self._cost_plus_pricing(cost_price)
    
    def _select_strategy(
        self,
        demand_score: float,
        competitor_prices: List[float]
    ) -> PricingStrategy:
        """Select best pricing strategy based on context."""
        if demand_score > 0.7 and competitor_prices:
            avg = sum(competitor_prices) / len(competitor_prices)
            if avg > 50:
                return PricingStrategy.PREMIUM
            return PricingStrategy.COMPETITIVE
        elif demand_score > 0.5:
            return PricingStrategy.COST_PLUS
        else:
            return PricingStrategy.PENETRATION
    
    def _cost_plus_pricing(self, cost_price: float) -> Dict[str, Any]:
        """Calculate price using cost-plus method."""
        optimal_price = cost_price * (1 + self.target_margin)
        profit = optimal_price - cost_price
        margin = (profit / optimal_price) * 100
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin, 1),
            "estimated_profit": round(profit, 2),
            "strategy": PricingStrategy.COST_PLUS.value
        }
    
    def _competitive_pricing(
        self,
        cost_price: float,
        competitor_prices: List[float],
        demand_score: float
    ) -> Dict[str, Any]:
        """Calculate price based on competitor analysis."""
        if not competitor_prices:
            return self._cost_plus_pricing(cost_price)
        
        avg_price = sum(competitor_prices) / len(competitor_prices)
        demand_factor = 0.9 if demand_score < 0.5 else 1.0 if demand_score < 0.7 else 1.1
        
        optimal_price = avg_price * 0.95 * demand_factor
        optimal_price = max(optimal_price, cost_price * 1.15)
        
        profit = optimal_price - cost_price
        margin = (profit / optimal_price) * 100
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin, 1),
            "estimated_profit": round(profit, 2),
            "strategy": PricingStrategy.COMPETITIVE.value,
            "competitor_analysis": {
                "min": round(min(competitor_prices), 2),
                "max": round(max(competitor_prices), 2),
                "avg": round(avg_price, 2)
            }
        }
    
    def _premium_pricing(
        self,
        cost_price: float,
        demand_score: float
    ) -> Dict[str, Any]:
        """Calculate premium pricing for high-demand products."""
        premium_margin = self.target_margin * (1 + demand_score * 0.5)
        premium_margin = min(premium_margin, self.max_margin)
        
        optimal_price = cost_price * (1 + premium_margin)
        profit = optimal_price - cost_price
        margin = (profit / optimal_price) * 100
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin * 100, 1),
            "estimated_profit": round(profit, 2),
            "strategy": PricingStrategy.PREMIUM.value
        }
    
    def _penetration_pricing(
        self,
        cost_price: float,
        competitor_prices: List[float]
    ) -> Dict[str, Any]:
        """Calculate penetration pricing to gain market share."""
        if competitor_prices:
            min_competitor = min(competitor_prices)
        else:
            min_competitor = cost_price * 1.1
        
        optimal_price = min_competitor * 0.85
        optimal_price = max(optimal_price, cost_price * 1.1)
        
        profit = optimal_price - cost_price
        margin = (profit / optimal_price) * 100
        
        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin * 100, 1),
            "estimated_profit": round(profit, 2),
            "strategy": PricingStrategy.PENETRATION.value
        }
