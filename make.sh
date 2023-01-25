#!/usr/bin/env bash

# This script is used to build the package.
python3 setup.py sdist bdist_wheel

# This installs the package to the local PyPi index.
# twine upload --repository pypi dist/*