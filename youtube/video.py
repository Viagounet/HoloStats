import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from user.user import User
from youtube.chat import Chat
from yt_api import get_video_details


@dataclass
class Video:
    def __init__(self, id: str, channel):
        """
        Information about a video and its statistics
        :param id: Youtube id of the video
        :param channel: The Youtube channel from which  the video originates
        """

        self.id = id

        # Retrieving the infos for the Video
        try:
            infos = get_video_details(self.id)
            for key, value in infos.items():
                setattr(self, key, value)
            print("Successfully retrieved video details for {}".format(self.id))
        # Broad exception but I really don't want the script to crash
        # I should probably look for the different exceptions when I have time
        except Exception as e:
            print("Video error occured (id={})".format(self.id))
            logging.error("Video error occured", exc_info=True)

    def json(self):
        json_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, datetime):
                    json_dict[key] = value.strftime('%m/%d/%Y - %H:%M:%S')
                elif isinstance(value, timedelta):
                    json_dict[key] = value.__str__()
                elif isinstance(value, Chat):
                    pass
                else:
                    json_dict[key] = value
        return json_dict

    def __repr__(self):
        try:
            string = "Video(id={}, views={}, title={}, duration={})".format(self.id, self.views, self.title,
                                                                            self.duration)

        # Yeah I know I should do a case-by-case exception system but honestly I don't really care
        except Exception as ex:
            string = str(ex)

        return string


class Stream(Video):
    def __init__(self, id, channel, json_format=None):
        super().__init__(id, channel)
        if json_format:
            self.load(json_format)
        else:
            self.chat = Chat(id, channel)
            self.chat.start()
            self.members = self.chat.members

    def json(self):
        return {**super().json(), **{"members": [member.json() for member in self.members]}}

    def load(self, json_format):
        # A little bit of a hack to load previous data..
        self.members = [User(channel_id=member_json["channel-id"], channel_url="", name=member_json["name"]) for
                        member_json in json_format["members"]]
        for member, member_json in zip(self.members, json_format["members"]):
            member.nb_messages = member_json["messages"]
            member.is_member = True
