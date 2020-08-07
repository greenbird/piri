# -*- coding: utf-8 -*-

"""Helpers for mapmallow mapping functions."""
from typing import Any, Dict, List, Union

from returns.result import safe

from mapmallow.valuetypes import MapValue, ValueTypes


@safe
def set_value_in_dict(
    new_value: MapValue,
    collection: Dict[str, Any],
    path: List[str],
) -> None:
    """Set value in a dict(pass by ref) by path."""
    if not path:
        raise ValueError('path list empty')

    for key in path[:-1]:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]

    collection[path[-1]] = new_value


@safe
def fetch_data_by_keys(
    collection: Union[Dict[str, Any], List[Any]],
    path: List[Union[str, int]],
) -> MapValue:
    """Find data in collection by following a list of path."""
    if not path:
        raise ValueError('path list empty')

    for key in path:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]  # type: ignore

    if isinstance(collection, ValueTypes):  # type: ignore
        return collection  # type: ignore

    raise ValueError(
        'Bad data found: {0} , with type: {1}'.format(
            str(collection), str(type(collection)),
        ),
    )


@safe
def fetch_list_by_keys(
    collection: Dict[str, Any],
    path: List[str],
) -> list:
    """Find data that *must* be a list else it fails.

    Example
        >>> fetch_list_by_keys(
        ...     {'object': {'some_list': ['1']}}, ['object', 'some_list'],
        ... ).unwrap()
        ['1']
    """
    if not path:
        raise ValueError('path list empty')

    for key in path:
        # this will return a Failure[KeyError] if not found
        collection = collection[key]

    if isinstance(collection, list):  # type: ignore
        return collection  # type: ignore

    raise ValueError('Non list data found: ', str(collection))
