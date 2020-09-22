from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(slicing_validator):
    """Test that we get dict back on valid validation."""
    test: dict = {'from': 1}
    assert slicing_validator(test).unwrap() == test


def test_invalid(slicing_validator):
    """Test that we get a list of errors."""
    test: dict = {'to': 'string'}
    validate_result = slicing_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert "'string' is not of type 'int" in str(validate_result.failure())
    assert "'from' is a required property" in str(validate_result.failure())
