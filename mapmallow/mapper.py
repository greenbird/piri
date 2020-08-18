from typing import Any, Dict, List, Optional, Union

from returns.curry import partial
from returns.maybe import maybe
from returns.pipeline import is_successful
from returns.result import safe

from mapmallow.collection_handlers import fetch_list_by_keys
from mapmallow.constants import (
    ARRAY,
    ATTRIBUTES,
    BRANCHING_ATTRIBUTES,
    BRANCHING_OBJECTS,
    NAME,
    OBJECTS,
    PATH_TO_ITERABLE,
)
from mapmallow.handlers import HandleAttribute

MappedDict = Dict[str, Any]


@safe
def map_data(
    input_data,
    configuration,
) -> Union[list, dict]:
    """Map entrypoint.

    Try to get iterable data
    if that fails then just run map_object normally, but make it into an array
    if array is true.

    If we had iterable data, iterate that data and run map_object with the
    current iteration data added to the root of the input_data dictionary
    """
    iterate_data = fetch_list_by_keys(
        input_data, configuration[PATH_TO_ITERABLE],
    )

    if not is_successful(iterate_data):
        return map_object(input_data, configuration).map(
            partial(set_array, array=configuration[ARRAY]),
        ).unwrap()

    mapped_objects: List[dict] = []

    # find returns function to work with iterables
    for iteration in iterate_data.unwrap():
        map_object(
            {
                **input_data,
                **{configuration[PATH_TO_ITERABLE][-1]: iteration},
            },
            configuration,
        ).map(
            mapped_objects.append,
        )

    return mapped_objects


def set_array(input_data, array):
    """Return data wrapped in array if if array=True."""
    if array:
        return [input_data]
    return input_data


@maybe
def map_object(input_data, configuration) -> Optional[MappedDict]:
    """Map one object.

    One object has a collections of:
    Attribute mappings,
    Nested object mappings,
    Branching object mappings,

    All functions we call return a dictionary with the mapped values
    so all we have to do is to call update on a shared object_data dict.

    return example:
    return {
        'attrib': 'val',
        'object1': {'attrib1': 'val'}
        'branching_object1: [{'attrib1': 'val'}]
    }
    """
    object_data: MappedDict = {}

    map_attributes(
        input_data, configuration[ATTRIBUTES],
    ).map(object_data.update)

    map_objects(
        input_data, configuration[OBJECTS],
    ).map(object_data.update)

    map_branching_objects(
        input_data, configuration[BRANCHING_OBJECTS],
    ).map(object_data.update)

    # need this as long as empty dict is not seen as None by returns.maybe
    return object_data or None


@maybe
def map_attributes(input_data, configuration) -> Optional[MappedDict]:
    """For all attributes map attribute.

    name of attribute should be set
    {
        'attribute1': 'value',
        'attribute2': 'value2',
    }
    """
    attributes: MappedDict = {}

    for attribute_cfg in configuration:
        attribute_value = HandleAttribute()(input_data, attribute_cfg)

        if is_successful(attribute_value):
            attributes[attribute_cfg[NAME]] = attribute_value.unwrap()

    return attributes or None


@maybe
def map_objects(
    input_data,
    configuration,
) -> Optional[MappedDict]:
    """For all objects map object.

    name of object should be set.
    {
        'name1': object,
        'name2': object2,
    }
    """
    mapped_objects: MappedDict = {}

    for object_cfg in configuration:
        object_value = map_data(input_data, object_cfg)

        if is_successful(object_value):
            mapped_objects[object_cfg[NAME]] = object_value.unwrap()

    return mapped_objects or None


@maybe
def map_branching_attributes(
    input_data,
    b_attributes,
) -> Optional[List[MappedDict]]:
    """Map branching attributes.

    Branching attributes are a list of attribute mappings that will be
    mapped to the same name in branching object.
    """
    mapped_attributes: List[MappedDict] = []

    for sub_cfg in b_attributes:
        map_attributes(
            input_data, sub_cfg,
        ).map(
            mapped_attributes.append,
        )

    # need this as long as empty dict is not seen as None by returns.maybe
    return mapped_attributes or None


@maybe
def map_branching_objects(
    input_data,
    configuration,
) -> Optional[MappedDict]:
    """Map branching object.

    Branching object is a case where we want to create the same object multiple
    times, however we want to find the data in different places.
    """
    mapped_objects: MappedDict = {}

    for b_object in configuration:
        mapped = map_branching_attributes(
            input_data, b_object[BRANCHING_ATTRIBUTES],
        )

        if is_successful(mapped):
            mapped_objects[b_object[NAME]] = mapped.unwrap()

    # need this as long as empty dict is not seen as None by returns.maybe
    return mapped_objects or None
