from returns.pipeline import is_successful

from mapmallow.functions import ApplyDefault


def test_apply_default():
    """Test if we get a default value."""
    assert ApplyDefault()(None, 'default').unwrap() == 'default'


def test_no_default_value():
    """Test value returned when exists."""
    assert ApplyDefault()('val', None).unwrap() == 'val'


def test_no_values():
    """Test returns Failure."""
    test = ApplyDefault()(None, None)
    assert not is_successful(test)
