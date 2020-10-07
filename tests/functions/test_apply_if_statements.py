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


def test_if_is_condition_array_value():
    """Test that we can do if is statement on arrays."""
    test = [
        ['target_value'],
        [
            {
                'condition': 'is',
                'target': ['target_value'],
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_is_condition_objects_value():
    """Test that we can do if is statement on objectss."""
    test = [
        {'val': 'target'},
        [
            {
                'condition': 'is',
                'target': {'val': 'target'},
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


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


def test_if_in_condition_array_value():
    """Test that we can do if in statement on arrays."""
    test = [
        ['target_value'],
        [
            {
                'condition': 'in',
                'target': [['target_value']],
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_in_condition_objects_value():
    """Test that we can do if is statement on objectss."""
    test = [
        {'val': 'target'},
        [
            {
                'condition': 'in',
                'target': [{'val': 'target'}],
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


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


def test_if_not_condition_array_value():
    """Test that we can do if not statement on arrays."""
    test = [
        ['target_value'],
        [
            {
                'condition': 'not',
                'target': ['not_target'],
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_not_condition_objects_value():
    """Test that we can do if not statement on objectss."""
    test = [
        {'val': 'target'},
        [
            {
                'condition': 'not',
                'target': {'val': 'tarnot'},
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


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


def test_if_contains_condition_array_value():
    """Test that we can do if contains statement on arrays."""
    test = [
        ['value', 'target'],
        [
            {
                'condition': 'contains',
                'target': 'target',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_contains_condition_objects_value():
    """Test that we can do if contains statement on objectss."""
    test = [
        {'val': 'target'},
        [
            {
                'condition': 'contains',
                'target': 'val',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_contains_objects_in_array_value():
    """Test that we can do if contains statement on objectss."""
    test = [
        [{'val': 'target'}],
        [
            {
                'condition': 'contains',
                'target': {'val': 'target'},
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


def test_if_contains_array_does_not_stringify():
    """Test that we can do if contains statement on array[objects].

    However its very important that list and object tests does not do
    string casting for check since it would give the check two possible
    ways to do the check and there should only be one.
    for objects the 'in' checks if the key exist
    for arrays the 'in' checks if the element exist inside the aray
    for everything else we will stringify the test value.
    """
    test = [
        [{'val': 'target'}],
        [
            {
                'condition': 'contains',
                'target': 'target',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success([{'val': 'target'}])


def test_if_contains_works_with_non_strings():
    """Test that we can do if contains statement on objectss."""
    test = [
        123,
        [
            {
                'condition': 'contains',
                'target': '123',
                'then': 'value2',
            },
        ],
    ]
    assert apply_if_statements(*test) == Success('value2')


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
