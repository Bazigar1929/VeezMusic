from os import path

from yt_dlp import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🔴 𝘃𝗶𝗱𝗲𝗼𝘀 𝗹𝗼𝗻𝗴𝗲𝗿 𝘁𝗵𝗮𝗻 {DURATION_LIMIT} 𝗠𝗶𝗻𝘂𝘁𝗲 (s)𝗔𝗿𝗲𝗻'𝘁 𝗔𝗹𝗹𝗼𝘄𝗲𝗱, 𝗧𝗵𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲𝗱 𝗩𝗶𝗱𝗲𝗼 𝗜𝘀 {duration} 𝗠𝗶𝗻𝘂𝘁𝗲(s)"
        )
    ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
