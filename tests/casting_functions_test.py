# -*- coding: utf-8 -*-

"""Test mapping operation functions."""

from decimal import Decimal

from returns.pipeline import is_successful

from mapmallow.functions import ApplyCasting


class TestCastingInteger(object):
    """Do extensive testing of our int casting functions."""

    _cast = ApplyCasting()

    def test_cast_string(self):
        """Cast a string with numbers to integer."""
        assert self._cast('123', {'to': 'integer'}).unwrap() == 123

    def test_cast_negative_string(self):
        """Cast string with negative number to integer."""
        assert self._cast('-123', {'to': 'integer'}).unwrap() == -123

    def test_cast_decimal_string(self):
        """Cast a decimal string to integer."""
        assert self._cast(
            '123.0',
            {'to': 'integer', 'original_format': 'decimal'},
        ).unwrap() == 123

    def test_cast_negative_decimal_string(self):
        """Cast a negative decimal string to integer."""
        assert self._cast(
            '-123.0', {'to': 'integer', 'original_format': 'decimal'},
        ).unwrap() == -123

    def test_cast_decimal_string_rounds_up(self):
        """Cast a decimal string >= .5 should round up."""
        assert self._cast(
            '123.5',
            {'to': 'integer', 'original_format': 'decimal'},
        ).unwrap() == 124

    def test_cast_decimal_string_rounds_down(self):
        """Cast a decimal string < .0 should round down."""
        assert self._cast(
            '123.49',
            {'to': 'integer', 'original_format': 'decimal'},
        ).unwrap() == 123

    def test_abc_fails(self):
        """Test that string with letters in fails."""
        test = self._cast('abc', {'to': 'integer'})
        assert not is_successful(test)
        assert isinstance(test.failure(), ValueError)
        assert 'Illegal characters in value' in str(test.failure())

    def test_abc_with_decimal_argument_fails(self):
        """Test that string with letters in fails when we supply 'decimal'."""
        test = self._cast(
            'abc',
            {'to': 'integer', 'original_format': 'decimal'},
        )
        assert not is_successful(test)
        assert isinstance(test.failure(), ValueError)
        assert 'Illegal characters in value' in str(test.failure())


