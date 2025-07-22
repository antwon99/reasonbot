"""ReasonBot Main Dispatcher

This module listens for @mentions on Twitter, pulls context from the tagged tweet
(and optionally prior tweets from the author), and passes the data into the
analyzer and replier modules to generate a strategic response.

Primary functions:
- :func:`check_mentions` – fetches recent @mentions
- :func:`dispatch` – full pipeline to analyze, reply, and avoid duplicates
"""

from __future__ import annotations

from typing import List
from pathlib import Path

import analyzer
import replier

import tweepy
from dotenv import load_dotenv
from utils import (
    get_env_var,
    is_rate_limited,
    load_processed_ids,
    save_processed_id,
)

# Local cache of tweets we've replied to
PROCESSED_FILE = Path("processed_ids.txt")


def check_mentions(count: int = 5) -> List[tweepy.tweet.Tweet]:
    """Fetch and print recent mentions of @ReasonBot.

    Parameters
    ----------
    count:
        The maximum number of tweets to retrieve and print.

    Returns
    -------
    List[tweepy.tweet.Tweet]
        The Tweet objects returned by the Twitter API.
    """

    # Load environment variables from a .env file for local development
    load_dotenv()

    bearer_token = get_env_var("TWITTER_BEARER_TOKEN")
    user_id = get_env_var("TWITTER_USER_ID")

    if not bearer_token or not user_id:
        print(
            "Twitter credentials are missing. Please set TWITTER_BEARER_TOKEN and "
            "TWITTER_USER_ID."
        )
        return []

    client = tweepy.Client(bearer_token=bearer_token)

    # Request the most recent mentions for the configured user ID
    response = client.get_users_mentions(id=user_id, max_results=count)
    tweets = response.data or []

    for tweet in tweets:
        # Each tweet object contains the id and text fields
        print(f"{tweet.id}: {tweet.text}")

    return tweets


def dispatch(count: int = 5, cooldown: int | None = None) -> None:
    """Process new mentions and post replies.

    This high-level dispatcher wires together the analyzer and replier modules.
    It also keeps a simple file-based cache of tweet IDs so we don't reply twice
    to the same mention across runs.

    Parameters
    ----------
    count:
        Number of @mentions to fetch and potentially reply to.
    cooldown:
        If provided, minimum seconds between successful dispatch runs.
    """

    load_dotenv()

    if cooldown and is_rate_limited(PROCESSED_FILE.with_suffix(".lock"), cooldown):
        print("Cooldown active. Skipping dispatch.")
        return

    processed = load_processed_ids(PROCESSED_FILE)

    tweets = check_mentions(count)

    if not tweets:
        return

    # Collect credentials required for posting a reply
    creds = {
        "bearer_token": get_env_var("TWITTER_BEARER_TOKEN"),
        "consumer_key": get_env_var("TWITTER_API_KEY"),
        "consumer_secret": get_env_var("TWITTER_API_SECRET"),
        "access_token": get_env_var("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": get_env_var("TWITTER_ACCESS_SECRET"),
    }

    if not all(creds.values()):
        print("Missing Twitter credentials for posting replies.")
        return

    client = tweepy.Client(**creds)

    for tweet in tweets:
        if str(tweet.id) in processed:
            continue

        try:
            context = analyzer.analyze_context(tweet.text)
            reply_text = replier.generate_reply(context, tweet.text)
            client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet.id)
            processed.add(str(tweet.id))
            save_processed_id(PROCESSED_FILE, str(tweet.id))
        except Exception as exc:  # keep loop going even if one tweet fails
            print(f"Error replying to {tweet.id}: {exc}")


if __name__ == "__main__":
    dispatch()
