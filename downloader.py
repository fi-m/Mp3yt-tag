"""
Handler for the main program.
"""

import os
import subprocess

from pytube import YouTube
from pytube.cli import on_progress

# PATH for temporary files
TMP_PATH = os.path.join(os.path.dirname(__file__), "tmp/")


class Downloader:
    """
    Handler for the main program.
    """

    def __init__(self):
        self.audio = None

    def _is_yt_url(self, url: str) -> bool:
        """
        Check if the link is a valid YouTube link.
        """
        try:
            YouTube(url)
            return True
        except Exception:
            print(f"Invalid YouTube url: {url}.")
            return False

    def _get_yt_audio(self, url: str):
        """
        Download the video from YouTube.
        """
        yt = YouTube(url, on_progress_callback=on_progress)
        self.audio = yt.streams.get_audio_only()

    def download_audio_file(self, url: str):
        """
        Download the video from YouTube.
        """
        if not self._is_yt_url(url):
            return
        self._get_yt_audio(url)
        out_file = self.audio.download(output_path=TMP_PATH)
        __import__("pprint").pprint(f"Downloading {self.audio.title}")
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        __import__("pprint").pprint(f"Converting {out_file} to mp3")
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                os.path.join(TMP_PATH, out_file),
                "-vn",
                "-sn",
                "-c:a",
                "mp3",
                "-ab",
                "320k",
                os.path.join(TMP_PATH, new_file),
            ]
        )
        os.remove(os.path.join(TMP_PATH, out_file))
        __import__("pprint").pprint(f"Saved {new_file}")
