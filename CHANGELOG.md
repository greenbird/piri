# Version history

| Change | Bumps |
| - | - |
| Breaking | major |
| New Feature | minor |
| otherwise | patch |


## Minor 1.1.0 - IN condition support in if statements

This minor release adds support for `in` condition for `if_statement`s. This lets you check if the value you found is `in` some list of values _or_ part of a string.

## Patch 1.0.2 - Bugfix

Loading schema.json used relatve path that did not work when package was imported by other package. Now we use `'{0}/schema.json'.format(os.path.dirname(__file__))` to get absolute path to our schema.json.


## Patch 1.0.1

* adds python versions badge
* removes bad part of documentation


## Version 1.0.0 Release: Piri Reis

The first release focuses on key mapping functionality. Finding values from multiple places and combining them to one. Setting default values, Casting values, and applying if statements. This should suffice for a lot of usecases where one need to transform json into structurally different json.

### Features

* Mapping with configuration File.
* Combine multiple values to one.
* Default values
* If statements
    * is, contains, not
* casting
    * integer, decimal, iso date
