# -*- coding: utf-8 -*-

"""
Claude deep link implementations.

Reference: ``.claude/skills/pypi-chatbot_deeplink/ref/claude.md``
"""

import dataclasses
from typing import ClassVar

from .base import BaseDeepLink


@dataclasses.dataclass
class Claude(BaseDeepLink):
    """
    Build a Claude Web (claude.ai) deep link that opens a new conversation
    with :attr:`prompt` pre-filled into the input box.

    Unlike ChatGPT's ``?q=``, this only pre-fills the input box -- the user
    still has to press Enter (or click send) to actually submit the message.

    :param prompt: the raw, un-encoded prompt text.
    """

    def build_url(self) -> str:
        return f"https://claude.ai/new?q={self.encode_prompt()}"


@dataclasses.dataclass
class ClaudeCode(BaseDeepLink):
    """
    Build a Claude Code (CLI) deep link using the ``claude-cli://open`` scheme.

    This targets the Claude Code CLI/desktop client, not a browser tab, so
    it's a distinct mechanism from :class:`Claude`. Anthropic's documented
    query length limit is :attr:`QUERY_LENGTH_LIMIT` characters; for prompts
    near or over that limit, Claude Code requires the user to scroll and
    confirm before it submits.

    :param prompt: the raw, un-encoded prompt text.
    """

    #: Anthropic's documented max length, in characters, for the ``q`` query
    #: value of this scheme.
    QUERY_LENGTH_LIMIT: ClassVar[int] = 5000

    def build_url(self) -> str:
        return f"claude-cli://open?q={self.encode_prompt()}"
