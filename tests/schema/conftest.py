import json

import pytest
from jsonschema import Draft7Validator, draft7_format_checker
from returns.result import safe

from piri.common import ReadLocalFile
from piri.schema import SchemaValidator


@pytest.fixture(scope='session')
def schema():
    """Get the schema."""
    return ReadLocalFile()('piri/schema.json', 'r').bind(
        safe(json.loads),
    ).unwrap()


@pytest.fixture(scope='session')
def if_statement_validator(schema):
    """Return a validator for if_statement part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['if_statement'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def slicing_validator(schema):
    """Return a validator for slicing part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['slicing'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def regexp_validator(schema):
    """Return validator for regexp part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['regexp'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def casting_validator(schema):
    """Return a validator for casting part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['casting'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def iterable_validator(schema):
    """Return a validator for casting part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['iterable'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def mapping_validator(schema):
    """Return a validator for mapping part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['mapping'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def attribute_validator(schema):
    """Return a validator for attribute part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['attribute'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def object_validator(schema):
    """Return a validator for object part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema,
        ),
    )


@pytest.fixture(scope='session')
def branching_object_validator(schema):
    """Return a validator for branching_object part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['branching_object'],
            format_checker=draft7_format_checker,
        ),
    )


@pytest.fixture(scope='session')
def valid() -> dict:
    """Load a valid example config."""
    with open('tests/schema/valid.json', 'r') as file_object:
        return json.loads(file_object.read())


@pytest.fixture(scope='session')
def invalid() -> dict:
    """Load an invalid example config."""
    with open('tests/schema/invalid.json', 'r') as file_object:
        return json.loads(file_object.read())
