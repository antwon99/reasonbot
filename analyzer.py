"""ReasonBot Context Analyzer

This module processes tweet content to determine sentiment, tone, and rhetorical
intent using an LLM or local NLP tools. It classifies ideology, detects slurs,
and recommends a tone for the response.

Primary function: analyze_context(tweet_text: str) -> dict
"""

from __future__ import annotations

import os
from typing import Any, Dict
import json

from dotenv import load_dotenv
import openai
import backoff


@backoff.on_exception(backoff.expo, openai.OpenAIError, max_tries=3)
def _chat_completion(client: openai.OpenAI, prompt: str):
    """Call the OpenAI chat completion API with retries."""

    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )


def analyze_context(tweet_text: str) -> Dict[str, Any]:
    """Analyze a tweet and return structured context data.

    Parameters
    ----------
    tweet_text:
        The content of the tweet that summoned ReasonBot.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the detected tone, ideology, emotion,
        whether the text contains a slur, and a recommended reply tone.
    """

    # Pull credentials from the environment. This keeps API keys out of source
    # code and allows developers to configure them locally via a .env file.
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print(
            "Missing OPENAI_API_KEY. Returning fallback analysis while we wait "
            "for credentials."
        )
        return {
            "tone": "neutral",
            "ideology": "unknown",
            "emotion": "neutral",
            "contains_slur": False,
            "reply_tone": "calm",
        }

    try:
        # Configure the OpenAI client. The library switched to a client-based
        # interface in v1.0 but still supports the old global methods. Using the
        # client keeps compatibility forward-looking.
        client = openai.OpenAI(api_key=api_key)

        # We ask the model to classify the tweet and respond in a compact JSON
        # format. Keeping the prompt short helps reduce latency and token usage.
        prompt = (
            "Classify the following tweet in JSON with the keys: tone, ideology, "
            "emotion, contains_slur (true/false), reply_tone. Respond only with "
            "JSON. Tweet: "
            f"{tweet_text}"
        )

        response = _chat_completion(client, prompt)

        # The API returns a list of choices; we take the first message content.
        content = response.choices[0].message.content

        # Attempt to parse the JSON returned by the model. If parsing fails we
        # fall back to a neutral baseline.
        analysis: Dict[str, Any] = {
            "tone": "neutral",
            "ideology": "unknown",
            "emotion": "neutral",
            "contains_slur": False,
            "reply_tone": "calm",
        }
        try:
            analysis.update(json.loads(content))
        except Exception:
            # Basic heuristic if the model didn't return pure JSON.
            if "slur" in tweet_text.lower():
                analysis["contains_slur"] = True
    except Exception as exc:  # broad catch to keep the bot running
        print(f"OpenAI API error: {exc}")
        analysis = {
            "tone": "neutral",
            "ideology": "unknown",
            "emotion": "neutral",
            "contains_slur": False,
            "reply_tone": "calm",
        }

    return analysis
