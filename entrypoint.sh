#!/bin/bash

RUN_PORT=${PORT:-8000}

/usr/local/bin/gunicorn --worker 4 --worker-class uvicorn.workers.UvicornWorker app.main:app --bind "0.0.0.0:${RUN_PORT}"
