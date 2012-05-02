from mock import patch
import logging
import congressbot


@patch('congressbot.house_collection')
@patch('congressbot.Reddit')
def test_feed_parse(reddit_mock, house_mock):
    house_mock.find_one.return_value = False
    congressbot.parse()
    assert False
