from returns.pipeline import is_successful

from mapmallow.functions import ApplyCasting


def test_no_value_raises_fails():
    """No cast_to string should just return input value."""
    assert ApplyCasting()('val', {'to': None}).unwrap() == 'val'


def test_value_but_cast_to_fails():
    """No value should just fail with ValueError."""
    test = ApplyCasting()(None, {})
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'value_to_cast is empty' in str(test.failure())


def test_not_implemented_cast_to():
    """Test that we get NotImplementedError for unknown cast_to's."""
    test = ApplyCasting()('val', {'to': 'not_supported'})
    assert not is_successful(test)
    assert isinstance(test.failure(), NotImplementedError)
    assert 'Unsupported cast to value' in str(test.failure())


def test_no_cast_to_returns_value():
    """Test that when we do not provide cast_to we get original value."""
    test = ApplyCasting()('val', {'to': None})
    assert test.unwrap() == 'val'
