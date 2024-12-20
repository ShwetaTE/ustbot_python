#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "6353b651-5476-45c1-96d4-9e05e7ac150a")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "EiI8Q~3GMsAQlhBbBZT4DTS1y4gJ4iwsrYJIWaS~")
