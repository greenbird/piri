from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(mapping_validator, valid):
    """Test that we get dict back on valid validation."""
    test: dict = {'default': 'test'}
    assert mapping_validator(test).unwrap() == test


def test_invalid(mapping_validator, invalid):
    """Test that we get a list of errors."""
    test: dict = {'if_statements': []}
    validate_result = mapping_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert 'path' in str(validate_result.failure())
