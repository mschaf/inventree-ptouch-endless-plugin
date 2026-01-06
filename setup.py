# -*- coding: utf-8 -*-

import importlib
import importlib.util
import os
import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-ptouch-endless-plugin",
    version="0.1.0",
    author="Martin Schaflitzl",
    author_email="dev@martin-sc.de",
    description="Printer driver for brother ptouch series printers, supporting a variable length labels.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="inventree label printer printing inventory dynamic width variable length ptouch",
    url="https://github.com/mschaf/inventree-ptouch-endless-plugin",
    license="Apache License Version 2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "pillow",
    ],
    setup_requires=[
        "wheel",
        "twine",
    ],
    python_requires=">=3.9",
    entry_points={
        "inventree_plugins": [
            "PTouchEndlessPlugin = inventree_ptouch_endless.plugin:PTouchEndlessPlugin"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: InvenTree",
    ],
)
