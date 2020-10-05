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
    input_data: dict = {'game': '1. e4 e5 2. f4 exf4 3. Nf3 d5 4. exd5 Bd6 5. Bc4 Nf6 6. Qe2+ Qe7 7. Qxe7+ Kxe7 8. d4 Re8 9. O-O h6 10. Ne5 g5 11. Re1 Kf8 12. Nc3 Nbd7 13. Nxd7+ Bxd7 14. Rxe8+ Rxe8 15. h3 a6 16. a3 Bf5'}  # noqa: E501
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
