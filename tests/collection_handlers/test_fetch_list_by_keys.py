from returns.pipeline import is_successful

from mapmallow.collection_handlers import fetch_list_by_keys


def test():
    """Test that we can fetch key in dict."""
    test = [{'key': ['val1']}, ['key']]
    assert fetch_list_by_keys(*test).unwrap() == ['val1']


def test_no_path_raises_value_error():
    """Test that we get an error when we dont send a path."""
    test = [{'key', 'val1'}, []]
    t_result = fetch_list_by_keys(*test)
    assert not is_successful(t_result)
    assert 'path list empty' in str(t_result.failure())


def test_that_found_value_must_be_list():
    """Test that the value we find must be a list, expect error."""
    test = [{'key': 'val1'}, ['key']]
    t_result = fetch_list_by_keys(*test)
    assert not is_successful(t_result)
    assert 'Non list data found' in str(t_result.failure())
