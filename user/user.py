from dataclasses import dataclass



@dataclass
class User:
    channel_id: str
    channel_url: str
    name: str

    def __post_init__(self):
        self.channels = {}
        self.is_member = False

    def add_message(self, message, channel):
        if message["author"]["type"] == "MEMBER":
            self.is_member = True
        if channel.id not in self.channels.keys():
            self.channels[channel.id] = {"messages": 1}
        else:
            self.channels[channel.id]["messages"] += 1
    @property
    def nb_messages(self):
        return sum([channel.nb_messages for channel in self.channels.values()])

    def __repr__(self):
        return "user(channel_id={}, channel_url={}, channels={})".format(self.channel_id, self.channel_url, self.channels)
