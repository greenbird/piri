from piri.functions import apply_slicing


def test_no_value_is_ok():
    """When value is None we get a Success(None)."""
    assert apply_slicing(None, {}) is None


def test_middle_of_value():
    """Test that we can get a value in middle of string."""
    assert apply_slicing('test', {'from': 1, 'to': 3}) == 'es'


def test_middle_to_end():
    """Test that we can slice from middle to end of value."""
    assert apply_slicing('test', {'from': 1}) == 'est'


def test_start_to_middle():
    """Test that we can slice from start to middle."""
    assert apply_slicing('test', {'from': 0, 'to': 3}) == 'tes'


def test_start_to_end():
    """Test that we can slice from start to end."""
    assert apply_slicing('test', {'from': 0, 'to': None}) == 'test'


def test_negative_from():
    """Test that a negative from value starts cutting at the end minus from."""
    assert apply_slicing('012345', {'from': -2}) == '45'


def test_negative_to():
    """Test that a negative to value ends cut at end minus to."""
    assert apply_slicing('01234', {'from': 0, 'to': -2}) == '012'


def test_int_is_stringified():
    """Test that a non string value will be stringified before slice."""
    assert apply_slicing(123, {'from': 2}) == '3'


def test_float_is_stringified():
    """Test that a float value is stringfied."""
    assert apply_slicing(123.123, {'from': -3}) == '123'


def test_boolean_is_stringified():
    """Test that a boolean value is stringfied."""
    assert apply_slicing(False, {'from': 0, 'to': 1}) == 'F'  # noqa: WPS425


def test_object_is_stringified():
    """Test that an object is stringified."""
    assert apply_slicing(
        {'test': 'bob'},
        {'from': -5, 'to': -2},
    ) == 'bob'


def test_list():
    """Test that we can slice a list and that its not cast to string."""
    assert apply_slicing(
        [0, 1, 2],
        {'from': 1, 'to': None},
    ) == [1, 2]


def test_slice_range_longer_than_string():
    """Test that slice range longer than the string length returns string."""
    assert apply_slicing('0123', {'from': 0, 'to': 50}) == '0123'


def test_slice_range_on_range_out_of_string():
    """Test that slice range out of the string."""
    assert apply_slicing('0123', {'from': 5, 'to': 10}) == ''
