"""
Path helper utilities for common file operations.
"""

from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory."""
    return get_project_root() / "data"


def get_reports_dir() -> Path:
    """Get the reports directory."""
    return get_project_root() / "reports"


def get_logs_dir() -> Path:
    """Get the logs directory."""
    return get_reports_dir() / "logs"


def get_config_dir() -> Path:
    """Get the config directory."""
    return get_project_root() / "config"


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists and return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path
