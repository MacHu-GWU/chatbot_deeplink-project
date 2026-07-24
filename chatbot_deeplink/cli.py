#!/usr/bin/env python3
"""Command line interface to build (and optionally open) chatbot deep link URLs."""

from __future__ import annotations

import argparse
import sys
from typing import Type

from chatbot_deeplink.base import BaseDeepLink
from chatbot_deeplink.chatgpt import ChatGPT
from chatbot_deeplink.claude import Claude, ClaudeCode
from chatbot_deeplink.doubao import Doubao

PROVIDERS: dict[str, Type[BaseDeepLink]] = {
    "claude": Claude,
    "claude-code": ClaudeCode,
    "chatgpt": ChatGPT,
    "doubao": Doubao,
}


def _main(provider: str, prompt: str, open_browser: bool = False) -> int:
    """Build a deep link URL for the given provider and prompt, print it to stdout.

    Returns an exit code: 0 on success, 1 on failure.
    """
    deep_link_class = PROVIDERS.get(provider)
    if deep_link_class is None:
        print(
            f"ERROR: unknown provider {provider!r}, must be one of {sorted(PROVIDERS)}",
            file=sys.stderr,
        )
        return 1

    deep_link = deep_link_class(prompt=prompt)
    print(deep_link.build_url())
    if open_browser:
        deep_link.open_in_browser()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="chatbot-deeplink",
        description="Build a chatbot deep link URL with a pre-filled prompt.",
    )
    subparsers = parser.add_subparsers(dest="provider", required=True)
    for name in PROVIDERS:
        subparser = subparsers.add_parser(name, help=f"build a {name} deep link")
        subparser.add_argument(
            "--prompt", required=True, help="the raw, un-encoded prompt text"
        )
        subparser.add_argument(
            "--open_browser",
            action="store_true",
            help="open the deep link URL in the default browser",
        )

    args = parser.parse_args(argv)
    return _main(
        provider=args.provider,
        prompt=args.prompt,
        open_browser=args.open_browser,
    )


if __name__ == "__main__":
    sys.exit(main())
