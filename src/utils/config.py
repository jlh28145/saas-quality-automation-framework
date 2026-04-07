"""
Configuration management for different environments.
Loads config from YAML files based on environment.
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml


class Config:
    """Configuration loader for different environments."""

    def __init__(self, environment: str = "dev"):
        """Initialize config for the given environment."""
        selected_environment = environment or os.getenv("ENV") or os.getenv("TEST_ENV") or "dev"
        self.environment = selected_environment
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML files."""
        settings_file = self.config_dir / "settings.yaml"
        if settings_file.exists():
            with open(settings_file) as f:
                self._config.update(yaml.safe_load(f) or {})

        env_file = self.config_dir / f"{self.environment}.yaml"
        if env_file.exists():
            with open(env_file) as f:
                env_config = yaml.safe_load(f) or {}
                self._config.update(env_config)
        else:
            raise FileNotFoundError(f"Config file not found: {env_file}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value by key (supports nested keys with dot notation)."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    def __getitem__(self, key: str) -> Any:
        """Get a config value using dict-like access."""
        return self.get(key)

    def __repr__(self) -> str:
        return f"Config({self.environment})"


_config = None


def get_config(environment: str = None) -> Config:
    """Get or create config instance."""
    global _config
    requested_environment = environment or os.getenv("ENV") or os.getenv("TEST_ENV") or "dev"
    if _config is None or _config.environment != requested_environment:
        _config = Config(requested_environment)
    return _config


def reset_config() -> None:
    """Reset config instance (useful for testing)."""
    global _config
    _config = None
