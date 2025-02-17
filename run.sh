#!/bin/bash

python -m alembic upgrade head || exit 1

gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind="0.0.0.0:$BACKEND_PORT" \
  --pythonpath src
