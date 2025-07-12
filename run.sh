#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "❌ 請指定要執行的 Python 檔案，例如：./run.sh test.py"
  exit 1
fi

SCRIPT="$1"

docker run --rm \
  -v "$PWD":/app \
  -w /app \
  python:3.8.10-slim \
  bash -c "PYTHONPATH=/app/.local python $SCRIPT"
