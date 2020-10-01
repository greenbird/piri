from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(iterable_validator):
    """Test that we get dict back on valid validation."""
    test: dict = {'alias': 'test', 'path': ['test', 0, 'a']}
    assert iterable_validator(test).unwrap() == test


def test_invalid_alias_required(iterable_validator):
    """Test that alias key is required."""
    test: dict = {'path': ['date']}
    validate_result = iterable_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert "'alias' is a required property" in str(validate_result.failure())


def test_invalid_path_required(iterable_validator):
    """Test that path key is required."""
    test: dict = {'alias': 'test'}
    validate_result = iterable_validator(test)
    assert not is_successful(validate_result)
    assert "'path' is a required property" in str(validate_result.failure())


def test_alias_and_path_bad_type(iterable_validator):
    """Test that alias must be string and path must be array."""
    test: dict = {'alias': True, 'path': 'test'}
    validate_result = iterable_validator(test)
    assert not is_successful(validate_result)
    assert "True is not of type 'string'" in str(validate_result.failure())
    assert "'test' is not of type 'array'" in str(validate_result.failure())
