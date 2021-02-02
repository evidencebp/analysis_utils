
import pytest

from representation_utils import convert_char_to_size, convert_minutes_to_text

@pytest.mark.parametrize(('chars'
                            , 'expected')
    , [
pytest.param(200, "200 b", id='reg1')
, pytest.param(1024, "1.0 KB", id='reg2')
, pytest.param(1024*1024, "1.0 MB", id='reg3')
, pytest.param(1.5*1024*1024, "1.5 MB", id='reg4')
, pytest.param(1.51*1024*1024, "1.5 MB", id='reg4.1')
, pytest.param(2*1024 * 1024, "2.0 MB", id='reg5')
                         ])
def test_convert_char_to_size(chars
                        , expected):

    actual = convert_char_to_size(chars)

    assert actual == expected

@pytest.mark.parametrize(('minutes'
                            , 'expected')
    , [
pytest.param(1, " 1 minute", id='reg1')
, pytest.param(62, " 1 hour, 2 minutes", id='reg2')
, pytest.param(1440 + 183, " 1 day, 3 hours, 3 minutes", id='reg3')
, pytest.param(9*1440 + 183, " 1 week, 2 days, 3 hours, 3 minutes", id='reg4')
, pytest.param(15*1440 + 183, " 2 weeks, 1 day, 3 hours, 3 minutes", id='reg5')
, pytest.param(366*1440 + 183, " 1 year, 1 day, 3 hours, 3 minutes", id='reg6')
, pytest.param(731*1440 + 183, " 2 years, 1 day, 3 hours, 3 minutes", id='reg7')
                         ])
def test_convert_char_to_size(minutes
                        , expected):

    actual = convert_minutes_to_text(minutes)

    assert actual == expected
