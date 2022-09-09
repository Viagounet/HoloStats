import inspect
from dataclasses import dataclass


@dataclass
class User:
    channel_id: str
    channel_url: str
    name: str

    def __post_init__(self):
        self.is_member = False
        self.nb_messages = 0

    def add_message(self, message, channel):
        self.nb_messages += 1
        if message["author"]["type"] == "MEMBER":
            self.is_member = True

    def json(self):
        return {"channel-id": self.channel_id, "name": self.name, "member": self.is_member,
                "messages": self.nb_messages}

    def __repr__(self):
        return "user(channel_id={}, channel_url={})".format(self.channel_id, self.channel_url)
