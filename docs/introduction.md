Piri uses a configuration file to govern output structure and contents. This section is the introductionary course to Piri.


## The setup

For this introduction course we will use [piri-cli](https://github.com/greenbird/piri-cli) since it provides you with a simple command line tool to run piri. And no need to create any python files.

Install with pip:
```sh
pip install piri-cli
```

All examples will have a config, input and output json tab like this:

=== "config.json"
    ```json
    {}
    ```
=== "input.json"
    ```json
    {}
    ```
=== "output.json"
    ```json
    {}
    ```

Copy the contents of config.json and input.json down to your working dir.

Run all examples with the following unless otherwise stated.
```sh
piri config.json input.json
```



## About JSON

Json is a human readable data format that stores data in objects consisting of attribute-value pairs and arrays. We will use the terms `object` and `attribute` quite often in this guide. To put it simply an __object__ contains __attributes__ that hold __values__. These values can sometimes be another object or even an array of objects.

```json
{
    "person": {
        "name": "Bob",
        "height": 180.5,
        "friends": [
            {
                "name": "John",
                "height": 170.5
            }
        ]
    }
}
```
`person` is an __object__, `name` and `height` are __attribtes__, `"Bob"` and `180.5` are __values__ to those attributes. `friends` is a list(array) of objects.


## The Root

The root of all ev... piri configs looks like this

```json
{
    "name": "root",
    "array": false,
    "attributes": [],
    "objects": []
}
```

So this will fail since we consider empty result a failure, but this config generates the enclosing {} brackets you can see in the example in the About JSON section.
```json
{}
```

## Adding Attributes to root

To actually map some data we can add `attributes`.

=== "config.json"

    ```json
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "firstname",
                "default": "Thomas"
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {}
    ```

=== "output.json"

    ```json
    {
        "firstname": "Thomas"
    }
    ```

Congratulations, you've just mapped a default value to an attribute! - Click `output.json` tab to see the output.

## Structuring with objects

=== "config.json"

    ```json
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "person",
                "array": false,
                "attributes": [
                    {
                        "name": "firstname",
                        "default": "Thomas"
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {}
    ```

=== "output.json"

    ```json hl_lines="2"
    {
        "person": {
            "firstname": "Thomas"
        }
    }
    ```

What we just did is the core principle of creating the output structure. We added an object with the name `person`, then we moved our `firstname` attribute to the `person` object.


## Time to Map some values!

We will now introduce the `mappings` key, it's and array of `mapping` objects.

The `mapping` object is the only place where you actually fetch data from the input. And you do that by specifying a `path`. The `path` describes the steps to take to get to the value we are interested in.

### Mapping.path with flat structure

=== "config.json"

    ```json hl_lines="13"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "person",
                "array": false,
                "attributes": [
                    {
                        "name": "firstname",
                        "mappings": [
                            {
                                "path": ["name"]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "name": "Neo"
    }
    ```

=== "output.json"

    ```json hl_lines="3"
    {
        "person": {
            "firstname": "Neo"
        }
    }

    ```


### Mapping.path with nested structure

=== "config.json"

    ```json hl_lines="6 12 13 14"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "actor",
                "array": false,
                "attributes": [
                    {
                        "name": "name",
                        "mappings": [
                            {
                                "path": ["the_matrix", "neo", "actor", "name"]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "the_matrix": {
            "neo": {
                "actor": {
                    "name": "Keanu Reeves"
                }
            }
        }
    }
    ```

=== "output.json"

    ```json hl_lines="3"
    {
        "actor": {
            "name": "Keanu Reeves"
        }
    }
    ```


### Mapping.path with data in lists

Consider the following json:
```json
{
    "data": ["Keanu", "Reeves", "The Matrix"]
}
```

In our `mapping` object we supply `path` which is a list of how we get to our data. So how do we get the `lastname` in that data?

Easy, we reference the `index` of the list. The first data in the list starts at `0`, second element `1`, third `2` and so on. This number is the `index` and to get the last name we must use the index: `1`

=== "config.json"

    ```json hl_lines="9 17"
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "firstname",
                "mappings": [
                    {
                        "path": ["data", 0]
                    }
                ]
            },
            {
                "name": "lastname",
                "mappings": [
                    {
                        "path": ["data", 1]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "data": ["Keanu", "Reeves", "The Matrix"]
    }
    ```

=== "output.json"

    ```json hl_lines="3"
    {
        "firstname": "Keanu",
        "lastname": "Reeves"
    }
    ```

!!! Note
    We still have to reference the `"data"` key first, so our `path` goes first to `data` then it finds the value at index `1`


### Mapping.path to list values and objects

Consider the following json:
```json
{
    "name": "neo",
    "in_movies": [1, 2, 3, 4]
}
```

When we are actually interested in keeping the array in the output then we can simply supply the path to the list and it'll be outputted as is.
This works for objects aswell.

=== "config.json"

    ```json hl_lines="9 17"
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "character",
                "mappings": [
                    {
                        "path": ["name"]
                    }
                ]
            },
            {
                "name": "plays_in_movies",
                "mappings": [
                    {
                        "path": ["in_movies"]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "name": "neo",
        "in_movies": [1, 2, 3, 4]
    }
    ```

=== "output.json"

    ```json hl_lines="3"
    {
        "character": "neo",
        "plays_in_movies": [
            1,
            2,
            3,
            4
        ]
    }
    ```

!!! Note
    When mapping objects and arrays values some other functionality like `casting` obviously won't work.

## Combining values

Now lets learn how to combine values from multiple places in the input.

It's fairly normal to only need `name` but getting `firstname` _and_ `lastname` in input data. Lets combine them!

=== "config.json"

    ```json hl_lines="15 16 17 19"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "actor",
                "array": false,
                "attributes": [
                    {
                        "name": "name",
                        "mappings": [
                            {
                                "path": ["the_matrix", "neo", "actor", "firstname"]
                            },
                            {
                                "path": ["the_matrix", "neo", "actor", "lastname"]
                            }
                        ],
                        "separator": " ",
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json hl_lines="5 6"
    {
        "the_matrix": {
            "neo": {
                "actor": {
                    "firstname": "Keanu",
                    "lastname": "Reeves"
                }
            }
        }
    }
    ```

=== "output.json"

    ```json hl_lines="3"
    {
        "actor": {
            "name": "Keanu Reeves"
        }
    }
    ```


To find more values and combine them, simply add another `mapping` object to `mappings` array.

Use `separator` to control with what char values should be separated.

## Regexp

You can use Regexp to find patterns in a given string and retrieve them as a string or as an array of strings.

### Regexp Example

Let's say you want to analyze your chess games, you get JSON with data BUT the fun part is inside `pgn` field, so let's retrieve Event, Site, Result, ECO and the game moves from `pgn` using Regexp.

=== "config.json"

    ```json hl_lines="19 20 21"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "game",
                "array": false,
                "attributes": [
                    {
                        "name": "event",
                        "mappings": [
                            {
                                    "path": ["pgn"],
                                    "regexp": {
                                        "search": "Event \\\"[\\w\\d ]+\\\""
                                    },
                                    "slicing": {
                                        "from": 7,
                                        "to": -1
                                    }
                            }
                        ]
                    },
                    {
                        "name": "site",
                        "mappings": [
                            {
                                "path": ["pgn"],
                                "regexp": {
                                    "search": "Site \\\"[\\w\\d. ]+\\\""
                                },
                                "slicing": {
                                    "from": 6,
                                    "to": -1
                                }
                            }
                        ]
                    },
                    {
                        "name": "result",
                        "mappings": [
                            {
                                "path": ["pgn"],
                                "regexp": {
                                    "search": "Result \\\"[\\w\\d\/ -]+\\\""
                                },
                                "slicing": {
                                    "from": 8,
                                    "to": -1
                                }
                            }
                        ]
                    },
                    {
                        "name": "eco",
                        "mappings": [
                            {
                                "path": ["pgn"],
                                "regexp": {
                                    "search": "ECO \\\"[\\w\\d ]+\\\""
                                },
                                "slicing": {
                                    "from": 5,
                                    "to": -1
                                }
                            }
                        ]
                    },
                    {
                        "name": "moves",
                        "mappings": [
                            {
                                "path": ["pgn"],
                                "regexp": {
                                    "search": "\\s1\\..*"
                                },
                                "slicing": {
                                    "from": 1
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "black": {
            "@id": "https://api.chess.com/pub/player/chameleoniasa",
            "rating": 1273,
            "result": "insufficient",
            "username": "ChameleonIASA"
        },
        "end_time": 1347534562,
        "fen": "8/8/8/8/7B/5k2/7K/8 b - -",
        "pgn": "[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2012.09.13\"]\n[Round \"-\"]\n[White \"GAURAV480\"]\n[Black \"ChameleonIASA\"]\n[Result \"1/2-1/2\"]\n[ECO \"A00\"]\n[ECOUrl \"https://www.chess.com/openings/Saragossa-Opening\"]\n[CurrentPosition \"8/8/8/8/7B/5k2/7K/8 b - -\"]\n[Timezone \"UTC\"]\n[UTCDate \"2012.09.13\"]\n[UTCTime \"11:03:43\"]\n[WhiteElo \"1283\"]\n[BlackElo \"1273\"]\n[TimeControl \"180\"]\n[Termination \"Game drawn by insufficient material\"]\n[StartTime \"11:03:43\"]\n[EndDate \"2012.09.13\"]\n[EndTime \"11:09:22\"]\n[Link \"https://www.chess.com/live/game/361066365\"]\n\n1. c3 {[%clk 0:03:00]} 1... e6 {[%clk 0:03:00]} 2. Qb3 {[%clk 0:02:57.1]} 2... Ne7 {[%clk 0:02:58.4]} 3. Nf3 {[%clk 0:02:47.7]} 3... d5 {[%clk 0:02:57.9]} 4. e3 {[%clk 0:02:45.6]} 4... Nd7 {[%clk 0:02:57.3]} 5. Be2 {[%clk 0:02:42.3]} 5... a6 {[%clk 0:02:56.9]} 6. O-O {[%clk 0:02:36.6]} 6... b5 {[%clk 0:02:56.3]} 7. d4 {[%clk 0:02:35.1]} 7... Bb7 {[%clk 0:02:55.7]} 8. Qc2 {[%clk 0:02:28.4]} 8... g6 {[%clk 0:02:55.3]} 9. Nbd2 {[%clk 0:02:25.4]} 9... Bg7 {[%clk 0:02:54.6]} 10. Nb3 {[%clk 0:02:23.6]} 10... c6 {[%clk 0:02:54.2]} 11. a3 {[%clk 0:02:21.3]} 11... a5 {[%clk 0:02:52]} 12. a4 {[%clk 0:02:17.9]} 12... bxa4 {[%clk 0:02:49.7]} 13. Rxa4 {[%clk 0:02:16.2]} 13... Nb6 {[%clk 0:02:45.5]} 14. Rxa5 {[%clk 0:02:12.4]} 14... Rxa5 {[%clk 0:02:43.9]} 15. Nxa5 {[%clk 0:02:11.4]} 15... Nc4 {[%clk 0:02:40.4]} 16. Nxb7 {[%clk 0:02:07.8]} 16... Qb6 {[%clk 0:02:36.9]} 17. Bxc4 {[%clk 0:01:59.4]} 17... dxc4 {[%clk 0:02:34.1]} 18. Nd6+ {[%clk 0:01:58.1]} 18... Kd7 {[%clk 0:02:30.1]} 19. Nxc4 {[%clk 0:01:55.2]} 19... Qa6 {[%clk 0:02:28.6]} 20. b4 {[%clk 0:01:49.9]} 20... Ra8 {[%clk 0:02:24.4]} 21. Qd3 {[%clk 0:01:45]} 21... Nd5 {[%clk 0:02:14.7]} 22. Nce5+ {[%clk 0:01:42.2]} 22... Bxe5 {[%clk 0:02:12.2]} 23. Nxe5+ {[%clk 0:01:37.6]} 23... Ke7 {[%clk 0:02:11.1]} 24. Qxa6 {[%clk 0:01:34.8]} 24... Rxa6 {[%clk 0:02:08.5]} 25. c4 {[%clk 0:01:32.9]} 25... Nxb4 {[%clk 0:02:05]} 26. Bd2 {[%clk 0:01:32]} 26... Nc2 {[%clk 0:01:59.5]} 27. h3 {[%clk 0:01:30.3]} 27... Kf6 {[%clk 0:01:55.7]} 28. Rb1 {[%clk 0:01:28.2]} 28... c5 {[%clk 0:01:43.9]} 29. dxc5 {[%clk 0:01:26.3]} 29... Kxe5 {[%clk 0:01:41.1]} 30. Bc3+ {[%clk 0:01:22.3]} 30... Ke4 {[%clk 0:01:39.6]} 31. Rb7 {[%clk 0:01:16.4]} 31... Kd3 {[%clk 0:01:37.9]} 32. Be5 {[%clk 0:01:11.9]} 32... Kxc4 {[%clk 0:01:35.7]} 33. Rxf7 {[%clk 0:01:07.8]} 33... Kxc5 {[%clk 0:01:34.2]} 34. Rxh7 {[%clk 0:01:06.7]} 34... Kd5 {[%clk 0:01:32.4]} 35. Bg3 {[%clk 0:01:03.4]} 35... Ra1+ {[%clk 0:01:28.5]} 36. Kh2 {[%clk 0:00:59.9]} 36... e5 {[%clk 0:01:24.4]} 37. Rh6 {[%clk 0:00:55.1]} 37... g5 {[%clk 0:01:21.8]} 38. Rh5 {[%clk 0:00:52.4]} 38... Ke4 {[%clk 0:01:17.7]} 39. Rxg5 {[%clk 0:00:51.4]} 39... Nb4 {[%clk 0:01:11.7]} 40. Rxe5+ {[%clk 0:00:48.3]} 40... Kd3 {[%clk 0:01:09.9]} 41. Rb5 {[%clk 0:00:44.8]} 41... Kc4 {[%clk 0:01:06.8]} 42. Rb8 {[%clk 0:00:39.9]} 42... Nd3 {[%clk 0:01:02.3]} 43. e4 {[%clk 0:00:35.4]} 43... Kd4 {[%clk 0:00:58.8]} 44. e5 {[%clk 0:00:33.6]} 44... Nxf2 {[%clk 0:00:53]} 45. Bxf2+ {[%clk 0:00:31]} 45... Kxe5 {[%clk 0:00:52.1]} 46. Rd8 {[%clk 0:00:23.4]} 46... Kf5 {[%clk 0:00:51.2]} 47. g4+ {[%clk 0:00:22.2]} 47... Kf4 {[%clk 0:00:49.1]} 48. h4 {[%clk 0:00:20.5]} 48... Kxg4 {[%clk 0:00:47.5]} 49. Rd4+ {[%clk 0:00:19.4]} 49... Kf3 {[%clk 0:00:44.7]} 50. h5 {[%clk 0:00:17.5]} 50... Ra6 {[%clk 0:00:41.5]} 51. h6 {[%clk 0:00:15.4]} 51... Rxh6+ {[%clk 0:00:37.6]} 52. Rh4 {[%clk 0:00:13.9]} 52... Rxh4+ {[%clk 0:00:34.9]} 53. Bxh4 {[%clk 0:00:12.8]} 1/2-1/2",
        "rated": true,
        "rules": "chess",
        "time_class": "blitz",
        "time_control": "180",
        "url": "https://www.chess.com/live/game/361066365",
        "white": {
            "@id": "https://api.chess.com/pub/player/gaurav480",
            "rating": 1283,
            "result": "insufficient",
            "username": "GAURAV480"
        }
    }
    ```

=== "output.json"

    ```json
    {
        "game": {
            "event": "Live Chess",
            "site": "Chess.com",
            "result": "1/2-1/2",
            "eco": "A00",
            "moves": "1. c3 {[%clk 0:03:00]} 1... e6 {[%clk 0:03:00]} 2. Qb3 {[%clk 0:02:57.1]} 2... Ne7 {[%clk 0:02:58.4]} 3. Nf3 {[%clk 0:02:47.7]} 3... d5 {[%clk 0:02:57.9]} 4. e3 {[%clk 0:02:45.6]} 4... Nd7 {[%clk 0:02:57.3]} 5. Be2 {[%clk 0:02:42.3]} 5... a6 {[%clk 0:02:56.9]} 6. O-O {[%clk 0:02:36.6]} 6... b5 {[%clk 0:02:56.3]} 7. d4 {[%clk 0:02:35.1]} 7... Bb7 {[%clk 0:02:55.7]} 8. Qc2 {[%clk 0:02:28.4]} 8... g6 {[%clk 0:02:55.3]} 9. Nbd2 {[%clk 0:02:25.4]} 9... Bg7 {[%clk 0:02:54.6]} 10. Nb3 {[%clk 0:02:23.6]} 10... c6 {[%clk 0:02:54.2]} 11. a3 {[%clk 0:02:21.3]} 11... a5 {[%clk 0:02:52]} 12. a4 {[%clk 0:02:17.9]} 12... bxa4 {[%clk 0:02:49.7]} 13. Rxa4 {[%clk 0:02:16.2]} 13... Nb6 {[%clk 0:02:45.5]} 14. Rxa5 {[%clk 0:02:12.4]} 14... Rxa5 {[%clk 0:02:43.9]} 15. Nxa5 {[%clk 0:02:11.4]} 15... Nc4 {[%clk 0:02:40.4]} 16. Nxb7 {[%clk 0:02:07.8]} 16... Qb6 {[%clk 0:02:36.9]} 17. Bxc4 {[%clk 0:01:59.4]} 17... dxc4 {[%clk 0:02:34.1]} 18. Nd6+ {[%clk 0:01:58.1]} 18... Kd7 {[%clk 0:02:30.1]} 19. Nxc4 {[%clk 0:01:55.2]} 19... Qa6 {[%clk 0:02:28.6]} 20. b4 {[%clk 0:01:49.9]} 20... Ra8 {[%clk 0:02:24.4]} 21. Qd3 {[%clk 0:01:45]} 21... Nd5 {[%clk 0:02:14.7]} 22. Nce5+ {[%clk 0:01:42.2]} 22... Bxe5 {[%clk 0:02:12.2]} 23. Nxe5+ {[%clk 0:01:37.6]} 23... Ke7 {[%clk 0:02:11.1]} 24. Qxa6 {[%clk 0:01:34.8]} 24... Rxa6 {[%clk 0:02:08.5]} 25. c4 {[%clk 0:01:32.9]} 25... Nxb4 {[%clk 0:02:05]} 26. Bd2 {[%clk 0:01:32]} 26... Nc2 {[%clk 0:01:59.5]} 27. h3 {[%clk 0:01:30.3]} 27... Kf6 {[%clk 0:01:55.7]} 28. Rb1 {[%clk 0:01:28.2]} 28... c5 {[%clk 0:01:43.9]} 29. dxc5 {[%clk 0:01:26.3]} 29... Kxe5 {[%clk 0:01:41.1]} 30. Bc3+ {[%clk 0:01:22.3]} 30... Ke4 {[%clk 0:01:39.6]} 31. Rb7 {[%clk 0:01:16.4]} 31... Kd3 {[%clk 0:01:37.9]} 32. Be5 {[%clk 0:01:11.9]} 32... Kxc4 {[%clk 0:01:35.7]} 33. Rxf7 {[%clk 0:01:07.8]} 33... Kxc5 {[%clk 0:01:34.2]} 34. Rxh7 {[%clk 0:01:06.7]} 34... Kd5 {[%clk 0:01:32.4]} 35. Bg3 {[%clk 0:01:03.4]} 35... Ra1+ {[%clk 0:01:28.5]} 36. Kh2 {[%clk 0:00:59.9]} 36... e5 {[%clk 0:01:24.4]} 37. Rh6 {[%clk 0:00:55.1]} 37... g5 {[%clk 0:01:21.8]} 38. Rh5 {[%clk 0:00:52.4]} 38... Ke4 {[%clk 0:01:17.7]} 39. Rxg5 {[%clk 0:00:51.4]} 39... Nb4 {[%clk 0:01:11.7]} 40. Rxe5+ {[%clk 0:00:48.3]} 40... Kd3 {[%clk 0:01:09.9]} 41. Rb5 {[%clk 0:00:44.8]} 41... Kc4 {[%clk 0:01:06.8]} 42. Rb8 {[%clk 0:00:39.9]} 42... Nd3 {[%clk 0:01:02.3]} 43. e4 {[%clk 0:00:35.4]} 43... Kd4 {[%clk 0:00:58.8]} 44. e5 {[%clk 0:00:33.6]} 44... Nxf2 {[%clk 0:00:53]} 45. Bxf2+ {[%clk 0:00:31]} 45... Kxe5 {[%clk 0:00:52.1]} 46. Rd8 {[%clk 0:00:23.4]} 46... Kf5 {[%clk 0:00:51.2]} 47. g4+ {[%clk 0:00:22.2]} 47... Kf4 {[%clk 0:00:49.1]} 48. h4 {[%clk 0:00:20.5]} 48... Kxg4 {[%clk 0:00:47.5]} 49. Rd4+ {[%clk 0:00:19.4]} 49... Kf3 {[%clk 0:00:44.7]} 50. h5 {[%clk 0:00:17.5]} 50... Ra6 {[%clk 0:00:41.5]} 51. h6 {[%clk 0:00:15.4]} 51... Rxh6+ {[%clk 0:00:37.6]} 52. Rh4 {[%clk 0:00:13.9]} 52... Rxh4+ {[%clk 0:00:34.9]} 53. Bxh4 {[%clk 0:00:12.8]} 1/2-1/2"
        }
    }
    ```


!!! Hint
    If you have doubts about your regexp expressions, check them out on: [Regex 101](https://regex101.com/). Also, make sure that your JSON is valid as Regexp may require extra escape slashes.

## Slicing

You can use slicing to cut values at value[from:to] which is very useful when you are only interested in part of a value. The value is turned into a string with `str()` before slicing is applied.

### String slice

Lets say that we have some value like this `street-Santas Polar city 45`. We would really like to filter away the `street-` part of that value. And that is exactly what Slicing is for.

=== "config.json"

    ```json hl_lines="19 20 21"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "fantasy",
                "array": true,
                "path_to_iterable": ["data"],
                "attributes": [
                    {
                        "name": "name",
                        "mappings": [{"path": ["data", 0]}]
                    },
                    {
                        "name": "street",
                        "mappings": [
                            {
                                "path": ["data", 1],
                                "slicing": {
                                    "from": 7
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "data": [
            ["santa", "street-Santas Polar city 45"],
            ["unicorn", "street-Fluffy St. 40"]
        ]
    }
    ```

=== "output.json"

    ```json hl_lines="5 9"
    {
        "fantasy": [
            {
                "name": "santa",
                "street": "Santas Polar city 45"
            },
            {
                "name": "unicorn",
                "street": "Fluffy St. 40"
            }
        ]
    }
    ```

!!! Hint
    If you have some max length on a database table, then you can use string slicing to make sure the length does not exceed a certain length with the `to` key. Some databases also has for example two address fields for when the length of one is too short. Then map both with slicing `"from" :0, "to": 50` and `"from": 50, "to": null` respectively and you'll solve the problem.


### Slicing numbers and casting

You can also slice numbers, bools and any other json value since we cast the value to string first. This means that if you for example get a social security number but is only interested in the `date` part of it, you can slice it. And then even cast the value to a `date`.

`2020123112345` -> `"20201231"` -> `"2020-12-31"`

=== "config.json"

    ```json hl_lines="19 20 21 22 25 26 27 28"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "fantasy",
                "array": true,
                "path_to_iterable": ["data"],
                "attributes": [
                    {
                        "name": "name",
                        "mappings": [{"path": ["data", 0]}]
                    },
                    {
                        "name": "birthday",
                        "mappings": [
                            {
                                "path": ["data", 1],
                                "slicing": {
                                    "from": 0,
                                    "to": 8
                                }
                            }
                        ],
                        "casting": {
                            "to": "date",
                            "original_format": "yyyymmdd"
                        }
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "data": [
            ["santa", 2020123112345],
            ["unicorn", 1991123012346]
        ]
    }
    ```

=== "output.json"

    ```json hl_lines="5 9"
    {
        "fantasy": [
            {
                "name": "santa",
                "birthday": "2020-12-31"
            },
            {
                "name": "unicorn",
                "birthday": "1991-12-30"
            }
        ]
    }
    ```

!!! Hint
    If you need to take values from end of string, like the 5 last characters, then you can use a negative `from` value to count from the end instead. This works just like [pythons slicing functionality.](https://stackoverflow.com/a/509295)


## If statements

Are useful for when you for example get some numbers in your data that are supposed to represent different types.


### Simple if statement

Let's check if the value equals `1` and output `type_one`.

=== "config.json"

    ```json hl_lines="10 11 12 13 14 15 16"
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "readable_type",
                "mappings": [
                    {
                        "path": ["type"],
                        "if_statements": [
                            {
                                "condition": "is",
                                "target": "1",
                                "then": "type_one"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json hl_lines="5 6"
    {
        "type": "1"
    }
    ```

=== "output.json"

    ```json hl_lines="3"
    {
        "readable_type": "type_one"
    }
    ```

If statements are really useful for changing the values depending on some condition. [Check the list of supported conditions](../configuration/#if-statement).

`otherwise` can also be used to specify should happen if the condition is `false`. If `otherwise` is not provided then output will be the original value.

### Chain If Statements

`if_statements` is a list of `if statement` objects. We designed it like this so that we can chain them. The output of the first one will be the input of the next one.

the `mapping` object is not the only one that can have if statements, the `attribute` can also have them. This allows for some interesting combinations.

=== "config.json"

    ```json hl_lines="14 20 25 32 35"
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "readable_type",
                "mappings": [
                    {
                        "path": ["type"],
                        "if_statements": [
                            {
                                "condition": "is",
                                "target": "1",
                                "then": "boring-type"
                            },
                            {
                                "condition": "is",
                                "target": "2",
                                "then": "boring-type-two",
                                "otherwise": "fun-type"
                            },
                            {
                                "condition": "contains",
                                "target": "fun",
                                "then": "funky_type"
                            }
                        ]
                    }
                ],
                "if_statements": [
                    {
                        "condition": "not",
                        "target": "funky_type",
                        "then": "junk",
                        "otherwise": "funk"
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "type": "1"
    }
    ```

=== "output.json"
    ```json
    {
        "readable_type": "funk"
    }
    ```

=== "input2.json"

    ```json
    {
        "type": "2"
    }
    ```

=== "output2.json"

    ```json
    {
        "readable_type": "junk"
    }
    ```

Using input.json the places that are highlighted is everywhere the value changes.

For input2.json the first if statement is false and no value change. The second if statement is true so value is changed to `boring-type-two`. The third if statement is false so no value change. The last if statement checks if the value is `not` `funky_type` which is true, so the value is changed to `junk`.

You can even add if statements for every `mapping` object you add into `mappings` so this can handle some quite complicated condition with multiple values.

!!! Note
    If statements on `array` and `object` values behave a bit differently. Have a look in the [configuration](../configuration)

## Casting values

You've learned how to structure your output with objects, find values and asigning them to attributes, combining values and applying if statements. Its now time to learn how to cast values.

Casting values is very useful for when we get string(text) data that should be numbers. Or when you get badly(non-iso) formatted date values that you want to change to ISO dates

Casting is straightforward. You map your value like you would and then add the casting object.

### Casting to decimal

=== "config.json"

    ```json hl_lines="12 13 14"
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "my_number",
                "mappings": [
                    {
                        "path": ["string_number"]
                    }
                ],
                "casting": {
                    "to": "decimal"
                }
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "string_number": "123.12"
    }
    ```

=== "output.json"

    ```json
    {
        "my_number": 123.12
    }
    ```

### Casting to ISO Date

When casting to a `date` we always have to supply the `original_format` which is the format that the input data is on. without knowing this there would be know way to know fore sure in every case if it was dd.mm.yy or yy.mm.dd

=== "config.json"

    ```json hl_lines="12 13 14"
    {
        "name": "root",
        "array": false,
        "attributes": [
            {
                "name": "my_iso_date",
                "mappings": [
                    {
                        "path": ["yymmdd_date"]
                    }
                ],
                "casting": {
                    "to": "date",
                    "original_format": "yymmdd"
                }
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "yymmdd_date": "101020"
    }
    ```

=== "output.json"

    ```json
    {
        "my_iso_date": "2010-10-20"
    }
    ```


Check our the [configuration docs on casting](../configuration#casting-object) for more info

## Working with lists

Finally! Last topic and the most interesting one!

Usually the data that you are processing is not one thing, but a list of things(data). We want to iterate the list and for each and every piece of data in that list we want to transform it. This is the section that lets you do that.

Lets say we are creating a website for an RPG game that dumps its data in a flat format. Every line is a player with a `name`, `class`, `money`, and `x`, `y` coordinates for where he is in the world.

=== "data.json"

    ```json
    {
        "data": {
            "something_uninteresting": [1, 2, 3],
            "character_data": [
                ["SuperAwesomeNick", 1, 500],
                ["OtherAwesomeDude", 2, 300],
                ["PoorDude", 2, 10]
            ]
        }
    }
    ```

Now to make the frontend dudes happy we would liketo structure this nicely... something like:

```json
{
    "players": [
        {
            "nickname": "SuperAwesomeNick",
            "class": "warrior",
            "gold": 500,
        },
        {
            "nickname": "OtherAwesomeDude",
            ...
        }
    ]
}
```

### Introducing Iterables

We can use `iterables` on an `object` which works similar to `mapping.path`, but it applies the current `object` and all its attribute mappings and nested objects to each and every element in whatever list `iterables` points to.

Lets solve the above example!

=== "config.json"

    ```json hl_lines="8 9 10 11 12 13 19 27 43"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "players",
                "array": true,
                "iterables": [
                    {
                        "alias": "character",
                        "path": ["data", "character_data"],
                    }
                ],
                "attributes": [
                    {
                        "name": "nickname",
                        "mappings": [
                            {
                                "path": ["character", 0]
                            }
                        ]
                    },
                    {
                        "name": "class",
                        "mappings": [
                            {
                                "path": ["character", 1]
                            }
                        ],
                        "if_statements": [
                            {
                                "condition": "is",
                                "target": 1,
                                "then": "warrior",
                                "otherwise": "cleric"
                            }
                        ]
                    },
                    {
                        "name": "gold",
                        "mappings": [
                            {
                                "path": ["character", 2]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "data": {
            "something_uninteresting": [1, 2, 3],
            "character_data": [
                ["SuperAwesomeNick", 1, 500],
                ["OtherAwesomeDude", 2, 300],
                ["PoorDude", 2, 10]
            ]
        }
    }
    ```

=== "output.json"

    ```json
    {
        "players": [
            {
                "nickname": "SuperAwesomeNick",
                "class": "warrior",
                "gold": 500
            },
            {
                "nickname": "OtherAwesomeDude",
                "class": "cleric",
                "gold": 300
            },
            {
                "nickname": "PoorDude",
                "class": "cleric",
                "gold": 10
            }
        ]
    }
    ```


`iterables` is an array of `iterable` objects that _must_ contain an `alias` and a `path`. `alias` is will be the name of the `key` that you will then be able to reference and `path` is the path to the iterable list/array in the input data.

!!! Note
    In our mappings.path we reference the key name(`character`) which is the `alias` we set up. Behind the scenes what really happens is that we add this `character` key to the root input data and run mapping for each val/obj in the list. Its completely name the `alias` the same as the last key to the iterable. This is demonstrated in the next example.

    This means that you must be sure to use unique aliases since otherwise you will overwrite other data.

### Iterables Continued

So you think that was cool? Well, we can have as many as we want.

consider the following input:

```json hl_lines="2 4 6 15 17"
{
    "data": [
        {
            "nested": [
                {
                    "another": [
                        {"a": "a"},
                        {"a": "b"}
                    ],
                    "name": "nested1"
                }
            ]
        },
        {
            "nested": [
                {
                    "another": [
                        {"a": "c"},
                        {"a": "d"}
                    ],
                    "name": "nested2"
                }
            ]
        }
    ]
}
```

Theres 3 levels of lists. But lets say we want to flatten this structure. Then we will have to get all combinations of `data.nested.another.a` = `a`, `b`, `c` and `d`.

Well its easy, first we just add iterables to `"data"`, then we must iterate `"nested"`, then we must iterate `"another"`.


=== "config.json"

    ```json
    {
        "name": "root",
        "array": true,
        "iterables": [
            {
                "alias": "data",
                "path": ["data"]
            },
            {
                "alias": "nested",
                "path": ["data", "nested"]
            },
            {
                "alias": "another",
                "path": ["nested", "another"]
            }
        ],
        "attributes": [
            {
                "name": "nested_name",
                "mappings": [
                    {
                        "path": ["nested", "name"]
                    }
                ]
            },
            {
                "name": "value_of_a",
                "mappings": [
                    {
                        "path": ["another", "a"]
                    }
                ]
            }
        ]
    }
    ```

=== "input.json"

    ```json
    {
        "data": [
            {
                "nested": [
                    {
                        "another": [
                            {"a": "a"},
                            {"a": "b"}
                        ],
                        "name": "nested1"
                    }
                ]
            },
            {
                "nested": [
                    {
                        "another": [
                            {"a": "c"},
                            {"a": "d"}
                        ],
                        "name": "nested2"
                    }
                ]
            }
        ]
    }
    ```

=== "output.json"

    ```json hl_lines="4 8 12 16"
    [
        {
            "nested_name": "nested1",
            "value_of_a": "a"
        },
        {
            "nested_name": "nested1",
            "value_of_a": "b"
        },
        {
            "nested_name": "nested2",
            "value_of_a": "c"
        },
        {
            "nested_name": "nested2",
            "value_of_a": "d"
        }
    ]
    ```


We will write a more in depth explanation of iterables and how they work internally. [Link to the issue](https://github.com/greenbird/piri/issues/113)


And thats it!

Congratulations the introduction course is done!

Time to map some data and have fun doing it!

Have a look in [usecases](../usecases/usecases) section for some quick starts and tutorials
