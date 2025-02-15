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
def get_connection(config: DBconfig):
    """Create a connection to the database connection"""

    # dataclass의 인스턴스
    config = DBconfig()

    # try하는 이유는 connection이라는 것이 실패할수 있는 callable객체이기 때문이다.
    # TODO: test connection to use pytest
    try:
        connection = mariadb.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
        )
        return connection
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")


def is_read_only_query(query: str) -> bool:
    """check if a query is read-only by examining its first word"""
    first_word = query.strip().split()[0].upper()

    read_only_commands = ["SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN"]

    return first_word in read_only_commands
