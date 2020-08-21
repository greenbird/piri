The goal of this library is to make configurable data transformation(mapping) easy and flexible.

We have decided to only support json to json mapping. This is because quite frankly its impossible to have configurable mapping that works on any format. We chose json because its quite easy to make anything into json and its quite easy to make json into anything.

When we made this library we have dealt primarily with csv data or xml data.

example csv file could looks something like this:

```file
thomas;borgen;street123;1010;20-10-10;500
john;doe;street124;1011;20-10-11;6000
```
which would easily be turned in a json file looking like this:
```json
{
    "data": [
        ["thomas", "borgen", "street123", "1010", "19-10-2020", "500"],
        ["john", "doe", "street124", "1011", "20-10-2020", "6000"],
    ]
}
```

Lets say we want to map this into a structure like this

```json
[
    {
        "name": "firstname lastname",
        "address": {
            "street": "street",
            "zip": "zipcode"
        },
        "invoice": {
            "due_date": "isodate",
            "amount": 10.0
        }
    }
]
```

Then we'd use a configuration that you will see is structurally quite similar to the output that we want.

```json
{
    "name": "root",
    "array": true,
    "path_to_iterable": ["data"],
    "attributes": [
        {
            "name": "name",
            "mappings": [
                {
                    "path": ["data", 0]
                },
                {
                    "path": ["data", 1]
                }
            ],
            "separator": " "
        }
    ],
    "objects": [
        {
            "name": "address",
            "array": false,
            "attributes": [
                {
                    "name": "street",
                    "mappings": [
                        {
                            "path": ["data", 2]
                        }
                    ]
                },
                {
                    "name": "zip",
                    "mappings": [
                        {
                            "path": ["data", 3]
                        }
                    ]
                }
            ]
        },
        {
            "name": "invoice",
            "array": false,
            "attributes": [
                {
                    "name": "due_date",
                    "mappings": [
                        {
                            "path": ["data", 4]
                        }
                    ],
                    "casting": {
                        "to": "date",
                        "original_format": "dd.mm.yyyy"
                    }
                },
                {
                    "name": "amount",
                    "mappings": [
                        {
                            "path": ["data", 5]
                        }
                    ],
                    "casting": {
                        "to": "decimal"
                    }
                }
            ]
        }
    ]
}
```

which will produce

```json
[
    {
        "name": "thomas borgen",
        "address": {
            "street": "street123",
            "zip": "1010"
        },
        "invoice": {
            "due_date": "2020-10-20",
            "amount": 500.0
        }
    },
    {
        "name": "john doe",
        "address": {
            "street": "street124",
            "zip": "1011"
        },
        "invoice": {
            "due_date": "2020-10-19",
            "amount": 6000.0
        }
    }
]
```
