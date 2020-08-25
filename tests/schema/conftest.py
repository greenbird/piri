import json

import pytest
from jsonschema import Draft7Validator
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
        ),
    )


@pytest.fixture(scope='session')
def casting_validator(schema):
    """Return a validator for casting part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['casting'],
        ),
    )


@pytest.fixture(scope='session')
def mapping_validator(schema):
    """Return a validator for mapping part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['mapping'],
        ),
    )


@pytest.fixture(scope='session')
def attribute_validator(schema):
    """Return a validator for attribute part of schema."""
    return SchemaValidator(
        Draft7Validator(
            schema['definitions']['attribute'],
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
