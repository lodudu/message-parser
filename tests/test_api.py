import json
import pytest

from api import app


@pytest.fixture
def client():
    return app.app.test_client()


def test_get_parsed_message(client):
    res = client.get('/parsed_message?message=@bob')

    expected = {
                    "mentions": ["bob"]
                }
    assert json.loads(res.data) == expected

    res = client.get('/parsed_message?message=(omg)')

    expected = {
                    "emoticons": ["omg"]
                }
    assert json.loads(res.data) == expected

    res = client.get('/parsed_message?message=http://www.google.com')

    expected = {
                "links":
                [
                    {
                        "url": "http://www.google.com",
                        "title": "Google"
                    }
                ]
                }
    assert json.loads(res.data) == expected

    res = client.get('/parsed_message?message=@bob @john (omg) refer to https://www.google.com')
    expected = {
                "mentions": ["bob", "john"],
                "emoticons": ["omg"],
                "links":
                [
                    {
                        "url": "https://www.google.com",
                        "title": "Google"
                    }
                ]
                }
    assert json.loads(res.data) == expected
