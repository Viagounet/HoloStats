from user.hololiver import Hololiver


class HololiversManager:
    def __init__(self):
        self.hololivers = {}

    def add_hololiver(self, name: str, channel_id: str):
        self.hololivers[channel_id] = Hololiver(name=name, id=channel_id)

    def retrieve_hololiver(self, id):
        return self.hololivers[id]
