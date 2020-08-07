# -*- coding: utf-8 -*-

"""Mapping functions for GBGO."""
from typing import Any, Dict, List, Union

from attr import dataclass
from returns.curry import partial
from returns.maybe import maybe
from returns.pipeline import flow, is_successful
from returns.pointfree import bind, fix
from returns.result import ResultE, safe
from typing_extensions import final

from mapmallow.collection_handlers import FetchListByKeys
from mapmallow.constants import (
    ARRAY,
    ATTRIBUTES,
    BRANCHING_ATTRIBUTES,
    BRANCHING_OBJECTS,
    ITERATE,
    NAME,
    OBJECTS,
    PATH_TO_ITERABLE,
)
from mapmallow.handlers import HandleAttribute
from mapmallow.valuetypes import MapResult


@final
@dataclass(frozen=True, slots=True)
class Map(object):
    """
    Maps a collection of data with the provided configuration and returns dict.

    .. versionadded:: 0.0.1

    :param configuration: :term:`configuration` data to use when mapping
    :type configuration: Dict[str, Any]

    :param collection: The collection of data to find data in
    :type collection: Union[Dict[str, Any], List[Any]]

    :return: Success/Failure containers
    :rtype: MapResult

    """

    _handle_attribute = HandleAttribute()
    _fetch_list = FetchListByKeys()

    def __call__(
        self,
        collection: Union[Dict[str, Any], List[Any]],
        configuration: Dict[str, Any],
    ) -> ResultE[MapResult]:
        """Entrypoint for all mapping."""
        # if loops data, then loop PATH_TO_ITERABLE and put it into clction

        return flow(
            collection,
            partial(self._get_loopable_data, configuration=configuration),
            fix(lambda _: None),  # type: ignore
            bind(partial(
                self._map, collection=collection, configuration=configuration,
            )),
        )

    @safe
    def _map(self, loopable_data, collection, configuration):
        if not loopable_data:
            if configuration[ARRAY]:
                return [self._map_object(collection, configuration).unwrap()]
            return self._map_object(collection, configuration).unwrap()

        # this is pretty complex, should be rewritten

        mapped_objects = []

        for rep in loopable_data['data']:

            mapped = self._map_object(  # type: ignore
                {
                    **collection,
                    **{loopable_data[NAME]: rep},
                },
                configuration,
            )
            if is_successful(mapped):
                mapped_objects.append(mapped.unwrap())

        return mapped_objects

    @maybe
    def _map_object(self, collection, configuration):
        """Return something like this."""
        # .map(object_data.update) updates the dictionary with result data
        # if the function returns Something else nothing happens

        object_data: Dict[str, Any] = {}

        self._map_attributes(
            collection, configuration[ATTRIBUTES],
        ).map(object_data.update)

        self._map_objects(
            collection, configuration[OBJECTS],
        ).map(object_data.update)

        self._map_branching_objects(
            collection, configuration[BRANCHING_OBJECTS],
        ).map(object_data.update)

        # need this as long as empty dict is not seen as None by returns.maybe
        return object_data if object_data else None

    @maybe
    def _map_attributes(self, collection, attributes):
        mapped_attributes: Dict[str, Any] = {}

        for attribute in attributes:
            mapped = self._handle_attribute(collection, attribute)

            if is_successful(mapped):
                mapped_attributes[attribute[NAME]] = mapped.unwrap()

        # need this as long as empty dict is not seen as None by returns.maybe
        return mapped_attributes if mapped_attributes else None

    @maybe
    def _map_objects(self, collection, configurations):
        mapped_objects = {}

        for cfg in configurations:
            # call Map(), without reinitializing
            mapped = self(collection, cfg)

            if is_successful(mapped):
                mapped_objects[cfg[NAME]] = mapped.unwrap()

        # need this as long as empty dict is not seen as None by returns.maybe
        return mapped_objects if mapped_objects else None

    @maybe
    def _map_branching_attributes(self, collection, b_attributes):
        mapped_attributes: List[Dict[str, Any]] = []

        for sub_cfg in b_attributes:
            self._map_attributes(
                collection, sub_cfg,
            ).map(
                mapped_attributes.append,
            )

        # need this as long as empty dict is not seen as None by returns.maybe
        return mapped_attributes if mapped_attributes else None

    @maybe
    def _map_branching_objects(self, collection, b_objects):
        mapped_objects = {}

        for b_object in b_objects:
            mapped = self._map_branching_attributes(  # type: ignore
                collection, b_object[BRANCHING_ATTRIBUTES],
            )

            if is_successful(mapped):
                mapped_objects[b_object[NAME]] = mapped.unwrap()

        # need this as long as empty dict is not seen as None by returns.maybe
        return mapped_objects if mapped_objects else None

    @safe
    def _get_loopable_data(self, collection, configuration):

        if not configuration[ITERATE]:
            raise ValueError('No iterate data found in cfg({cfg})'.format(
                cfg=configuration,
            ))

        return {
            NAME: configuration[PATH_TO_ITERABLE][-1],
            'data': self._fetch_list(
                collection, configuration[PATH_TO_ITERABLE],
            ).unwrap(),
        }
