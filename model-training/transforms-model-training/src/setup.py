#!/usr/bin/env python
import os
import sys
from setuptools import find_packages, setup

pipeline_name = os.environ.get("PIPELINE_OVERRIDE_UUID", "root")

setup(
    name=os.environ["PKG_NAME"],
    version=os.environ["PKG_VERSION"],
    description="Model training project",
    author="Enterprise Fraud Detection(EFD)",
    packages=find_packages(exclude=["contrib", "docs", "test"]),
    install_requires=[],
    entry_points={"transforms.pipelines": [f"{pipeline_name} = main.pipeline:pipeline"]},
)
