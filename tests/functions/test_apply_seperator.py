import pytest
from returns.primitives.exceptions import UnwrapFailedError

from mapmallow.functions import ApplySeparator


def test_separator():
    """Test separator is applied between two values."""
    test = [['val1', 'val2'], '-']
    assert ApplySeparator()(*test).unwrap() == 'val1-val2'


def test_separator_one_value():
    """Test when theres only one value, no separator should be applied."""
    test = [['val1'], '-']
    assert ApplySeparator()(*test).unwrap() == 'val1'


def test_one_integer_value_not_stringified():
    """One value should allways return just the value uncasted."""
    test = [[1], '']
    assert ApplySeparator()(*test).unwrap() == 1


def test_one_integer_value_with_other_value():
    """Two values no matter the type should be cast to string."""
    test = [[1, 'val2'], '-']
    assert ApplySeparator()(*test).unwrap() == '1-val2'


def test_no_value():
    """When no value is given we should return Failure."""
    test = [[], '-']
    with pytest.raises(UnwrapFailedError):
        ApplySeparator()(*test).unwrap()


def test_no_separator():
    """Test that no separator throws error."""
    test = [['val1', 'val2'], None]
    with pytest.raises(UnwrapFailedError):
        ApplySeparator()(*test).unwrap()
