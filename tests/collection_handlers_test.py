# -*- coding: utf-8 -*-

"""Test mapping operation functions."""
from returns.pipeline import is_successful

from mapmallow.collection_handlers import (
    fetch_data_by_keys,
    fetch_list_by_keys,
    set_value_in_dict,
)


class TestFetchDataByKeys(object):
    """Test FetchDataByKeys function."""

    def test(self):
        """Test that we can fetch key in dict."""
        test = [{'key': 'val1'}, ['key']]
        assert fetch_data_by_keys(*test).unwrap() == 'val1'

    def test_two_keys(self):
        """Test that we are able to map with multiple keys."""
        test = [{'key1': {'key2': 'val1'}}, ['key1', 'key2']]
        assert fetch_data_by_keys(*test).unwrap() == 'val1'

    def test_no_such_key(self):
        """Test Failure on missing key."""
        test = [{'key': 'val1'}, ['missing']]
        t_result = fetch_data_by_keys(*test)
        assert not is_successful(t_result)
        assert 'missing' in str(t_result.failure())

    def test_no_path(self):
        """Test no path should return Failure."""
        test = [{'key': 'val'}, []]
        t_result = fetch_data_by_keys(*test)
        assert not is_successful(t_result)
        assert 'path list empty' in str(t_result.failure())

    def test_no_data(self):
        """Test no data should return Failure."""
        test = [{}, ['keys']]
        t_result = fetch_data_by_keys(*test)
        assert not is_successful(t_result)
        assert 'keys' in str(t_result.failure())

    def test_bad_valuetype(self):
        """Test that giving path to dict will give us an error."""
        test = [{'key': {'key1': 'val'}}, ['key']]
        t_result = fetch_data_by_keys(*test)
        assert not is_successful(t_result)
        assert 'Bad data found' in str(t_result.failure())


class TestFetchListByKeys(object):
    """Test FetchListByKeys function."""

    def test(self):
        """Test that we can fetch key in dict."""
        test = [{'key': ['val1']}, ['key']]
        assert fetch_list_by_keys(*test).unwrap() == ['val1']

    def test_no_path_raises_value_error(self):
        """Test that we get an error when we dont send a path."""
        test = [{'key', 'val1'}, []]
        t_result = fetch_list_by_keys(*test)
        assert not is_successful(t_result)
        assert 'path list empty' in str(t_result.failure())

    def test_that_found_value_must_be_list(self):
        """Test that the value we find must be a list, expect error."""
        test = [{'key': 'val1'}, ['key']]
        t_result = fetch_list_by_keys(*test)
        assert not is_successful(t_result)
        assert 'Non list data found' in str(t_result.failure())


class TestSetValueInDict(object):
    """Test set_value_in_dict function."""

    def test(self):
        """Test that we can fetch key in dict."""
        dictionary = {'key': 'val1'}
        test = ['val2', dictionary, ['key']]
        assert is_successful(set_value_in_dict(*test))
        assert dictionary['key'] == 'val2'

    def test_multiple_path(self):
        """Test that we can fetch key in dict."""
        dictionary = {'key': {'key2': 'val1'}}
        test = ['val2', dictionary, ['key', 'key2']]
        assert is_successful(set_value_in_dict(*test))
        assert dictionary['key']['key2'] == 'val2'

    def test_no_path_raises_value_error(self):
        """Test that we get an error when we dont send a path."""
        test = ['val2', {'key': ['val1']}, []]
        t_result = set_value_in_dict(*test)
        assert not is_successful(t_result)
        assert 'path list empty' in str(t_result.failure())

    def test_path_to_missing_key_is_ok(self):
        """Test that missing keys are okay."""
        dictionary = {'key': ['val1']}
        test = ['val2', dictionary, ['bob']]
        t_result = set_value_in_dict(*test)
        assert is_successful(t_result)
        assert dictionary['bob'] == 'val2'  # type: ignore
