#!/bin/sh

SCRIPTS_DIR=$(dirname $(readlink -e "$0"))
ROOT_DIR=$(dirname "$SCRIPTS_DIR")

uv run ruff check "$ROOT_DIR"
