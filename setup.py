#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from screcord import (
    __AUTHOR__,
    __AUTHOR_EMAIL__,
    __URL__,
    __LICENSE__,
    __VERSION__,
    __PROJECT_NAME__,
    __DESCRIPTION__,
)

setup(
    name=__PROJECT_NAME__,
    version=__VERSION__,
    description=__DESCRIPTION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    url=__URL__,
    packages=find_packages(),
    package_data={'': ['xrecord']},
    license=__LICENSE__,
    python_requires=">=3.6",
    install_requires=["loguru"]
)
