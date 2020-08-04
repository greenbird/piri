import json

from jsonschema import Draft7Validator, ValidationError
from returns.pipeline import is_successful

from mapmallow.schema import SchemaValidator

schema = {}
with open(
    'mapmallow/schema.json',
    'r',
) as schema_file:
    schema = json.load(schema_file)

validator = SchemaValidator(
    Draft7Validator(schema=schema),
)


def test_validates(valid):
    """Test that we get dict back on valid validation."""
    result = validator(valid)
    assert result.unwrap() == valid


def test_invalid(invalid):
    """Test that we get a list of errors."""
    result = validator(invalid)
    assert not is_successful(result)
    assert isinstance(result.failure(), list)
    assert isinstance(result.failure()[0], ValidationError)
