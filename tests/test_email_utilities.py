import pytest

from analysis_utils.email_utilities import generate_text_from_template, generate_email_message

@pytest.mark.parametrize(('template'
                         , 'params_dict'
                         , 'expected')
    , [
pytest.param(
        "Dear {name}, I'd like to alert on a potential problem in commit {commit}"
        , {'name' : 'Alan Turing', 'commit' : '1'}
        , "Dear Alan Turing, I'd like to alert on a potential problem in commit 1"
, id='reg1')
, pytest.param(
 "Dear {name}, I'd like to alert on a potential problem in commit {commit}"
 , {'name': 'Alan Turing', 'commit': '1', 'type' : 'Legend'}
 , "Dear Alan Turing, I'd like to alert on a potential problem in commit 1"
 , id='extra_parameter')
                         ])
def test_generate_text_from_template(template
                         , params_dict
                         , expected
                         ):
    actual = generate_text_from_template(template
                         , params_dict
                         )

    assert actual == expected


@pytest.mark.parametrize(('from_user'
                            , 'recipient'
                            , 'subject'
                            , 'body'
                            , 'expected')
    , [
pytest.param(
        "f@mail.com"
        , "t@mail.com"
        , "My important subject"
        , "My important text"
        , 'From: f@mail.com\nTo: [\'t@mail.com\']\nSubject: My important subject\nMime-Version: 1.0;\nContent-Type: text/html; charset="ISO-8859-1";\nContent-Transfer-Encoding: 7bit;\n\n\n<html>\n<body>\nMy important text\n</body>\n</html>\n '
, id='reg1')
                         ])
def test_generate_email_message(from_user : str
                                    , recipient : str
                                    , subject : str
                                    , body : str
                                    , expected
                         ):
    actual = generate_email_message(from_user
                            , recipient
                            , subject
                            , body
                         )

    assert actual == expected

