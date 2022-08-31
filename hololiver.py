import logging

from dataclasses import dataclass

from yt_api import return_video_ids, get_video_details
import pytchat
import json

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s\n\n\n',
                    datefmt='%d-%b-%y %H:%M:%S')


class Holostats:
    pass


@dataclass
class Video:
    id: str
    channel_id: str

    def __post_init__(self):
        try:
            infos = get_video_details(self.id)
            for key, value in infos.items():
                setattr(self, key, value)
            print("Successfully retrieved video details for {}".format(self.id))
        except Exception as e:
            print("Video error occured (id={})".format(self.id))
            logging.error("Exception occurred", exc_info=True)

    def json(self):
        return {
            key: value for key, value in self.__dict__.items() if not key.startswith("_")
        }

    def __repr__(self):
        return "Video(id={}, views={}, title={}, date={}, length={})".format(self.id, self.views, self.title, self.date,
                                                                             self.length)


class Stream(Video):
    def __init__(self, id, channel_id):
        super().__init__(id, channel_id)
        self.chat = Chat(id, channel_id)
        self.chat.start()


class UserSet:
    def __init__(self, users):
        self.users = users

    def retrieve_user_by_id(self, id):
        return self.users[id]

    def manage_message(self, message, channel_id):
        if message["author"]["channelId"] in self.users:
            user = self.retrieve_user_by_id(message["author"]["channelId"])
            user.add_message(message, channel_id)
            print(user)
        else:
            user = User(message["author"]["channelId"], message["author"]["channelUrl"])
            user.add_message(message, channel_id)
            self.users[user.channel_id] = user


    def __repr__(self):
        return "UserSet(users={})".format(self.users.keys())


class ChannelUserStat:
    def __init__(self, user_channel_id, streamer_channel_id, sub_type):
        self.nb_messages = 1
        self.is_chat_owner = streamer_channel_id == user_channel_id
        if sub_type == "MEMBER":
            self.is_member = True
        else:
            self.is_member = False

    def add_message(self):
        self.nb_messages += 1

    def __repr__(self):
        return "ChannelUserStat(nb_messages={}, is_chat_owner={}, is_member={})".format(self.nb_messages, self.is_chat_owner, self.is_member)

@dataclass
class User:
    channel_id: str
    channel_url: str

    def __post_init__(self):
        self.channels = {}

    def add_message(self, message, channel_id):
        if channel_id not in self.channels.keys():
            self.channels[channel_id] = ChannelUserStat(self.channel_id, channel_id, message["author"]["type"])
        else:
            self.channels[channel_id].add_message()

    @property
    def nb_messages(self):
        return sum([channel.nb_messages for channel in self.channels.values()])

    def __repr__(self):
        return "User(channel_id={}, channel_url={}, channels={})".format(self.channel_id, self.channel_url, self.channels)

@dataclass
class Chat:
    id: str
    channel_id: str
    chatters: UserSet = UserSet({})
    n_messages: int = 0

    def start(self):
        chat = pytchat.create(video_id="1viouXswSRA")
        while chat.is_alive():
            _ = json.loads(chat.get().json())

            for message in _:
                self.chatters.manage_message(message, self.channel_id)
                self.n_messages += 1

    @property
    def members(self):
        return [c for c in self.chatters if c.is_member]


@dataclass
class Channel:
    def __init__(self, id):
        self.id: str = id
        self.playlist_id: str = "UU" + self.id[
                                       2:]  # Replacing the U with a C in the channel id to obtain the playlist id
        self.videos: list[Video] = [Stream(id=video_id, channel_id=self.id) for video_id in
                                    return_video_ids(self.playlist_id)]

        self.name: str = ""

    def __repr__(self):
        return f"Channel(id={self.id}, videos={[video for video in self.videos[:3]]}, ..., {self.videos[-1]})"

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "videos": [video.json() for video in self.videos]
        }


@dataclass
class Hololiver:
    name: str
    channel: Channel
    statistics: Holostats = Holostats()

    def __post_init__(self):
        self.members = {}

    def add_member(self, user):
        self.members[user.channel_id] = user

    def nb_numbers(self):
        return len(self.members)

    def __repr__(self):
        return f"Hololiver(name={self.name}, channel={self.channel})"

    @property
    def json(self):
        return {
            "name": self.name,
            "channel": self.channel.json,
            "statistics": []
        }

    def save(self):
        with open(f"{self.name}.json", "w") as f:
            json.dump(self.json, f)
