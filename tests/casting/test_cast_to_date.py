from returns.pipeline import is_successful
from typing_extensions import Final

from mapmallow.casting import CastToDate

target_after_2000: Final['str'] = '2019-09-07'
target_before_2000: Final['str'] = '1994-06-08'


def test_string_yyyymmdd_no_delimiter():
    """Test that yyyymmdd pattern is accepted."""
    assert CastToDate()(
        '20190907',
        'yyyymmdd',
    ).unwrap() == target_after_2000


def test_string_ddmmyyyy_no_delimiter():
    """Test that ddmmyyyy pattern is accepted."""
    assert CastToDate()(
        '07092019',
        'ddmmyyyy',
    ).unwrap() == target_after_2000


def test_string_mmddyyyy_no_delimiter():
    """Test that mmddyyyy pattern is accepted."""
    assert CastToDate()(
        '09072019',
        'mmddyyyy',
    ).unwrap() == target_after_2000


def test_string_yyyymmdd_with_hyphen():
    """Test that yyyy-mm-dd pattern is accepted."""
    assert CastToDate()(
        '2019-09-07',
        'yyyy-mm-dd',
    ).unwrap() == target_after_2000


def test_string_yyyymmdd_with_back_slash():
    """Test that yyyy/mm/dd pattern is accepted."""
    assert CastToDate()(
        '2019/09/07',
        'yyyy/mm/dd',
    ).unwrap() == target_after_2000


def test_string_yyyymmdd_with_dots():
    """Test that yyyy.mm.dd pattern is accepted."""
    assert CastToDate()(
        '2019.09.07',
        'yyyy.mm.dd',
    ).unwrap() == target_after_2000


def test_string_ddmmyyyy_with_hyphen():
    """Test that dd-mm-yyyy pattern is accepted."""
    assert CastToDate()(
        '07-09-2019',
        'dd-mm-yyyy',
    ).unwrap() == target_after_2000


def test_string_ddmmmyyyy_with_back_slash():
    """Test that dd/mm/yyyy pattern is accepted."""
    assert CastToDate()(
        '07/09/2019',
        'dd/mm/yyyy',
    ).unwrap() == target_after_2000


def test_string_ddmmmyyyy_with_dots():
    """Test that dd.mm.yyyy pattern is accepted."""
    assert CastToDate()(
        '07.09.2019',
        'dd.mm.yyyy',
    ).unwrap() == target_after_2000


def test_string_mmddyyyy_hyphen():
    """Test that mm-dd-yyyy pattern is accepted."""
    assert CastToDate()(
        '09-07-2019',
        'mm-dd-yyyy',
    ).unwrap() == target_after_2000


def test_string_mmddyyyy_back_slash():
    """Test that mm/dd/yyyy pattern is accepted."""
    assert CastToDate()(
        '09/07/2019',
        'mm/dd/yyyy',
    ).unwrap() == target_after_2000


def test_string_mmddyyyy_dots():
    """Test that mm.dd.yyyy pattern is accepted."""
    assert CastToDate()(
        '09.07.2019',
        'mm.dd.yyyy',
    ).unwrap() == target_after_2000


def test_string_mmddyy_no_delimiter_after_2000():
    """Test that mmddyy pattern is accepted."""
    assert CastToDate()(
        '090719',
        'mmddyy',
    ).unwrap() == target_after_2000


def test_string_mmddyy_no_delimiter_before_2000():
    """Test that mm.dd.yy pattern is accepted."""
    assert CastToDate()(
        '060894',
        'mmddyy',
    ).unwrap() == target_before_2000


def test_string_yymmdd_no_delimiter_after_2000():
    """Test that yymmdd pattern is accepted."""
    assert CastToDate()(
        '190907',
        'yymmdd',
    ).unwrap() == target_after_2000


def test_string_yymmdd_no_delimiter_before_2000():
    """Test that yymmdd pattern is accepted."""
    assert CastToDate()(
        '940608',
        'yymmdd',
    ).unwrap() == target_before_2000


def test_string_ddmmyy_no_delimiter_after_2000():
    """Test that ddmmyy pattern is accepted."""
    assert CastToDate()(
        '070919',
        'ddmmyy',
    ).unwrap() == target_after_2000


def test_string_ddmmyy_no_delimiter_before_2000():
    """Test that ddmmyy pattern is accepted."""
    assert CastToDate()(
        '080694',
        'ddmmyy',
    ).unwrap() == target_before_2000


def test_string_mmddyy_with_dots_after_2000():
    """Test that mm.dd.yy pattern is accepted."""
    assert CastToDate()(
        '09.07.19',
        'mm.dd.yy',
    ).unwrap() == target_after_2000


def test_string_mmddyy_with_dots_before_2000():
    """Test that mm.dd.yy pattern is accepted."""
    assert CastToDate()(
        '06.08.94',
        'mm.dd.yy',
    ).unwrap() == target_before_2000


def test_string_ddmmyy_with_dots_after_2000():
    """Test that dd.mm.yy pattern is accepted."""
    assert CastToDate()(
        '07.09.19',
        'dd.mm.yy',
    ).unwrap() == target_after_2000


def test_string_ddmmyy_with_dots_before_2000():
    """Test that dd.mm.yy pattern is accepted."""
    assert CastToDate()(
        '08.06.94',
        'dd.mm.yy',
    ).unwrap() == target_before_2000


def test_string_yymmdd_with_dots_after_2000():
    """Test that yy.mm.dd pattern is accepted."""
    assert CastToDate()(
        '19.09.07',
        'yy.mm.dd',
    ).unwrap() == target_after_2000


def test_string_yymmdd_with_dots_before_2000():
    """Test that yy.mm.dd pattern is accepted."""
    assert CastToDate()(
        '94.06.08',
        'yy.mm.dd',
    ).unwrap() == target_before_2000


def test_string_fails_as_invalid_date():
    """Test threws ValueError when invalid date passed."""
    test = CastToDate()(
        '994.06.08',
        'yyy.mm.dd',
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Unable to cast (994.06.08) to ISO date. Exc(Unable to cast to no millennia format: 994.06.08)' in str(  # noqa: E501
        test.failure(),
    )


def test_string_fails_when_month_out_of_range():
    """Test threws ValueError when month out of range."""
    test = CastToDate()(
        '19.14.12',
        'yy.mm.dd',
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert 'Unable to cast (19.14.12) to ISO date. Exc(month must be in 1..12)' in str(  # noqa: E501
        test.failure(),
    )


def test_string_fails_when_month_is_not_integer():
    """Test threws ValueError when month out of range."""
    test = CastToDate()(
        '19.MM.12',
        'yy.mm.dd',
    )
    expected = '{0}{1}'.format(
        'Unable to cast (19.MM.12) to ISO date. ',
        "Exc(invalid literal for int() with base 10: '.M')",
    )
    assert not is_successful(test)
    assert isinstance(test.failure(), ValueError)
    assert str(test.failure()) == expected
