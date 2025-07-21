"""Tests for ReasonBot Core Logic

This file contains unit tests and simple integration tests for core ReasonBot functions,
especially in bot.py and analyzer.py. Ensure all responses are well-formed, compliant,
and trigger only under expected conditions.
"""

from unittest.mock import MagicMock, patch
import os
import sys
from pathlib import Path

# Ensure the project root is on the import path so `bot` can be imported during tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import bot


def test_check_mentions_outputs_text(capsys):
    """check_mentions() should print tweet text and return the tweet objects."""

    mock_tweet = MagicMock(id=123, text="hello world")
    mock_response = MagicMock(data=[mock_tweet])

    with patch("bot.tweepy.Client") as MockClient, patch("bot.load_dotenv"), patch.dict(
        os.environ,
        {"TWITTER_BEARER_TOKEN": "token", "TWITTER_USER_ID": "1"},
    ):
        instance = MockClient.return_value
        instance.get_users_mentions.return_value = mock_response

        tweets = bot.check_mentions(1)

        captured = capsys.readouterr()

        assert "hello world" in captured.out
        assert tweets == [mock_tweet]
        instance.get_users_mentions.assert_called_once_with(id="1", max_results=1)
