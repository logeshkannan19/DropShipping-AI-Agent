"""
Application Configuration Module.

This module handles all configuration management using Pydantic Settings.
Supports environment variables, .env files, and development/production modes.
"""

import os
from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: str = Field(
        default="sqlite+aiosqlite:///./data/dropshipping.db",
        description="Database connection URL"
    )
    echo: bool = Field(default=False, description="Echo SQL queries")
    pool_size: int = Field(default=5, ge=1, description="Connection pool size")
    max_overflow: int = Field(default=10, ge=0, description="Max overflow connections")
    pool_timeout: int = Field(default=30, ge=1, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=3600, ge=0, description="Pool recycle time")

    class Config:
        env_prefix = "DATABASE_"
        case_sensitive = False


class RedisSettings(BaseSettings):
    """Redis cache configuration settings."""
    
    enabled: bool = Field(default=False, description="Enable Redis caching")
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, ge=1, le=65535, description="Redis port")
    db: int = Field(default=0, ge=0, description="Redis database number")
    password: Optional[str] = Field(default=None, description="Redis password")
    ssl: bool = Field(default=False, description="Use SSL connection")
    ttl: int = Field(default=3600, ge=0, description="Default cache TTL in seconds")

    class Config:
        env_prefix = "REDIS_"
        case_sensitive = False


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT tokens"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        ge=1,
        description="Refresh token expiration in days"
    )

    class Config:
        env_prefix = "SECURITY_"
        case_sensitive = False


class OpenAISettings(BaseSettings):
    """OpenAI API configuration settings."""
    
    api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    model: str = Field(default="gpt-3.5-turbo", description="Default model")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(default=500, ge=1, description="Max tokens per response")
    use_mock: bool = Field(default=True, description="Use mock LLM responses")
    request_timeout: int = Field(default=60, ge=1, description="Request timeout in seconds")

    class Config:
        env_prefix = "OPENAI_"
        case_sensitive = False


class ScraperSettings(BaseSettings):
    """Web scraper configuration settings."""
    
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        description="User agent for scraping"
    )
    timeout: int = Field(default=30, ge=1, description="Request timeout in seconds")
    max_retries: int = Field(default=3, ge=0, description="Max retry attempts")
    delay_between_requests: float = Field(
        default=2.0,
        ge=0,
        description="Delay between requests in seconds"
    )
    proxy: Optional[str] = Field(default=None, description="Proxy URL for scraping")

    class Config:
        env_prefix = "SCRAPER_"
        case_sensitive = False


class PricingSettings(BaseSettings):
    """Pricing optimization configuration settings."""
    
    default_margin: float = Field(
        default=0.30,
        ge=0.0,
        le=1.0,
        description="Default profit margin"
    )
    min_margin: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Minimum profit margin"
    )
    max_margin: float = Field(
        default=0.60,
        ge=0.0,
        le=1.0,
        description="Maximum profit margin"
    )
    competitor_adjustment_factor: float = Field(
        default=0.05,
        ge=0.0,
        le=0.5,
        description="Competitor price adjustment factor"
    )
    demand_threshold_high: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="High demand threshold"
    )
    demand_threshold_low: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Low demand threshold"
    )

    class Config:
        env_prefix = "PRICING_"
        case_sensitive = False


class AgentSettings(BaseSettings):
    """AI Agent configuration settings."""
    
    planning_horizon: int = Field(
        default=7,
        ge=1,
        description="Planning horizon in days"
    )
    max_products_to_evaluate: int = Field(
        default=50,
        ge=1,
        description="Max products to evaluate per run"
    )
    top_products_count: int = Field(
        default=10,
        ge=1,
        description="Number of top products to select"
    )
    evaluation_interval: int = Field(
        default=3600,
        ge=60,
        description="Evaluation interval in seconds"
    )
    confidence_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold"
    )

    class Config:
        env_prefix = "AGENT_"
        case_sensitive = False


class ServerSettings(BaseSettings):
    """Server configuration settings."""
    
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    workers: int = Field(default=1, ge=1, description="Number of workers")
    reload: bool = Field(default=False, description="Enable auto-reload")
    log_level: str = Field(default="INFO", description="Log level")

    class Config:
        env_prefix = "SERVER_"
        case_sensitive = False


class AppSettings(BaseSettings):
    """Main application settings."""
    
    name: str = Field(default="DropShipping AI Agent", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    description: str = Field(
        default="AI-powered autonomous dropshipping business system",
        description="Application description"
    )
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment")
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    allowed_origins: List[str] = Field(
        default=["*"],
        description="Allowed CORS origins"
    )

    @validator("environment")
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class Settings(BaseSettings):
    """
    Main settings class that aggregates all configuration sections.
    
    This is the single source of truth for all application configuration.
    Settings are loaded from environment variables and .env files.
    """
    
    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    scraper: ScraperSettings = Field(default_factory=ScraperSettings)
    pricing: PricingSettings = Field(default_factory=PricingSettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    This function uses LRU caching to ensure settings are only
    loaded once and reused throughout the application lifecycle.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Global settings instance for convenience
settings = get_settings()
