import json

from returns.pipeline import is_successful

from piri.mapper import map_data


def test_creating_key_to_name():
    """Test that we can fetch key in dict."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': False,
        'attributes': [
            {
                'name': 'name',
                'mappings': [
                    {
                        'path': ['key'],
                    },
                ],
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
        'attributes': [
            {
                'name': 'name',
                'mappings': [
                    {
                        'path': ['key'],
                    },
                ],
            },
        ],
    }

    assert map_data(
        input_data,
        config,
    ).unwrap() == [{'name': 'test name'}]


def test_missing_data_gives_nothing():
    """Test that we get an array if we set array = true in object."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': True,
        'attributes': [
            {
                'name': 'name',
                'mappings': [
                    {
                        'path': ['missing'],
                    },
                ],
            },
        ],
    }

    assert not is_successful(map_data(
        input_data,
        config,
    ))


def test_missing_data_creates_no_object():
    """Test that if an object mapping result is empty we create now 'key'."""
    input_data = {'key': 'test name'}
    config = {
        'name': 'root',
        'array': True,
        'attributes': [
            {
                'name': 'an_attribute',
                'default': 'val',
            },
        ],
        'objects': [
            {
                'name': 'test',
                'array': False,
                'attributes': [
                    {
                        'name': 'name',
                        'mappings': [
                            {
                                'path': ['missing'],
                            },
                        ],
                    },
                ],
            },
        ],
    }

    expected_result = [{
        'an_attribute': 'val',
    }]

    assert map_data(
        input_data,
        config,
    ).unwrap() == expected_result


