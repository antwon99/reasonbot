"""ReasonBot Strategic Replier

This module constructs replies using template logic, rhetorical framing, and
cause-effect chains. It adapts tone based on the analyzer’s output and avoids
moralizing, aiming instead for strategic disarmament.

Primary function: generate_reply(context_data: dict, tweet_text: str) -> str
"""

from __future__ import annotations

from typing import Any, Dict

from utils import load_env, get_env_var
import openai
import backoff


@backoff.on_exception(backoff.expo, openai.OpenAIError, max_tries=3)
def _chat_completion(client: openai.OpenAI, prompt: str):
    """Call the OpenAI chat completion API with retries."""

    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are ReasonBot, a calm and strategic debater.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )


def _build_prompt(context: Dict[str, Any], tweet_text: str) -> str:
    """Assemble the LLM prompt based on context data.

    The function uses a mini logic tree to decide which instructions to send to
    the model. This keeps the prompt readable and enforces length and tone
    constraints.

    Parameters
    ----------
    context:
        Output dictionary from :func:`analyze_context`.
    tweet_text:
        The original tweet that summoned ReasonBot.

    Returns
    -------
    str
        The prompt to feed into the OpenAI chat model.
    """

    reply_tone = context.get("reply_tone", "calm")
    instructions = [
        f"Respond in a {reply_tone} tone",
        "no more than 50 words",
        "avoid moralizing",
        "use cause-effect reasoning",
    ]

    if context.get("contains_slur"):
        instructions.append("acknowledge the hateful language without repeating it")

    ideology = context.get("ideology")
    if ideology in {"conspiracy", "extremist"}:
        instructions.append("highlight factual contradictions")

    emotion = context.get("emotion")
    if emotion in {"anger", "rage"} or context.get("tone") == "aggressive":
        instructions.append("defuse the tension")

    instruction_text = "; ".join(instructions)
    prompt = f"You are ReasonBot. {instruction_text}.\n" f"Tweet: {tweet_text}"
    return prompt


def generate_reply(context_data: Dict[str, Any], tweet_text: str) -> str:
    """Return a strategic reply for the provided tweet.

    Parameters
    ----------
    context_data:
        The dictionary returned from :func:`analyze_context`.
    tweet_text:
        The full text of the tweet requiring a reply.

    Returns
    -------
    str
        A tactically worded response generated via OpenAI or a fallback message
        if the API is unavailable.
    """

    # Ensure environment variables are loaded before accessing them
    load_env()
    api_key = get_env_var("OPENAI_API_KEY")

    if not api_key:
        print(
            "Missing OPENAI_API_KEY. Returning fallback reply while we wait for credentials."
        )
        return "ReasonBot cannot respond right now."  # short placeholder

    try:
        client = openai.OpenAI(api_key=api_key)
        prompt = _build_prompt(context_data, tweet_text)

        response = _chat_completion(client, prompt)

        return response.choices[0].message.content.strip()

    except Exception as exc:  # broad catch to keep the bot running
        print(f"OpenAI API error: {exc}")
        return "ReasonBot encountered an error and cannot reply."  # fallback
