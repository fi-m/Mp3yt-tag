"""
Program for tagging mp3 files with metadata from yt download.
"""
import os

import click

from downloader import Downloader
from mp3_tagger import MP3tagger

TMP_PATH = os.path.join(os.path.dirname(__file__), "tmp/")
SUCCESS_DIR = os.path.join(os.path.dirname(__file__), "successful_tags/")
FAILED_DIR = os.path.join(os.path.dirname(__file__), "failed_tags/")

# Add click commands for single url or a txt file with urls:


@click.command()
# Make it either url or a txt file with urls:
@click.option("--url", "-u", help="YouTube link", default=None)
@click.option("--file", "-f", "file_name", help="Path to file with urls", default=None)
def main(url, file_name):
    """
    Download mp3 files from youtube and tag them with metadata.
    The youtube title shoudle be artist - title.
    """
    # Create directories if they don't exist:
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)
    if not os.path.exists(SUCCESS_DIR):
        os.makedirs(SUCCESS_DIR)
    if not os.path.exists(FAILED_DIR):
        os.makedirs(FAILED_DIR)

    urls = []
    if url:
        urls.append(url)
    elif file_name:
        with open(file_name, "r") as f:
            for line in f:
                print(line)
                urls.append(line.strip())
        f.close()
    # TODO: Add for playlist urls:

    for url in urls:
        if url:
            downloader = Downloader()
            downloader.download_audio_file(url)

    for file in os.listdir(TMP_PATH):
        if file.endswith(".mp3"):
            mp3 = MP3tagger(file, os.path.join(TMP_PATH, file))
            mp3.tag_mp3_file()

            if mp3.success:
                os.rename(
                    os.path.join(TMP_PATH, file),
                    os.path.join(SUCCESS_DIR, f"{mp3.artist} - {mp3.title}.mp3"),
                )
            else:
                os.rename(os.path.join(TMP_PATH, file), os.path.join(FAILED_DIR, file))

    # Remove temporary directory
    __import__("pprint").pprint(f"Removing temporary directory: {TMP_PATH}")
    os.rmdir(TMP_PATH)


if __name__ == "__main__":
    main()
