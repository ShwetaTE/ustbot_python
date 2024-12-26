#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import sys

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    # PORT = 8000
    # APP_ID = os.environ.get("MicrosoftAppId", "6353b651-5476-45c1-96d4-9e05e7ac150a")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "EiI8Q~3GMsAQlhBbBZT4DTS1y4gJ4iwsrYJIWaS~")
    # APP_TYPE = os.environ.get("MicrosoftAppType", "SingleTenant")
    # APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "3d7a3f90-1d2c-4d91-9b49-52e098cf9eb8")
    
    APP_ID = os.environ.get("MicrosoftAppId", "04edc2a1-dc5a-4e0b-a0d5-36e360259dab")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "PDZ8Q~sT.KHWN..zbPUx3U-F5IuEwM11aju5dc_d")
    APP_TYPE = os.environ.get("MicrosoftAppType", "Multi Tenant")
