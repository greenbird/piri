from typing import List

from attr import dataclass
from jsonschema import ValidationError
from returns.result import Failure, Result, Success
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class SchemaValidator(object):
    """Validates data with given JsonSchema Validator."""

    validator: object

    def __call__(
        self,
        schema_data: dict,
    ) -> Result[dict, List[ValidationError]]:
        """If is valid return success(schema_data) otherwise list of errors."""
        if self.validator.is_valid(schema_data):  # type: ignore
            return Success(schema_data)

        return Failure(
            list(self.validator.iter_errors(schema_data)),  # type: ignore
        )
