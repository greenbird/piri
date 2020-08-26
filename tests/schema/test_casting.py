from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(casting_validator, valid):
    """Test that we get dict back on valid validation."""
    test: dict = {'to': 'integer'}
    assert casting_validator(test).unwrap() == test


def test_invalid(casting_validator, invalid):
    """Test that we get a list of errors."""
    test: dict = {'to': 'date'}
    validate_result = casting_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert 'original_format' in str(validate_result.failure())
