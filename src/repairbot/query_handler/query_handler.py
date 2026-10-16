from uuid import uuid4

from repairbot.ai_provider.ai_handler import AIHandler
from repairbot.query_handler.query_DBM import QueryDBM


class QueryHandler:
    def __init__(
        self, use_ai=True, data_path: str = "data/query_data/query_database.txt"
    ):
        self.dbm = QueryDBM(data_path)
        self.use_ai = use_ai
        if self.use_ai:
            self.ai_handler = AIHandler()

    def add_query(self, username: str, question: str) -> str | None:
        query_id = str(uuid4())

        answer: str = ""
        if self.use_ai:
            answer = self.ai_handler.query(question)
        else:
            answer = f"Answer to {question}"

        success: bool = self.dbm.add_query(query_id, username, question, answer)
        if success:
            return query_id
        return None

    def get_query(self, query_id: str) -> dict[str, dict[str, str]] | None:
        return self.dbm.get_query(query_id)

    def list_queries(self, username: str) -> list[dict[str, dict[str, str]]]:
        return self.dbm.list_queries(username)

    def delete_query(self, query_id: str) -> bool:
        return self.dbm.delete_query(query_id)
