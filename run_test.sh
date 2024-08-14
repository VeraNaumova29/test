#!/bin/bash

export POSTGRES_URL="postgres://user:password@host:port"
export BACK_API_HOST="some_back_host:port"
export UI_URL="https://host:port/url"
export TEST_VAR1="42"
export REPORTS_DIR="report"

python3 -m pytest tests.py --some_filtes=regression* --reports_out="$REPORTS_DIR"