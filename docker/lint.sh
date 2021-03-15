#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_file_system/ tests/

black d8s_file_system/ tests/

mypy d8s_file_system/ tests/

pylint --fail-under 9 d8s_file_system/*.py

flake8 d8s_file_system/ tests/

bandit -r d8s_file_system/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_file_system/ tests/
