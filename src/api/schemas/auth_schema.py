"""
JSON schemas for authentication responses.
"""

AUTH_LOGIN_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["success", "user", "token"],
    "properties": {
        "success": {"type": "boolean"},
        "user": {
            "type": "object",
            "required": ["email", "name"],
            "properties": {
                "email": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "token": {"type": "string"},
    },
}

AUTH_ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["error"],
    "properties": {
        "error": {"type": "string"},
    },
}
