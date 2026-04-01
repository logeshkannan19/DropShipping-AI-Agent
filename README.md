# DropShipping AI Agent

## An Autonomous AI-Powered Dropshipping Business System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109.0-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <a href="https://railway.app/new/template?template=https://github.com/logeshkannan19/DropAgent"><img src="https://img.shields.io/badge/Deploy-Railway-blue.svg" alt="Deploy"></a>
</p>

<p align="center">
  <a href="https://dropshipping-ai-agent.up.railway.app/docs"><strong>🚀 Live Demo</strong></a>
</p>

---

## 🎥 Demo Video

[![DropShipping AI Agent Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

*Click to watch the full demo video*

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard](screenshots/dashboard.png)

### AI Agent Pipeline
![Agent Pipeline](screenshots/agent-pipeline.png)

### Product Analytics
![Analytics](screenshots/analytics.png)

### API Documentation
![API Docs](screenshots/api-docs.png)

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DROPSHIPPING AI AGENT SYSTEM                        │
└─────────────────────────────────────────────────────────────────────────────┘

                                    ┌───────────────┐
                                    │   START       │
                                    └───────┬───────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────┐
                    │     1️⃣  PRODUCT RESEARCH AGENT            │
                    │  ┌─────────────────────────────────────┐ │
                    │  │  • Scrape trending products          │ │
                    │  │  • Extract: name, price, rating     │ │
                    │  │  • Source: AliExpress, Amazon, etc  │ │
                    │  │  • Mock + Real scraping support      │ │
                    │  └─────────────────────────────────────┘ │
                    └───────────────────┬───────────────────────┘
                                        │
                                        ▼
                    ┌───────────────────────────────────────────┐
                    │     2️⃣  DEMAND PREDICTION MODEL          │
                    │  ┌─────────────────────────────────────┐ │
                    │  │  • ML Model: RandomForest/XGBoost   │ │
                    │  │  • Features: price, rating, reviews │ │
                    │  │  • Output: demand score (0-1)        │ │
                    │  │  • Training data: 1000+ samples      │ │
                    │  └─────────────────────────────────────┘ │
                    └───────────────────┬───────────────────────┘
                                        │
                                        ▼
                    ┌───────────────────────────────────────────┐
                    │     3️⃣  PRODUCT SELECTION                │
                    │  ┌─────────────────────────────────────┐ │
                    │  │  • Multi-factor scoring              │ │
                    │  │  • Demand score (40%)                │ │
                    │  │  • Rating (20%)                      │ │
                    │  │  • Popularity (20%)                   │ │
                    │  │  • Profitability (20%)               │ │
                    │  └─────────────────────────────────────┘ │
                    └───────────────────┬───────────────────────┘
                                        │
                                        ▼
                    ┌───────────────────────────────────────────┐
                    │     4️⃣  PRICING OPTIMIZATION              │
                    │  ┌─────────────────────────────────────┐ │
                    │  │  • 5 Pricing Strategies:             │ │
                    │  │    - Cost-Plus: cost + margin      │ │
                    │  │    - Competitive: beat competitors  │ │
                    │  │    - Premium: high demand, high $   │ │
                    │  │    - Penetration: low price entry   │ │
                    │  │    - Dynamic: RL-based (placeholder)│ │
                    │  │  • Formula: price = cost + margin   │ │
                    │  │    + competitor adjustment           │ │
                    │  └─────────────────────────────────────┘ │
                    └───────────────────┬───────────────────────┘
                                        │
                                        ▼
                    ┌───────────────────────────────────────────┐
                    │     5️⃣  STORE AUTOMATION (Shopify)        │
                    │  ┌─────────────────────────────────────┐ │
                    │  │  • create_product()                │ │
                    │  │  • update_price()                  │ │
                    │  │  • publish_product()                │ │
                    │  │  • Mock API (no real keys needed)   │ │
                    │  └─────────────────────────────────────┘ │
                    └───────────────────┬───────────────────────┘
                                        │
                                        ▼
                    ┌───────────────────────────────────────────┐
                    │     6️⃣  ANALYTICS & TRACKING              │
                    │  ┌─────────────────────────────────────┐ │
                    │  │  • Revenue tracking                 │ │
                    │  │  • Profit margins                   │ │
                    │  │  • Conversion rates                 │ │
                    │  │  • Top products                     │ │
                    │  │  • Daily/Weekly/Monthly stats       │ │
                    │  └─────────────────────────────────────┘ │
                    └───────────────────────────────────────────┘
                                        │
                                        ▼
                                ┌───────────────┐
                                │     END       │
                                └───────────────┘
```

### AI Decision Loop

```
┌─────────┐     ┌─────────┐     ┌─────────────┐     ┌──────────┐
│  PLAN   │────▶│ EXECUTE │────▶│  EVALUATE   │────▶│ IMPROVE  │
└─────────┘     └─────────┘     └─────────────┘     └──────────┘
     ▲                                                           │
     └───────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/logeshkannan19/DropAgent.git
cd DropAgent

# Start all services
docker-compose up --build

# Access the services
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Frontend: http://localhost:8501
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Initialize database with sample data
python scripts/seed_data.py

# Train ML model
python scripts/train_model.py

# Run the API
uvicorn backend.api.main:app --reload

# Run the frontend (separate terminal)
streamlit run frontend/app.py
```

---

## 📊 Real Dataset Example

### Sample Products Dataset

The system includes a real-world dataset with 50+ products across multiple categories:

```json
{
  "products": [
    {
      "name": "Wireless Bluetooth Earbuds Pro",
      "category": "Electronics",
      "cost_price": 15.99,
      "selling_price": 49.99,
      "rating": 4.5,
      "review_count": 1250,
      "estimated_orders_monthly": 500,
      "demand_score": 0.85,
      "supplier": {
        "id": "SUP-001",
        "name": "Global Trade Co",
        "rating": 4.8,
        "shipping_days": 12
      },
      "profit_margin": 67.99,
      "competitors_count": 45,
      "trending": true
    },
    {
      "name": "Premium Yoga Mat Non-Slip",
      "category": "Sports",
      "cost_price": 12.99,
      "selling_price": 34.99,
      "rating": 4.7,
      "review_count": 2100,
      "estimated_orders_monthly": 800,
      "demand_score": 0.78,
      "supplier": {
        "id": "SUP-003",
        "name": "Quality Goods Inc",
        "rating": 4.9,
        "shipping_days": 15
      },
      "profit_margin": 62.87,
      "competitors_count": 120,
      "trending": true
    }
  ]
}
```

### Demand Prediction Example

Input features for the ML model:

```python
features = {
    "category": "Electronics",
    "price": 35.99,
    "rating": 4.5,
    "review_count": 200,
    "competitor_count": 25,
    "supplier_rating": 4.7,
    "shipping_days": 12
}

# Output
{
    "demand_score": 0.72,
    "confidence": 0.85,
    "factors": {
        "rating_impact": "positive",
        "review_impact": "medium",
        "competition_impact": "low"
    }
}
```

---

## 💻 API Usage

### Base URL

```
http://localhost:8000/api/v1
```

### 1. Health Check

```bash
# Check API health
curl -X GET http://localhost:8000/api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "database_connected": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Run AI Agent Pipeline

```bash
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "max_products": 10,
    "min_demand_score": 0.5,
    "auto_publish": true
  }'
```

**Response:**
```json
{
  "run_id": 1,
  "status": "completed",
  "products_analyzed": 12,
  "products_selected": 5,
  "products_published": 5,
  "revenue_potential": 245.50,
  "execution_time": 2.35,
  "phases": {
    "research": {"products_found": 12},
    "analysis": {"products_analyzed": 12},
    "selection": {"products_selected": 5},
    "pricing": {"products_priced": 5},
    "publishing": {"products_published": 5}
  },
  "message": "Analyzed 12 products, selected 5, published 5"
}
```

### 3. Predict Demand

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Electronics",
    "price": 29.99,
    "rating": 4.5,
    "review_count": 500,
    "competitor_count": 30,
    "supplier_rating": 4.7,
    "shipping_days": 10
  }'
