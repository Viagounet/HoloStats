from dataclasses import dataclass

from youtube.video import Video, Stream
from yt_api import return_video_ids


@dataclass
class Channel:
    def __init__(self, id):
        self.id = id
        self.playlist_id: str = "UU" + self.id[
                                       2:]  # Replacing the U with a C in the channel id to obtain the playlist id

        self.name: str = ""
        self.videos = []


    def retrieve_streams(self):
        for stream_id in return_video_ids(self.playlist_id):
            stream = Stream(stream_id, self)
            stream.chat.start()
            self.videos.append(stream)

    def __repr__(self):
        return f"Channel(id={self.id}, videos={[video for video in self.videos[:3]]}, ..., {self.videos[-1]})"

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "videos": [video.json() for video in self.videos]
        }