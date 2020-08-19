import decimal

from mapmallow.handlers import handle_attribute


def test_get_key_in_dict():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'val1'}
    config = {
        'name': 'attrib',
        'mappings': [
            {'path': ['key'], 'if_statements': []},
        ],
        'separator': '',
        'if_statements': [],
        'casting': {},
    }

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'val1'


def test_casting_to_decimal():
    """Test that we can cast a string value to decimal."""
    input_data = {'key': '1,123,123.12'}
    config = {
        'name': 'attrib',
        'mappings': [
            {'path': ['key'], 'if_statements': []},
        ],
        'separator': '',
        'if_statements': [],
        'casting': {'to': 'decimal'},
    }

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == decimal.Decimal('1123123.12')


def test_all():
    """Test a full attribute schema."""
    input_data = {'key': 'val1', 'key2': 'val2'}
    config = {
        'name': 'attrib',
        'mappings': [
            {
                'path': ['key'],
                'if_statements': [
                    {
                        'condition': 'is',
                        'target': 'val1',
                        'then': None,
                    },
                ],
                'default': 'default',
            },
            {
                'path': ['key2'],
                'if_statements': [
                    {
                        'condition': 'is',
                        'target': 'val2',
                        'then': 'if',
                    },
                ],
            },
        ],
        'separator': '-',
        'if_statements': [
            {
                'condition': 'is',
                'target': 'default-if',
                'then': None,
            },
        ],
        'casting': {},
        'default': 'default2',
    }

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'default2'
