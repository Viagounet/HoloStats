import json
import logging
import time

import httpx
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
        validated = False
        i = 0
        while not validated or i > 3:
            try:
                chat = pytchat.create(video_id=self.id)
                validated = True
            except httpx.ReadTimeout:
                i += 1
                print("Error loading chat")
                logging.error("Exception occurred (Error loading chat) ", exc_info=True)
                time.sleep(5)

        while chat.is_alive():
            try:
                _ = json.loads(chat.get().json())
                for message in _:
                    self.chatters.manage_message(message, self.channel)
                    self.n_messages += 1
            except Exception:
                print("Error reading chat")
                logging.error("Exception occurred (Error reading chat) ", exc_info=True)

    def json(self):
        return {"members":[member.json() for member in self.members], "number messages":self.n_messages}
    @property
    def members(self):
        return [c for c in self.chatters if c.is_member]