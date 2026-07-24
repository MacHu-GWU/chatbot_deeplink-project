# -*- coding: utf-8 -*-

"""
Base "Command" class shared by every chatbot deep link implementation.

See ``.claude/skills/pypi-chatbot_deeplink/ref/about.md`` for the general
deep link mechanism background this module implements.
"""

import dataclasses
import webbrowser
from urllib.parse import quote


@dataclasses.dataclass
class BaseDeepLink:
    """
    Base class for every chatbot deep link "Command" object.

    Each subclass represents one deep link entry point of one chatbot
    provider (a provider can have more than one entry point, e.g. Claude Web
    vs Claude Code). Subclasses only need to implement :meth:`build_url`;
    the UTF-8 + percent-encoding rule (NOT Base64) is shared by every known
    provider and lives in :meth:`encode_prompt`.

    :param prompt: the raw, un-encoded prompt text to send.
    """

    prompt: str

    def encode_prompt(self) -> str:
        """
        Percent-encode :attr:`prompt` as UTF-8 bytes.

        ``safe=""`` also encodes ``/`` so a prompt that itself contains a
        URL can't be mistaken for part of the deep link's query string.
        """
        return quote(self.prompt, safe="")

    def build_url(self) -> str:
        """
        Build the final deep link URL. Every subclass must implement this.
        """
        raise NotImplementedError

    def __call__(self) -> str:
        """
        Shorthand for :meth:`build_url`, so a Command instance can be
        invoked directly: ``ChatGPT(prompt="...")()``.
        """
        return self.build_url()

    def open_in_browser(self) -> None:
        """
        One-click convenience: open :meth:`build_url` in the default browser.
        """
        webbrowser.open_new_tab(self.build_url())
