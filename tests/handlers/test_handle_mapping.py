from returns.pipeline import is_successful

from piri.handlers import handle_mapping


def test_get_key_in_dict():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'val1'}
    config = {'path': ['key']}

    assert handle_mapping(
        input_data,
        config,
    ).unwrap() == 'val1'


def test_default_value_is_used():
    """Test that we get a default value when no path and no ifs."""
    input_data = {'key': 'val'}
    config = {'default': 'default'}

    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'default'


def test_slicing_is_applied():
    """Test that applying slicing works."""
    input_data = {'key': 'value'}
    config = {
        'path': ['key'],
        'slicing': {
            'from': 2,
            'to': 3,
        },
    }
    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'l'


def test_if_statements_are_applied():
    """Test that applying if statements works."""
    input_data = {'key': 'val'}
    config = {
        'if_statements': [{
            'condition': 'is',
            'target': None,
            'then': 'otherval',
        }],
        'default': 'bob',
    }
    assert handle_mapping(
        input_data, config,
    ).unwrap() == 'otherval'


def test_default_value_not_none():
    """Test that providing bad data returns Failure instance."""
    failure = handle_mapping(
        {'fail': 'failure'},
        {'path': [], 'default': None},
    )
    assert not is_successful(failure)
    assert 'Default value should not be `None`' in str(failure.failure())
