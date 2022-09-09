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
        self.members_dict = {}
        self.members_by_month_dict = {}
        self.statistics: Holostats = Holostats()

    @property
    def members(self):
        for stream in self.videos:
            user_set = stream.chat.members
            for user in user_set:
                if user.is_member and user.channel_id not in self.members_dict:
                    self.members_dict[user.channel_id] = {"name": user.name, "nb_messages": user.nb_messages,
                                                          "channel_url": user.channel_url}
                elif user.is_member and user.channel_id in self.members_dict:
                    self.members_dict[user.channel_id]["nb_messages"] += user.nb_messages
        return self.members_dict

    @property
    def members_by_month(self):
        for stream in self.videos:
            if hasattr(stream, 'actual_start_time'):
                year, month = stream.actual_start_time.year, stream.actual_start_time.month
                self.members_by_month_dict.setdefault(year, {})
                self.members_by_month_dict[year].setdefault(month, {})
                user_set = stream.chat.members
                for user in user_set:
                    # A little bit convoluted but ay, it works..
                    if user.is_member and user.channel_id not in self.members_by_month_dict[year][month].keys():
                        self.members_by_month_dict[year][month][user.channel_id] = {"name": user.name,
                                                                                    "channel_url": user.channel_url}
        return self.members_by_month_dict

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
                self.videos.append(stream)
                print(
                    f"Done! Members found {len(stream.chat.members)} / Total members for {self.name} : {self.nb_numbers} - {stream}")
                self.save()
            except Exception as ex:
                print("There's been an error while processing streams :", ex)
                logging.error("There's been an error while processing streams", exc_info=True)

    @property
    def json(self):
        videos = self.videos
        videos_json = [video.json() for video in videos]
        self.monthly_members_dict = self.members_by_month
        json_dict = {
            "videos": videos_json,
            "name": self.name,
            "stats": [],
            "members": {
                year: {
                    month: {"members-list": [member for member in self.monthly_members_dict[year][month].values()],
                            "nb-members": len(
                                [member for member in self.monthly_members_dict[year][month].values()])} for month in
                    self.monthly_members_dict[year].keys()} for year in self.monthly_members_dict.keys()}
        }
        return json_dict

    @property
    def light_json(self):
        return {
            "name": self.name,
            "stats": [],
            "members": {
                year: {
                    month: {"nb-members": len(
                        [member for member in self.members_by_month[year][month].values()])} for month in
                    self.members_by_month[year].keys()} for year in self.members_by_month.keys()}
        }

    def save(self):
        with open(f"data/full/{self.name}.json", "w") as f:
            json.dump(self.json, f)
        with open(f"data/light/{self.name}.json", "w") as f:
            json.dump(self.light_json, f)
