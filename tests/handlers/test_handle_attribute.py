import decimal

from piri.handlers import handle_attribute


def test_get_key_in_dict():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'val1'}
    config = {
        'name': 'attrib',
        'mappings': [
            {'path': ['key']},
        ],
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
            {'path': ['key']},
        ],
        'casting': {'to': 'decimal'},
    }

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == decimal.Decimal('1123123.12')


def test_regexp_is_applied_to_attribute():
    """Test that we can search by pattern."""
    input_data: dict = {'game': '1. e4 e5 ... 14. Rxe8+ Rxe8'}
    config: dict = {
        'name': 'moves',
        'mappings': [
            {
                'path': ['game'],
                'regexp': {
                    'search': '(Rxe8)',
                    'group': 1,
                },
            },
        ],
    }
    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'Rxe8'


def test_regexp_is_not_applied_to_attribute():
    """Test that we don't lose data when search by pattern fails."""
    input_data: dict = {'game': '1. d4 d5'}
    config: dict = {
        'name': 'moves',
        'mappings': [
            {
                'path': ['game'],
                'regexp': {
                    'search': '(d6)',
                    'group': 0,
                },
            },
        ],
    }
    regexp = handle_attribute(input_data, config)
    assert isinstance(regexp.failure(), ValueError) is True
    assert regexp.failure().args == ('Default value should not be `None`',)


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
        'default': 'default2',
    }

    assert handle_attribute(
        input_data,
        config,
    ).unwrap() == 'default2'
