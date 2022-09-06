from user.user import User


class UserSet:
    def __init__(self, users):
        self.users = users

    def retrieve_user_by_id(self, id):
        return self.users[id]

    def manage_message(self, message, channel_id):
        if message["author"]["channelId"] in self.users:
            user = self.retrieve_user_by_id(message["author"]["channelId"])
            user.add_message(message, channel_id)

        else:
            user = User(message["author"]["channelId"], message["author"]["channelUrl"], message["author"]["name"])
            user.add_message(message, channel_id)
            self.users[user.channel_id] = user

    def __iter__(self):
        return (user for user in self.users.values())

    def __repr__(self):
        return self.users.keys()