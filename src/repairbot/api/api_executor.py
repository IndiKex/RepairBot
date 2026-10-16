from enum import Enum

from repairbot.query_handler.query_handler import QueryHandler
from repairbot.user_handler.user_handler import UserHandler


class user_cmd_type(Enum):
    ADD = 0
    REMOVE = 1
    AUTH = 2


class query_cmd_type(Enum):
    LIST = 0
    ADD = 1
    GET = 2


class APIExecutor:
    def __init__(self):
        self.user_handler = UserHandler()
        self.query_handler = QueryHandler()

    def user_handling(self, cmd: user_cmd_type, username: str, password: str) -> bool:
        match cmd:
            case user_cmd_type.ADD:
                return self.user_handler.add_user(username, password)
            case user_cmd_type.REMOVE:
                return self.user_handler.remove_user(username, password)
            case user_cmd_type.AUTH:
                return self.user_handler.authenticate_user(username, password)
        return False

    def query_handling(
        self,
        cmd: query_cmd_type,
        query_id: str | None,
        username: str | None,
        question: str | None,
    ) -> str | dict[str, dict[str, str]] | list[dict[str, dict[str, str]]] | None:
        match cmd:
            case query_cmd_type.ADD:
                return self.query_handler.add_query(username, question)
            case query_cmd_type.GET:
                return self.query_handler.get_query(query_id)
            case query_cmd_type.LIST:
                return self.query_handler.list_queries(username)
        return None
