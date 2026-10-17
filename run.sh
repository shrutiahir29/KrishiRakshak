#!/bin/bash
# KrishiRakshak — Start Local Development Server
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "🌾 Starting KrishiRakshak..."
echo "📂 Root Directory: $DIR"

# Verify virtual environment
if [ -f ".venv/bin/uvicorn" ]; then
    echo "✅ Using virtual environment in .venv/"
    exec .venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "⚠️ .venv/bin/uvicorn not found. Attempting global uvicorn..."
    exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
fi