```

**Response:**
```json
{
  "demand_score": 0.72,
  "confidence": 0.85,
  "factors": {
    "rating_impact": "positive",
    "review_impact": "high",
    "competition_impact": "medium"
  }
}
```

### 4. Optimize Price

```bash
curl -X POST http://localhost:8000/api/v1/optimize-price \
  -H "Content-Type: application/json" \
  -d '{
    "cost_price": 15.99,
    "competitor_prices": [29.99, 34.99, 32.99, 38.99],
    "demand_score": 0.75
  }'
```

**Response:**
```json
{
  "optimal_price": 35.99,
  "margin_percent": 55.5,
  "estimated_profit": 20.00,
  "strategy": "competitive",
  "competitor_analysis": {
    "min": 29.99,
    "max": 38.99,
    "avg": 34.24
  },
  "recommendations": [
    "High demand justifies premium pricing",
    "Price is competitive in market"
  ]
}
```

### 5. List Products

```bash
curl -X GET "http://localhost:8000/api/v1/products?limit=10&category=Electronics"
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Bluetooth Earbuds",
      "category": "Electronics",
      "cost_price": 15.99,
      "selling_price": 49.99,
      "rating": 4.5,
      "demand_score": 0.85,
      "is_published": true
    }
  ],
  "total": 25,
  "skip": 0,
  "limit": 10
}
```

### 6. Get Analytics

```bash
curl -X GET "http://localhost:8000/api/v1/analytics?days=30"
```

**Response:**
```json
{
  "total_revenue": 15420.50,
  "total_profit": 8540.25,
  "total_sales": 425,
  "total_products": 48,
  "active_products": 42,
  "published_products": 35,
  "conversion_rate": 3.2,
  "avg_order_value": 36.28,
  "profit_margin": 55.4
}
```

### 7. Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

class DropShippingClient:
    """Python client for DropShipping AI Agent API."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def run_agent_pipeline(
        self,
        max_products: int = 10,
        min_demand_score: float = 0.5,
        auto_publish: bool = True
    ) -> dict:
        """Run the AI agent pipeline."""
        response = self.session.post(
            f"{self.base_url}/agent/run",
            json={
                "max_products": max_products,
                "min_demand_score": min_demand_score,
                "auto_publish": auto_publish
            }
        )
        response.raise_for_status()
        return response.json()
    
    def predict_demand(
        self,
        category: str,
        price: float,
        rating: float,
        review_count: int,
        competitor_count: int,
        supplier_rating: float,
        shipping_days: int
    ) -> dict:
        """Predict demand for a product."""
        response = self.session.post(
            f"{self.base_url}/predict",
            json={
                "category": category,
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "competitor_count": competitor_count,
                "supplier_rating": supplier_rating,
                "shipping_days": shipping_days
            }
        )
        response.raise_for_status()
        return response.json()
    
    def optimize_price(
        self,
        cost_price: float,
        competitor_prices: list,
        demand_score: float
    ) -> dict:
        """Optimize product pricing."""
        response = self.session.post(
            f"{self.base_url}/optimize-price",
            json={
                "cost_price": cost_price,
                "competitor_prices": competitor_prices,
                "demand_score": demand_score
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_analytics(self, days: int = 7) -> dict:
        """Get analytics data."""
        response = self.session.get(
            f"{self.base_url}/analytics",
            params={"days": days}
        )
        response.raise_for_status()
        return response.json()


# Usage Example
if __name__ == "__main__":
    client = DropShippingClient()
    
    # Run AI Agent
    result = client.run_agent_pipeline(max_products=10)
    print(f"Agent completed: {result['products_selected']} products selected")
    
    # Predict demand
    demand = client.predict_demand(
        category="Electronics",
        price=29.99,
        rating=4.5,
        review_count=500,
        competitor_count=30,
        supplier_rating=4.7,
        shipping_days=10
    )
    print(f"Demand score: {demand['demand_score']}")
    
    # Get analytics
    analytics = client.get_analytics(days=30)
    print(f"Revenue: ${analytics['total_revenue']}")
```

