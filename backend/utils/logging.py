"""Logging utilities for DropShipping AI Agent."""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from functools import wraps
import traceback


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels."""
    
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"
    
    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


class Logger:
    """Centralized logging utility."""
    
    _loggers = {}
    
    def __init__(self, name: str, log_dir: Optional[Path] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.log_dir = log_dir
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with handlers and formatters."""
        if self.logger.handlers:
            return
        
        self.logger.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        colored_formatter = ColoredFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(colored_formatter)
        self.logger.addHandler(console_handler)
        
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(
                self.log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    @classmethod
    def get_logger(cls, name: str, log_dir: Optional[Path] = None) -> logging.Logger:
        """Get or create a logger instance."""
        if name not in cls._loggers:
            cls._loggers[name] = cls(name, log_dir).logger
        return cls._loggers[name]


def setup_logging(log_level: str = "INFO", log_dir: Optional[Path] = None):
    """Setup global logging configuration."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    colored_formatter = ColoredFormatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)
    
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)


def log_exceptions(func):
    """Decorator to log exceptions raised by functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = Logger.get_logger(func.__module__)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    return wrapper


def async_log_exceptions(func):
    """Decorator to log exceptions in async functions."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger = Logger.get_logger(func.__module__)
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Async exception in {func.__name__}: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    return wrapper
