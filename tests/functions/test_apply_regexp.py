import pytest

from piri.functions import apply_regexp


def test_regexp_on_index_out_of_range():
    """Test regexp when group indeces are out of range."""
    with pytest.raises(IndexError):
        assert apply_regexp(
            'Hard work',
            {'search': 'r', 'group': [1, 2, 3]},
        )


def test_no_value_is_ok():
    """When value is None we get a Success(None)."""
    assert apply_regexp(None, {}) is None
