"""
System tests for export file creation and validation.

Verifies that export functionality correctly generates CSV files
with proper structure and content.
"""

import csv
import pytest
from pathlib import Path


def get_export_file_path():
    """Get the export file path."""
    return Path(__file__).parent.parent.parent / "reports" / "export.csv"


def get_forms_data_path():
    """Get the forms data file path."""
    return Path(__file__).parent.parent.parent / "data" / "forms.json"


def clear_export_file(file_path):
    """Clear/remove export file before test."""
    if file_path.exists():
        file_path.unlink()


@pytest.mark.system
def test_export_file_created_after_request(exports_client):
    """Verify that export request creates a CSV file."""
    export_path = get_export_file_path()
    clear_export_file(export_path)

    # Request export
    result = exports_client.request_export()

    # Verify response
    assert result["status_code"] == 200
    assert result["body"]["success"] is True
    assert result["body"]["export_file"] == "export.csv"

    # Verify file exists
    assert export_path.exists(), f"Export file not created at {export_path}"


@pytest.mark.system
def test_export_file_has_csv_headers(exports_client):
    """Verify that export CSV has correct headers."""
    export_path = get_export_file_path()
    clear_export_file(export_path)

    # Request export
    exports_client.request_export()

    # Read and verify CSV headers
    with open(export_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)

    expected_headers = ["timestamp", "name", "email", "message"]
    assert (
        headers == expected_headers
    ), f"Headers mismatch. Got: {headers}, Expected: {expected_headers}"


@pytest.mark.system
def test_export_file_contains_submitted_forms(forms_client, exports_client):
    """Verify that export file contains submitted form data."""
    export_path = get_export_file_path()
    clear_export_file(export_path)

    # Submit a form
    form_name = "Jane Doe"
    form_email = "jane@example.com"
    form_message = "This is a test form submission for export validation"

    forms_client.submit_form(form_name, form_email, form_message)

    # Request export
    exports_client.request_export()

    # Verify form data is in export
    with open(export_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Find the submitted form row
    submitted_row = next((row for row in rows if row.get("name") == form_name), None)

    assert (
        submitted_row is not None
    ), f"Form submission not found in export. Rows: {rows}"
    assert submitted_row["email"] == form_email
    assert submitted_row["message"] == form_message
    assert "timestamp" in submitted_row


@pytest.mark.system
def test_export_file_structure_is_valid(forms_client, exports_client):
    """Verify that export file is a well-formed CSV."""
    export_path = get_export_file_path()
    clear_export_file(export_path)

    # Submit a form to ensure data exists
    forms_client.submit_form("Test User", "test@example.com", "Test message content")

    # Request export
    exports_client.request_export()

    # Validate CSV structure
    assert export_path.exists()

    with open(export_path, "r") as f:
        try:
            reader = csv.DictReader(f)
            rows = list(reader)

            # Verify we can read rows and they have expected fields
            assert len(rows) > 0, "Export file is empty"

            for row in rows:
                assert "timestamp" in row
                assert "name" in row
                assert "email" in row
                assert "message" in row
        except Exception as e:
            pytest.fail(f"Failed to parse export CSV: {e}")


@pytest.mark.system
def test_export_response_matches_file_content(forms_client, exports_client):
    """Verify that export response metadata matches actual file content."""
    export_path = get_export_file_path()
    clear_export_file(export_path)

    # Submit forms
    forms_client.submit_form("User 1", "user1@example.com", "Message 1 test content")
    forms_client.submit_form("User 2", "user2@example.com", "Message 2 test content")

    # Request export
    result = exports_client.request_export()
    response_record_count = result["body"]["total_records"]

    # Count rows in actual file
    with open(export_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        actual_record_count = sum(1 for _ in reader)

    assert (
        actual_record_count == response_record_count
    ), f"Record count mismatch. Response: {response_record_count}, Actual: {actual_record_count}"
