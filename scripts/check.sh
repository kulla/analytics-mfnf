#!/bin/bash

SCRIPTS_DIR=$(dirname "$(readlink -e "$0")")

"$SCRIPTS_DIR/check-code.sh" || exit 1
"$SCRIPTS_DIR/check-format.sh" || exit 1
