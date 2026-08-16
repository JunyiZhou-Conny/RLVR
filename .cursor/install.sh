#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for S-Seg-RLVR.
# Creates a project-local virtualenv (.venv, already gitignored) and installs
# the sseg_rlvr package in editable mode with the dev + vision extras so the
# reward stubs, literature/issue scripts, and future unit tests are runnable.
#
# The base image's stdlib venv lacks ensurepip (no python3-venv), so we use the
# standalone `virtualenv` package, which bootstraps pip without apt/sudo.
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR=".venv"

if [ ! -x "${VENV_DIR}/bin/python" ]; then
  echo "==> Ensuring virtualenv is available"
  if ! "${PYTHON_BIN}" -m virtualenv --version >/dev/null 2>&1; then
    "${PYTHON_BIN}" -m pip install --user --upgrade virtualenv
  fi
  echo "==> Creating virtualenv at ${VENV_DIR}"
  "${PYTHON_BIN}" -m virtualenv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "==> Upgrading pip tooling"
python -m pip install --upgrade pip setuptools wheel

echo "==> Installing sseg_rlvr (editable) with dev + vision extras"
python -m pip install -e ".[dev,vision]"

echo "==> Environment ready"
python --version
python -c "import sseg_rlvr; print('sseg_rlvr', sseg_rlvr.__version__)"
