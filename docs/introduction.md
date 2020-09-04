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

Congratulations, you've just mapped a default value to an attribute!

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

If statements are really useful for changing the values depending on some condition. Check the [list](../configuration/#if-statement) of supported conditions.

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

### Introducing Path to Iterable

We can use `path_to_iterable` on an `object` which works similar to `mapping.path`, but it applies the current `object` and all its attrbute mappings and nested objects to each and every element in whatever list `path_to_iterable` points to.

Lets solve the above example!

=== "config.json"

    ```json hl_lines="8 14 22 38"
    {
        "name": "root",
        "array": false,
        "objects": [
            {
                "name": "players",
                "array": true,
                "path_to_iterable": ["data", "character_data"],
                "attributes": [
                    {
                        "name": "nickname",
                        "mappings": [
                            {
                                "path": ["character_data", 0]
                            }
                        ]
                    },
                    {
                        "name": "class",
                        "mappings": [
                            {
                                "path": ["character_data", 1]
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
                                "path": ["character_data", 2]
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

Note that we still have to reference the key when mapping. The key name(`character_data`) is the last name in the list of `path_to_iterable`.

And thats it!

Congratulations the introduction course is done!

Time to map some data and have fun doing it!
