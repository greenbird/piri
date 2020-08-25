import pytest
from returns.primitives.exceptions import UnwrapFailedError

from piri.iso import GetCountryCode, GetCurrencyCode, GetLanguageCode


class TestGetCountryCode(object):
    """Test FetchDataByKeys function.

    Norway, NO, NOR, 578
    Albania, AL, ALB, 008
    """

    _get = GetCountryCode()

    def test(self):
        """Test that we can fetch key in dict."""
        assert self._get('NO').unwrap()['alpha_2'] == 'NO'

    def test_no_official_name(self):
        """Some countries does not have official name.

        We should be able to get these and official_name should be `None`
        """
        assert self._get('CA').unwrap()['official_name'] is None

    def test_by_numeric(self):
        """Test that we can fetch currency by numeric value."""
        assert self._get('578').unwrap()['numeric'] == '578'

    def test_by_numeric_int(self):
        """Test get by numeric with integer."""
        assert self._get(578).unwrap()['numeric'] == '578'  # noqa: Z432

    def test_by_numeric_below_hundred(self):
        """Test get by numeric with number < 100."""
        assert self._get('8').unwrap()['numeric'] == '008'

    def test_by_name(self):
        """Test getting by name."""
        assert self._get('Norway').unwrap()['name'] == 'Norway'

    def test_by_official_name(self):
        """Test getting by official name."""
        test_value = self._get('Kingdom of Norway').unwrap()['official_name']
        assert test_value == 'Kingdom of Norway'


class TestGetCountryCodeRaises(object):
    """Test GetCountryCode function raises with bad data."""

    _get = GetCountryCode()

    def test_bad_code(self):
        """Assert raises with bad name."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('Noway').unwrap()

    def test_bad_numeric(self):
        """Assert raises with bad numeric value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get(123).unwrap()  # noqa: Z432

    def test_bad_alpha_two(self):
        """Assert raises with bad alpha 2 value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('XX').unwrap()

    def test_bad_alpha_three(self):
        """Assert raises with bad alpha 3 value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('XXX').unwrap()


class TestGetCurrencyCode(object):
    """Test FetchDataByKeys function."""

    _get = GetCurrencyCode()

    def test_by_alpha_three_upper(self):
        """Get currency by alpha 3 code."""
        assert self._get('NOK').unwrap()['alpha_3'] == 'NOK'

    def test_by_alpha_three_lower(self):
        """Get currency by alpha 3 lower cased."""
        assert self._get('nok').unwrap()['alpha_3'] == 'NOK'

    def test_by_numeric(self):
        """Test that we can fetch currency by numeric value."""
        assert self._get('578').unwrap()['alpha_3'] == 'NOK'

    def test_by_numeric_int(self):
        """Test get by numeric with integer."""
        assert self._get(578).unwrap()['alpha_3'] == 'NOK'  # noqa: Z432

    def test_by_numeric_below_hundred(self):
        """Test get by numeric with number < 100."""
        assert self._get('8').unwrap()['alpha_3'] == 'ALL'

    def test_by_name(self):
        """Test getting by name."""
        assert self._get('Norwegian Krone').unwrap()['alpha_3'] == 'NOK'


class TestGetCurrencyCodeRaises(object):
    """Test GetCountryCode function raises with bad data."""

    _get = GetCurrencyCode()

    def test_bad_code(self):
        """Assert raises with bad name."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('Noway').unwrap()

    def test_bad_numeric(self):
        """Assert raises with bad numeric value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get(123).unwrap()  # noqa: Z432

    def test_bad_alpha_two(self):
        """Assert raises with bad alpha 2 value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('XX').unwrap()

    def test_bad_alpha_three(self):
        """Assert raises with bad alpha 3 value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('NAN').unwrap()


class TestGetLanguageCode(object):
    """Test FetchDataByKeys function."""

    _get = GetLanguageCode()

    def test_by_alpha_two(self):
        """Test that we can fetch key in dict."""
        assert self._get('NO').unwrap()['alpha_3'] == 'NOR'

    def test_by_alpha_three(self):
        """Test that we can fetch key in dict."""
        assert self._get('NOR').unwrap()['alpha_3'] == 'NOR'

    def test_by_name(self):
        """Test getting by name."""
        assert self._get('Norwegian').unwrap()['alpha_3'] == 'NOR'


class TestGetLanguageCodeRaises(object):
    """Test GetLanguageCode function raises with bad data."""

    _get = GetLanguageCode()

    def test_bad_code(self):
        """Assert raises with bad name."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('somelanguage').unwrap()

    def test_bad_alpha_two(self):
        """Assert raises with bad alpha 2 value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('XX').unwrap()

    def test_bad_alpha_three(self):
        """Assert raises with bad alpha 3 value."""
        with pytest.raises(UnwrapFailedError):
            assert self._get('XXX').unwrap()
