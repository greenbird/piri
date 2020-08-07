from mapmallow.functions import ApplyIfStatements


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
    assert ApplyIfStatements()(*test).value_or(None) == 'value2'


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
    assert ApplyIfStatements()(*test).unwrap() == 'value3'


def test_if_failed_condition():
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
    assert ApplyIfStatements()(*test).unwrap() == 'not_target_value'


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
    assert ApplyIfStatements()(*test).unwrap() == 'yes'
