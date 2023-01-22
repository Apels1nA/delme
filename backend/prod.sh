#!/usr/bin/env bash

source ./env/bin/activate

APP_MODE=production uvicorn app:app --port 8000 --timeout-keep-alive 10000 > log.txt
