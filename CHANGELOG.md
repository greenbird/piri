# Version history

| Change | Bumps |
| - | - |
| Breaking | major |
| New Feature | minor |
| otherwise | patch |


## 2.1.0 - リミッター解除 - Removes Type Restriction

This release focuses on removing the type restriction we previously had when finding values. This is a huge quality of life improvement for the users since you will be able to get whatever you want. With great power comes... some caveats, obviously casting objects won't work and slicing them will turn them into strings. So there are features that won't work with objects and arrays. However those that work nicely like `if statements` have gotten updated documentation.

### Features
* Removes type restriction when finding values with mapping.path
* Slicing now works with arrays

### Misc
* Adds lots of test + ensures that we do not loose precicion on decimal casting.
* Contribution Doc updates, poetry settings commands are now correct and contribution is easier to follow
* Github actions run on push only to master
* Github actions run on pull requests to master even from forks
* Pre commit action for 'test files must end in `_test`' removed. We prefix our test files with `test_`

[Docs 2.1.0](https://piri.readthedocs.io/en/2.1.0/)

ps: The japanese just means `Limiter Release`, and is sometimes used in anime fighting scenes, I thought it was fitting.

## 2.0.0 - Iterables

This release introduces a breaking change where `path_to_iterable` is renamed to `iterables`. `iterables` is also now a list of `iterable` objects that contain an `alias` and a `path`. This lets you iterate over multiple lists recursively from 1 object.

* Feature: Adds recursive multiple iteration with `iterables`
* Breaking: Removes `path_to_iterable`
* Updates docs/configuration.md
* Updates docs/introduction.md
* Fix: Points links in docs to read the docs

[Docs 2.0.0](https://piri.readthedocs.io/en/2.0.0/)

## 1.2.0 - Slicing support

This release adds support for slicing values. With slicing you can decide from where to where to cut a value. This enables us to pick only the interesting parts of the input values.

* Adds Slicing feature
* Adds Slicing entry to docs/configuration.md
* Adds Slicing parth to docs/introduction.md

[Docs 1.2.0](https://piri.readthedocs.io/en/1.2.1/)


## 1.1.0 - IN condition support in if statements

This minor release adds support for `in` condition for `if_statement`s. This lets you check if the value you found is `in` some list of values _or_ part of a string.

## 1.0.2 - Bugfix

Loading schema.json used relatve path that did not work when package was imported by other package. Now we use `'{0}/schema.json'.format(os.path.dirname(__file__))` to get absolute path to our schema.json.


## 1.0.1

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
