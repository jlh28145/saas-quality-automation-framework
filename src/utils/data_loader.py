"""
Test data loading utilities.
Loads test data from JSON files in the data directory.
"""

import json
from pathlib import Path
from typing import Any, Dict


class DataLoader:
    """Utility for loading test data from JSON files."""
    
    def __init__(self, data_dir: Path = None):
        """Initialize data loader."""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir = data_dir
    
    def load(self, filename: str) -> Dict[str, Any]:
        """Load data from a JSON file."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return {}
        
        with open(filepath) as f:
            return json.load(f)
    
    def get_users(self) -> list:
        """Get test users from users.json."""
        data = self.load("users.json")
        return data.get("users", [])
    
    def get_user(self, email: str) -> Dict[str, Any]:
        """Get a specific user by email."""
        users = self.get_users()
        for user in users:
            if user.get("email") == email:
                return user
        return {}
    
    def get_forms(self) -> list:
        """Get form submissions."""
        data = self.load("forms.json")
        return data.get("submissions", [])
    
    def get_expected_exports(self) -> list:
        """Get expected export data."""
        data = self.load("expected_exports.json")
        return data.get("exports", [])


# Singleton instance
_loader = None


def get_data_loader() -> DataLoader:
    """Get or create data loader instance."""
    global _loader
    if _loader is None:
        _loader = DataLoader()
    return _loader
