# Configuration Json data
The configuration governs not only where to find data, but also the structure of the output which will mirror the structure in the configuration json.

The two main components of the configuration json is the object and attributes. An object can contain nested objects and/or attributes. In the attribute part of the file is where you actually tell the mapper where to find data. In the object you are deciding the structure and also telling the mapper if there are iterable data anywhere that needs to be iterated to create multiple instances.

## The Object

An object has a name, it can have attributes, nested objects or a special type of objects called [branching objects](#branching-object). It will also know if itself is an array and the path to where the input data can be iterated to create multiple objects.

| name | type | description | comment |
| - | - | - | - |
| `name` | str | name of the key it will get in parent object | the root will not get a name |
| `array` | bool | tells the mapper if this should be an array or not | |
| `path_to_iterable` | array of `str` `int` | path to itrable data where this and child parts of the configuration should be applied per iteration | |
| `attributes` | array of [attributes](#attribute) | An array of this objects attribute mappings | |
| `objects` | array of objects | here you can nest more objects. | |
| `branching_objects ` | array of [branching objects](#branching_object) | | |


* name: the objects name, this is the name it will get in the parent object.
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
