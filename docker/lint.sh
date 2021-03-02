#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort democritus_file_system/ tests/

black democritus_file_system/ tests/

mypy democritus_file_system/ tests/

pylint --fail-under 9 democritus_file_system/*.py

flake8 democritus_file_system/ tests/

bandit -r democritus_file_system/

# we run black again at the end to undo any odd changes made by any of the linters above
black democritus_file_system/ tests/
