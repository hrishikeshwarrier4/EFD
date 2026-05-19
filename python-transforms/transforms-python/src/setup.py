#!/usr/bin/env python
import os
from setuptools import find_packages, setup

setup(
    name=os.environ["PKG_NAME"],
    version=os.environ["PKG_VERSION"],
    description="Python data transformation project",
    author="Enterprise Fraud Detection(EFD)",
    packages=find_packages(exclude=["contrib", "docs", "test"]),
    install_requires=[],
    entry_points={"transforms.pipelines": ["root = myproject.pipeline:my_pipeline"]},
)
