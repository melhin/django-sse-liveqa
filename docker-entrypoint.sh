#!/bin/bash
set -eu

for arg in "$@"
do
    case "$arg" in
        main)
            echo "Starting async server"
            exec gunicorn sse_liveqa.asgi:application -c uvicorn.conf.py --worker-class uvicorn.workers.UvicornWorker 
            ;;
        local)
            echo "Starting async server"
            exec uvicorn sse_liveqa.asgi:application --port 8002 --reload --timeout-graceful-shutdown 0 --reload-include "*.html"
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
done