class TestCastingDate(object):  # noqa: WPS214 too many methods ok.
    """Test that we cast various date strings to Date."""

    _cast = ApplyCasting()
    _target_after_2000 = '2019-09-07'
    _target_before_2000 = '1994-06-08'

    def test_string_yyyymmdd_no_delimiter(self):
        """Test that yyyymmdd pattern is accepted."""
        assert self._cast(
            '20190907',
            {
                'to': 'date',
                'original_format': 'yyyymmdd',
            },
        ).unwrap() == self._target_after_2000

    def test_string_ddmmyyyy_no_delimiter(self):
        """Test that ddmmyyyy pattern is accepted."""
        assert self._cast(
            '07092019',
            {
                'to': 'date',
                'original_format': 'ddmmyyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyyyy_no_delimiter(self):
        """Test that mmddyyyy pattern is accepted."""
        assert self._cast(
            '09072019',
            {
                'to': 'date',
                'original_format': 'mmddyyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_yyyymmdd_with_hyphen(self):
        """Test that yyyy-mm-dd pattern is accepted."""
        assert self._cast(
            '2019-09-07',
            {
                'to': 'date',
                'original_format': 'yyyy-mm-dd',
            },
        ).unwrap() == self._target_after_2000

    def test_string_yyyymmdd_with_back_slash(self):
        """Test that yyyy/mm/dd pattern is accepted."""
        assert self._cast(
            '2019/09/07',
            {
                'to': 'date',
                'original_format': 'yyyy/mm/dd',
            },
        ).unwrap() == self._target_after_2000

    def test_string_yyyymmdd_with_dots(self):
        """Test that yyyy.mm.dd pattern is accepted."""
        assert self._cast(
            '2019.09.07',
            {
                'to': 'date',
                'original_format': 'yyyy.mm.dd',
            },
        ).unwrap() == self._target_after_2000

    def test_string_ddmmyyyy_with_hyphen(self):
        """Test that dd-mm-yyyy pattern is accepted."""
        assert self._cast(
            '07-09-2019',
            {
                'to': 'date',
                'original_format': 'dd-mm-yyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_ddmmmyyyy_with_back_slash(self):
        """Test that dd/mm/yyyy pattern is accepted."""
        assert self._cast(
            '07/09/2019',
            {
                'to': 'date',
                'original_format': 'dd/mm/yyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_ddmmmyyyy_with_dots(self):
        """Test that dd.mm.yyyy pattern is accepted."""
        assert self._cast(
            '07.09.2019',
            {
                'to': 'date',
                'original_format': 'dd.mm.yyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyyyy_hyphen(self):
        """Test that mm-dd-yyyy pattern is accepted."""
        assert self._cast(
            '09-07-2019',
            {
                'to': 'date',
                'original_format': 'mm-dd-yyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyyyy_back_slash(self):
        """Test that mm/dd/yyyy pattern is accepted."""
        assert self._cast(
            '09/07/2019',
            {
                'to': 'date',
                'original_format': 'mm/dd/yyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyyyy_dots(self):
        """Test that mm.dd.yyyy pattern is accepted."""
        assert self._cast(
            '09.07.2019',
            {
                'to': 'date',
                'original_format': 'mm.dd.yyyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyy_no_delimiter_after_2000(self):
        """Test that mmddyy pattern is accepted."""
        assert self._cast(
            '090719',
            {
                'to': 'date',
                'original_format': 'mmddyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyy_no_delimiter_before_2000(self):
        """Test that mm.dd.yy pattern is accepted."""
        assert self._cast(
            '060894',
            {
                'to': 'date',
                'original_format': 'mmddyy',
            },
        ).unwrap() == self._target_before_2000

    def test_string_yymmdd_no_delimiter_after_2000(self):
        """Test that yymmdd pattern is accepted."""
        assert self._cast(
            '190907',
            {
                'to': 'date',
                'original_format': 'yymmdd',
            },
        ).unwrap() == self._target_after_2000

    def test_string_yymmdd_no_delimiter_before_2000(self):
        """Test that yymmdd pattern is accepted."""
        assert self._cast(
            '940608',
            {
                'to': 'date',
                'original_format': 'yymmdd',
            },
        ).unwrap() == self._target_before_2000

    def test_string_ddmmyy_no_delimiter_after_2000(self):
        """Test that ddmmyy pattern is accepted."""
        assert self._cast(
            '070919',
            {
                'to': 'date',
                'original_format': 'ddmmyy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_ddmmyy_no_delimiter_before_2000(self):
        """Test that ddmmyy pattern is accepted."""
        assert self._cast(
            '080694',
            {
                'to': 'date',
                'original_format': 'ddmmyy',
            },
        ).unwrap() == self._target_before_2000

    def test_string_mmddyy_with_dots_after_2000(self):
        """Test that mm.dd.yy pattern is accepted."""
        assert self._cast(
            '09.07.19',
            {
                'to': 'date',
                'original_format': 'mm.dd.yy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_mmddyy_with_dots_before_2000(self):
        """Test that mm.dd.yy pattern is accepted."""
        assert self._cast(
            '06.08.94',
            {
                'to': 'date',
                'original_format': 'mm.dd.yy',
            },
        ).unwrap() == self._target_before_2000

    def test_string_ddmmyy_with_dots_after_2000(self):
        """Test that dd.mm.yy pattern is accepted."""
        assert self._cast(
            '07.09.19',
            {
                'to': 'date',
                'original_format': 'dd.mm.yy',
            },
        ).unwrap() == self._target_after_2000

    def test_string_ddmmyy_with_dots_before_2000(self):
        """Test that dd.mm.yy pattern is accepted."""
        assert self._cast(
            '08.06.94',
            {
                'to': 'date',
                'original_format': 'dd.mm.yy',
            },
        ).unwrap() == self._target_before_2000

    def test_string_yymmdd_with_dots_after_2000(self):
        """Test that yy.mm.dd pattern is accepted."""
        assert self._cast(
            '19.09.07',
            {
                'to': 'date',
                'original_format': 'yy.mm.dd',
            },
        ).unwrap() == self._target_after_2000

    def test_string_yymmdd_with_dots_before_2000(self):
        """Test that yy.mm.dd pattern is accepted."""
        assert self._cast(
            '94.06.08',
            {
                'to': 'date',
                'original_format': 'yy.mm.dd',
            },
        ).unwrap() == self._target_before_2000

    def test_string_fails_as_invalid_date(self):
        """Test threws ValueError when invalid date passed."""
        test = self._cast(
            '994.06.08',
            {
                'to': 'date',
                'original_format': 'yyy.mm.dd',
            },
        )
        assert not is_successful(test)
        assert isinstance(test.failure(), ValueError)
        assert 'Unable to cast (994.06.08) to ISO date. Exc(Unable to cast to no millennia format: 994.06.08)' in str(  # noqa: E501
            test.failure(),
        )

    def test_string_fails_when_month_out_of_range(self):
        """Test threws ValueError when month out of range."""
        test = self._cast(
            '19.14.12',
            {
                'to': 'date',
                'original_format': 'yy.mm.dd',
            },
        )
        assert not is_successful(test)
        assert isinstance(test.failure(), ValueError)
        assert 'Unable to cast (19.14.12) to ISO date. Exc(month must be in 1..12)' in str(  # noqa: E501
            test.failure(),
        )

    def test_string_fails_when_month_is_not_integer(self):
        """Test threws ValueError when month out of range."""
        test = self._cast(
            '19.MM.12',
            {
                'to': 'date',
                'original_format': 'yy.mm.dd',
            },
        )
        expected = '{0}{1}'.format(
            'Unable to cast (19.MM.12) to ISO date. ',
            "Exc(invalid literal for int() with base 10: '.M')",
        )
        assert not is_successful(test)
        assert isinstance(test.failure(), ValueError)
        assert str(test.failure()) == expected
