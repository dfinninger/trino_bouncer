"""Run an integration test against trino_bouncer"""

import requests
from trino.dbapi import connect, Connection

HOST="http://127.0.0.1"

def query(conn: Connection) -> None:
    cur = conn.cursor()
    result = cur.execute("select count(*) from tpch.sf1.nation")
    assert [[25]] == result.fetchall(), "oops"

def swap(color: str) -> None:
    requests.post(f"{HOST}:5000/switch?cluster={color}")

def get_active() -> dict[str, str]:
    return requests.get(f"{HOST}:5000/status").json()


if __name__ == "__main__":
    conn = connect(host=HOST, port=5000, user="test")

    swap("green")
    for _ in range(10):
        assert "green" == get_active()['name']
        query(conn)

    swap("blue")
    for _ in range(10):
        assert "blue" == get_active()['name']
        query(conn)

