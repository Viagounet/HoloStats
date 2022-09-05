import json
from dataclasses import dataclass

from stats.holostats import Holostats
from youtube.channel import Channel
from youtube.video import Stream
from yt_api import return_video_ids


@dataclass
class Hololiver(Channel):
    def __init__(self, name: str, id: str):
        super(Hololiver, self).__init__(id=id)
        self.name = name
        self.id = id

        self.statistics: Holostats = Holostats()

    @property
    def members(self):
        members_dict = {}
        for stream in self.videos:
            user_set = stream.chat.members
            for user in user_set:
                if user.is_member and user.channel_id not in members_dict:
                    members_dict[user.channel_id] = user
        return members_dict

    @property
    def nb_numbers(self):
        return len(self.members)

    def __repr__(self):
        return f"Hololiver(name={self.name}, channel={self.channel})"

    def retrieve_streams(self):
        for stream_id in return_video_ids(self.playlist_id):
            print(f"Retrieving info about : {stream_id}")
            stream = Stream(stream_id, self)
            stream.chat.start()
            self.videos.append(stream)
            print(f"Done! Members found {len(stream.chat.members)} / Total members for {self.name} : {self.nb_numbers} - {stream}")


    @property
    def json(self):
        return {
            "channel": super(Hololiver, self).json(),
            "name": self.name,
            "stats": [],
            "members": self.members
        }

    def save(self):
        with open(f"{self.name}.json", "w") as f:
            json.dump(self.json, f)