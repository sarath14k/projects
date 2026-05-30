#!/bin/bash
# start_server.sh - Local Server Bootstrapper

# Locate the script directory
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find an open port starting from 8000
PORT=8000
while lsof -i :$PORT >/dev/null 2>&1; do
    PORT=$((PORT+1))
done

echo -e "\033[1;36m====================================================\033[0m"
echo -e "\033[1;32m   PARETO LEETCODE PRACTICE TRACKER LOCAL SERVER\033[0m"
echo -e "\033[1;36m====================================================\033[0m"
echo -e "📂 Directory: $DIR"
echo -e "🔌 Port:      $PORT"
echo -e "🚀 Starting local web server..."

# Run python compilation server in background
python3 "$DIR/server.py" $PORT &
SERVER_PID=$!

# Let the server bind to the port
sleep 1.5

if ps -p $SERVER_PID > /dev/null; then
    echo -e "\033[1;32m✓ Local server started successfully!\033[0m"
    echo -e "🔗 Access your app at: \033[1;34mhttp://localhost:$PORT\033[0m"
    echo -e "💡 To stop the server later, press Ctrl+C or run 'kill $SERVER_PID'"
    echo -e "\033[1;36m====================================================\033[0m"
    
    # Keep script open to show logs, handle shutdown gracefully
    trap "kill $SERVER_PID; echo -e '\n🛑 Server stopped.'; exit" INT TERM
    wait $SERVER_PID
else
    echo -e "\033[1;31m✗ Failed to start the server. Verify python3 is installed.\033[0m"
    exit 1
fi
