import argparse
import os
from contextlib import closing
from dataclasses import dataclass, field
import mariadb
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

import sqlparse
from sqlparse.tokens import DML


load_dotenv()

mcp = FastMCP(
    "MariaDB Explorer", dependencies=["mysql-connector-python", "python-dotenv"]
)

READ_ONLY_KEYWORDS = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")
READ_ONLY_KEYWORD_NAMES = ", ".join(READ_ONLY_KEYWORDS)


def get_arguments() -> dict:
    """Parse command-line arguments and return as a dictionary."""
    parser = argparse.ArgumentParser(description="MariaDB Configuration")
    parser.add_argument("--host", help="MariaDB host")
    parser.add_argument("--port", type=int, help="MariaDB port")
    parser.add_argument("--user", help="MariaDB user")
    parser.add_argument("--password", help="MariaDB password")
    parser.add_argument("--database", help="MariaDB database")
    args = parser.parse_args()

    return {k: v for k, v in vars(args).items() if v is not None}


@dataclass
class DBconfig:
    """Database configuration"""

    host: str = field(default_factory=lambda: os.getenv("MARIADB_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("MARIADB_PORT", "3306")))
    user: str = field(default_factory=lambda: os.getenv("MARIADB_USER", ""))
    password: str = field(default_factory=lambda: os.getenv("MARIADB_PASSWORD", ""))
    database: str = field(default_factory=lambda: os.getenv("MARIADB_DATABASE", ""))

    @classmethod
    def from_args(cls) -> "DBconfig":
        """Create a DBconfig instance from command-line arguments and environment variables."""
        cli_args = get_arguments()
        return cls(**{**cls().__dict__, **cli_args})


def get_connection():
    """Create a connection to the database connection"""
    config = DBconfig.from_args()

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


def is_read_only_query(query: str) -> str:
    # only allow readonly keywords
    READ_ONLY_KEYWORDS = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")
    
    cleaned = sqlparse.format(query, strip_comments=True, strip_whitespace=True, strip_newlines=True)
    statements = sqlparse.parse(cleaned)

    

    # evaluate each statement, to handle multi-statement query
    for statement in statements:
        first_token = next((token for token in statement.tokens if token.ttype is not token.is_whitespace), None)
        
        # query is empty, invalid
        if first_token is None:
            return False
        
        # keyword is not a valid DML
        if (first_token.value.upper() not in READ_ONLY_KEYWORDS):
            return False
        
        tokens = cleaned.upper().split()
        blacklisted_keywords = (
            "INSERT", 
            "UPDATE", 
            "DELETE", 
            "REPLACE", 
            "CREATE", 
            "ALTER", 
            "DROP",
            "INTO",
            "TRUNCATE",
            "LOAD_FILE",
            "DUMPFILE",
            "OUTFILE"
        )
        
        # if any tokens are in blacklisted keywords, return false
        if any(token in tokens for token in blacklisted_keywords):
            return False
    
    return True
        



@mcp.resource("schema://tables")
def list_tables() -> str:
    """Get the schema for a specific table"""
    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            return "\n".join(table[0] for table in tables)
    except Exception as e:
        return f"Error retrieving tables: {str(e)}"


@mcp.tool()
def query_database(query: str) -> str:
    """
    Execute a read-only SQL query on the database

    Args:
        query: SQL query to execute (must be SELECT, SHOW, DESCRIBE, DESC, EXPLAIN)
    """

    if not is_read_only_query(query):
        return "Error: Only read-only queries (SELECT, SHOW, DESCRIBE, DESC, EXPLAIN) are allowed"

    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in cursor.description]

            # Format results as a table
            output = []
            output.append(" | ".join(columns))
            output.append(
                "-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1))
            )

            for row in results:
                output.append(" | ".join(str(val) for val in row))

            return "\n".join(output)
    except Exception as e:
        return f"Error executing query {str(e)}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
