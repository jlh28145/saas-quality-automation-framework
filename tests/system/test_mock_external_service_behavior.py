"""
System tests for mocked external email behavior.

Verifies that form submissions produce deterministic mock-email artifacts
instead of depending on a live third-party provider.
"""

import json
from pathlib import Path

import pytest


def get_mock_email_log_path():
    """Get the mock email log path."""
    return Path(__file__).parent.parent.parent / "reports" / "logs" / "mock_email.log"


def clear_mock_email_log():
    """Clear the mock email log before a test."""
    log_path = get_mock_email_log_path()
    if log_path.exists():
        log_path.write_text("")


def read_mock_email_entries():
    """Read mock email log entries as JSON lines."""
    log_path = get_mock_email_log_path()
    if not log_path.exists():
        return []

    entries = []
    with open(log_path, "r") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


@pytest.mark.system
def test_form_submission_writes_mock_email_artifact(forms_client):
    """Verify form submission triggers a deterministic mock email entry."""
    clear_mock_email_log()

    result = forms_client.submit_form(
        "Email Test User",
        "email-test@example.com",
        "This submission should trigger a mock email artifact.",
    )

    assert result["status_code"] == 201
    entries = read_mock_email_entries()
    assert len(entries) > 0

    latest = entries[-1]
    assert latest["recipient"] == "email-test@example.com"
    assert latest["template"] == "api_form_submission_confirmation"
    assert latest["status"] == "sent"
