# -*- coding: utf-8 -*-

"""Mapping functions for GBGO."""
from typing import Any, Dict, List, Union

from attr import dataclass
from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind, fix, rescue
from returns.result import ResultE, safe
from typing_extensions import final

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
    ApplyCasting,
    ApplyDefault,
    ApplyIfStatements,
    ApplySeparator,
)
from mapmallow.valuetypes import MapValue


@final
@dataclass(frozen=True, slots=True)
class HandleMapping(object):
    """Finds data in the collection and applies some functions to it.

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
    """

    _apply_ifs = ApplyIfStatements()
    _apply_default = ApplyDefault()

    def __call__(
        self,
        collection: Union[Dict[str, Any], List[Any]],
        cfg: Dict[str, Any],
    ) -> ResultE[MapValue]:
        """Map data to value by cfg.

        find data from path or None ->
        apply if statements ->
        return default value if Failure else mapped value
        """
        return flow(
            collection,
            partial(fetch_data_by_keys, path=cfg[PATH]),
            fix(lambda _: None),  # type: ignore
            bind(partial(self._apply_ifs, if_objects=cfg[IF_STATEMENTS])),
            rescue(  # type: ignore
                lambda _: self._apply_default(cfg[DEFAULT]),
            ),
        )


@final
@dataclass(frozen=True, slots=True)
class HandleAttribute(object):
    """
    Fetch all the data and apply operations on it.

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
            "mappings": [],  # array of mapping objects
            "separator": None,
            "if_statements": [],  # array of if statement objects
            "casting": {}  # casting object, for casting types
            "default": "default value"
        }

    """

    _handle_mapping = HandleMapping()
    _separate = ApplySeparator()
    _apply_ifs = ApplyIfStatements()
    _cast = ApplyCasting()
    _apply_default = ApplyDefault()

    def __call__(
        self,
        collection: Union[Dict[str, Any], List[Any]],
        cfg: dict,
    ) -> ResultE[MapValue]:
        """Handle an attribute mapping.

        Map all objects in cfg[MAPPINGS] ->
        Apply separator to values if there are more than 1
        Failure -> fix to Success(None)
        Apply if statements
        Success -> Cast Value
        Failure -> apply default value

        Return Result
        """
        return flow(
            collection,
            partial(self._map, cfg=cfg[MAPPINGS]),
            bind(partial(self._separate, separator=cfg[SEPARATOR])),
            fix(lambda _: None),  # type: ignore
            bind(partial(self._apply_ifs, if_objects=cfg[IF_STATEMENTS])),
            bind(partial(self._cast, casting=cfg[CASTING])),
            rescue(  # type: ignore
                lambda _: self._apply_default(default=cfg[DEFAULT]),
            ),
        )

    @safe
    def _map(
        self,
        collection: Union[Dict[str, Any], List[Any]],
        cfg: List[Dict[str, Any]],
    ) -> List[MapValue]:
        """Call HandleMapping and accumulate only successfull results."""
        return [
            mapped.unwrap()
            for mapped in
            [self._handle_mapping(collection, mapping) for mapping in cfg]
            if is_successful(mapped)
        ]
