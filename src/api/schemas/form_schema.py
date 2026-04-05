"""
JSON schemas for form responses.
"""

FORM_SUBMIT_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["success", "message"],
    "properties": {
        "success": {"type": "boolean"},
        "message": {"type": "string"},
    }
}

FORM_VALIDATION_ERROR_SCHEMA = {
    "type": "object",
    "required": ["error", "details"],
    "properties": {
        "error": {"type": "string"},
        "details": {"type": "object"},
    }
}
