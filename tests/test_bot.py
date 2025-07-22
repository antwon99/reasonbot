"""Tests for ReasonBot Core Logic

This file contains unit tests and simple integration tests for core ReasonBot functions,
especially in bot.py and analyzer.py. Ensure all responses are well-formed, compliant,
and trigger only under expected conditions.
"""

from unittest.mock import MagicMock, patch
import os
import sys
from pathlib import Path
import openai

# Ensure the project root is on the import path so `bot` can be imported during tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import bot  # noqa: E402


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


def test_dispatch_posts_replies(tmp_path):
    """dispatch() should create tweets only for new mentions."""

    mock_tweet = MagicMock(id=1, text="hi")

    cache_file = tmp_path / "ids.txt"

    with patch("bot.PROCESSED_FILE", cache_file), patch(
        "bot.check_mentions", return_value=[mock_tweet]
    ), patch(
        "bot.analyzer.analyze_context", return_value={"reply_tone": "calm"}
    ), patch(
        "bot.replier.generate_reply", return_value="ok"
    ), patch(
        "bot.tweepy.Client"
    ) as MockClient, patch(
        "bot.load_dotenv"
    ), patch.dict(
        os.environ,
        {
            "TWITTER_BEARER_TOKEN": "token",
            "TWITTER_USER_ID": "1",
            "TWITTER_API_KEY": "a",
            "TWITTER_API_SECRET": "b",
            "TWITTER_ACCESS_TOKEN": "c",
            "TWITTER_ACCESS_SECRET": "d",
        },
    ):
        client_instance = MockClient.return_value

        bot.dispatch(1)
        client_instance.create_tweet.assert_called_once_with(
            text="ok", in_reply_to_tweet_id=1
        )
        assert cache_file.read_text().strip() == "1"

        client_instance.create_tweet.reset_mock()
        bot.dispatch(1)
        client_instance.create_tweet.assert_not_called()


def test_dispatch_respects_cooldown(tmp_path):
    """dispatch() should exit early when rate limited."""

    cache_file = tmp_path / "ids.txt"

    with patch("bot.PROCESSED_FILE", cache_file), patch(
        "bot.is_rate_limited", return_value=True
    ) as mock_rate, patch("bot.check_mentions") as check, patch(
        "bot.load_dotenv"
    ), patch.dict(
        os.environ,
        {
            "TWITTER_BEARER_TOKEN": "token",
            "TWITTER_USER_ID": "1",
            "TWITTER_API_KEY": "a",
            "TWITTER_API_SECRET": "b",
            "TWITTER_ACCESS_TOKEN": "c",
            "TWITTER_ACCESS_SECRET": "d",
        },
    ), patch(
        "bot.tweepy.Client"
    ) as MockClient:
        bot.dispatch(1, cooldown=10)
        mock_rate.assert_called_once()
        check.assert_not_called()
        MockClient.assert_not_called()


def test_dispatch_missing_twitter_credentials(tmp_path):
    """dispatch() should exit if credentials for posting are missing."""
    mock_tweet = MagicMock(id=1, text="hi")
    cache_file = tmp_path / "ids.txt"

    with patch("bot.PROCESSED_FILE", cache_file), patch(
        "bot.check_mentions",
        return_value=[mock_tweet],
    ), patch("bot.load_processed_ids", return_value=set()), patch(
        "bot.load_dotenv"
    ), patch.dict(
        os.environ,
        {
            "TWITTER_BEARER_TOKEN": "token",
            "TWITTER_USER_ID": "1",
            # Missing posting keys
        },
        clear=True,
    ), patch(
        "bot.tweepy.Client"
    ) as MockClient, patch(
        "builtins.print"
    ) as p:
        bot.dispatch(1)
        p.assert_any_call("Missing Twitter credentials for posting replies.")
        MockClient.assert_not_called()


def test_dispatch_handles_openai_error(tmp_path):
    """Errors from analyzer or replier should be caught and logged."""
    mock_tweet = MagicMock(id=1, text="hi")
    cache_file = tmp_path / "ids.txt"

    with patch("bot.PROCESSED_FILE", cache_file), patch(
        "bot.check_mentions",
        return_value=[mock_tweet],
    ), patch(
        "bot.analyzer.analyze_context",
        side_effect=openai.OpenAIError("boom"),
    ), patch(
        "bot.replier.generate_reply"
    ) as gen_reply, patch(
        "bot.load_processed_ids",
        return_value=set(),
    ), patch(
        "bot.save_processed_id"
    ) as save_id, patch(
        "bot.load_dotenv"
    ), patch.dict(
        os.environ,
        {
            "TWITTER_BEARER_TOKEN": "token",
            "TWITTER_USER_ID": "1",
            "TWITTER_API_KEY": "a",
            "TWITTER_API_SECRET": "b",
            "TWITTER_ACCESS_TOKEN": "c",
            "TWITTER_ACCESS_SECRET": "d",
        },
    ), patch(
        "bot.tweepy.Client"
    ) as MockClient, patch(
        "builtins.print"
    ) as p:
        client_instance = MockClient.return_value

        bot.dispatch(1)

        gen_reply.assert_not_called()
        client_instance.create_tweet.assert_not_called()
        save_id.assert_not_called()
        p.assert_any_call("Error replying to 1: boom")
