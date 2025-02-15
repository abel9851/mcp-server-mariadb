import os
from dataclasses import dataclass

import mariadb
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(
    "MariaDB Explorer", dependencies=["mysql-connector-python", "python-dotenv"]
)


# TODO: dataclass, decorator 친숙해지기
# DBconfig는 connection을 하기 위한 정보를 보관하는 클래스이니까 dataclass로 정의하자.
@dataclass
class DBconfig:
    host: str = os.getenv("MARIADB_HOST")
    port: int = int(os.getenv("MARIADB_PORT", "3306"))
    user: str = os.getenv("MARIADB_USER", "")
    password: str = os.getenv("MARIADB_PASSWORD", "")
    database: str = os.getenv("MARIADB_DATABASE", "")


# TODO: 함수가 커지면 DB manager와 같은 class로 변경하자.
def get_connection():
    """Create a connection to the database connection"""

    # dataclass의 인스턴스
    config = DBconfig()

    # try하는 이유는 connection이라는 것이 실패할수 있는 callable객체이기 때문이다.
    # TODO: test connection to use pytest
    try:
        conn = mariadb.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")


def is_read_only_query(query: str) -> bool:
    """check if a query is read-only by examining its first word"""
    first_word = query.strip().split()[0].upper()

    read_only_commands = ["SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN"]

    return first_word in read_only_commands


# TODO: what is resource?
# TODO: decorator pattern
# after understand pattern, create framework?
# 1. Build a mariadb mcp server
# 2. Build a xxxx mcp server(javascript)
# 3. Build a framework from scratch
# 4. Build a mcp server by using framework
# TODO: 제일 먼저 할 것은, 이 list_tables가 mcp server로서 claude와 cursor에서 동작하는지 검증하는 것.
# 산책갔다 온 다음에 하자
# claude에서 mcp를 사용하려면 tool을 등록해야하나보다?
# TODO: tool까지 등록한 다음에 cluade desktop에서 mcp를 사용해보자
@mcp.resource("schema://tables")
def list_tables() -> str:
    """Get the schema for a specific table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()  # TODO: what fetchall?
        return "\n".join(table[0] for table in tables)
    except Exception as e:
        return f"Error retreiving tables: {str(e)}"
    finally:
        # TODO: locals()?
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")
