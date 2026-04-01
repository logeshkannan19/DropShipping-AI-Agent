"""Configuration module for DropShipping AI Agent."""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    type: str = "sqlite"
    path: str = "data/dropshipping.db"
    echo: bool = False


@dataclass
class OpenAIConfig:
    """OpenAI API configuration."""
    api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 500
    use_mock: bool = True


@dataclass
class ScraperConfig:
    """Web scraper configuration."""
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    timeout: int = 30
    max_retries: int = 3
    delay_between_requests: float = 2.0


@dataclass
class PricingConfig:
    """Pricing optimization configuration."""
    default_margin: float = 0.30
    min_margin: float = 0.15
    max_margin: float = 0.60
    competitor_adjustment_factor: float = 0.05
    demand_threshold_high: float = 0.7
    demand_threshold_low: float = 0.3


@dataclass
class AgentConfig:
    """AI Agent configuration."""
    planning_horizon: int = 7
    max_products_to_evaluate: int = 50
    top_products_count: int = 10
    evaluation_interval: int = 3600
    confidence_threshold: float = 0.6


@dataclass
class RedisConfig:
    """Redis cache configuration."""
    enabled: bool = False
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    ttl: int = 3600


@dataclass
class AppConfig:
    """Main application configuration."""
    app_name: str = "DropShipping AI Agent"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    scraper: ScraperConfig = field(default_factory=ScraperConfig)
    pricing: PricingConfig = field(default_factory=PricingConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        config = cls()
        
        config.debug = os.getenv("DEBUG", "false").lower() == "true"
        config.host = os.getenv("HOST", "0.0.0.0")
        config.port = int(os.getenv("PORT", "8000"))
        config.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        config.openai.api_key = os.getenv("OPENAI_API_KEY")
        config.openai.use_mock = os.getenv("USE_MOCK_LLM", "true").lower() == "true"
        
        config.database.path = os.getenv("DATABASE_PATH", "data/dropshipping.db")
        
        if os.getenv("REDIS_ENABLED", "false").lower() == "true":
            config.redis.enabled = True
            config.redis.host = os.getenv("REDIS_HOST", "localhost")
            config.redis.port = int(os.getenv("REDIS_PORT", "6379"))
        
        return config


def get_config() -> AppConfig:
    """Get application configuration."""
    return AppConfig.from_env()


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get data directory path."""
    data_dir = get_project_root() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def get_models_dir() -> Path:
    """Get models directory path."""
    models_dir = get_project_root() / "backend" / "models"
    models_dir.mkdir(exist_ok=True)
    return models_dir