def test_double_repeatable():
    """Test that we can map nested repeatable objects."""
    config = {
        'name': 'root',
        'array': True,
        'iterables': [
            {
                'alias': 'journals',
                'path': ['journals'],
            },
        ],
        'attributes': [
            {
                'name': 'journal_id',
                'mappings': [
                    {
                        'path': ['journals', 'journal', 'id'],
                    },
                ],
            },
        ],
        'objects': [
            {
                'name': 'invoices',
                'array': True,
                'iterables': [
                    {
                        'alias': 'invoices',
                        'path': ['journals', 'journal', 'invoices'],
                    },
                ],
                'attributes': [
                    {
                        'name': 'amount',
                        'mappings': [
                            {
                                'path': ['invoices', 'amount'],
                            },
                        ],
                    },
                ],
            },
        ],
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
        'iterables': [
            {
                'alias': 'journals',
                'path': ['journals'],
            },
        ],
        'attributes': [
            {
                'name': 'journal_id',
                'mappings': [
                    {
                        'path': ['journals', 'journal', 'id'],
                    },
                ],
            },
        ],
        'objects': [
            {
                'name': 'invoices',
                'array': True,
                'iterables': [
                    {
                        'alias': 'invoices',
                        'path': ['journals', 'journal', 'invoices'],
                    },
                ],
                'attributes': [
                    {
                        'name': 'amount',
                        'mappings': [
                            {
                                'path': ['invoices', 'amount'],
                            },
                        ],
                    },
                ],
            },
        ],
        'branching_objects': [
            {
                'name': 'extrafield',
                'array': True,
                'branching_attributes': [
                    [
                        {
                            'name': 'datavalue',
                            'mappings': [
                                {
                                    'path': ['extra', 'extra1'],
                                },
                            ],
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
            'invoices': [],
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
                'default': 'default2',
            },
        ],
        'objects': [
            {
                'name': 'address',
                'array': False,
                'attributes': [
                    {
                        'name': 'address1',
                        'mappings': [
                            {
                                'path': ['a1'],
                            },
                        ],
                    },
                    {
                        'name': 'address2',
                        'mappings': [
                            {
                                'path': ['a2'],
                            },
                        ],
                    },
                ],
            },
            {
                'name': 'people',
                'array': True,
                'iterables': [
                    {
                        'alias': 'persons',
                        'path': ['persons'],
                    },
                ],
                'attributes': [
                    {
                        'name': 'firstname',
                        'mappings': [
                            {
                                'path': ['persons', 'name'],
                            },
                        ],
                    },
                ],
            },
        ],
        'branching_objects': [
            {
                'name': 'extrafield',
                'array': True,
                'branching_attributes': [
                    [
                        {
                            'name': 'dataname',
                            'default': 'one',
                        },
                        {
                            'name': 'datavalue',
                            'mappings': [
                                {
                                    'path': ['extra', 'extra1'],
                                },
                            ],
                        },
                    ],
                    [
                        {
                            'name': 'dataname',
                            'default': 'two',
                        },
                        {
                            'name': 'datavalue',
                            'mappings': [
                                {
                                    'path': ['extra', 'extra2'],
                                },
                            ],
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


def test_regexp_feature():
    """Test Regexp on the example from the docs."""
    with open('tests/json/config_regexp.json', 'r') as jfile:
        config = json.load(jfile)

    input_data = {
        'black': {
            '@id': 'https://api.chess.com/pub/player/chameleoniasa',
            'rating': 1273,
            'result': 'insufficient',
            'username': 'ChameleonIASA',
        },
        'end_time': 1347534562,
        'fen': '8/8/8/8/7B/5k2/7K/8 b - -',
        'pgn': '[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2012.09.13\"]\n[Round \"-\"]\n[White \"GAURAV480\"]\n[Black \"ChameleonIASA\"]\n[Result \"1/2-1/2\"]\n[ECO \"A00\"]\n[ECOUrl \"https://www.chess.com/openings/Saragossa-Opening\"]\n[CurrentPosition \"8/8/8/8/7B/5k2/7K/8 b - -\"]\n[Timezone \"UTC\"]\n[UTCDate \"2012.09.13\"]\n[UTCTime \"11:03:43\"]\n[WhiteElo \"1283\"]\n[BlackElo \"1273\"]\n[TimeControl \"180\"]\n[Termination \"Game drawn by insufficient material\"]\n[StartTime \"11:03:43\"]\n[EndDate \"2012.09.13\"]\n[EndTime \"11:09:22\"]\n[Link \"https://www.chess.com/live/game/361066365\"]\n\n1. c3 {[%clk 0:03:00]} 1... e6 {[%clk 0:03:00]} 2. Qb3 {[%clk 0:02:57.1]} 2... Ne7 {[%clk 0:02:58.4]} 3. Nf3 {[%clk 0:02:47.7]} 3... d5 {[%clk 0:02:57.9]} 4. e3 {[%clk 0:02:45.6]} 4... Nd7 {[%clk 0:02:57.3]} 5. Be2 {[%clk 0:02:42.3]} 5... a6 {[%clk 0:02:56.9]} 6. O-O {[%clk 0:02:36.6]} 6... b5 {[%clk 0:02:56.3]} 7. d4 {[%clk 0:02:35.1]} 7... Bb7 {[%clk 0:02:55.7]} 8. Qc2 {[%clk 0:02:28.4]} 8... g6 {[%clk 0:02:55.3]} 9. Nbd2 {[%clk 0:02:25.4]} 9... Bg7 {[%clk 0:02:54.6]} 10. Nb3 {[%clk 0:02:23.6]} 10... c6 {[%clk 0:02:54.2]} 11. a3 {[%clk 0:02:21.3]} 11... a5 {[%clk 0:02:52]} 12. a4 {[%clk 0:02:17.9]} 12... bxa4 {[%clk 0:02:49.7]} 13. Rxa4 {[%clk 0:02:16.2]} 13... Nb6 {[%clk 0:02:45.5]} 14. Rxa5 {[%clk 0:02:12.4]} 14... Rxa5 {[%clk 0:02:43.9]} 15. Nxa5 {[%clk 0:02:11.4]} 15... Nc4 {[%clk 0:02:40.4]} 16. Nxb7 {[%clk 0:02:07.8]} 16... Qb6 {[%clk 0:02:36.9]} 17. Bxc4 {[%clk 0:01:59.4]} 17... dxc4 {[%clk 0:02:34.1]} 18. Nd6+ {[%clk 0:01:58.1]} 18... Kd7 {[%clk 0:02:30.1]} 19. Nxc4 {[%clk 0:01:55.2]} 19... Qa6 {[%clk 0:02:28.6]} 20. b4 {[%clk 0:01:49.9]} 20... Ra8 {[%clk 0:02:24.4]} 21. Qd3 {[%clk 0:01:45]} 21... Nd5 {[%clk 0:02:14.7]} 22. Nce5+ {[%clk 0:01:42.2]} 22... Bxe5 {[%clk 0:02:12.2]} 23. Nxe5+ {[%clk 0:01:37.6]} 23... Ke7 {[%clk 0:02:11.1]} 24. Qxa6 {[%clk 0:01:34.8]} 24... Rxa6 {[%clk 0:02:08.5]} 25. c4 {[%clk 0:01:32.9]} 25... Nxb4 {[%clk 0:02:05]} 26. Bd2 {[%clk 0:01:32]} 26... Nc2 {[%clk 0:01:59.5]} 27. h3 {[%clk 0:01:30.3]} 27... Kf6 {[%clk 0:01:55.7]} 28. Rb1 {[%clk 0:01:28.2]} 28... c5 {[%clk 0:01:43.9]} 29. dxc5 {[%clk 0:01:26.3]} 29... Kxe5 {[%clk 0:01:41.1]} 30. Bc3+ {[%clk 0:01:22.3]} 30... Ke4 {[%clk 0:01:39.6]} 31. Rb7 {[%clk 0:01:16.4]} 31... Kd3 {[%clk 0:01:37.9]} 32. Be5 {[%clk 0:01:11.9]} 32... Kxc4 {[%clk 0:01:35.7]} 33. Rxf7 {[%clk 0:01:07.8]} 33... Kxc5 {[%clk 0:01:34.2]} 34. Rxh7 {[%clk 0:01:06.7]} 34... Kd5 {[%clk 0:01:32.4]} 35. Bg3 {[%clk 0:01:03.4]} 35... Ra1+ {[%clk 0:01:28.5]} 36. Kh2 {[%clk 0:00:59.9]} 36... e5 {[%clk 0:01:24.4]} 37. Rh6 {[%clk 0:00:55.1]} 37... g5 {[%clk 0:01:21.8]} 38. Rh5 {[%clk 0:00:52.4]} 38... Ke4 {[%clk 0:01:17.7]} 39. Rxg5 {[%clk 0:00:51.4]} 39... Nb4 {[%clk 0:01:11.7]} 40. Rxe5+ {[%clk 0:00:48.3]} 40... Kd3 {[%clk 0:01:09.9]} 41. Rb5 {[%clk 0:00:44.8]} 41... Kc4 {[%clk 0:01:06.8]} 42. Rb8 {[%clk 0:00:39.9]} 42... Nd3 {[%clk 0:01:02.3]} 43. e4 {[%clk 0:00:35.4]} 43... Kd4 {[%clk 0:00:58.8]} 44. e5 {[%clk 0:00:33.6]} 44... Nxf2 {[%clk 0:00:53]} 45. Bxf2+ {[%clk 0:00:31]} 45... Kxe5 {[%clk 0:00:52.1]} 46. Rd8 {[%clk 0:00:23.4]} 46... Kf5 {[%clk 0:00:51.2]} 47. g4+ {[%clk 0:00:22.2]} 47... Kf4 {[%clk 0:00:49.1]} 48. h4 {[%clk 0:00:20.5]} 48... Kxg4 {[%clk 0:00:47.5]} 49. Rd4+ {[%clk 0:00:19.4]} 49... Kf3 {[%clk 0:00:44.7]} 50. h5 {[%clk 0:00:17.5]} 50... Ra6 {[%clk 0:00:41.5]} 51. h6 {[%clk 0:00:15.4]} 51... Rxh6+ {[%clk 0:00:37.6]} 52. Rh4 {[%clk 0:00:13.9]} 52... Rxh4+ {[%clk 0:00:34.9]} 53. Bxh4 {[%clk 0:00:12.8]} 1/2-1/2',  # noqa: E501, WPS323
        'rated': True,
        'rules': 'chess',
        'time_class': 'blitz',
        'time_control': '180',
        'url': 'https://www.chess.com/live/game/361066365',
        'white': {
            '@id': 'https://api.chess.com/pub/player/gaurav480',
            'rating': 1283,
            'result': 'insufficient',
            'username': 'GAURAV480',
        },
    }

    expected_result = {
        'game': {
            'event': 'Live Chess',
        },
    }

    assert map_data(
        input_data,
        config,
    ).unwrap() == expected_result
