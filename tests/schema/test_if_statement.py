from jsonschema import ValidationError
from returns.pipeline import is_successful


def test_validates(if_statement_validator):
    """Test that we get dict back on valid validation."""
    test = {
        'condition': 'is',
        'target': 'bob',
        'then': 'arne',
    }
    assert if_statement_validator(test).unwrap() == test


def test_invalid(if_statement_validator):
    """Test that we get a list of errors."""
    test = {
        'condition': 'is',
        'target': 'bob',
    }
    validate_result = if_statement_validator(test)

    assert not is_successful(validate_result)
    assert isinstance(validate_result.failure(), ValueError)
    assert isinstance(validate_result.failure().args[0][0], ValidationError)
    assert "'then' is a required property" in str(validate_result.failure())


def test_when_condition_in_target_string_or_array(if_statement_validator):
    """When condition is `in` target must be `string` or `array`."""
    test = {
        'condition': 'in',
        'target': 123,
        'then': 'bob',
    }
    validate_result = if_statement_validator(test)

    assert not is_successful(validate_result)
    assert "not of type 'string', 'array'" in str(validate_result.failure())
