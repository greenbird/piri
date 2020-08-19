# -*- coding: utf-8 -*-

"""Mapping functions for GBGO."""
from typing import Any, Dict, List, Union

from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind, fix, rescue
from returns.result import ResultE

from mapmallow.collection_handlers import fetch_data_by_keys
from mapmallow.constants import (
    CASTING,
    DEFAULT,
    IF_STATEMENTS,
    MAPPINGS,
    PATH,
    SEPARATOR,
)
from mapmallow.functions import (
    apply_casting,
    apply_default,
    apply_if_statements,
    apply_separator,
)
from mapmallow.valuetypes import MapValue


def handle_mapping(
    collection: Union[Dict[str, Any], List[Any]],
    cfg: Dict[str, Any],
) -> ResultE[MapValue]:
    """Find data in path and apply if statements or default value.

    .. versionadded:: 0.0.1

    :param configuration: :term:`configuration` data to use when mapping
    :type configuration: Dict[str, Any]

    :param collection: The collection of data to find data in
    :type collection: Union[Dict[str, Any], List[Any]]

    :return: Success/Failure containers
    :rtype: GoResult

    configuration expected to look like this:

    .. code-block:: json
        {
            "path": [],
            "if_statementss": [{}, {}],
            "default": 'val'
        }

    Flow description:

    find data from path or None ->
    apply if statements ->
    return default value if Failure else mapped value
    """
    return flow(
        collection,
        partial(fetch_data_by_keys, path=cfg[PATH]),
        fix(lambda _: None),  # type: ignore
        bind(partial(apply_if_statements, if_objects=cfg[IF_STATEMENTS])),
        rescue(  # type: ignore
            lambda _: apply_default(cfg[DEFAULT]),
        ),
    )


def handle_attribute(
    collection: Union[Dict[str, Any], List[Any]],
    cfg: dict,
) -> ResultE[MapValue]:
    """Handle one attribute with mappings, ifs, casting and default value.

    :param collection: The collection of data to find data in
    :type collection: Union[Dict[str, Any], List[Any]]

    :param configuration: :term:`configuration` data to use when mapping
    :type configuration: Dict[str, Any]

    :return: Success/Failure containers
    :rtype: MapValue

    configuration expected to look like this:

    .. code-block:: json

        {
            "mappings": [],  # array of mapping objects
            "separator": None,
            "if_statements": [],  # array of if statement objects
            "casting": {}  # casting object, for casting types
            "default": "default value"
        }

    flow description:

    Map all objects in cfg[MAPPINGS] ->
    Apply separator to values if there are more than 1
    Failure -> fix to Success(None)
    Apply if statements
    Success -> Cast Value
    Failure -> apply default value

    Return Result
    """
    mapped_values = [
        mapped.unwrap()
        for mapped in
        [handle_mapping(collection, mapping) for mapping in cfg[MAPPINGS]]
        if is_successful(mapped)
    ]

    return flow(
        mapped_values,
        partial(apply_separator, separator=cfg[SEPARATOR]),
        fix(lambda _: None),  # type: ignore
        bind(partial(apply_if_statements, if_objects=cfg[IF_STATEMENTS])),
        bind(partial(apply_casting, casting=cfg[CASTING])),
        rescue(  # type: ignore
            lambda _: apply_default(default=cfg[DEFAULT]),
        ),
    )
