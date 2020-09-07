#!/usr/bin/env python

import setuptools
from distutils.core import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="inseminator",
    version="0.2",
    description="Python dependency injection library based on type hints",
    author="Milan Suk",
    author_email="Milansuk@email.com",
    url="https://www.github.com/sukovanej/inseminator/",
    package_dir={"inseminator": "src", "inseminator.integrations": "src/integrations"},
    packages=["inseminator", "inseminator.integrations"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
