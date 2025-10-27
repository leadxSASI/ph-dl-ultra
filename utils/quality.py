def get_quality_options():
    return {
        "4K": "best[height<=2160]",
        "1080p": "best[height<=1080]",
        "720p": "best[height<=720]",
        "480p": "best[height<=480]",
        "Audio Only": "bestaudio"
    }
