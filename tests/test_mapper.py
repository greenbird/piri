from mapmallow.mapper import map_data


def test_creating_key_to_name():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': False,
        'path_to_iterable': [],
        'objects': [],
        'branching_objects': [],
        'attributes': [
            {
                'name': 'name',
                'mappings': [
                    {
                        'path': ['key'],
                        'if_statements': [],
                    },
                ],
                'separator': '',
                'if_statements': [],
                'casting': [],
                'default': None,
            },
        ],
    }

    assert map_data(
        input_data,
        config,
    ).unwrap() == {'name': 'test name'}


def test_array_true_but_no_loop_gives_array():
    """Test that we get an array if we set array = true in object."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': True,
        'path_to_iterable': [],
        'objects': [],
        'branching_objects': [],
        'attributes': [
            {
                'name': 'name',
                'mappings': [
                    {
                        'path': ['key'],
                        'if_statements': [],
                    },
                ],
                'separator': '',
                'if_statements': [],
                'casting': [],
                'default': None,
            },
        ],
    }

    assert map_data(
        input_data,
        config,
    ).unwrap() == [{'name': 'test name'}]


def test_double_repeatable():
    """Test that we can map nested repeatable objects."""
    config = {
        'name': 'root',
        'array': True,
        'path_to_iterable': ['journals'],
        'attributes': [
            {
                'name': 'journal_id',
                'mappings': [
                    {
                        'path': ['journals', 'journal', 'id'],
                        'if_statements': [],
                    },
                ],
                'separator': '',
                'if_statements': [],
                'casting': [],
                'default': None,
            },
        ],
        'objects': [
            {
                'name': 'invoices',
                'array': True,
                'path_to_iterable': [
                    'journals', 'journal', 'invoices',
                ],
                'objects': [],
                'branching_objects': [],
                'attributes': [
                    {
                        'name': 'amount',
                        'mappings': [
                            {
                                'path': ['invoices', 'amount'],
                                'if_statements': [],
                            },
                        ],
                        'separator': '',
                        'if_statements': [],
                        'casting': [],
                        'default': None,
                    },
                ],
            },
        ],
        'branching_objects': [],
    }
    input_data = {
        'journals': [
            {
                'journal': {
                    'id': 1,
                    'invoices': [{'amount': 1.1}, {'amount': 1.2}],
                },
            },
            {
                'journal': {
                    'id': 2,
                    'invoices': [{'amount': 1.3}, {'amount': 1.4}],
                },
            },
        ],
    }
    expected_result = [
        {
            'journal_id': 1,
            'invoices': [
                {'amount': 1.1},
                {'amount': 1.2},
            ],
        },
        {
            'journal_id': 2,
            'invoices': [
                {'amount': 1.3},
                {'amount': 1.4},
            ],
        },
    ]

    assert map_data(
        input_data,
        config,
    ).unwrap() == expected_result


def test_mapping_where_data_is_not_found():
    """Test that when we map and don't find data its okay."""
    config = {
        'name': 'root',
        'array': True,
        'path_to_iterable': ['journals'],
        'attributes': [
            {
                'name': 'journal_id',
                'mappings': [
                    {
                        'path': ['journals', 'journal', 'id'],
                        'if_statements': [],
                    },
                ],
                'separator': '',
                'if_statements': [],
                'casting': [],
                'default': None,
            },
        ],
        'objects': [
            {
                'name': 'invoices',
                'array': True,
                'path_to_iterable': [
                    'journals', 'journal', 'invoices',
                ],
                'objects': [],
                'branching_objects': [],
                'attributes': [
                    {
                        'name': 'amount',
                        'mappings': [
                            {
                                'path': ['invoices', 'amount'],
                                'if_statements': [],
                                'default': None,
                            },
                        ],
                        'separator': '',
                        'if_statements': [],
                        'casting': [],
                        'default': None,
                    },
                ],
            },
        ],
        'branching_objects': [
            {
                'name': 'extrafield',
                'array': True,
                'path_to_iterable': [],
                'branching_attributes': [
                    [
                        {
                            'name': 'datavalue',
                            'mappings': [
                                {
                                    'path': ['extra', 'extra1'],
                                    'if_statements': [],
                                    'default': None,
                                },
                            ],
                            'separator': '',
                            'if_statements': [],
                            'casting': [],
                            'default': None,
                        },
                    ],
                ],
            },
        ],
    }
    input_data = {
        'journals': [
            {
                'journal': {
                    'id': 1,
                    'invoices': [{}, {'amount': 1.2}],
                },
            },
            {
                'journal': {
                    'id': 2,
                },
            },
        ],
    }
    expected_result = [
        {
            'journal_id': 1,
            'invoices': [
                {'amount': 1.2},
            ],
        },
        {
            'journal_id': 2,
        },
    ]

    assert map_data(
        input_data,
        config,
    ).unwrap() == expected_result


