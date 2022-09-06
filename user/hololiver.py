import json
import logging
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
                elif user.is_member and user.channel_id in members_dict:
                    members_dict[user.channel_id].nb_messages += user.nb_messages
        return members_dict

    @property
    def members_by_month(self):
        members = {}
        for stream in self.videos:
            if hasattr(stream, 'actual_start_time'):
                year, month = stream.actual_start_time.year, stream.actual_start_time.month
                members.setdefault(year, {})
                members[year].setdefault(month, {})
                user_set = stream.chat.members
                for user in user_set:
                    # A little bit convoluted but ay, it works..
                    if user.is_member and user.channel_id not in members[year][month].keys():
                        members[year][month][user.channel_id] = user
                    elif user.is_member and user.channel_id in members:
                        members[year][month][user.channel_id].nb_messages += user.nb_messages
        return members

    @property
    def nb_numbers(self):
        return len(self.members)

    def __repr__(self):
        return f"Hololiver(name={self.name}, channel={self.channel})"

    def retrieve_streams(self):
        for stream_id in return_video_ids(self.playlist_id):
            try:
                print(f"Retrieving info about : {stream_id}")
                stream = Stream(stream_id, self)
                stream.chat.start()
                self.videos.append(stream)
                print(
                    f"Done! Members found {len(stream.chat.members)} / Total members for {self.name} : {self.nb_numbers} - {stream}")
                self.save()
            except Exception as ex:
                print("There's been an error while processing streams :", ex)
                logging.error("There's been an error while processing streams", exc_info=True)

    @property
    def json(self):
        return {
            "videos": [video.json() for video in self.videos],
            "name": self.name,
            "stats": [],
            "members": {
                year: {
                    month: {"members-list": [member.json() for member in self.members_by_month[year][month].values()],
                            "nb-members": len(
                                [member.json() for member in self.members_by_month[year][month].values()])} for month in
                    self.members_by_month[year].keys()} for year in self.members_by_month.keys()}
        }

    @property
    def light_json(self):
        return {
            "name": self.name,
            "stats": [],
            "members": {
                year: {
                    month: {"nb-members": len(
                                [member.json() for member in self.members_by_month[year][month].values()])} for month in
                    self.members_by_month[year].keys()} for year in self.members_by_month.keys()}
        }
    def save(self):
        with open(f"data/full/{self.name}.json", "w") as f:
            json.dump(self.json, f)
        with open(f"data/light/{self.name}.json", "w") as f:
            json.dump(self.light_json, f)
