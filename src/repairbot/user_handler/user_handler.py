from repairbot.user_handler.user_DBM import UserDBM


class UserHandler:
    def __init__(self):
        self.dbm = UserDBM()

    def add_user(self, username: str, password: str) -> bool:
        return self.dbm.add_user(username, password)

    def authenticate_user(self, username: str, password: str) -> bool:
        return self.dbm.authenticate_user(username, password)

    def remove_user(self, username: str, password: str) -> bool:
        return self.dbm.remove_user(username, password)
