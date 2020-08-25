from decimal import Decimal

from returns.pipeline import is_successful
from typing_extensions import Final

from piri.casting import CastToDecimal

target: Final[Decimal] = Decimal('1234567.89')


def test_string_with_one_period():
    """Test normal decimal value with one period."""
    assert CastToDecimal()(
        '1234567.89',
    ).unwrap() == target


def test_string_with_one_comma():
    """Test normal decimal value with one comma."""
    assert CastToDecimal()(
        '1234567,89',
    ).unwrap() == target


def test_string_with_period_and_space():
    """Test space separated decimal number with 1 period."""
    assert CastToDecimal()(
        '1 234 567.89',
    ).unwrap() == target


def test_string_with_commas_and_period():
    """Test comma as thousands separator with period as decimal."""
    assert CastToDecimal()(
        '1,234,567.89',
    ).unwrap() == target


def test_string_with_periods_and_comma():
    """Test period as thousands separator with comma as decimal."""
    assert CastToDecimal()(
        '1.234.567,89',
    ).unwrap() == target


def test_string_with_no_period_nor_comma():
    """Test an integer number will nicely become a decimal."""
    test = CastToDecimal()('123456789')
    assert is_successful(test)
    assert test.unwrap() == Decimal('123456789')


def test_with_integer_containing_decimals_format():
    """Integer_containing_decimals format, should be divided by 100."""
    test = CastToDecimal()(
        '123456789',
        'integer_containing_decimals',
    )
    assert test.unwrap() == target


def test_abc_fails():
    """Test that string with letters in fails."""
    test = CastToDecimal()('abc')
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Illegal characters in value' in str(test.failure())


def test_abc_with_decimal_argument_fails():
    """Test that string with letters in fails when we supply 'decimal'."""
    test = CastToDecimal()(
        'abc', 'integer_containing_decimals',
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Illegal characters in value' in str(test.failure())
