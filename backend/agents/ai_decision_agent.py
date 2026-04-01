"""
AI Decision Agent Module

This is the core brain of the dropshipping agent system:
- Select best products based on demand and profitability
- Decide pricing strategies
- Decide when to drop products
- Implement planning loop: plan → execute → evaluate → improve
"""

import asyncio
import random
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from enum import Enum
from loguru import logger
from backend.config.settings import get_settings

settings = get_settings()


class AgentAction(str, Enum):
    """Possible agent actions."""
    RESEARCH = "research"
    ANALYZE = "analyze"
    PRICING = "pricing"
    PUBLISH = "publish"
    DROP = "drop"
    WAIT = "wait"


class AgentDecision:
    """Represents an agent decision."""
    
    def __init__(
        self,
        action: AgentAction,
        reason: str,
        confidence: float,
        metadata: Dict[str, Any] = None
    ):
        self.action = action
        self.reason = reason
        self.confidence = confidence
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()


class AIDecisionAgent:
    """
    Core AI decision agent for the dropshipping system.
    
    Uses AI-style decision making to:
    - Select best products
    - Determine pricing
    - Decide when to drop products
    - Execute the plan loop
    """
    
    def __init__(
        self,
        min_demand_score: float = 0.5,
        min_profit_margin: float = 20.0
    ):
        """
        Initialize the AI decision agent.
        
        Args:
            min_demand_score: Minimum demand score to consider a product
            min_profit_margin: Minimum profit margin percentage
        """
        self.min_demand_score = min_demand_score
        self.min_profit_margin = min_profit_margin
        self.decision_history: List[AgentDecision] = []
        self.performance_metrics = {
            "products_analyzed": 0,
            "products_selected": 0,
            "products_published": 0,
            "products_dropped": 0,
            "successful_decisions": 0
        }
        logger.info(f"AIDecisionAgent initialized (min_demand={min_demand_score}, min_margin={min_profit_margin}%)")
    
    async def run_full_pipeline(
        self,
        max_products: int = 10,
        auto_publish: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete AI agent pipeline.
        
        This implements the plan → execute → evaluate → improve loop.
        
        Args:
            max_products: Maximum products to analyze
            auto_publish: Whether to auto-publish selected products
            
        Returns:
            Pipeline results
        """
        logger.info("Starting AI agent full pipeline")
        
        start_time = datetime.utcnow()
        results = {
            "status": "running",
            "phases": {}
        }
        
        # Phase 1: Research
        logger.info("Phase 1: Product Research")
        from backend.agents.product_research import ProductResearchAgent
        research_agent = ProductResearchAgent()
        products = await research_agent.research_products(max_products)
        results["phases"]["research"] = {
            "products_found": len(products),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Phase 2: Analyze (Demand Prediction)
        logger.info("Phase 2: Demand Analysis")
        from backend.models.demand_prediction import DemandPredictor
        predictor = DemandPredictor()
        
        analyzed_products = []
        for product in products:
            features = {
                "category": product.get("category", "Electronics"),
                "price": product.get("cost_price", 0),
                "rating": product.get("rating", 4.0),
                "review_count": product.get("review_count", 100),
                "competitor_count": random.randint(10, 50),
                "supplier_rating": product.get("supplier_rating", 4.0),
                "shipping_days": product.get("shipping_time_days", 14)
            }
            prediction = predictor.predict(features)
            product["demand_score"] = prediction["demand_score"]
            product["prediction_confidence"] = prediction.get("confidence", 0.7)
            analyzed_products.append(product)
        
        results["phases"]["analysis"] = {
            "products_analyzed": len(analyzed_products),
            "avg_demand_score": round(sum(p["demand_score"] for p in analyzed_products) / len(analyzed_products), 3),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Phase 3: Select products
        logger.info("Phase 3: Product Selection")
        selected_products = await self._select_products(analyzed_products)
        results["phases"]["selection"] = {
            "products_selected": len(selected_products),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Phase 4: Pricing optimization
        logger.info("Phase 4: Price Optimization")
        from backend.agents.pricing_optimization import PricingOptimizationAgent
        pricing_agent = PricingOptimizationAgent()
        
        for product in selected_products:
            competitor_prices = [
                product["cost_price"] * random.uniform(1.5, 2.5)
                for _ in range(random.randint(3, 8))
            ]
            pricing_result = pricing_agent.optimize_price(
                cost_price=product["cost_price"],
                competitor_prices=competitor_prices,
                demand_score=product["demand_score"]
            )
            product["selling_price"] = pricing_result["optimal_price"]
            product["margin_percent"] = pricing_result["margin_percent"]
            product["pricing_strategy"] = pricing_result["strategy"]
        
        results["phases"]["pricing"] = {
            "products_priced": len(selected_products),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Phase 5: Publish (if enabled)
        published_count = 0
        if auto_publish:
            logger.info("Phase 5: Product Publishing")
            from backend.services.store_service import get_store_service
            store_service = get_store_service()
            
            for product in selected_products:
                try:
                    await store_service.create_product(
                        title=product["name"],
                        description=product.get("description", f"High-quality {product['name']}"),
                        price=product["selling_price"],
                        tags=[product.get("category", "General")]
                    )
                    published_count += 1
                except Exception as e:
                    logger.error(f"Failed to publish product: {e}")
            
            results["phases"]["publishing"] = {
                "products_published": published_count,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Finalize results
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        results["status"] = "completed"
        results["total_duration_seconds"] = round(duration, 2)
        results["products_analyzed"] = len(products)
        results["products_selected"] = len(selected_products)
        results["products_published"] = published_count
        results["revenue_potential"] = round(
            sum(p["selling_price"] - p["cost_price"] for p in selected_products), 2
        )
        
        self.performance_metrics["products_analyzed"] += len(products)
        self.performance_metrics["products_selected"] += len(selected_products)
        self.performance_metrics["products_published"] += published_count
        
        logger.info(f"Pipeline complete: {len(selected_products)} products selected, {published_count} published")
        
        return results
    
    async def _select_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Select best products based on multiple criteria.
        
        Args:
            products: List of analyzed products
            
        Returns:
            List of selected products
        """
        scored_products = []
        
        for product in products:
            score = self._calculate_selection_score(product)
            product["selection_score"] = score
            scored_products.append((score, product))
        
        # Sort by score descending
        scored_products.sort(key=lambda x: x[0], reverse=True)
        
        # Select top products
        selected = []
        for score, product in scored_products:
            if score >= self.min_demand_score:
                decision = self._make_decision(
                    action=AgentAction.SELECT if score >= 0.7 else AgentAction.WAIT,
                    reason=f"Score: {score:.2f}, Demand: {product.get('demand_score', 0):.2f}",
                    confidence=score
                )
                selected.append(product)
                
                if len(selected) >= 5:  # Max 5 products per run
                    break
        
        self.performance_metrics["successful_decisions"] += len(selected)
        
        return selected
    
    def _calculate_selection_score(self, product: Dict[str, Any]) -> float:
        """
        Calculate overall selection score for a product.
        
        Args:
            product: Product data
            
        Returns:
            Selection score (0-1)
        """
        demand_score = product.get("demand_score", 0.5)
        rating = product.get("rating", 4.0)
        estimated_orders = product.get("estimated_orders", 100)
        cost = product.get("cost_price", 30)
        
        # Demand component (40%)
        demand_weight = 0.4
        demand_component = demand_score
        
        # Rating component (20%)
        rating_weight = 0.2
        rating_component = rating / 5.0
        
        # Popularity component (20%)
        popularity_weight = 0.2
        popularity_component = min(estimated_orders / 2000, 1.0)
        
        # Profitability component (20%)
        profitability_weight = 0.2
        if cost < 20:
            profitability_component = 1.0
        elif cost < 40:
            profitability_component = 0.7
        else:
            profitability_component = 0.4
        
        total_score = (
            demand_weight * demand_component +
            rating_weight * rating_component +
            popularity_weight * popularity_weight +
            profitability_weight * profitability_component
        )
        
        return round(total_score, 3)
    
    def _make_decision(
        self,
        action: AgentAction,
        reason: str,
        confidence: float,
        metadata: Dict[str, Any] = None
    ) -> AgentDecision:
        """
        Make a decision and record it.
        
        Args:
            action: Action to take
            reason: Reason for decision
            confidence: Confidence level
            metadata: Additional metadata
            
        Returns:
            The decision
        """
        decision = AgentDecision(
            action=action,
            reason=reason,
            confidence=confidence,
            metadata=metadata
        )
        
        self.decision_history.append(decision)
        
        logger.debug(f"Agent decision: {action.value} - {reason} (confidence: {confidence:.2f})")
        
        return decision
    
    async def evaluate_product(
        self,
        product: Dict[str, Any],
        sales_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate a product's performance and decide if it should be dropped.
        
        Args:
            product: Product data
            sales_data: Sales metrics
            
        Returns:
            Evaluation result with recommendation
        """
        logger.info(f"Evaluating product: {product.get('name')}")
        
        # Calculate performance score
        sales_count = sales_data.get("sales_count", 0)
        revenue = sales_data.get("revenue", 0)
        conversion_rate = sales_data.get("conversion_rate", 0)
        
        # Decision logic
        if sales_count == 0 and revenue == 0:
            action = AgentAction.DROP
            reason = "No sales after 30 days"
            confidence = 0.9
        elif conversion_rate < 1.0:
            action = AgentAction.DROP
            reason = f"Low conversion rate: {conversion_rate:.1f}%"
            confidence = 0.8
        elif sales_count < 5 and revenue < 50:
            action = AgentAction.DROP
            reason = f"Low performance: {sales_count} sales, ${revenue:.2f} revenue"
            confidence = 0.7
        else:
            action = AgentAction.WAIT
            reason = "Product performing adequately"
            confidence = 0.6
        
        decision = self._make_decision(action, reason, confidence)
        
        self.performance_metrics["products_dropped"] += (1 if action == AgentAction.DROP else 0)
        
        return {
            "product_id": product.get("id"),
            "product_name": product.get("name"),
            "action": action.value,
            "reason": reason,
            "confidence": confidence,
            "recommendation": self._get_recommendation(action)
        }
    
    def _get_recommendation(self, action: AgentAction) -> str:
        """Get human-readable recommendation."""
        recommendations = {
            AgentAction.DROP: "Consider removing this product from the store",
            AgentAction.WAIT: "Continue monitoring this product",
            AgentAction.PUBLISH: "Publish this product to the store",
            AgentAction.PRICING: "Adjust pricing for better performance"
        }
        return recommendations.get(action, "No specific action")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        return {
            **self.performance_metrics,
            "total_decisions": len(self.decision_history),
            "decision_breakdown": self._get_decision_breakdown()
        }
    
    def _get_decision_breakdown(self) -> Dict[str, int]:
        """Get breakdown of decisions by action."""
        breakdown = {}
        for decision in self.decision_history:
            action = decision.action.value
            breakdown[action] = breakdown.get(action, 0) + 1
        return breakdown
    
    def get_recent_decisions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent agent decisions."""
        recent = self.decision_history[-limit:] if len(self.decision_history) >= limit else self.decision_history
        
        return [
            {
                "action": d.action.value,
                "reason": d.reason,
                "confidence": d.confidence,
                "timestamp": d.timestamp.isoformat()
            }
            for d in recent
        ]


async def run_agent_pipeline(
    max_products: int = 10,
    auto_publish: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to run the agent pipeline.
    
    Args:
        max_products: Maximum products to analyze
        auto_publish: Whether to auto-publish
        
    Returns:
        Pipeline results
    """
    agent = AIDecisionAgent()
    return await agent.run_full_pipeline(max_products, auto_publish)