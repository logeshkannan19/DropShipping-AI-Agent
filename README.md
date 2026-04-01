# DropShipping AI Agent

## An Autonomous AI-Powered Dropshipping Business System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109.0-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

---

## Overview

DropShipping AI Agent is a production-ready, end-to-end automation system for managing a dropshipping business using artificial intelligence. It leverages modern AI techniques to research products, predict demand, optimize pricing, and automate store operations.

---

## Features

### Core AI Agents

| Agent | Description |
|-------|-------------|
| **Product Research Agent** | Scrapes and analyzes trending products from multiple sources |
| **Demand Prediction Model** | ML-based demand forecasting using ensemble methods |
| **Pricing Optimization Agent** | Rule-based and dynamic pricing strategies |
| **AI Decision Agent** | Orchestrates the entire pipeline with planning loop |

### Business Services

- **Supplier Management**: Mock supplier API with inventory and shipping tracking
- **Store Automation**: Mock Shopify integration for product management
- **Analytics Dashboard**: Real-time metrics on revenue, profit, and conversions

### Technical Features

- **Async Architecture**: Built with FastAPI and asyncio for high performance
- **Modular Design**: Clean separation of concerns with service layers
- **Type Safety**: Full Pydantic validation on all inputs/outputs
- **Production Ready**: Docker support, logging, error handling
- **Testing**: Comprehensive unit and integration tests

---

## Architecture

```
DropShipping-AI-Agent/
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/       # API endpoints
│   ├── core/
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # Database models & session
│   │   ├── security.py          # Authentication & JWT
│   │   └── dependencies.py     # FastAPI dependencies
│   ├── agents/
│   │   ├── product_research/    # Product research agent
│   │   ├── pricing/            # Pricing optimization
│   │   └── ai_decision/         # Core AI decision agent
│   ├── services/                # Business logic services
│   ├── scripts/                 # Utility scripts
│   └── utils/                   # Helper utilities
├── frontend/
│   └── app.py                  # Streamlit dashboard
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/             # Integration tests
├── data/                       # Data storage
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container image
└── requirements.txt            # Python dependencies
```

---

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-repo/dropshipping-ai-agent.git
cd dropshipping-ai-agent

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

# Initialize database
python scripts/seed_data.py

# Run the API
uvicorn backend.api.main:app --reload

# Run the frontend (separate terminal)
streamlit run frontend/app.py
```

---

## API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints Overview

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

### Example Request

```bash
# Run AI Agent Pipeline
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "max_products": 10,
    "min_demand_score": 0.5,
    "auto_publish": true
  }'
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/dropshipping.db` | Database connection |
| `SECRET_KEY` | (required) | JWT secret key |
| `LOG_LEVEL` | `INFO` | Logging level |
| `OPENAI_API_KEY` | (optional) | OpenAI API key |
| `REDIS_ENABLED` | `false` | Enable Redis caching |
| `ENVIRONMENT` | `development` | Environment mode |

### Pricing Configuration

```python
# Default margins
PRICING_DEFAULT_MARGIN = 0.30  # 30%
PRICING_MIN_MARGIN = 0.15     # 15%
PRICING_MAX_MARGIN = 0.60     # 60%
```

---

## Development

### Project Structure

```
backend/
├── api/v1/endpoints/     # API route handlers
├── core/                 # Core application logic
├── agents/              # AI agent implementations
├── services/            # Business logic services
├── scripts/             # Utility scripts
└── utils/               # Helper functions
```

### Adding New Features

1. **New API Endpoint**: Add to `backend/api/v1/endpoints/`
2. **New Agent**: Add to `backend/agents/`
3. **New Service**: Add to `backend/services/`
4. **Update Router**: Register in `backend/api/v1/router.py`

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=backend --cov-report=html

# Run specific test file
pytest tests/unit/test_product_research.py -v

# Run integration tests
pytest tests/integration/ -v
```

---

## Deployment

### Docker Deployment

```bash
# Build production image
docker build -t dropshipping-api .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Scale API
docker-compose up -d --scale api=3
```

### Production Checklist

- [ ] Set `SECRET_KEY` to a secure value
- [ ] Configure `DATABASE_URL` for production database
- [ ] Enable Redis for caching (optional)
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure CORS origins
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

---

<p align="center">
  Made with ❤️ for dropshipping automation
</p>
