import datetime
import decimal
import re
from typing import Callable, Optional

from attr import dataclass
from returns.pipeline import flow
from returns.pointfree import alt, bind, map_, rescue
from returns.result import Failure, ResultE, safe
from typing_extensions import final

from piri.constants import (
    COMMA,
    DATE,
    DECIMAL,
    EMPTY,
    INTEGER,
    INTEGER_CONTAINING_DECIMALS,
    PERIOD,
)
from piri.valuetypes import MapValue


@safe
def get_casting_function(cast_to: str) -> Callable:
    """Return casting function depending on name."""
    if cast_to == INTEGER:
        return CastToInteger()

    elif cast_to == DECIMAL:
        return CastToDecimal()

    elif cast_to == DATE:
        return CastToDate()

    raise NotImplementedError(
        'Unsupported cast to value ({0})'.format(cast_to),
    )


@final
@dataclass(frozen=True, slots=True)
class CastToDecimal(object):
    """Cast input to decimal."""

    _decimal_pattern = re.compile(r'^([0-9]|-|\.|,)+$')
    _decimal_with_period_after_commas = re.compile(r'^-?(\d+\,)*\d+\.\d+$')
    _decimal_with_comma_after_periods = re.compile(r'^-?(\d+\.)*\d+\,\d+$')

    @safe
    def __call__(
        self,
        value_to_cast: MapValue,
        original_format: Optional[str] = None,
    ) -> decimal.Decimal:
        """Make this object callable."""
        the_value = str(value_to_cast).replace(' ', EMPTY)

        if not self._decimal_pattern.match(the_value):
            raise ValueError(
                "Illegal characters in value '{0}'".format(the_value),
            )

        if original_format == INTEGER_CONTAINING_DECIMALS:
            return decimal.Decimal(the_value) / 100

        # ie 1234567,89 only comma as decimal separator
        if the_value.count(COMMA) == 1 and not the_value.count(PERIOD):
            return decimal.Decimal(the_value.replace(COMMA, PERIOD))

        # ie 1,234,567.89 many commas followed by one period
        if self._decimal_with_period_after_commas.match(the_value):
            return decimal.Decimal(the_value.replace(COMMA, EMPTY))

        # ie 1.234.567,89 many periods followed by one comma
        if self._decimal_with_comma_after_periods.match(the_value):
            return decimal.Decimal(
                the_value.replace(PERIOD, EMPTY).replace(COMMA, PERIOD),
            )

        return decimal.Decimal(the_value)


@final
@dataclass(frozen=True, slots=True)
class CastToInteger(object):
    """Cast input to integer."""

    _cast_to_decimal = CastToDecimal()

    def __call__(
        self,
        value_to_cast: MapValue,
        original_format: Optional[str] = None,
    ) -> ResultE[int]:
        """Make this object callable."""
        return flow(
            value_to_cast,
            self._cast_to_decimal,
            map_(quantize_decimal),
            map_(int),
        )


def quantize_decimal(number: decimal.Decimal) -> decimal.Decimal:
    """Quantize a decimal to whole number."""
    return number.quantize(decimal.Decimal('1.'))


