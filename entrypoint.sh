#!/bin/sh
set -e

# Run the manifest script
if [ -f "zen_api/manifest.py" ]; then
    python zen_api/manifest.py
fi

# Start the Uvicorn server
exec uvicorn zen_api.main:app --host 0.0.0.0 --port 8000
