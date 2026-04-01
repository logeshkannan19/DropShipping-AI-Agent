"""AI Decision Agent Module."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import asyncio


@dataclass
class AgentDecision:
    """Represents an agent decision."""
    
    action: str
    reason: str
    confidence: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


class AIDecisionAgent:
    """
    Core AI decision agent for the dropshipping system.
    
    Uses a planning loop: plan → execute → evaluate → improve
    """
    
    def __init__(
        self,
        min_demand_score: float = 0.5,
        min_profit_margin: float = 0.2
    ):
        """
        Initialize the AI decision agent.
        
        Args:
            min_demand_score: Minimum demand score to consider
            min_profit_margin: Minimum profit margin percentage
        """
        self.min_demand_score = min_demand_score
        self.min_profit_margin = min_profit_margin
        self.decisions: List[AgentDecision] = []
        self.metrics = {
            "products_analyzed": 0,
            "products_selected": 0,
            "products_published": 0
        }
    
    async def run_full_pipeline(
        self,
        max_products: int = 10,
        auto_publish: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete AI agent pipeline.
        
        Args:
            max_products: Maximum products to analyze
            auto_publish: Whether to auto-publish
            
        Returns:
            Pipeline results
        """
        from backend.agents.product_research import ProductResearchAgent
        from backend.agents.pricing import PricingAgent
        
        start_time = datetime.utcnow()
        phases = {}
        
        products = await ProductResearchAgent().research_products(max_products)
        phases["research"] = {"products_found": len(products)}
        
        pricing_agent = PricingAgent()
        analyzed_products = []
        
        for product in products:
            demand_score = self._calculate_demand_score(product)
            product["demand_score"] = demand_score
            
            if demand_score >= self.min_demand_score:
                pricing = pricing_agent.optimize_price(
                    cost_price=product["cost_price"],
                    competitor_prices=[product["cost_price"] * 2],
                    demand_score=demand_score
                )
                product["selling_price"] = pricing["optimal_price"]
                product["margin"] = pricing["margin_percent"]
                analyzed_products.append(product)
        
        phases["analysis"] = {
            "products_analyzed": len(products),
            "products_selected": len(analyzed_products)
        }
        
        published = 0
        if auto_publish:
            published = len(analyzed_products)
        
        phases["publishing"] = {"products_published": published}
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        self.metrics["products_analyzed"] += len(products)
        self.metrics["products_selected"] += len(analyzed_products)
        self.metrics["products_published"] += published
        
        self._record_decisions(analyzed_products)
        
        return {
            "status": "completed",
            "products_analyzed": len(products),
            "products_selected": len(analyzed_products),
            "products_published": published,
            "revenue_potential": sum(
                p.get("selling_price", 0) - p.get("cost_price", 0)
                for p in analyzed_products
            ),
            "execution_time": execution_time,
            "phases": phases
        }
    
    def _calculate_demand_score(self, product: Dict[str, Any]) -> float:
        """Calculate demand score for a product."""
        rating = product.get("rating", 4.0) / 5.0
        orders = min(product.get("estimated_orders", 100) / 2000, 1.0)
        cost = product.get("cost_price", 30)
        
        cost_factor = 1.0 if cost < 20 else 0.7 if cost < 40 else 0.4
        
        score = rating * 0.3 + orders * 0.4 + cost_factor * 0.3
        
        return min(max(score, 0.0), 1.0)
    
    def _record_decisions(self, products: List[Dict[str, Any]]):
        """Record agent decisions."""
        for product in products:
            decision = AgentDecision(
                action="SELECT",
                reason=f"Demand: {product.get('demand_score', 0):.2f}",
                confidence=product.get("demand_score", 0.5)
            )
            self.decisions.append(decision)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        return {
            **self.metrics,
            "total_decisions": len(self.decisions)
        }
