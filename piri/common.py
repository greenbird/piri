from typing import Any, overload

from attr import dataclass
from returns.result import ResultE, safe
from typing_extensions import Literal, final


@final
@dataclass(frozen=True, slots=True)
class ReadLocalFile(object):
    """Reads local file.

    :param file_path: path to the file to read.
    :type file_path: str

    :parm mode: read mode, r = read string, rb =read bytes.
    :type mode: str

    :return: Success[bytes], Success[str], Failure[Exception]
    :rtype: bytes, str
    """

    @overload
    def __call__(
        self, file_path: str, mode: Literal['r'],
    ) -> ResultE[str]:
        """When 'r' is supplied we return 'str'."""

    @overload  # noqa: WPS440, F811
    def __call__(
        self, file_path: str, mode: Literal['rb'],
    ) -> ResultE[bytes]:
        """When 'rb' is supplied we return 'bytes' instead of a 'str'."""

    @overload  # noqa: WPS440, F811
    def __call__(self, file_path: str, mode: str) -> ResultE[Any]:
        """Any other options might return Any-thing!."""

    @safe  # noqa: WPS440, F811
    def __call__(self, file_path: str, mode: str) -> Any:
        """Open the file and return its contents."""
        with open(file_path, mode) as data_file:
            return data_file.read()