def test_most_features():
    """Test that we can fetch key in dict."""
    config = {
        'name': 'schema',
        'array': False,
        'path_to_iterable': [],
        'attributes': [
            {
                'name': 'name',
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
            },
        ],
        'objects': [
            {
                'name': 'address',
                'array': False,
                'path_to_iterable': [],
                'objects': [],
                'branching_objects': [],
                'attributes': [
                    {
                        'name': 'address1',
                        'mappings': [
                            {
                                'path': ['a1'],
                                'if_statements': [],
                            },
                        ],
                        'separator': '',
                        'if_statements': [],
                        'casting': [],
                        'default': None,
                    },
                    {
                        'name': 'address2',
                        'mappings': [
                            {
                                'path': ['a2'],
                                'if_statements': [],
                            },
                        ],
                        'separator': '',
                        'if_statements': [],
                        'casting': [],
                        'default': None,
                    },
                ],
            },
            {
                'name': 'people',
                'array': True,
                'path_to_iterable': ['persons'],
                'objects': [],
                'branching_objects': [],
                'attributes': [
                    {
                        'name': 'firstname',
                        'mappings': [
                            {
                                'path': ['persons', 'name'],
                                'if_statements': [],
                            },
                        ],
                        'separator': '',
                        'if_statements': [],
                        'casting': [],
                        'default': None,
                    },
                ],
            },
        ],
        'branching_objects': [
            {
                'name': 'extrafield',
                'array': True,
                'path_to_iterable': [],
                'branching_attributes': [
                    [
                        {
                            'name': 'dataname',
                            'mappings': [],
                            'separator': '',
                            'if_statements': [],
                            'casting': [],
                            'default': 'one',
                        },
                        {
                            'name': 'datavalue',
                            'mappings': [
                                {
                                    'path': ['extra', 'extra1'],
                                    'if_statements': [],
                                },
                            ],
                            'separator': '',
                            'if_statements': [],
                            'casting': [],
                            'default': None,
                        },
                    ],
                    [
                        {
                            'name': 'dataname',
                            'mappings': [],
                            'separator': '',
                            'if_statements': [],
                            'casting': [],
                            'default': 'two',
                        },
                        {
                            'name': 'datavalue',
                            'mappings': [
                                {
                                    'path': ['extra', 'extra2'],
                                    'if_statements': [],
                                },
                            ],
                            'separator': '',
                            'if_statements': [],
                            'casting': [],
                            'default': None,
                        },
                    ],
                ],
            },
        ],
    }
    input_data = {
        'key': 'val1',
        'key2': 'val2',
        'a1': 'a1',
        'a2': 'a2',
        'persons': [{'name': 'john'}, {'name': 'bob'}],
        'extra': {
            'extra1': 'extra1val',
            'extra2': 'extra2val',
        },
    }
    expected_result = {
        'name': 'default2',
        'address': {
            'address1': 'a1',
            'address2': 'a2',
        },
        'people': [
            {'firstname': 'john'},
            {'firstname': 'bob'},
        ],
        'extrafield': [
            {'dataname': 'one', 'datavalue': 'extra1val'},
            {'dataname': 'two', 'datavalue': 'extra2val'},
        ],
    }

    assert map_data(
        input_data,
        config,
    ).unwrap() == expected_result
