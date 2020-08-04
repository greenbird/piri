import json
import uuid

import pytest


@pytest.fixture(scope='session')
def valid():
    """Loads a valid example config."""
    _input_data: dict = {}
    with open('tests/schema/valid.json', 'r') as file_object:
        _input_data = json.loads(file_object.read())

    return _input_data


@pytest.fixture(scope='session')
def invalid():
    """Loads an invalid example config """
    _input_data: dict = {}
    with open('tests/schema/invalid.json', 'r') as file_object:
        _input_data = json.loads(file_object.read())

    return _input_data
