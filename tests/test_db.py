from dotenv import load_dotenv

from mariadb_server import DBconfig, get_connection

load_dotenv()

config = DBconfig()


# TODO: 127.0.0.1와 localhost 각각 connect할때 어떤 소켓을 사용하는지 확인하자.
# localhost일때에는 Error connecting to MariaDB Platform: Can't connect to local server through socket '/tmp/mysql.sock' (2)
def test_db_connection():
    connection = get_connection(config)

    assert connection is not None
