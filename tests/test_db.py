from dotenv import load_dotenv
import pytest
from src.mcp_server_mariadb.server import get_connection, is_read_only_query

load_dotenv()

def test_db_connection():
    connection = get_connection()

    assert connection is not None

@pytest.mark.parametrize("query, expected", [
    
    ("SELECT * FROM users", True),
    ("SHOW TABLES", True),
    ("DESCRIBE users", True),
    ("DESC users", True),
    ("EXPLAIN SELECT * FROM users", True),
    
    # EDGE CASE: fails when using multiple queries, the trailing query being non-read only
    # This would have failed with earlier version
    ("SELECT * FROM users; DROP TABLE users;", False),
    
    ("""SELECT 
    employee_name, 
    department, status 
    FROM 
        Employee 
    WHERE 
        status = 'Active'
    ORDER BY 
        employee_name ASC;""", True),
    
    ("""DELETE FROM Employee 
    WHERE status = 'Left';""", False),
    
    ("SELECT * FROM Employee; DROP TABLE Employee;", False),
    
    ("""
    SELECT employee_name, department FROM Employee WHERE status = 'Active';
    SELECT department, COUNT(*) FROM Employee GROUP BY department;""", True),
    
    ("""
    SELECT employee_name, department FROM Employee WHERE status = 'Active';
    DELETE FROM Employee WHERE status = 'Left';""", False),
])
def test_query(query, expected):
    assert is_read_only_query(query) == expected


def test_is_read_only_query():
    assert is_read_only_query("SELECT * FROM users")
    assert is_read_only_query("SHOW TABLES")
    assert is_read_only_query("DESCRIBE users")
    assert is_read_only_query("DESC users")
    assert is_read_only_query("EXPLAIN SELECT * FROM users")
    


def test_is_not_read_only_query():
    assert not is_read_only_query(
        "INSERT INTO users (name, email) VALUES ('John', 'john@example.com');"
    )
    assert not is_read_only_query(
        "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')"
    )
    assert not is_read_only_query(
        "UPDATE users SET email = 'john@example.com' WHERE id = 1"
    )
    assert not is_read_only_query("DELETE FROM users WHERE id = 1")
    assert not is_read_only_query(
        "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))"
    )
    assert not is_read_only_query("DROP TABLE users")
