# -*- coding: utf-8 -*-

"""
ChatGPT deep link implementation.

Reference: ``.claude/skills/pypi-chatbot_deeplink/ref/chatgpt.md``
"""

import dataclasses

from .base import BaseDeepLink


@dataclasses.dataclass
class ChatGPT(BaseDeepLink):
    """
    Build a ChatGPT Web (chatgpt.com) deep link that opens a new conversation
    with :attr:`prompt`.

    Whether the prompt is auto-submitted or only pre-filled isn't a
    documented, stable behavior -- OpenAI hasn't published a ``?q=`` deep
    link API spec, so treat this as observed web behavior that can change.

    :param prompt: the raw, un-encoded prompt text.
    """

    def build_url(self) -> str:
        return f"https://chatgpt.com/?q={self.encode_prompt()}"
