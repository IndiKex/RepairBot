import json


class QueryDBM:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def find_query(self, query_id: str) -> dict[str, dict[str, str]] | None:
        with open(self.data_path, "r") as f:
            line = f.readline()

            while line != "":
                try:
                    line_data = json.loads(line)
                    if line_data["query_id"] == query_id:
                        return line_data

                except json.JSONDecodeError:
                    continue

                line = f.readline()

        return None

    def get_query(self, query_id: str) -> dict[str, dict[str, str]] | None:
        query = self.find_query(query_id)
        return query

    def add_query(
        self, query_id: str, username: str, question: str, answer: str
    ) -> bool:
        found_query = self.find_query(query_id)
        if found_query:
            return False

        query = {
            "query_id": query_id,
            "content": {"username": username, "question": question, "answer": answer},
        }

        with open(self.data_path, "a") as f:
            f.write(json.dumps(query) + "\n")

        return True

    def list_queries(self, username: str) -> list[dict[str, dict[str, str]]]:
        res = []
        with open(self.data_path, "r") as f:
            line = f.readline()
            while line != "":
                try:
                    line_data = json.loads(line)
                    if line_data["content"]["username"] == username:
                        res.append(line_data)

                except json.JSONDecodeError:
                    continue

                line = f.readline()

        return res

    def delete_query(self, query_id: str) -> bool:
        found: bool = False
        lines: list[str] = []
        with open(self.data_path, "r") as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                try:
                    line_data = json.loads(line)
                    if line_data["query_id"] == query_id:
                        lines[i] = ""
                        found = True
                        break

                except json.JSONDecodeError:
                    continue

                line = f.readline()

        if not found:
            return False

        with open(self.data_path, "w") as f:
            f.writelines(lines)

        return True
