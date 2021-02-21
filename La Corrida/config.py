#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "e0571edf-341f-451e-960e-eeb340116da9")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "nR21v5DT^w:gEVJ}fx}(Um6LX)
