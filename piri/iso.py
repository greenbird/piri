from attr import dataclass
from pycountry import countries, currencies, languages
from returns.result import safe
from typing_extensions import final

from piri.constants import ALPHA_THREE, ALPHA_TWO, NAME, NUMERIC, OFFICIAL_NAME


@final
@dataclass(frozen=True, slots=True)
class GetCountryCode(object):
    """Get Country code from string."""

    # dependiencies, country package
    _countries = countries
    _get = safe(countries.get)

    @safe
    def __call__(self, code: str) -> dict:
        """Find country by code or name."""
        code = str(code).strip()
        country = self._countries.get(alpha_2=code.upper())
        country = country or self._countries.get(alpha_3=code.upper())
        country = country or self._countries.get(numeric=code.zfill(3))
        country = country or self._countries.get(name=code)
        country = country or self._countries.get(official_name=code)

        if not country:
            raise ValueError(
                '{message}({country})'.format(
                    message='Could not find country matching value',
                    country=code,
                ),
            )

        return {
            ALPHA_TWO: country.alpha_2.upper(),
            ALPHA_THREE: country.alpha_3.upper(),
            NAME: country.name,
            NUMERIC: country.numeric,
            OFFICIAL_NAME: self._get_official_name(country).value_or(None),
        }

    @safe
    def _get_official_name(self, country) -> str:
        return country.official_name


@final
@dataclass(frozen=True, slots=True)
class GetCurrencyCode(object):
    """Get Currency code from string."""

    # dependiencies, country package
    _currencies = currencies
    _get = currencies.get

    @safe
    def __call__(self, code: str) -> dict:
        """Try to create a Currency object."""
        code = str(code).strip()

        cur = self._currencies.get(alpha_3=code.upper())
        cur = cur or self._currencies.get(numeric=code.zfill(3))
        cur = cur or self._currencies.get(name=code)

        if not cur:
            raise ValueError(
                '{message}({code})'.format(
                    message='Could not find currency matching code',
                    code=code,
                ),
            )

        return {
            ALPHA_THREE: cur.alpha_3.upper(),
            NUMERIC: cur.numeric,
            NAME: cur.name,
        }


@final
@dataclass(frozen=True, slots=True)
class GetLanguageCode(object):
    """SRO to get language code."""

    _languages = languages

    @safe
    def __call__(self, code: str) -> dict:
        """Try to create a Language object."""
        code = str(code).strip()
        lan = self._languages.get(alpha_2=code.lower())
        lan = lan or self._languages.get(alpha_3=code.lower())
        lan = lan or self._languages.get(name=code)

        if not lan:
            raise ValueError(
                '{message}({code})'.format(
                    message='Could not find language matching value',
                    code=code,
                ),
            )
        return {
            ALPHA_TWO: lan.alpha_2.upper(),
            ALPHA_THREE: lan.alpha_3.upper(),
            NAME: lan.name,
            'scope': lan.scope,
            'type': lan.type,
        }
