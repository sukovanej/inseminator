#!/usr/bin/env python

from distutils.core import setup

setup(
    name="Container",
    version="0.1",
    description="Python dependency injection library based on type hints",
    author="Milan Suk",
    author_email="Milansuk@email.com",
    url="https://www.github.com/sukovanej/container/",
    package_dir={"container": "src"},
    packages=["container"],
)
