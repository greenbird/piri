from piri.mapper import iterable_data_handler


def test_iterable_data_handler():

    data = {
        'data': [
            {
                'nested': [
                    {
                        'another': [
                            {
                                'a': 'a',
                            },
                            {
                                'a': 'b'
                            }
                        ]
                    }
                ]
            },
            {
                'nested': [
                    {
                        'another': [
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
        ]
    }

    paths_to_iterables = [
        ['data'],
        ['data', 'nested'],
        ['nested', 'another']
    ]

    result = iterable_data_handler(data, paths_to_iterables)
    print('hei')
    print('result', result)
    print()
    res = [r for r in result]
    print('res', res)
    assert 1 == 2
