from decimal import Decimal
from typing import Any, Callable, Dict, List, Union

from returns.result import Result

ValueTypes = (str, int, float, bool, Decimal)

Value = Union[str, int, float, bool, Decimal]
ValueDict = Dict[str, Value]
ValueDictList = List[ValueDict]
NewValue = Union[dict, list, Value]

MapValue = Value
MapAttribute = Union[Value, ValueDict, ValueDictList]
MapObject = Dict[str, MapAttribute]
MapResult = Union[MapObject, List[MapObject]]

# Callables
CallableValidateAndMarshall = Callable[[dict], Result[dict, Exception]]
CallablePreProcess = Callable[[Any], Result[dict, Exception]]
CallableOutput = Callable[[dict], Result[Any, Exception]]
CallableLogFunction = Callable[[Any], None]

CallableMapFunction = Callable[
    [
        Union[Dict[str, Any], List[Any]],
        Dict[str, Any],
    ],
    Result[MapResult, Exception],
]
