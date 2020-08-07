from returns.pipeline import is_successful

from mapmallow.collection_handlers import set_value_in_dict


def test():
    """Test that we can fetch key in dict."""
    dictionary = {'key': 'val1'}
    test = ['val2', dictionary, ['key']]
    assert is_successful(set_value_in_dict(*test))
    assert dictionary['key'] == 'val2'


def test_multiple_path():
    """Test that we can fetch key in dict."""
    dictionary = {'key': {'key2': 'val1'}}
    test = ['val2', dictionary, ['key', 'key2']]
    assert is_successful(set_value_in_dict(*test))
    assert dictionary['key']['key2'] == 'val2'


def test_no_path_raises_value_error():
    """Test that we get an error when we dont send a path."""
    test = ['val2', {'key': ['val1']}, []]
    t_result = set_value_in_dict(*test)
    assert not is_successful(t_result)
    assert 'path list empty' in str(t_result.failure())


def test_path_to_missing_key_is_ok():
    """Test that missing keys are okay."""
    dictionary = {'key': ['val1']}
    test = ['val2', dictionary, ['bob']]
    t_result = set_value_in_dict(*test)
    assert is_successful(t_result)
    assert dictionary['bob'] == 'val2'  # type: ignore
