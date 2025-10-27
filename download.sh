#!/bin/bash
# Ultra Pornhub Downloader - Termux Share Menu
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

# Auto login if cookies missing
if [ ! -f ~/.config/ph-dl-ultra/cookies.txt ]; then
    echo "Exporting cookies..."
    python3 main.py --login
fi

# If URL from share menu
if [ -n "$1" ] && [[ "$1" == http* ]]; then
    echo "Shared URL detected: $1"
    python3 main.py "$1"
else
    echo "Usage: $0 <URL>  or Share from browser"
    echo "Example: $0 https://www.pornhub.com/view_video.php?viewkey=phabc123"
    python3 main.py --gui
fi
