from returns.pipeline import is_successful

from mapmallow.handlers import handle_mapping


def test_get_key_in_dict():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'val1'}
    config = {'path': ['key'], 'if_statements': []}

    assert handle_mapping(
        input_data,
        config,
    ).unwrap() == 'val1'


def test_default_value_is_used():
    """Test that we get a default value when no path and no ifs."""
    input_data = {'key': 'val'}
    config = {'path': [], 'if_statements': [], 'default': 'default'}

    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'default'


def test_default_value_not_none():
    """Test that providing bad data returns Failure instance."""
    failure = handle_mapping(
        {'fail': 'failure'},
        {'path': [], 'if_statements': [], 'default': None},
    )
    assert not is_successful(failure)
    assert 'Default value should not be `None`' in str(failure.failure())
