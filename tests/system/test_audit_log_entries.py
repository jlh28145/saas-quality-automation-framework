"""
System tests for audit log validation.

Verifies that user actions (login, form submission, export) generate
corresponding audit log entries with correct structure and content.
"""

import json
import pytest
from pathlib import Path


def get_audit_log_path():
    """Get the audit log file path."""
    return Path(__file__).parent.parent.parent / "reports" / "logs" / "audit.log"


def read_audit_log(log_path):
    """
    Parse audit log file (JSON lines format).
    Returns list of dict entries or empty list if file doesn't exist.
    """
    if not log_path.exists():
        return []
    
    entries = []
    with open(log_path, "r") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def clear_audit_log(log_path):
    """Clear audit log before test."""
    if log_path.exists():
        log_path.write_text("")


@pytest.mark.system
def test_successful_login_creates_audit_entry(auth_client):
    """Verify that successful login creates an audit log entry."""
    log_path = get_audit_log_path()
    clear_audit_log(log_path)
    
    # Perform login
    auth_client.login("testuser@example.com", "password123")
    
    # Verify audit log entry
    entries = read_audit_log(log_path)
    assert len(entries) > 0, "No audit log entries found after login"
    
    # Find the login_successful entry
    login_entry = next(
        (e for e in entries if e["action"] == "api_login_successful"),
        None
    )
    assert login_entry is not None, "No login_successful entry found"
    assert login_entry["username"] == "testuser@example.com"
    assert "timestamp" in login_entry
    assert "details" in login_entry


@pytest.mark.system
def test_failed_login_creates_audit_entry(auth_client):
    """Verify that failed login creates an audit log entry."""
    log_path = get_audit_log_path()
    clear_audit_log(log_path)
    
    # Attempt invalid login
    auth_client.login("testuser@example.com", "wrongpassword")
    
    # Verify audit log entry
    entries = read_audit_log(log_path)
    assert len(entries) > 0, "No audit log entries found after failed login"
    
    # Find the login_failed entry
    failed_entry = next(
        (e for e in entries if e["action"] == "api_login_failed"),
        None
    )
    assert failed_entry is not None, "No login_failed entry found"
    assert failed_entry["details"]["reason"] == "invalid_password"


@pytest.mark.system
def test_form_submission_creates_audit_entry(forms_client):
    """Verify that form submission creates an audit log entry."""
    log_path = get_audit_log_path()
    clear_audit_log(log_path)
    
    # Submit form via API
    forms_client.submit_form("John Doe", "john@example.com", "This is a test message")
    
    # Verify audit log entry
    entries = read_audit_log(log_path)
    form_entry = next(
        (e for e in entries if e["action"] == "api_form_submitted"),
        None
    )
    assert form_entry is not None, "No form_submitted entry found"
    assert form_entry["details"]["name"] == "John Doe"
    assert form_entry["username"] == "api"


@pytest.mark.system
def test_export_request_creates_audit_entry(exports_client):
    """Verify that export request creates an audit log entry."""
    log_path = get_audit_log_path()
    clear_audit_log(log_path)
    
    # Request export
    exports_client.request_export()
    
    # Verify audit log entry
    entries = read_audit_log(log_path)
    export_entry = next(
        (e for e in entries if e["action"] == "api_export_requested"),
        None
    )
    assert export_entry is not None, "No export_requested entry found"
    assert "rows" in export_entry["details"]


@pytest.mark.system
def test_audit_log_entry_structure(auth_client):
    """Verify that audit log entries have required fields and valid JSON."""
    log_path = get_audit_log_path()
    clear_audit_log(log_path)
    
    # Generate an audit event
    auth_client.login("testuser@example.com", "password123")
    
    # Read and validate structure
    entries = read_audit_log(log_path)
    assert len(entries) > 0
    
    for entry in entries:
        # Check required fields
        assert "timestamp" in entry, f"Missing timestamp in entry: {entry}"
        assert "action" in entry, f"Missing action in entry: {entry}"
        assert "username" in entry, f"Missing username in entry: {entry}"
        assert "details" in entry, f"Missing details in entry: {entry}"
        
        # Validate field types
        assert isinstance(entry["timestamp"], str)
        assert isinstance(entry["action"], str)
        assert isinstance(entry["username"], str)
        assert isinstance(entry["details"], dict)
        
        # Timestamp should be ISO format
        assert "T" in entry["timestamp"] or ":" in entry["timestamp"]
