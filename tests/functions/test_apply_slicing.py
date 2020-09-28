from piri.functions import apply_slicing


def test_no_value_is_ok():
    """When value is None we get a Success(None)."""
    assert apply_slicing(None, {}) is None


def test_slice_middle_of_value():
    """Test that we can get a value in middle of string."""
    assert apply_slicing('test', {'from': 1, 'to': 3}) == 'es'


def test_slice_middle_to_end():
    """Test that we can slice from middle to end of value."""
    assert apply_slicing('test', {'from': 1}) == 'est'


def test_slice_start_to_middle():
    """Test that we can slice from start to middle."""
    assert apply_slicing('test', {'from': 0, 'to': 3}) == 'tes'


def test_slice_start_to_end():
    """Test that we can slice from start to end."""
    assert apply_slicing('test', {'from': 0, 'to': None}) == 'test'


def test_slice_negative_from():
    """Test that a negative from value starts cutting at the end minus from."""
    assert apply_slicing('012345', {'from': -2}) == '45'


def test_slice_negative_to():
    """Test that a negative to value ends cut at end minus to."""
    assert apply_slicing('01234', {'from': 0, 'to': -2}) == '012'
