import mock

from api.message import Message


def test_username_parser():
    message = Message("@tom")
    assert message.mentions == ["tom"]

    message = Message("@john_doe @jimmy123 test message")
    assert message.mentions == ["john_doe", "jimmy123"]

    message = Message("@#%$$#!@ @@%!")
    assert message.mentions == []


@mock.patch("api.message.Message._get_supported_emoticons")
def test_emoticon_parser(mock_get):
    mock_get.return_value = ["smile", "nod"]

    message = Message("(sssmile) [smile] (kneel)")
    assert message.emoticons == []

    message = Message("(smile) (smile) (invalid) (nod)")
    assert message.emoticons == ["smile", "smile", "nod"]


@mock.patch("api.message.Message._get_title")
def test_link_parser(mock_get):
    mock_get.return_value = "a test title"

    message = Message("http://www.google.com")
    link = {
            "url": "http://www.google.com",
            "title": "a test title"
            }
    assert message.links == [link]

    message = Message("http://www.url1.com  https://www.url2.com")
    links = [
        {
            "url": "http://www.url1.com",
            "title": "a test title"
        },
        {
            "url": "https://www.url2.com",
            "title": "a test title"
            }
        ]
    assert message.links == links
