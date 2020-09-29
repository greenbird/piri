from piri.mapper import iterable_data_handler


def test_iterable_data_handler():

    data = {
        'data': [
            {
                'nested': [
                    {
                        'a': 'a',
                    },
                    {
                        'a': 'b'
                    }
                ]
            },
            {
                'nested': [
                    {
                        'a': 'c',
                    },
                    {
                        'a': 'd'
                    }
                ]
            }
        ]
    }

    paths_to_iterables = [
        ['data'],
        ['data', 'nested'],
    ]

    result = iterable_data_handler(data, paths_to_iterables)
    print('hei')
    print([r for r in result])
    assert 1 == 2
