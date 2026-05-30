#!/usr/bin/env bash
# launch_app.sh - Native Desktop Web App Launcher

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if server is already running for our directory
PID=$(pgrep -f "python3 -m http.server .* --directory $DIR")

if [ -n "$PID" ]; then
    # Server is already running. Find the active port:
    PORT=$(lsof -i -P -n | grep "$PID" | grep -oE ":[0-9]+" | head -n 1 | tr -d ':')
    if [ -z "$PORT" ]; then
        PORT=8000
    fi
else
    # Find an open port starting from 8000
    PORT=8000
    while lsof -i :$PORT >/dev/null 2>&1; do
        PORT=$((PORT+1))
    done
    
    # Boot python HTTP server in background
    python3 -m http.server $PORT --directory "$DIR" > /dev/null 2>&1 &
    sleep 1.0
fi

# Launch in native standalone chromeless application mode
if command -v google-chrome >/dev/null 2>&1; then
    google-chrome --app="http://localhost:$PORT" --class="pareto-tracker" --name="pareto-tracker" &
elif command -v chromium >/dev/null 2>&1; then
    chromium --app="http://localhost:$PORT" --class="pareto-tracker" --name="pareto-tracker" &
else
    xdg-open "http://localhost:$PORT" &
fi