@final
@dataclass(frozen=True, slots=True)
class CastToDate(object):
    """Cast input to date."""

    _yymmdd_pattern = re.compile(r'^yy[^\w]?mm[^\w]?dd$')
    _ddmmyy_pattern = re.compile(r'^dd[^\w]?mm[^\w]?yy$')
    _mmddyy_pattern = re.compile(r'^mm[^\w]?dd[^\w]?yy$')

    _mmddyyyy_pattern = re.compile(r'^mm[^\w]?dd[^\w]?yyyy$')
    _ddmmyyyy_pattern = re.compile(r'^dd[^\w]?mm[^\w]?yyyy$')
    _yyyymmdd_pattern = re.compile(r'^yyyy[^\w]?mm[^\w]?dd$')
    _iso_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')

    _error_message = 'Unable to cast ({value}) to ISO date. Exc({failure})'

    # @pipeline(ResultE)
    def __call__(
        self,
        value_to_cast: MapValue,
        original_format: str,
    ) -> ResultE[MapValue]:
        r"""
        purpose: Convert string date into ISO format date.

        :input value_to_cast: the string to be converted to a date
        :input original_format: a string describing the format the data string
                             is before convertion.
        :raises ValueError:  when not able to convert or value_to_cast
                             does not match original_format.
        regex_tips  ^ = start of string
                    $ = end of string
                    [^[0-9]] = matches anything not [0-9]
                    [^\d] = matches anything not digits
                    \d = matches digits
                    {n} = matches previous match n amount of times
                    () = grouper, groups up stuff for use in replace.
        """
        date_value: str = str(value_to_cast)
        return flow(
            date_value,
            self._value_is_iso,
            rescue(  # type: ignore
                lambda _: self._cast_with_millennia(
                    date_value,
                    original_format=original_format,
                ),
            ),
            rescue(  # type: ignore
                lambda _: self._cast_with_no_millennia(
                    date_value,
                    original_format=original_format,
                ),
            ),
            bind(self._validate_date),
            alt(  # type: ignore
                lambda failure: ValueError(
                    self._error_message.format(
                        value=date_value,
                        failure=failure,
                    ),
                ),
            ),
        )

    @safe
    def _value_is_iso(self, value_to_cast: str) -> str:
        if self._iso_pattern.match(value_to_cast):
            return value_to_cast
        raise ValueError('Unable to cast to ISO date')

    def _cast_with_millennia(
        self,
        value_to_cast: str,
        original_format: str,
    ) -> ResultE[str]:
        # mm[.]dd[.]yyyy any separator
        if self._mmddyyyy_pattern.match(original_format):
            return self._apply_regex_sub(
                r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{4})',
                r'\3-\1-\2',
                value_to_cast,
            )

        # dd[.]mm[.]yyyy any separator
        if self._ddmmyyyy_pattern.match(original_format):
            return self._apply_regex_sub(
                r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{4})',
                r'\3-\2-\1',
                value_to_cast,
            )

        # yyyy[.]mm[.]dd any separator
        if self._yyyymmdd_pattern.match(original_format):
            return self._apply_regex_sub(
                r'(\d{4})[^\w]?(\d{2})[^\w]?(\d{2})',
                r'\1-\2-\3',
                value_to_cast,
            )

        return Failure(
            ValueError(
                'Unable to case to milennia format: {value}'.format(
                    value=value_to_cast,
                ),
            ),
        )

    def _cast_with_no_millennia(
        self,
        value_to_cast: str,
        original_format: str,
    ) -> ResultE[str]:
        no_millenia_patterns = {
            self._yymmdd_pattern: (
                r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{2})',
                r'\3\2\1',
            ),
            self._ddmmyy_pattern: (
                r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{2})',
                r'\1\2\3',
            ),
            self._mmddyy_pattern: (
                r'(\d{2})[^\w]?(\d{2})[^\w]?(\d{2})',
                r'\2\1\3',
            ),
        }
        for no_millenia_pattern in no_millenia_patterns:  # noqa: WPS528
            if no_millenia_pattern.match(original_format):
                pattern, arrangement = no_millenia_patterns[no_millenia_pattern]
                return self._apply_regex_sub(
                    pattern, arrangement, value_to_cast,
                ).bind(
                    self._convert_ddmmyy_to_iso_date,
                )

        return Failure(
            ValueError(
                'Unable to cast to no millennia format: {value}'.format(
                    value=value_to_cast,
                ),
            ),
        )

    @safe
    def _validate_date(self, date_string: str) -> str:
        return datetime.date(
            *map(
                int,
                date_string.split('-'),
            ),
        ).isoformat()

    @safe
    def _apply_regex_sub(
        self,
        pattern: str,
        arrangement: str,
        input_string: str,
    ) -> str:
        return re.sub(pattern, arrangement, input_string)

    @safe  # noqa: WPS210, Hard to reduce variables
    def _convert_ddmmyy_to_iso_date(  # noqa: WPS210
        self,
        date_string: str,
    ) -> str:

        in_day = int(date_string[:2])
        in_month = int(date_string[2:4])
        in_year = int(date_string[4:6])

        today = datetime.date.today()
        # think of this 'century' variable as century - 1. as in:
        # 2018 = 2000, 1990 = 1900
        century = (today.year // 100) * 100
        # yy = last two digits of year. 2018 = 18, 1990 = 90
        yy = today.year % 100
        if in_year > yy:
            century -= 100
        year = century + in_year
        date_obj = datetime.date(year, in_month, in_day)

        return date_obj.isoformat()
