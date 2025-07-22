import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure the project root is on the import path so `analyzer` can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import analyzer  # noqa: E402


EXPECTED_KEYS = {"tone", "ideology", "emotion", "contains_slur", "reply_tone"}


def test_analyze_context_parses_json():
    """Valid JSON from OpenAI should populate the analysis dict."""
    data = {
        "tone": "hostile",
        "ideology": "extremist",
        "emotion": "anger",
        "contains_slur": True,
        "reply_tone": "calm",
    }

    with patch("analyzer.load_dotenv"), patch.dict(
        os.environ, {"OPENAI_API_KEY": "k"}
    ), patch("analyzer.openai.OpenAI") as MockClient:
        instance = MockClient.return_value
        chat = instance.chat.completions
        mock_choice = MagicMock()
        mock_choice.message.content = json.dumps(data)
        chat.create.return_value = MagicMock(choices=[mock_choice])

        result = analyzer.analyze_context("text")

    assert result == data
    assert EXPECTED_KEYS == set(result)


def test_analyze_context_invalid_json():
    """Invalid JSON should trigger fallback analysis with slur detection."""
    with patch("analyzer.load_dotenv"), patch.dict(
        os.environ, {"OPENAI_API_KEY": "k"}
    ), patch("analyzer.openai.OpenAI") as MockClient:
        instance = MockClient.return_value
        chat = instance.chat.completions
        mock_choice = MagicMock()
        mock_choice.message.content = "not json"
        chat.create.return_value = MagicMock(choices=[mock_choice])

        result = analyzer.analyze_context("this slur text")

    assert result["contains_slur"] is True
    for key in EXPECTED_KEYS:
        assert key in result


def test_analyze_context_no_api_key():
    """If OPENAI_API_KEY is missing the function should skip API calls."""
    with patch("analyzer.load_dotenv"), patch.dict(os.environ, {}, clear=True), patch(
        "analyzer.openai.OpenAI"
    ) as MockClient:
        result = analyzer.analyze_context("whatever")
        MockClient.assert_not_called()

    for key in EXPECTED_KEYS:
        assert key in result
    assert result["tone"] == "neutral"
