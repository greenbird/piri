from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(object_validator, valid):
    """Test that we get dict back on valid validation."""
    validate_result = object_validator(valid)
    assert validate_result.unwrap() == valid


def test_invalid(object_validator, invalid):
    """Test that we get a list of errors."""
    validate_result = object_validator(invalid)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), list)
    assert isinstance(validate_result.failure()[0], ValidationError)
