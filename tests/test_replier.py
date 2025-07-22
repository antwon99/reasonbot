import os
from unittest.mock import MagicMock, patch

import replier


def test_generate_reply_calls_openai():
    context = {
        "tone": "aggressive",
        "ideology": "conspiracy",
        "emotion": "anger",
        "contains_slur": False,
        "reply_tone": "calm",
    }

    with patch("replier.openai.OpenAI") as MockClient, patch(
        "utils.load_env"
    ), patch.dict(os.environ, {"OPENAI_API_KEY": "key"}):
        instance = MockClient.return_value
        chat = instance.chat.completions
        mock_choice = MagicMock()
        mock_choice.message.content = "Response"
        chat.create.return_value = MagicMock(choices=[mock_choice])

        reply = replier.generate_reply(context, "The earth is flat")

        assert reply == "Response"
        chat.create.assert_called_once()


def test_generate_reply_no_key():
    context = {"reply_tone": "calm"}
    with patch("utils.load_env"), patch.dict(os.environ, {}, clear=True):
        reply = replier.generate_reply(context, "hi")
        assert "cannot respond" in reply.lower()


def test_build_prompt_adds_contextual_instructions():
    """_build_prompt should incorporate context flags into the prompt."""
    context = {
        "reply_tone": "calm",
        "contains_slur": True,
        "ideology": "conspiracy",
        "emotion": "anger",
    }

    prompt = replier._build_prompt(context, "Test tweet")

    assert "Respond in a calm tone" in prompt
    assert "acknowledge the hateful language" in prompt
    assert "highlight factual contradictions" in prompt
    assert "defuse the tension" in prompt
    assert "Tweet: Test tweet" in prompt


def test_build_prompt_aggressive_tone():
    """Aggressive tone should also trigger tension defusing instruction."""
    context = {"tone": "aggressive", "reply_tone": "sarcastic"}

    prompt = replier._build_prompt(context, "example")

    assert "Respond in a sarcastic tone" in prompt
    assert "defuse the tension" in prompt


def test_generate_reply_openai_error():
    """Exceptions from openai.OpenAI should return the fallback reply."""
    context = {"reply_tone": "calm"}

    with patch("utils.load_env"), patch.dict(
        os.environ,
        {"OPENAI_API_KEY": "k"},
    ), patch(
        "replier.openai.OpenAI",
        side_effect=replier.openai.OpenAIError("boom"),
    ):
        reply = replier.generate_reply(context, "hi")

    assert reply == "ReasonBot encountered an error and cannot reply."
