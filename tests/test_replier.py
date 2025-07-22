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
        "replier.load_dotenv"
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
    with patch("replier.load_dotenv"), patch.dict(os.environ, {}, clear=True):
        reply = replier.generate_reply(context, "hi")
        assert "cannot respond" in reply.lower()
