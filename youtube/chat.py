import json
import pytchat

from dataclasses import dataclass

from user.userset import UserSet


@dataclass
class Chat:
    def __init__(self, id: str, channel):
        self.id = id
        self.channel = channel

        self.chatters: UserSet = UserSet({})
        self.n_messages: int = 0

    def start(self):
        chat = pytchat.create(video_id=self.id)
        while chat.is_alive():
            _ = json.loads(chat.get().json())
            for message in _:
                self.chatters.manage_message(message, self.channel)
                self.n_messages += 1

    @property
    def members(self):
        return [c for c in self.chatters if c.is_member]