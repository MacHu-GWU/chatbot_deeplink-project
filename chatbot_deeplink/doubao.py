# -*- coding: utf-8 -*-

"""
Doubao (豆包) deep link implementation.

Reference: ``.claude/skills/pypi-chatbot_deeplink/ref/doubao.md``
"""

import dataclasses
import json
from typing import ClassVar
from urllib.parse import quote

from .base import BaseDeepLink


@dataclasses.dataclass
class Doubao(BaseDeepLink):
    """
    Build a Doubao (豆包) deep link that opens a new conversation and sends
    :attr:`prompt`.

    Doubao is the first provider that breaks the ``?q=<encoded_prompt>``
    shape every other provider follows. It takes a JSON "action" object
    instead, with the prompt nested at ``payload.text``::

        https://www.doubao.com/chat/url-action?action={"pluginId":"Send_Message","payload":{"text":"..."}}

    That's why this class overrides :meth:`build_url` outright and never
    calls :meth:`~chatbot_deeplink.base.BaseDeepLink.encode_prompt` -- what
    gets percent-encoded here is the whole JSON document, not the prompt
    alone.

    Doubao's web app is lenient enough to accept the JSON (and non-ASCII
    prompt text) completely un-encoded, which is how the URL is usually
    passed around by hand. We still percent-encode it: ``{``, ``}``, ``"``
    and spaces are unsafe in a URL, and an un-encoded URL breaks as soon as
    it's put in a Markdown link, an HTML ``href``, a shell command or an
    HTTP header. The server decodes back to the identical JSON, so the two
    forms are equivalent.

    .. note::

        Doubao region-bans requests from outside mainland China -- the URL
        redirects to ``/security/doubao-region-ban`` there, so generated
        links may simply not work for overseas users.

    :param prompt: the raw, un-encoded prompt text.
    """

    #: Endpoint that consumes the ``action`` JSON.
    URL: ClassVar[str] = "https://www.doubao.com/chat/url-action"

    #: The only plugin id we use: send ``payload.text`` as a chat message.
    PLUGIN_ID: ClassVar[str] = "Send_Message"

    def build_action(self) -> dict:
        """
        Build the ``action`` object that Doubao's endpoint expects.
        """
        return {
            "pluginId": self.PLUGIN_ID,
            "payload": {"text": self.prompt},
        }

    def encode_action(self) -> str:
        """
        Serialize :meth:`build_action` to compact JSON, then percent-encode it.

        ``ensure_ascii=False`` keeps CJK text as real characters so that
        :func:`~urllib.parse.quote` encodes them as UTF-8 bytes, rather than
        as ``\\uXXXX`` escapes that would survive into the URL as literal
        backslashes.
        """
        action_json = json.dumps(
            self.build_action(),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return quote(action_json, safe="")

    def build_url(self) -> str:
        return f"{self.URL}?action={self.encode_action()}"
