#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django_nose import NoseTestSuiteRunner


if __name__ == '__main__':
    NoseTestSuiteRunner(verbosity=1).run_tests(['tests'])