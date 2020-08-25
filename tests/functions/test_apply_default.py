from returns.pipeline import is_successful

from piri.functions import apply_default


def test_apply_default():
    """Test if we get a default value."""
    assert apply_default(None, 'default').unwrap() == 'default'


def test_no_default_value():
    """Test value returned when exists."""
    assert apply_default('val', None).unwrap() == 'val'


def test_no_values():
    """Test returns Failure."""
    test = apply_default(None, None)
    assert not is_successful(test)


def test_bad_mapped_value():
    """Test if we get a Failure when we give bad mapped value."""
    test = apply_default(['array'], None)
    assert not is_successful(test)
    assert 'Unable to give default value' in str(test.failure())
