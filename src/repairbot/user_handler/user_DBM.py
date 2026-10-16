import json


class UserDBM:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def find_user_id(self, username: str) -> int:
        with open(self.data_path, "r") as f:
            i = 0
            line = f.readline()
            while line != "":
                try:
                    line_data = json.loads(line)
                    if line_data["username"] == username:
                        return i
                except json.JSONDecodeError:
                    continue
                line = f.readline()
                i += 1
        return -1

    def find_user(self, username: str) -> dict[str, str] | None:
        with open(self.data_path, "r") as f:
            line = f.readline()
            while line != "":
                try:
                    line_data = json.loads(line)
                    if line_data["username"] == username:
                        return line_data
                except json.JSONDecodeError:
                    continue
                line = f.readline()
        return None

    def add_user(self, username: str, password: str) -> bool:
        if self.find_user(username):
            return False
        with open(self.data_path, "a") as f:
            user_data = {"username": username, "password": password}
            f.write(json.dumps(user_data) + "\n")
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        user_data = self.find_user(username)
        return user_data != None and user_data["password"] == password

    def remove_user(self, username: str, password: str) -> bool:
        target_idx = self.find_user_id(username)
        target_user = self.find_user(username)

        if target_idx < 0 or not target_user or target_user["password"] != password:
            return False

        lines: list[str]
        with open(self.data_path, "r") as f:
            lines = f.readlines()
            lines[target_idx] = ""

        with open(self.data_path, "w") as f:
            f.writelines(lines)

        return True
