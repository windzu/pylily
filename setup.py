"""
Author: wind windzu1@gmail.com
Date: 2024-1-16
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-14 15:53:39
Description: 
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""
import sys

from setuptools import find_packages, setup

# 获取当前Python版本
current_python_version = sys.version_info


def parse_requirements(fname_list=[]):
    """Parse the package dependencies listed in a requirements list file."""
    filename = "requirements.txt"
    requirements = []

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                requirements.append(line)
    # remove duplicates
    requirements = list(set(requirements))
    return requirements


# basic
setup(
    # 描述信息
    name="pylily",
    version="0.0.1",
    description="python implementation of Lily",
    author="windzu",
    author_email="windzu1@gmail.com",
    url="",
    license="MIT license",
    keywords="adas deeplearning",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # 主要设置
    python_requires=">=3.6",
    packages=find_packages(exclude=("docs")),
    install_requires=parse_requirements(),
    entry_points={"console_scripts": ["pylily=pylily.main:main"]},
    # 次要设置
    include_package_data=True,
    zip_safe=False,
)
