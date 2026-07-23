# -*- coding: utf-8 -*-

from chatbot_deeplink import api


def test():
    _ = api


if __name__ == "__main__":
    from chatbot_deeplink.tests import run_cov_test

    run_cov_test(
        __file__,
        "chatbot_deeplink.api",
        preview=False,
    )
