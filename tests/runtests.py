#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django_nose import NoseTestSuiteRunner


if __name__ == '__main__':
    NoseTestSuiteRunner(verbosity=1).run_tests(['tests'])