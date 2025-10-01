#!/bin/bash

# change to the directory where the script is located
cd "$(dirname "$0")"
poetry install > /dev/null 2>&1
poetry run wikimedia-enterprise-mcp
