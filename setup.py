#!/usr/bin/env python3

from setuptools import setup

setup(
    name="nnote",
    version="0.1.0",
    description="cli note taker",
    author="Agil Mammadov",
    author_email="mammadovagil@tutamail.com",
    url="https://github.com/stiermid/nnote",
    packages=["nnote"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "nnote=nnote.cli:cli",
        ],
    },
)