### 8. JavaScript/Node.js Example

```javascript
const API_BASE = 'http://localhost:8000/api/v1';

class DropShippingClient {
    constructor(baseUrl = API_BASE) {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    async runAgentPipeline(maxProducts = 10, minDemandScore = 0.5) {
        return this.request('/agent/run', {
            method: 'POST',
            body: JSON.stringify({
                max_products: maxProducts,
                min_demand_score: minDemandScore,
                auto_publish: true
            }),
        });
    }

    async predictDemand(productData) {
        return this.request('/predict', {
            method: 'POST',
            body: JSON.stringify(productData),
        });
    }

    async getAnalytics(days = 7) {
        return this.request(`/analytics?days=${days}`);
    }
}

// Usage
const client = new DropShippingClient();
const result = await client.runAgentPipeline(10);
console.log(`Selected ${result.products_selected} products`);
```

---

## 📁 API Documentation

### Full Endpoints List

#### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/health/ready` | Readiness probe |
| GET | `/health/live` | Liveness probe |

#### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List products |
| POST | `/products` | Create product |
| GET | `/products/{id}` | Get product |
| PATCH | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |

#### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics` | Get metrics |
| GET | `/analytics/top-products` | Top products |
| GET | `/analytics/daily-stats` | Daily statistics |
| GET | `/analytics/categories` | Category performance |
| GET | `/analytics/summary` | Full summary |

