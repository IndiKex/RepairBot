from src.repairbot.query_handler.query_DBM import QueryDBM
from src.repairbot.ai_provider.ai_handler import AIHandler
from uuid import uuid4

class QueryHandler:
    def __init__(self):
        self.dbm = QueryDBM()
        self.ai_handler = AIHandler()

    def add_query(self, username: str, question: str) -> str | None:
        query_id = str(uuid4())
        answer: str = self.ai_handler.query(question)
        success: bool = self.dbm.add_query(query_id, username, question, answer)
        if success:
            return query_id
        return None
    
    def get_query(self, query_id: str) -> dict[str, dict[str, str]] | None:
        return self.dbm.get_query(query_id)
    
    def list_queries(self, username: str) -> list[dict[str, dict[str, str]]]:
        return self.dbm.list_queries(username)


