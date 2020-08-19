from returns.pipeline import is_successful
from typing_extensions import Final

from mapmallow.casting import CastToInteger

target: Final[int] = 123


def test_cast_string():
    """Cast a string with numbers to integer."""
    assert CastToInteger()('123').unwrap() == target


def test_cast_negative_string():
    """Cast string with negative number to integer."""
    assert CastToInteger()('-123').unwrap() == -target


def test_cast_decimal_string():
    """Cast a decimal string to integer."""
    assert CastToInteger()(
        '123.0',
        'decimal',
    ).unwrap() == target


def test_cast_negative_decimal_string():
    """Cast a negative decimal string to integer."""
    assert CastToInteger()(
        '-123.0', 'decimal',
    ).unwrap() == -target


def test_cast_decimal_string_rounds_up():
    """Cast a decimal string >= .5 should round up."""
    assert CastToInteger()(
        '122.5',
        'decimal',
    ).unwrap() == target


def test_once_more_cast_decimal_string_rounds_up():
    """Cast a decimal string >= .5 should round up."""
    assert CastToInteger()(
        '123.5',
        'decimal',
    ).unwrap() == 124


def test_cast_decimal_string_rounds_down():
    """Cast a decimal string < .0 should round down."""
    assert CastToInteger()(
        '123.49',
        'decimal',
    ).unwrap() == target


def test_abc_fails():
    """Test that string with letters in fails."""
    test = CastToInteger()('abc')
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Illegal characters in value' in str(test.failure())


def test_abc_with_decimal_argument_fails():
    """Test that string with letters in fails when we supply 'decimal'."""
    test = CastToInteger()(
        'abc',
        'decimal',
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Illegal characters in value' in str(test.failure())