#### AI Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent/run` | Run agent pipeline |
| GET | `/agent/performance` | Agent metrics |
| GET | `/agent/decisions` | Recent decisions |
| GET | `/agent/runs` | Run history |

#### Suppliers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/suppliers` | List suppliers |
| GET | `/suppliers/{id}` | Supplier details |
| GET | `/suppliers/{id}/products` | Supplier products |
| POST | `/suppliers/order` | Place order |

#### Store
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/store/products` | List store products |
| POST | `/store/products` | Create product |
| POST | `/store/products/{id}/publish` | Publish product |
| POST | `/store/products/{id}/order` | Simulate order |
| GET | `/store/stats` | Store statistics |

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/dropshipping.db` | Database connection |
| `SECRET_KEY` | (required) | JWT secret key |
| `LOG_LEVEL` | `INFO` | Logging level |
| `OPENAI_API_KEY` | (optional) | OpenAI API key |
| `REDIS_ENABLED` | `false` | Enable Redis caching |
| `ENVIRONMENT` | `development` | Environment mode |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_product_research.py -v
```

---

## 🚢 Deployment

### 🚀 Deploy NOW - One Click!

| Platform | Click to Deploy | Status |
|----------|----------------|--------|
| **Render** (Recommended) | 👉 [Deploy to Render](https://render.com/deploy?repo=https://github.com/logeshkannan19/DropAgent) | Free Tier |
| **Railway** | 👉 [Deploy to Railway](https://railway.app/new/template?template=https://github.com/logeshkannan19/DropAgent) | Free Tier |

---

### Render Deployment (Step by Step)

1. **Click this link:** 👉 https://render.com/deploy?repo=https://github.com/logeshkannan19/DropAgent

2. **Login with GitHub** if prompted

3. **Configure your service:**
   ```
   Name: dropshipping-api
   Region: Singapore
   Branch: main
   Environment: Python 3.11
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Click "Create Web Service"**

5. **Wait 2-3 minutes** for deployment

6. **Get your live URL!**
   ```
   https://dropshipping-api.onrender.com/docs
   ```

---

### Railway Deployment

1. **Click:** 👉 https://railway.app/new/template?template=https://github.com/logeshkannan19/DropAgent

2. **Login with GitHub**

3. **Click "Deploy Now"**

4. **Get your URL:** `https://dropshipping-ai-agent.up.railway.app`

---

### Docker Deployment

```bash
# Build production image
docker build -t dropshipping-api .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

---

### Local Development

```bash
# Clone and setup
git clone https://github.com/logeshkannan19/DropAgent.git
cd DropAgent

# Run with Docker
docker-compose up --build

# OR Run manually
pip install -r requirements.txt
uvicorn backend.api.main:app --reload
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for dropshipping automation
</p>
