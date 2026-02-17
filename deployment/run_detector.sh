#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

export PLATFORM_OVERRIDE=jetson

python3 camera_app.py "$@"