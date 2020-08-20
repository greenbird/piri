[![CircleCI](https://circleci.com/bb/cloudwheel/mapmallow.svg?style=svg&circle-token=f7613e4f9b3530fed648a14ce8088adc1023c62d)](https://circleci.com/bb/cloudwheel/mapmallow) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide) [![coverage](https://circleci.com/api/v1.1/project/bitbucket/cloudwheel/mapmallow/latest/artifacts/0/home/circleci/project/htmlcov/coverage-badge.svg?circle-token=90a86670390b81f167032150a44d59de42a00557)](https://circleci.com/api/v1.1/project/bitbucket/cloudwheel/mapmallow/latest/artifacts/0/home/circleci/project/htmlcov/index.html?circle-token=90a86670390b81f167032150a44d59de42a00557)

# Features

* Maps list/dicts to other lists/dicts
* Use your own marshmallow schemas for validation
* Write your own dict -> output functions
* All mapping done with configuration file

# Contributing
>Please see CONTRIBUTING.md

# Installation
```sh
$ poetry add mapmallow
```

# Contents

* Process function that will validate, map and output
* Map function that maps data into structures described by configuration
* ApplySchema function that loads - validates - dumps data with marshmallow.
* Error handlers that can try to rescue invalid data.
* fields - helper fields types for iso values like country code

>We make heavy use of [Returns library](https://github.com/dry-python/returns) so any time you call a library function you will receive a Result Monad that is a Success or Failure container. To retrieve the data inside call .unwrap or .value_or(None).


# Quickstart
```python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields

from mapmallow.process import Process
from mapmallow.schema import ApplySchema

my_config = {
    'name': 'schema',
    'array': False,
    'loops_data': False,
    'objects': [
        {
            'name': 'invoices',
            'array': True,
            'loops_data': True,
            'loopable_data_path': ['root', 'invoices'],
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


class Invoice(Schema):
    """Invoice Schema."""

    amount = fields.Decimal(required=True)
    debtor = fields.String(required=True)


class MySchema(Schema):
    """Base schema."""

    invoices = fields.List(fields.Nested(Invoice))


if __name__ == '__main__':
    process = Process(
        ApplySchema(MySchema()),
    )
    mapped_data = process(my_config, example_data)
    print(mapped_data)
    print(mapped_data.unwrap())

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


# Map

Together with a [configuration file](#configuration-file) this function will create some data structured like the configuration file. The different pieces of the configuration file will tell the mapper how to structure the output.


# ApplySchema

The Apply Schema function is here to load a Map() result into a marshmallow schema. This will then validate the data. If there are any errors it will try to fix the errors by applying the functions provided to rescue_functions. When it has done that, the errors will either be gone or not. If they are gone, we do a Schema.dump() on the data to let marshmallow do all of the dump output formatting it wants to. Return the resulting dictionary.

>If you used fields.Decimal() remember that dumped values will be Decimal(x.yy) so when you create output dont forget to handle this. If you use fields.Decimal(,,, as_string=True) then it will be dumped to string.




# Configuration File
The configuration file governs not only where to find data, but also the structure of the output which will mirror the structure in the configuration file.

The two main components of the configuration file is the object and attributes. An object can contain more object and/or attributes. In the attribute part of the file is where you actually tell the mapper where to find data. In the object you are deciding the structure and also telling the mapper if there are loopable data anywhere that needs to be looped.

## Object

An object has a name, it can have attributes, nested objects or a special type of objects called branching objects. It will also know if itself is an array and the path to where the input data can be looped to create more of itself.

* name: the objects name, this is the name it will get in the parent object or if this is root, the dataset will be named this.
* array: forces result to be an array even if it is not
* loops_data: tells us if we should loop some input data to create more of this object
* loopable_data_path: path to loopable data ie: list of invoices
* objects: list of [ojects](#object).
* branching_objects: list of [branching objects](#branching-object)
* attributes: list of [attribute objects](#attribute-object)

```json
{
	"name": "object_name",
	"array": true,
	"loops_data": true,
	"loopable_data_path": ["path", "to", "list"],
	"objects": [],
	"branching_objects": [],
	"attributes": []
}
```

## Attribute Object

The attributes are like 'color' of a car or 'amount' in an invoice. Attributes are have a name ('amount'), a number of mappings, separator, if statements, casting and a default value if all else fails.

* name: the attributes name, this is the name it will get in the parent object
* mappings: list of [mapping objects](#mapping-object)
* separator: string to separate each value in case multiple are found
* if_statements: list of [if statement objects](#if-statement-object) that can change the data based on conditions
* casting: [casting object](#casting-object) that lets you cast to integer, decimal or date types
* default: a default value if result is None after all the above

```json
{
	"name": "attribute_name",
	"mappings": [],
	"separator": "",
	"if_statements": [],
	"casting": {},
	"default": "default value"
}
```

## Mapping Object

This is the only place where actual interaction with the input data is done.

* path: you add a list of strings or integers that will get you to your data. so for example if you needed to get to the second element in the list called 'my_list' in the following json then your path will be ```["my_list", 1]``` and you will get the value ```index1```

```json
{
	"my_list": ["index0", "index1"]
}
```

* if_statements: list of [if statement objects](#if-statement-object) that can change the data depending on conditions
* default: a default value if none is found or value found is ```None```

```json
{
	"path": ["path", "to", "data"],
	"if_statements": [],
	"default": "default"
}
```
>input({'path': { 'to': { 'data': 'value'}}}) -> 'value'

>input({'path': { 'does_not_exist'}}) -> 'default'

>input() -> 'default'

## If Statement object

This is where you can change found(or not found) data to something else based on a condition. There is always a list of if statement objects and they are chained in the sense that what the first one produces will be the input to the next one. Thus if you want the original value if the first one fails, then leave out ```otherwise```

* condition: is|not|contains is how we will check the value against target
* target: is what we do our condition against
* then: value that we will return if the condition is true
* otherwise: Optional value that we can return if the condition is false

```json
{
	"condition": "is",
	"target": "1",
	"then": "first_type",
	"otherwise": "default_type"
}
```
>input('2') -> 'default_type'

>input('1') -> 'first_type'

## Casting object
The casting object lets you cast whatever value is found to some new value. Currently integer, decimal and date are supported and original format is optional helper data that we need for some special cases where the format of the input value cannot be asserted automatically.

* to: integer|decimal|date - what type to cast the value to
* original_format: integer_containing_decimals|decimal - the first one is used when some integer value should be casted to decimal, and we need to divide it by 100. and decimal is used when we cast a decimal number to integer so we get rounding correct. (round up half)

```json
{
    "to": "decimal",
    "original_format": "integer_containing_decimals"
}
```
>input(10050) -> Decimal(100.50)


## Branching Object
The branching object is a special object that does not have attributes or object childs but has a special branching_attributes child. The point of this object is to make sure that we can map data from different sources into the same element. for example, we have an object called "extradata" with the attributes 'name' and 'data'. This is kind of a field that can _be_ many things. like 'name' = 'extra_address_line1', and another one with 'extra_address_line2'. This must then get its data from different places, and thats what these branching objects are for.

* name: name of the object
* array: if it should be an array or not
* loops_data: if it should repeat this object on a set on data.
* loopable_data_path: path to list
* branching_attributes: list of list of attributes where each list of attributes will create a branching object.

```json
{
    "name": "extradata",
    "array": true,
    "loops_data": false,
    "branching_attributes": [
        [
            {
                "name": "name",
                "default": "extra_address_line1"
            },
            {
                "name": "data",
                "mappings": [{"path": ["list", "to", "line1", "value"]}]
            }
        ],
        [
            {
                "name": "name",
                "default": "extra_address_line2"
            },
            {
                "name": "data",
                "mappings": [{"path": ["list", "to", "line2", "value"]}]
            }
        ]
    ]
}
```

this will produce:

```json
{
    "extradata": [
        {
            "name": "extra_address_line1",
            "data": "address value 1"
        },
        {
            "name": "extra_address_line2",
            "data": "address value 2"
        }
    ]
}
```
