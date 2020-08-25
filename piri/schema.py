import json

from attr import dataclass
from jsonschema import Draft7Validator
from returns.result import Failure, ResultE, Success, safe
from typing_extensions import Final, final

from piri.common import ReadLocalFile

schema: Final[dict] = ReadLocalFile()(
    'piri/schema.json', 'r',
).bind(safe(json.loads)).unwrap()


@final
@dataclass(frozen=True, slots=True)
class SchemaValidator(object):
    """Validates data with given JsonSchema Validator."""

    validator: Draft7Validator = Draft7Validator(schema)

    def __call__(
        self,
        input_data: dict,
    ) -> ResultE[dict]:
        """If is valid return success(input_data) otherwise list of errors."""
        if self.validator.is_valid(input_data):
            return Success(input_data)

        return Failure(
            list(self.validator.iter_errors(input_data)),  # type: ignore
        )
