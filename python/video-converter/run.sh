#!/usr/bin/env fish

# Clear Python cache
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Run the application
python -B -m src.main
