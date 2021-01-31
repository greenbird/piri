CSV is a very normal and quite convenient filetype used and supported by systems around the world.

CSV stands for Comma Seperated Values. But modern csv files can use any delimiter like `,`, `;` and `|` to mention a few where `;` is as far as our experience go, the most frequently used.

One other special thing about csv files is that they are quite similar to database tables. Each set of data has to be on one line. There are more complex csv files that are based on `row types`. We'll add examples for those later.

While its quite easy transform csv data into a flat json structure with python code. You will then still have to document your code. Piri solves this by giving you the configuration.json file to contractualise the mapping.


## Pre Processing
First since piri does not understand csv, we must use some code to turn the csv into a json list. You can use whatever you want, but heres a small example of how it can be done with python.

```csv
thomas;borgen;street123;1010;20-10-10;500
john;doe;street124;1011;20-10-11;6000
```

```python
import csv
import json

data = "thomas;borgen;street123;1010;20-10-10;500\njohn;doe;street124;1011;20-10-11;6000"
data_list = [row for row in csv.reader(data.split('\n'), delimiter=';')]

with open('json_data.json', 'w') as output_file:
    output_file.write(json.dumps({'data': data_list}))
```

The output of the above code looks like this
```json
{
    "data": [
        ["thomas", "borgen", "street123", "1010", "19-10-2020", "500"],
        ["john", "doe", "street124", "1011", "20-10-2020", "6000"],
    ]
}
```

## Mapping

What to keep in mind when working with CSV data is that we reference data by indexes of an array.

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
    ...
]
```

Then we'd use a configuration that you will see is structurally quite similar to the output that we want.

!!! Piri

    Run piri with the following `config.json` and `input.json` will produce `output.json`

    ```sh
    piri config.json data.json
    ```

    === "config.json"

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

    === "data.json"

        ```json
        {
            "data": [
                ["thomas", "borgen", "street123", "1010", "19-10-2020", "500"],
                ["john", "doe", "street124", "1011", "20-10-2020", "6000"],
            ]
        }
        ```

    === "output.json"

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
