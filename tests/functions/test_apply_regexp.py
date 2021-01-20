from piri.functions import apply_regexp


def test_regexp_on_index_out_of_range():
    """Test regexp when group indeces are out of range."""
    regexp = apply_regexp(
        'Hard work',
        {'search': 'r', 'group': [1, 2, 3]},
    )
    assert isinstance(regexp.failure(), IndexError) is True
    assert regexp.failure().args == ('list index out of range',)


def test_no_value_is_ok():
    """When value is None we get a Success(None)."""
    assert apply_regexp(None, {}).unwrap() is None
