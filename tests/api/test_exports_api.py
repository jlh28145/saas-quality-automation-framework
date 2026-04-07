"""
API tests for export endpoints.
"""

from pathlib import Path

import pytest

from src.api.assertions.response_assertions import (
    assert_json_field_equals,
    assert_status_code,
)
from src.api.assertions.schema_assertions import assert_schema_valid
from src.api.schemas.export_schema import EXPORT_RESPONSE_SCHEMA


def get_export_file_path():
    """Get the export file path."""
    return Path(__file__).parent.parent.parent / "reports" / "export.csv"


def clear_export_file():
    """Remove the export file to ensure deterministic assertions."""
    export_path = get_export_file_path()
    if export_path.exists():
        export_path.unlink()


@pytest.mark.api
@pytest.mark.regression
def test_api_export_returns_schema_valid_metadata(exports_client):
    """Test the export endpoint returns the expected metadata schema."""
    clear_export_file()

    result = exports_client.request_export()

    assert_status_code(result["response"], 200)
    assert_schema_valid(result["response"], EXPORT_RESPONSE_SCHEMA)
    assert_json_field_equals(result["response"], "success", True)
    assert_json_field_equals(result["response"], "export_file", "export.csv")


@pytest.mark.api
def test_api_export_creates_report_file(exports_client):
    """Test the export endpoint creates the CSV artifact."""
    clear_export_file()

    result = exports_client.request_export()

    assert_status_code(result["response"], 200)
    assert get_export_file_path().exists()
