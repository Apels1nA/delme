#!/usr/bin/env bash

APP_MODE=develop uvicorn --reload app:app --port 8000 --timeout-keep-alive 10000
