from returns.pipeline import is_successful

from mapmallow.collection_handlers import fetch_data_by_keys


def test():
    """Test that we can fetch key in dict."""
    test = [{'key': 'val1'}, ['key']]
    assert fetch_data_by_keys(*test).unwrap() == 'val1'


def test_two_keys():
    """Test that we are able to map with multiple keys."""
    test = [{'key1': {'key2': 'val1'}}, ['key1', 'key2']]
    assert fetch_data_by_keys(*test).unwrap() == 'val1'


def test_no_such_key():
    """Test Failure on missing key."""
    test = [{'key': 'val1'}, ['missing']]
    t_result = fetch_data_by_keys(*test)
    assert not is_successful(t_result)
    assert 'missing' in str(t_result.failure())


def test_no_path():
    """Test no path should return Failure."""
    test = [{'key': 'val'}, []]
    t_result = fetch_data_by_keys(*test)
    assert not is_successful(t_result)
    assert 'path list empty' in str(t_result.failure())


def test_no_data():
    """Test no data should return Failure."""
    test = [{}, ['keys']]
    t_result = fetch_data_by_keys(*test)
    assert not is_successful(t_result)
    assert 'keys' in str(t_result.failure())


def test_bad_valuetype():
    """Test that giving path to dict will give us an error."""
    test = [{'key': {'key1': 'val'}}, ['key']]
    t_result = fetch_data_by_keys(*test)
    assert not is_successful(t_result)
    assert 'Bad data found' in str(t_result.failure())
