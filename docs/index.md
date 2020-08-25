# Piri
Configurable Data Mapping for mortals
___
![test](https://github.com/greenbird/piri/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/greenbird/piri/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/piri)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
___


## Goal

The goal of this library is to make JSON to JSON transformation/mapping configurable. We achieve this by using a simple but feature-rich JSON configuration which then also acts as a contract.

## Features

* Mapping with configuration File.
* Transforms JSON
* Combine multiple values to one.
* Default values
* If statements
    * is, contains, not
* casting
    * integer, decimal, iso date

## Contributing
Please see [contribute](../contributing)

## Installation

!!! info
    Package is on pypi. Use pip or poetry to install

```sh
pip install piri
```
```sh
poetry add piri
```

## Quickstart
```python
import simplejson

from piri.mapper import map_data

my_config = {
    'name': 'schema',
    'array': False,
    'objects': [
        {
            'name': 'invoices',
            'array': True,
            'path_to_iterable': ['root', 'invoices'],
            'attributes': [
                {
                    'name': 'amount',
                    'mappings': [
                        {
                            'path': ['invoices', 'amount'],
                        },
                    ],
                    'casting': {
                        'to': 'decimal',
                        'original_format': 'integer_containing_decimals',
                    },
                    'default': 0,
                },
                {
                    'name': 'debtor',
                    'mappings': [
                        {
                            'path': ['root', 'customer', 'first_name'],
                        },
                        {
                            'path': ['root', 'customer', 'last_name'],
                        },
                    ],
                    'separator': ' ',
                },
            ],
            'objects': [],
        },
    ],
}

example_data = {
    'root': {
        'customer': {
            'first_name': 'John',
            'last_name': 'Smith',
        },
        'invoices': [
            {
                'amount': 10050,
            },
            {
                'amount': 20050,
            },
            {
                'amount': -15005,
            },
        ],
    },
}

mapped_data = map_data(example_data, my_config)

with open('resultfile.json', 'w') as output_file:
    output_file.write(simplejson.dumps(mapped_data.unwrap()))

```

contents of resultfile.json
```json
{
    "invoices": [
        {
            "amount": 100.5,
            "debtor": "John Smith"
        },
        {
            "amount": 200.5,
            "debtor": "John Smith"
        },
        {
            "amount": -150.05,
            "debtor": "John Smith"
        }
    ]
}
```

# Process

The Process function tries to make it easy to run all steps in order. Since its a callable object then dependencies(functions) can be changed before calling. This is the execution order:

* validate configuration data
  * configuration must be valid and also we apply some output formatting to the configuration data.
* run pre processing
  * a pre_process function can be supplied that must change raw data to python dictionary if it isn't already
* map data
  * run mapping function with the validated configuration and pre_processed data.
  * this outputs a dictionary
* validate and marshall
  * this loads the mapping result into a marshmallow Schema that will validate the data for us. after that it will return the dump(marshall) of the schema that can apply any output formatting rules needed.
  * this is the only function that is required to provide when process is initiated.
* create output
  * run provided output function.
  * if none is provided it simply returns the dictionary.
  * to provide an output function simply add it while initiating Process. with the argument \_output=function. The function must receive dictionary and can return anything
