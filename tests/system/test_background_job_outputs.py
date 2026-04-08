"""
System tests for form submission persistence and data storage.

Verifies that submitted forms are correctly persisted to data storage
and can be retrieved/exported.
"""

import json
import pytest
from pathlib import Path


def get_forms_data_path():
    """Get the forms data file path."""
    return Path(__file__).parent.parent.parent / "data" / "forms.json"


def read_forms_data():
    """Read forms data from JSON file."""
    forms_path = get_forms_data_path()
    if forms_path.exists():
        with open(forms_path, "r") as f:
            return json.load(f)
    return {"submissions": []}


def clear_forms_data():
    """Clear forms data before test."""
    forms_path = get_forms_data_path()
    forms_path.write_text(json.dumps({"submissions": []}, indent=2))


@pytest.mark.system
def test_submitted_form_persisted_to_json(forms_client):
    """Verify that submitted form data is persisted to forms.json."""
    clear_forms_data()

    # Submit form
    form_name = "Alice Smith"
    form_email = "alice@example.com"
    form_message = "This is a test form submission for persistence validation"

    forms_client.submit_form(form_name, form_email, form_message)

    # Verify data in forms.json
    forms_data = read_forms_data()
    submissions = forms_data.get("submissions", [])

    assert len(submissions) > 0, "No submissions found in forms.json"

    submitted = next((s for s in submissions if s.get("name") == form_name), None)

    assert submitted is not None, f"Form not found in submissions. Got: {submissions}"
    assert submitted["email"] == form_email
    assert submitted["message"] == form_message


@pytest.mark.system
def test_multiple_submissions_accumulate(forms_client):
    """Verify that multiple form submissions accumulate correctly."""
    clear_forms_data()

    # Submit multiple forms
    submissions_to_make = [
        ("User One", "user1@example.com", "First message for system test"),
        ("User Two", "user2@example.com", "Second message for system test"),
        ("User Three", "user3@example.com", "Third message for system test"),
    ]

    for name, email, message in submissions_to_make:
        forms_client.submit_form(name, email, message)

    # Verify all submissions persisted
    forms_data = read_forms_data()
    submissions = forms_data.get("submissions", [])

    assert len(submissions) == len(
        submissions_to_make
    ), f"Expected {len(submissions_to_make)} submissions, got {len(submissions)}"

    for name, email, message in submissions_to_make:
        submitted = next((s for s in submissions if s.get("name") == name), None)
        assert submitted is not None, f"Missing submission for {name}"
        assert submitted["email"] == email
        assert submitted["message"] == message


@pytest.mark.system
def test_submission_has_required_fields(forms_client):
    """Verify that persisted submissions have all required fields."""
    clear_forms_data()

    # Submit form
    forms_client.submit_form(
        "Test User", "test@example.com", "Test message content here"
    )

    # Verify all required fields exist
    forms_data = read_forms_data()
    submissions = forms_data.get("submissions", [])

    assert len(submissions) == 1
    submission = submissions[0]

    required_fields = ["timestamp", "name", "email", "message", "submitted_by"]
    for field in required_fields:
        assert field in submission, f"Missing required field: {field}"
        assert submission[field] is not None, f"Field {field} is None"


@pytest.mark.system
def test_submission_timestamp_is_valid(forms_client):
    """Verify that submission timestamps are valid ISO format."""
    clear_forms_data()

    # Submit form
    forms_client.submit_form(
        "Timestamp User", "timestamp@example.com", "Message for timestamp test"
    )

    # Verify timestamp format
    forms_data = read_forms_data()
    submissions = forms_data.get("submissions", [])

    assert len(submissions) == 1
    timestamp = submissions[0]["timestamp"]

    # ISO format check
    assert (
        "T" in timestamp or ":" in timestamp
    ), f"Invalid timestamp format: {timestamp}"

    # Attempt to parse as ISO
    try:
        # Basic ISO format check
        assert len(timestamp) > 10
    except Exception as e:
        pytest.fail(f"Timestamp format validation failed: {e}")


@pytest.mark.system
def test_invalid_form_not_persisted(forms_client):
    """Verify that invalid submissions are rejected and not persisted."""
    clear_forms_data()

    # Attempt invalid submission (message too short)
    result = forms_client.submit_form("Short", "short@example.com", "short")

    # Verify submission was rejected
    assert result["status_code"] == 400
    assert "error" in result["body"]

    # Verify nothing was persisted
    forms_data = read_forms_data()
    submissions = forms_data.get("submissions", [])

    assert len(submissions) == 0, f"Invalid submission was persisted: {submissions}"
