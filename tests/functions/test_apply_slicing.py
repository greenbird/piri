from returns.pipeline import is_successful
from returns.result import Success

from piri.functions import apply_slicing


def test_no_value_fails():
    """When value is None we get a Failure."""
    assert not is_successful(apply_slicing(None, {}))


def test_slice_middle_of_value():
    """Test that we can get a value in middle of string."""
    assert apply_slicing('test', {'from': 1, 'to': 3}) == Success('es')


def test_slice_middle_to_end():
    """Test that we can slice from middle to end of value."""
    assert apply_slicing('test', {'from': 1}) == Success('est')


def test_slice_start_to_middle():
    """Test that we can slice from start to middle."""
    assert apply_slicing('test', {'from': 0, 'to': 3}) == Success('tes')


def test_slice_start_to_end():
    """test that we can slice from start to end."""
    assert apply_slicing('test', {'from': 0, 'to': None}) == Success('test')
