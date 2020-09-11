from returns.result import Success

from piri.functions import apply_if_statements


def test_if_is():
    """Test that 1 if (is) statement works."""
    test = [
        'target_value',
        [
            {
                'condition': 'is',
                'target': 'target_value',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_is_condition_false():
    """Test if condition False."""
    test = [
        'not_target_value',
        [
            {
                'condition': 'is',
                'target': 'target_value',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('not_target_value')


def test_if_in():
    """Test that 1 if (in) statement works."""
    test = [
        'target_value',
        [
            {
                'condition': 'in',
                'target': ['target_value'],
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_in_condition_false():
    """Test if in condition False."""
    test = [
        'not_target_value',
        [
            {
                'condition': 'in',
                'target': 'target_value',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('not_target_value')


def test_if_not():
    """Test that 1 if (not) statement works."""
    test = [
        'target_value',
        [
            {
                'condition': 'not',
                'target': 'not_target',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_not_condition_false():
    """Test if not condition False."""
    test = [
        'target_value',
        [
            {
                'condition': 'not',
                'target': 'target_value',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('target_value')


def test_if_contains():
    """Test that 1 if (contains) statement works."""
    test = [
        'target_value',
        [
            {
                'condition': 'contains',
                'target': '_value',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_contains_condition_false():
    """Test if contains condition False."""
    test = [
        'not_target_value',
        [
            {
                'condition': 'contains',
                'target': 'does_not_contain',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('not_target_value')


def test_if_chained():
    """Test that two if (is) statement works."""
    test = [
        'target_value',
        [
            {
                'condition': 'is',
                'target': 'target_value',
                'then': 'value2',
            },
            {
                'condition': 'is',
                'target': 'value2',
                'then': 'value3',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value3')


def test_if_failed_condition_goes_to_otherwise():
    """Test that we get the then value when condition fails."""
    test = [
        'not_target_value',
        [
            {
                'condition': 'is',
                'target': 'target_value',
                'then': 'no',
                'otherwise': 'yes',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('yes')
