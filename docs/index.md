# Piri
Configurable Data Mapping for mortals
___
![test](https://github.com/greenbird/piri/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/greenbird/piri/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/piri)
[![Python Version](https://img.shields.io/pypi/pyversions/piri.svg)](https://pypi.org/project/piri/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
___

**[Documentation](https://greenbird.github.io/piri/) |
[Source Code](https://github.com/greenbird/piri) |
[Task Tracker](https://github.com/greenbird/piri/issues)**

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

from piri.process import process

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

mapped_data = process(example_data, my_config)

with open('resultfile.json', 'w') as output_file:
    output_file.write(simplejson.dumps(mapped_data))

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
