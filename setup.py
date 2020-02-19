#!/usr/bin/env python

from distutils.core import setup

setup(
    name="Inseminator",
    version="0.1",
    description="Python dependency injection library based on type hints",
    author="Milan Suk",
    author_email="Milansuk@email.com",
    url="https://www.github.com/sukovanej/container/",
    package_dir={"inseminator": "src", "inseminator.integrations": "src/integrations"},
    packages=["inseminator", "inseminator.integrations"],
)
