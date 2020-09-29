from piri.mapper import iterable_data_handler


def test_iterable_data_handler():

    data = {
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
        ]
    }

    paths_to_iterables = [
        ['data'],
        ['data', 'nested'],
        ['nested', 'another']
    ]

    result = iterable_data_handler(data, paths_to_iterables)
    assert len(result) == 4
    assert result[3]['another']['a'] == 'd'
