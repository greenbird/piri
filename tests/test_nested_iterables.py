from piri.collection_handlers import iterable_data_handler


def test_iterable_data_handler():
    """Test that we can iterate multiple levels in one go."""
    input_data = {
        'data': [
            {'nested': [
                {'another': [
                    {'a': 'a'},
                    {'a': 'b'},
                ]},
            ]},
            {'nested': [
                {'another': [
                    {'a': 'c'},
                    {'a': 'd'},
                ]},
            ]},
        ],
    }

    paths_to_iterables = [
        ['data'],
        ['data', 'nested'],
        ['does', 'not', 'exist'],
        ['nested', 'another'],
    ]

    iterables = iterable_data_handler(input_data, paths_to_iterables).unwrap()
    assert len(iterables) == 4
    assert iterables[3]['another']['a'] == 'd'
    # assert False
