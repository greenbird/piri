import json

from jsonschema import Draft7Validator


def test_validate_schema():
    """Test that our schema.json is a valid draft7 schema."""
    schema_data = {}
    with open('mapmallow/schema.json', 'r') as schema_file:
        schema_data = json.load(schema_file)

    assert Draft7Validator.check_schema(schema_data) is None
