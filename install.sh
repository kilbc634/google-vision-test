#!/bin/bash

# 建立 .local 資料夾（如果不存在）
mkdir -p .local

# 執行 pip 安裝到 .local
docker run --rm \
  -v "$PWD":/app \
  -w /app \
  python:3.8.10-slim \
  bash -c "pip install --upgrade pip && pip install --target=.local -r requirements.txt"
