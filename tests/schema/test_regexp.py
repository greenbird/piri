from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(regexp_validator):
    """Test that we get dict back on valid validation."""
    test: dict = {'search': '[abc]+'}
    assert regexp_validator(test).unwrap() == test


def test_missing_search_keyword(regexp_validator):
    """Test that we get a list of errors."""
    test: dict = {}
    validate_result = regexp_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert "'search' is a required property" in str(validate_result.failure())


def test_wrong_search_keyword_type(regexp_validator):
    """Test that we get a list of errors when type is wrong."""
    test: dict = {'search': 123244}
    validate_result = regexp_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert "123244 is not of type 'string'" in str(validate_result.failure())


def test_invalid_regex_string(regexp_validator):
    """Test that a normal string, but invalid regex expression fails."""
    test: dict = {'search': '[a-zA-Z0-9%&'}
    validate_result = regexp_validator(test)
    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert "is not a 'regex'" in str(validate_result.failure())
