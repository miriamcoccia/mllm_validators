"""
test_openai_provider.py: tests for OpenAIProvider's parsing logic.
"""

import json
from providers.openai_provider import OpenAIProvider
from providers.base import PromptRequest


def test_parse_batch_line():
    fake_line = json.dumps(
        {
            "custom_id": "fake_fingerprint_123",
            "response": {
                "body": {
                    "output": [
                        {"type": "reasoning", "content": []},  # should be skipped
                        {"type": "message", "content": [{"text": '{"verdicts": []}'}]},
                    ],
                    "usage": {"input_tokens": 100, "output_tokens": 20},
                }
            },
        }
    )

    provider = OpenAIProvider(api_key="fake-key-not-used")
    result = provider._parse_batch_line(fake_line)

    assert result.content == '{"verdicts": []}'
    assert result.input_tokens == 100
    assert result.output_tokens == 20


def test_build_batch_line_with_image():
    provider = OpenAIProvider(api_key="fake-key-not-used")
    provider._uploaded_files["fake_image.png"] = "file-fake123"

    request = PromptRequest(
        custom_id="q1",
        prompt="test prompt",
        endpoint="fake-endpoint-123",
        image_path="fake_image.png",
    )
    line = provider._build_batch_line(request)

    assert line["custom_id"] == "q1"
    assert line["method"] == "POST"
    assert line["url"] == "/v1/responses"
    assert line["body"]["model"] == "fake-endpoint-123"

    content = line["body"]["input"][0]["content"]

    assert content[0]["type"] == "input_text"
    assert content[0]["text"] == "test prompt"
    assert content[1]["type"] == "input_image"
    assert content[1]["file_id"] == "file-fake123"


def test_build_batch_line_without_image():
    provider = OpenAIProvider(api_key="fake-key-not-used")

    request = PromptRequest(
        custom_id="q2",
        prompt="test prompt",
        endpoint="fake-endpoint-123",
        image_path=None,
    )
    line = provider._build_batch_line(request)

    content = line["body"]["input"][0]["content"]

    assert content[0]["type"] == "input_text"
    assert content[0]["text"] == "test prompt"
    assert len(content) == 1
