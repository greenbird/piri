from typing import Callable, Union

from attr import dataclass
from returns.functions import raise_exception
from returns.pipeline import is_successful
from returns.result import ResultE
from typing_extensions import final

from piri.mapper import map_data
from piri.schema import SchemaValidator


@final
@dataclass(frozen=True, slots=True)
class Process(object):
    """Process Callable Object."""

    validate: Callable[[dict], ResultE[dict]] = SchemaValidator()

    def __call__(
        self,
        input_data: dict,
        configuration: dict,
    ) -> ResultE[Union[list, dict]]:
        """Validate configuration then process data."""
        cfg = self.validate(configuration)

        if not is_successful(cfg):
            return cfg

        return map_data(input_data, cfg.unwrap())


def process(
    input_data: dict,
    configuration: dict,
) -> Union[list, dict]:
    """Call Process and unwrap value if no error, otherwise raise."""
    return Process()(
        input_data,
        configuration,
    ).alt(
        raise_exception,
    ).unwrap()
