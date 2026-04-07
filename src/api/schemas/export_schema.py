"""
JSON schemas for export responses.
"""

EXPORT_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["success", "export_file", "total_records", "timestamp"],
    "properties": {
        "success": {"type": "boolean"},
        "export_file": {"type": "string"},
        "total_records": {"type": "integer"},
        "timestamp": {"type": "string"},
    },
}
