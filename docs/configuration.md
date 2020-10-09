# Configuration Json data
The configuration governs not only where to find data, but also the structure of the output which will mirror the structure in the configuration json.

The two main components of the configuration json is the object and attributes. An object can contain nested objects and/or attributes. In the attribute part of the file is where you actually tell the mapper where to find data. In the object you are deciding the structure and also telling the mapper if there are iterable data anywhere that needs to be iterated to create multiple instances.


## Object

An object has a name, it can have attributes, nested objects or a special type of objects called [branching objects](#branching-object). It will also know if itself is an array and the path to where the input data can be iterated to create multiple objects.

| name | type | description | comment |
| --- | --- | --- | --- |
| __name__ | str | name of the key it will get in parent object | the root will not get a name |
| __array__ | bool | tells the mapper if this should be an array or not | |
| iterables | array[[iterable](#iterable)] | Lets you iterate over lists in input data and apply configuration to every iteration of the lists | |
| _attributes_ | array[[attribute](#attribute)] | An array of this objects attribute mappings | |
| _objects_ | array[[object](#object)] | Here you can nest more objects. | |
| _branching_objects_ | array[[branching object](#branching-object)] | Array of a special kind of object | rarely used |


```json
{
    "name": "object_name",
    "array": true,
    "iterables": [],
    "objects": [],
    "branching_objects": [],
    "attributes": []
}
```

## Iterable

Iterables are your bread and butter for looping lists in the input data. For each an every one of the elements in the list we apply the current object and its childrens mapping configuration.

| name | type | description |
| --- | --- | --- |
| __alias__ | str | The aliased name the current iteration will get in the data which mapping is applied to |
| __path__ | array[str\|int] | path to the iterable list/array in the input data |

```json
{
    "alias": "keyname",
    "path": ["path", "to", "list"]
}
```
[Explanation of path](#explanation-of-path)

[Iterables will get more explained](https://github.com/greenbird/piri/issues/113)

## Attribute

The attributes are like 'color' of a car or 'amount' in an invoice. Attributes are have a name ('amount'), a number of mappings, separator, if statements, casting and a default value if all else fails.

| name | type | description | default |
| --- | --- | --- | --- |
| __name__ | str | The name it will get in the parent object | |
| _mappings_ | array[[mapping](#mapping)] | list of mapping objects which is where to find data | `[]` |
| separator | str | string to separate each value in case multiple are found in mapping step | `''` |
| if_statements | array[[if statement](#if-statement)] | If statements that can change data based on conditions | `[]` |
| casting | [casting](#casting) | Lets you cast data to a spesific type [int, decimal, date] | `{}` |
| _default_ | Any | If after all mapping, if statements and casting the result is None this value is used | `None` |

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

## Mapping

This is the only place where actual interaction with the input data is done.

| name | type | description | default |
| --- | --- | --- | --- |
| _path_ | array[str\|int] | path to data you want to retrieve. | `[]` |
| if_statements | array[[if statement](#if-statement)] | If statements that can change data based on conditions | `[]` |
| _default_ | Any | If no value is found or value is None after if_statements then this value is used | `None` |

!!! note
    either `path` or `default` must contain a something

### Explanation of path

You add a list of `strings` or `integers` that will get you to your data. so for example if you needed to get to the second element in the list called `my_list` in the following json then your `path` will be `["my_list", 1]` and you will get the value `index1`

```json
{
    "my_list": ["index0", "index1"]
}
```

* if_statements: list of [if statements](#if-statement) that can change the data depending on conditions
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

## Slicing

Lets you slice a value from index `from` to index `to`. Slicing is implemented exactly like pythons string[x:x] slicing. This means that when `from` is negative you count back from the end, and if `to` is `null` or left out then we consume the rest of the string.


| name | type | description | default |
| --- | --- | --- | --- |
| __from__ | int | Where to cut value from counted from `0` | |
| to | int\|null | To what index we cut to, leave key/value out or set value=`null` to go to end of string | |

```json
{
    "from": 1,
    "to": 3,
}
```
> input('hello') -> 'el'

!!! Note
    All values are turned into `string` before slicing is applied. This lets you also slice any values independant on their original type in the input data. If the config Slicing object is empty, this str casting is also skipped. Any result after slicing is also a string. So if you need a different format use [casting to change it](#casting)

## If Statement

This is where you can change found(or not found) data to something else based on a condition. They are chained in the sense that what the first one produces will be the input to the next one. Thus if you want the original value if the first one fails, then leave out ```otherwise```


| name | type | description | default |
| --- | --- | --- | --- |
| __condition__ | one of ["is", "not", "in", "contains"] | What condition to use when checking `value` against `target` | |
| __target__ | str\|number\|bool\|array\|object | Target what we do our condition against ie: `value == target` when condition is `is` | |
| __then__ | str\|number\|bool\|array\|object | value that we will return if the condition is true | |
| otherwise | str\|number\|bool\|array\|object | Optional value that we can return if the condition is false | `None` |

```json
{
    "condition": "is",
    "target": "1",
    "then": "first_type",
    "otherwise": "default_type"
}
```
> input('2') -> 'default_type'

> input('1') -> 'first_type'

If statements work a bit different depending on what value you expect to get. This table shows the exact operators used for all valuetypes

| condition | valuetype | code | comment |
| --- | --- | --- | --- |
| is | all | `value == target` | |
| not | all | `value != target` | |
| in | array\|object | `value in target` | target must be an array or a string. where value must then equal one of the array `items` or a substring when target is a string. This means that the array values can be arrays or objects for when checking against array and object values |
| contains | object | `target in value` | For objects this means that the `target is a key in object` |
| contains | array | `target in value` | For arrays this means that `target equals one or more item in the array` |
| contains | rest | `target in str(value)` | For the rest we string cast the value so that we can do this check for the rest of the types |


## Casting
The casting object lets you cast whatever value is found to some new value. Currently integer, decimal and date are supported and original format is optional helper data that we need for some special cases where the format of the input value cannot be asserted automatically.

| name | type | description | default |
| --- | --- | --- | --- |
| __to__ | one of ["integer", "decimal", "date"] | What type to cast the value to | |
| original_format | "integer_containing_decimals" or spesific date format(see below)" | For some values we need to specify extra information in order to correctly cast it.| `None` |

__about original format__

!!! note
    When `to` is `date` then original_format is `required`.

| when to is | original format | description |
| --- | --- | --- |
| decimal | integer_containing_decimals | is used when some integer value should be casted to decimal and we need to divide it by 100 |
| date | `yyyy.mm.dd` `yy.mm.dd` `yymmdd` `dd.mm.yyyy` `dd.mm.yy` `ddmmyy` | The format of the input date. `.` means any delimiter. Output is always iso-date yyyy-mm-dd |


__Examples__
```json
{
    "to": "decimal",
    "original_format": "integer_containing_decimals"
}
```
`"10050" -> Decimal(100.50)`

```json
{
    "to": "date",
    "original_format": "ddmmyyyy"
}
```
`"01012001" -> "2010-01-01"`


## Branching Object
The branching object is a special object that does not have attributes or object childs but has a special branching_attributes child. The point of this object is to make sure that we can map data from different sources into the same element. for example, we have an object called "extradata" with the attributes 'name' and 'data'. This is kind of a field that can _be_ many things. like 'name' = 'extra_address_line1', and another one with 'extra_address_line2'. This must then get its data from different places, and thats what these branching objects are for.


| name | type | description |
| --- | --- | --- |
| __name__ | str | Name of the object |
| __array__ | bool | if it should be an array or not |
| iterables | array[[iterable](#iterable)] | Lets you iterate over lists in input data and apply configuration to every iteration of the lists |
| __branching_attributes__ | array[array[[attribute](#attribute)]] | list of list of attributes where each list of attributes will create a branching object. |


__Example__

```json
{
    "name": "extradata",
    "array": true,
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

This will produce:

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
