from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(attribute_validator, valid):
    """Test that we get dict back on valid validation."""
    test: dict = {'name': 'attrib', 'default': 'bob'}
    assert attribute_validator(test).unwrap() == test


def test_invalid(attribute_validator, invalid):
    """Test that we get a list of errors."""
    test: dict = {'seperator': ' '}
    validate_result = attribute_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), list)
    assert isinstance(validate_result.failure()[0], ValidationError)
    assert 'name' in str(validate_result.failure())
