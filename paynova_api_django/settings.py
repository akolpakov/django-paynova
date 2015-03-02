#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.conf import settings

PAYNOVA_USERNAME = getattr(settings, 'PAYNOVA_USERNAME', None)
PAYNOVA_PASSWORD = getattr(settings, 'PAYNOVA_PASSWORD', None)
PAYNOVA_LIVE = getattr(settings, 'PAYNOVA_LIVE', False)
PAYNOVA_ENDPOINT = getattr(settings, 'PAYNOVA_ENDPOINT', None)
PAYNOVA_DEFAULT_LANGUAGE = getattr(settings, 'PAYNOVA_DEFAULT_LANGUAGE', 'eng')