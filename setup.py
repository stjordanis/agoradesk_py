#!/usr/bin/env python

from setuptools import setup

setup(
    name="agoradesk_py",
    version="0.1.0",
    packages=["agoradesk_py"],
    install_requires=[
        "arrow",
        "httpx",
    ],
    author="marvin8",
    author_email="marvin8@tuta.io",
    url="https://codeberg.org/MarvinsCryptoTools/agoradesk_py",
    description="Python Interface for Agoradesk.com and LocalMonero.co API",
    long_description=open("README.md").read(),
    keywords="Agoradesk LocalMonero info xmr monero api",
    license="AGPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
    ],
)
