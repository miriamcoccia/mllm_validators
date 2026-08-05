"""
test_openai_provider.py: tests for OpenAIProvider's parsing logic.
"""

import json
from providers.openai_provider import OpenAIProvider


def test_parse_batch_line():
    fake_line = json.dumps(
        {
            "response": {
                "body": {
                    "output": [{"content": [{"text": '{"verdicts": []}'}]}],
                    "usage": {"input_tokens": 100, "output_tokens": 20},
                }
            }
        }
    )

    provider = OpenAIProvider(api_key="fake-key-not-used")
    result = provider._parse_batch_line(fake_line)

    assert result.content == '{"verdicts": []}'
    assert result.input_tokens == 100
    assert result.output_tokens == 20
