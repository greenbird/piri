# Piri
Configurable Data Mapping for mortals
___
![test](https://github.com/greenbird/piri/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/greenbird/piri/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/piri)
[![Python Version](https://img.shields.io/pypi/pyversions/piri.svg)](https://pypi.org/project/piri/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
___

**Documentation
([Stable](https://piri.readthedocs.io/) |
[Latest](https://piri.readthedocs.io/en/latest/)) |
[Source Code](https://github.com/greenbird/piri) |
[Task Tracker](https://github.com/greenbird/piri/issues)**

## What is Piri

Piri is a JSON to JSON mapper. That means that we read input JSON and create output JSON. How the output is created is based on instructions from a configuration file. The configuration file governs the the output structure and tells piri where in the input to find data and where to place it in the output. In addition to this Piri supports data transformation with `data casting`, `if conditions`, `combination of data from multiple places` and of course setting `default` values.

__This enables you to change any input into the output you desire.__

## Typical usecases

* You `GET` data from api, but need to transform it for your backend system
* `POST`ing data to an api that needs data on a different format than what your system produces
* All your backends speak different language? pipe it through __Piri__
* Customer delivers weirdly formatted data? Use __Piri__ to make it sexy
* Have CSV but need nicely structured JSON? make CSV into a JSON list and transform it with __Piri__
* Have XML but need to change it? make it into JSON, transform it with __Piri__ and then dump it to XML again.
* Customers legacy system needs CSV. Use __Piri__ to transform your nicely structured JSON data into a JSON List that can be easily dumped to CSV

## Official Open Piri Solutions

[piri-cli](https://github.com/greenbird/piri-cli), commandline interface for file to file mapping.

[piri-web](https://github.com/greenbird/piri-web), One Click deploy Web REST API for Piri JSON mapping.

## Enterprise solutions

Coming...

## Goal

The goal of this library is to make JSON to JSON transformation/mapping easy, configurable and documentable. We achieve this by using a simple but feature-rich JSON configuration which then also acts as documentation and as a contract between parties.

## Why

Piri was born because we really dislike mapping. Documenting whatever decisions made in your code so that some product owner understands it is also _no me gusto_. Transforming data from one format to another is something software engineers do allmost daily... It should be easy! And documenting it shouldn't be something you have to worry about.

After the Worst POC in History we never wanted to do mapping by scripts and code again. This lead to the idea that it should be possible to create a file which governs how the structure should look and how the data should be transformed. This would then be the `single source of truth` and with Piri we have achieved this.

We believe that this will make collaboration between teams faster and easier. Use Piri to agree with data formats between Front-end and Back-end. Between the 3rd party system and your back-end. You can even use Piri for testing existing integrations ;-)

## Features

* Mapping with configuration File.
* [JSON Schema](https://json-schema.org/) validation of the config file.
* Structurally Transform JSON
* Combine multiple values to one.
* Default values
* If statements
    * is, contains, not
* casting
    * integer, decimal, iso date

## Contributing
Please see [contribute](https://piri.readthedocs.io/en/stable/contributing)

## Installation

Package is on pypi. Use pip or poetry to install

```sh
pip install piri
```
```sh
poetry add piri
```

## Introduction

Have a look at our introduction course [here](https://piri.readthedocs.io/en/stable/introduction)

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
            'iterables': [
                {
                    'alias': 'invoices',
                    'path': ['root', 'invoices'],
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
