import os
import re
import sys
import urllib.request
import contextlib
from typing import Union

import discogs_client
import eyed3
from eyed3.mp3 import Mp3AudioFile

# TOKEN FOR DISCOGS API
TOKEN = ""


class MP3tagger:
    """
    Class for tagging mp3 files with metadata
    """

    def __init__(self, file_name: str, file_path: str):
        self.success = False
        self.file_name: str = file_name
        self.name: str = re.sub(
            "( ?\\((?!feat|FEAT|Feat|ft)(.*)\\) ?)*|( ?\\[(?!feat|FEAT|Feat|ft)(.*)\\] ?)*|(\\.mp3)$",
            "",
            file_name,
        )
        self.audio_file: Mp3AudioFile = eyed3.load(file_path)
        self.client = discogs_client.Client("ExampleApplication/0.1", user_token=TOKEN)
        self.artist: str = ""
        self.title: str = ""
        self.year: str = ""
        self.genre: str = ""
        self.cover_art = None

    def tag_mp3_file(self) -> None:
        """
        Set artist and title from file name
        """
        data = self._fetch_metadata_from_discogs()
        if not data:
            return None

        self.artist = self.name.split(" - ")[0]
        self.title = self.name.split(" - ")[1]
        self.year = str(data.get("year"))
        self.album = data.get("title").split(" - ")[1]
        self.genre = data.get("genre")[0]

        image_url = data.get("cover_image")
        image_data = urllib.request.urlopen(image_url).read()

        # Remove annoying complaints
        with contextlib.redirect_stderr(None):
            # set new meta data
            self.audio_file.tag.artist = self.artist
            self.audio_file.tag.title = self.title
            self.audio_file.tag.release_date = self.year
            self.audio_file.tag.genre = self.genre
            self.audio_file.tag.album = self.album
            self.audio_file.tag.images.set(3, image_data, "image/jpeg", "cover")

            # save new meta data
            self.audio_file.tag.save(version=eyed3.id3.ID3_V2_3)

        __import__('pprint').pprint(f"Successfully tagged {self.name}")
        self.success = True

    def _fetch_metadata_from_discogs(self) -> Union[dict[str, str], None]:
        """
        Fetch metadata from discogs
        """
        try:
            results = self.client.search(self.name, type="release")
            __import__('pprint').pprint(f"Found metadata for {self.name}")
            return results[0].__dict__.get("data")
        except Exception:
            __import__('pprint').pprint(f"Could not find metadata for {self.name}")
            return None
