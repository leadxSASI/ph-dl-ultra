#!/usr/bin/env python3
import os
import sys
import yaml
import subprocess
import logging
from pathlib import Path
from utils.gui import PornhubDownloaderGUI
from utils.login import export_cookies
from utils.quality import get_quality_options

# ==================== CONFIG ====================
CONFIG_FILE = Path.home() / ".config" / "ph-dl-ultra" / "config.yaml"
HISTORY_FILE = Path.home() / ".config" / "ph-dl-ultra" / "history.log"
COOKIES_FILE = Path.home() / ".config" / "ph-dl-ultra" / "cookies.txt"

os.makedirs(CONFIG_FILE.parent, exist_ok=True)

DEFAULT_CONFIG = {
    "output_dir": "~/storage/downloads/Pornhub",
    "quality": "best[height<=1080]",
    "format": "mp4",
    "embed_subs": True,
    "embed_thumbnail": True,
    "concurrent_fragments": 16,
    "browser": "firefox",
    "vpn": False
}

if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text(yaml.dump(DEFAULT_CONFIG))

config = yaml.safe_load(CONFIG_FILE.read_text())

# Expand ~
for key in ["output_dir"]:
    config[key] = os.path.expanduser(config[key])

# Logging
logging.basicConfig(filename=HISTORY_FILE, level=logging.INFO,
                    format='%(asctime)s | %(message)s')

# ==================== CORE DOWNLOADER ====================
def download(url, quality=None, gui_mode=False):
    output_dir = config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    quality = quality or config["quality"]
    cmd = [
        "yt-dlp",
        "--cookies", str(COOKIES_FILE),
        "-o", f"{output_dir}/%(title)s.%(ext)s",
        "--concurrent-fragments", str(config["concurrent_fragments"]),
        "--remux-video", config["format"],
    ]

    if config["embed_subs"]:
        cmd.append("--embed-subs")
    if config["embed_thumbnail"]:
        cmd.append("--embed-thumbnail")

    cmd += ["-f", quality, url]

    print(f"Downloading: {url}")
    print(f"Quality: {quality}")
    print(f"Output: {output_dir}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            title = [line for line in result.stdout.splitlines() if "Merging" in line or "has already been" in line]
            msg = f"SUCCESS: {url}"
            print(msg)
            logging.info(msg)
            if gui_mode:
                return True, msg
        else:
            msg = f"ERROR: {result.stderr.splitlines()[-1]}"
            print(msg)
            logging.error(msg)
            if gui_mode:
                return False, msg
    except Exception as e:
        msg = f"EXCEPTION: {e}"
        print(msg)
        logging.error(msg)
        if gui_mode:
            return False, msg

    return False, "Unknown error"

# ==================== CLI MODE ====================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if "--login" in sys.argv:
            export_cookies(config["browser"], COOKIES_FILE)
            print("Cookies exported!")
            sys.exit(0)
        if "--gui" in sys.argv:
            app = PornhubDownloaderGUI(config, download)
            app.run()
        else:
            download(url)
    else:
        # Auto GUI if no args
        app = PornhubDownloaderGUI(config, download)
        app.run()
