import json


class UserDatabase:
    def __init__(self):
        self.file_path = "src/repairbot/api/experiment/user_data.txt"

    def find_user(self, user_name: str) -> dict[str, str] | None:
        with open(self.file_path, "r", encoding="utf-8") as f:
            line = f.readline()

            while line != "":
                try:
                    line_data = json.loads(line)
                    if line_data["username"] == user_name:
                        return line_data
                except json.JSONDecodeError:
                    continue
                line = f.readline()

            return None

    def add(self, user_data: dict[str, str]):
        with open(self.file_path, "a", encoding="utf-8") as f:
            if not self.find_user(user_data["username"]):
                f.write(json.dumps(user_data) + "\n")

    def authenticate(self, user_data: dict[str, str]) -> bool:
        saved_user_data = self.find_user(user_data["username"])
        return bool(
            saved_user_data and saved_user_data["password"] == user_data["password"]
        )
