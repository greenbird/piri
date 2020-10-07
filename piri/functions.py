from typing import Any, Dict, List, Optional

from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Failure, ResultE, Success, safe

from piri.casting import get_casting_function
from piri.constants import (  # noqa: WPS235
    CONDITION,
    CONTAINS,
    FROM,
    IN,
    IS,
    NOT,
    ORIGINAL_FORMAT,
    OTHERWISE,
    TARGET,
    THEN,
    TO,
)
from piri.valuetypes import MapValue, ValueTypes


@safe
def apply_if_statements(if_value, if_objects) -> MapValue:
    """Apply if statements to a value.

    :param if_value: The value to use when evaluating if statements
    :type if_value: MapValue

    :param if_objects: :term:`if_objects` collection of if operations
    :type if_objects: List[Dict[str, Any]]

    :return: Success/Failure containers
    :rtype: MapValue

    one if object looks like this

    .. code-block:: json

        {
            "condition": "is",
            "target": "foo",
            "then": "bar",
            "otherwise": "no foo" - optional
        }

    The if statements are chained so that the next works on the output of the
    previous. If no "otherwise" is provided then the original value or value
    from the previous operation will be returned.

    Example
        >>> apply_if_statements(
        ...     '1', [{'condition': 'is', 'target': '1', 'then': '2'}],
        ... ).unwrap() == '2'
        True
        >>> apply_if_statements(
        ...     'a',
        ...     [{
        ...         'condition': 'is',
        ...         'target': '1',
        ...         'then': '2',
        ...         'otherwise': '3'
        ...     }],
        ... ).unwrap() == '3'
        True

    """
    for if_object in if_objects:

        if_value = _apply_statement(
            if_value, if_object,
        ).value_or(if_value)

    if if_value is None:
        raise ValueError('If statement failed or produced `None`')

    return if_value


@safe
def _apply_statement(
    if_value: Optional[MapValue],
    if_object: Dict[str, Any],
) -> Optional[MapValue]:
    evaluation: bool = False

    condition = if_object[CONDITION]
    target = if_object[TARGET]

    if condition == IS:
        evaluation = if_value == target

    if condition == NOT:
        evaluation = if_value != target

    if condition == IN:
        evaluation = if_value in target

    if condition == CONTAINS:
        list_or_dict = isinstance(if_value, (dict, list))
        evaluation = list_or_dict and target in if_value  # type: ignore
        evaluation = evaluation or not list_or_dict and target in str(if_value)

    if evaluation:
        return if_object[THEN]

    return if_object.get(OTHERWISE, if_value)


@safe
def apply_separator(
    mapped_values: List[MapValue],
    separator: str,
) -> MapValue:
    """Apply separator between the values of a List[Any].

    :param mapped_values: The list of values to join with the separator
    :type mapped_values: List[MapValue]

    :param separator: :term:`separator` value to join mapped_values list with
    :type separator: str

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> from returns.pipeline import is_successful
        >>> apply_separator(['a', 'b', 'c'], ' ').unwrap()
        'a b c'
        >>> apply_separator([1, 'b', True], ' ').unwrap()
        '1 b True'
        >>> is_successful(apply_separator([], ' '))
        False

    """
    if not mapped_values:
        raise ValueError('mapped_values is empty')

    if len(mapped_values) == 1:
        return mapped_values[0]

    return separator.join([str(mapped) for mapped in mapped_values])


def apply_slicing(
    value_to_slice: Optional[MapValue],
    slicing: Dict[str, Any],
) -> Optional[MapValue]:
    """Slice value from index to index.

    :param slicing: :term:`slicing` object
    :type slicing: dict

    :param value_to_slice: The value to slice
    :type value_to_slice: MapValue

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> apply_slicing('123', {'from': 1})
        '23'
        >>> apply_slicing('test', {'from': 1, 'to': 3})
        'es'
    """
    if value_to_slice is None:
        return value_to_slice

    if not slicing:
        return value_to_slice

    return str(value_to_slice)[slicing[FROM]:slicing.get(TO)]


def apply_casting(
    value_to_cast: Optional[MapValue],
    casting: Dict[str, Any],
) -> ResultE[MapValue]:
    """Cast one type of code to another.

    :param casting: :term:`casting` object
    :type casting: dict

    :param value_to_cast: The value to cast to casting['to']
    :type value_to_cast: MapValue

    :return: Success/Failure containers
    :rtype: MapValue

    Example
        >>> apply_casting('123', {'to': 'integer'}).unwrap()
        123
        >>> apply_casting('123.12', {'to': 'decimal'}).unwrap()
        Decimal('123.12')
    """
    if value_to_cast is None:
        return Failure(ValueError('value_to_cast is empty'))

    if TO not in casting or casting[TO] is None:
        return Success(value_to_cast)

    return flow(
        casting[TO],
        get_casting_function,
        bind(  # type: ignore
            lambda function: function(  # type: ignore
                value_to_cast, casting.get(ORIGINAL_FORMAT),
            ),
        ),
    )


@safe
def apply_default(
    mapped_value: Optional[Any] = None,
    default: Optional[MapValue] = None,
) -> MapValue:
    """Apply default value if exists and if mapped value is None.

    :param mapped_value: If this value is *None* the default value is returned
    :type mapped_value: Optional[MapValue]

    :param default: :term:`default` value to return if mapped value is None
    :type default: Optional[MapValue]

    :return: Success/Failure containers
    :rtype: MapValue

    If default *is not* none and mapped_value *is* None then return default
    else if mapped_value is not in accepted ValueTypes then throw an error
    else return mapped value

    Example
        >>> apply_default('test', None).unwrap() == 'test'
        True
        >>> apply_default('nope', 'test').unwrap() == 'nope'
        True
    """
    if default is not None:
        if mapped_value is None:
            return default

    if mapped_value is None:
        raise ValueError('Default value should not be `None`')

    if not isinstance(mapped_value, ValueTypes):
        raise ValueError('Unable to give default value')

    return mapped_value
