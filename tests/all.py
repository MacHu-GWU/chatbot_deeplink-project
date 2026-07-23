# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from chatbot_deeplink.tests import run_cov_test

    run_cov_test(
        __file__,
        "chatbot_deeplink",
        is_folder=True,
        preview=False,
    )
