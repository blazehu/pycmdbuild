# coding=utf-8
import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = "pycmdbuild"
DESCRIPTION = "Python library to access the REST interface of a CMDBuild server"
URL = "https://github.com/blazehu/pycmdbuild/tree/master"
EMAIL = "viease@foxmail.com"
AUTHOR = "yhhu"
VERSION = "0.1"


def get_version(project='cmdbuild'):
    package_root = os.path.dirname(__file__)
    version_path = os.path.join(package_root, project, 'version')
    if os.path.exists(version_path):
        with open(version_path) as f:
            version = f.read().strip()
    else:
        version = VERSION
    return version


setup(
    name=NAME,
    version=get_version(),
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(),
    requires=["requests"],
    package_data={
        'cmdbuild': [
            'version',
        ],
    },
)
