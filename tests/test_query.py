import os

from repairbot.query_handler.query_handler import QueryHandler

data_path = "tests/test_query_data.txt"

with open(data_path, "w") as f:
    f.write("")

qh = QueryHandler(use_ai=False, data_path=data_path)
username1: str = "TEST1"
username2: str = "TEST2"
query_ids: dict[str, list[str]] = {username1: [], username2: []}
expected_queries: dict[str, list[dict[str, dict[str, str]]]] = {
    username1: [],
    username2: [],
}


def add_query_id_expected(query_id: str, username: str):
    query_ids[username].append(query_id)
    expected_query = {
        "query_id": query_id,
        "content": {
            "username": username,
            "question": "test?" + str(len(query_ids[username])),
            "answer": "Answer to test?" + str(len(query_ids[username])),
        },
    }
    expected_queries[username].append(expected_query)


def test_query_list_none():
    assert qh.list_queries(username1) == []
    assert qh.list_queries(username2) == []


def test_query_add_1():
    query_id = qh.add_query(username1, "test?1")
    assert query_id != None
    add_query_id_expected(query_id, username1)


def test_query_get_1():
    print(query_ids[username1][0])
    result = qh.get_query(query_ids[username1][0])
    assert result == expected_queries[username1][0]


def test_query_list_1():
    result = qh.list_queries(username1)
    assert result == expected_queries[username1]


def test_query_list_2():
    result = qh.list_queries(username2)
    assert result == []


def test_query_add_2():
    query_id = qh.add_query(username1, "test?2")
    assert query_id != None
    add_query_id_expected(query_id, username1)


def test_query_get_1_after_2():
    result = qh.get_query(query_ids[username1][0])
    assert result == expected_queries[username1][0]


def test_query_get_2_after_2():
    result = qh.get_query(query_ids[username1][1])
    assert result == expected_queries[username1][1]


def test_query_list_afte_2():
    result = qh.list_queries(username1)
    assert result == expected_queries[username1]


def test_delete():
    for query_id in query_ids[username1]:
        assert qh.delete_query(query_id) == True


def test_list_after_delete():
    assert qh.list_queries(username1) == []
    assert qh.list_queries(username2) == []


def test_remove_file():
    if os.path.exists(data_path):
        os.remove(data_path)
    else:
        assert False
