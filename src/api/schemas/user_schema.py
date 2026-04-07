"""
JSON schemas for user responses.
"""

USERS_LIST_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["users"],
    "properties": {
        "users": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["email", "name"],
                "properties": {
                    "email": {"type": "string"},
                    "name": {"type": "string"},
                },
            },
        }
    },
}
