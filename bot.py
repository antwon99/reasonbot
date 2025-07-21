"""ReasonBot Main Dispatcher

This module listens for @mentions on Twitter, pulls context from the tagged tweet
(and optionally prior tweets from the author), and passes the data into the analyzer
and replier modules to generate a strategic response.

Primary function: check_mentions()
"""

from __future__ import annotations

import os
from typing import List

import tweepy
from dotenv import load_dotenv


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

    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    user_id = os.getenv("TWITTER_USER_ID")

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


if __name__ == "__main__":
    check_mentions()
