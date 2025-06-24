# mcp-server-mariadb

An MCP server implementation for retrieving data from MariaDB

## Features

### Resources

Expose the schema list in database

### Tools

- query_database
  - Execute read-only operations against MariaDB

## Dependencies

### Install MariaDB

- Macintosh
  - When installing MariaDB, you may oserve the following OS error. You can resolve this by installing mariadb-connector-c.

```bash
OSError: mariadb_config not found.

      This error typically indicates that MariaDB Connector/C, a dependency which
      must be preinstalled, is not found.
      If MariaDB Connector/C is not installed, see installation instructions
      If MariaDB Connector/C is installed, either set the environment variable
      MARIADB_CONFIG or edit the configuration file 'site.cfg' to set the
       'mariadb_config' option to the file location of the mariadb_config utility.
```

1. Execute `brew install mariadb-connector-c`
2. Execute `echo 'export PATH="/opt/homebrew/opt/mariadb-connector-c/bin:$PATH"' >> ~/.bashrc`
3. Set an environment variable `export MARIADB_CONFIG=$(brew --prefix mariadb-connector-c)/bin/mariadb_config`
4. Execute `uv add mariadb` again.

## Usage with Claude Desktop

### Configuration File

Paths to the Claude Desktop configuration file:

- **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
<!-- markdownlint-disable MD033 -->
<details>
<summary>Add this configuration to enable published servers</summary>

```json

{
    "mcpServers": {
        "mcp_server_mariadb": {
            "command": "/PATH/TO/uvx"
            "args": [
                "mcp-server-mariadb",
                "--host",
                "${DB_HOST}",
                "--port",
                "${DB_PORT}",
                "--user",
                "${DB_USER}",
                "--password",
                "${DB_PASSWORD}",
                "--database",
                "${DB_NAME}"
            ]
        }
    }
}

```

**Note**: Replace these placeholders with actual paths:

- `/PATH/TO/uvx`: Full path to uvx executable

</details>

<details>
<summary>Add this configuration to enable development/unpublished servers</summary>

```json
{
    "mcpServers": {
        "mcp_server_mariadb": {
            "command": "/PATH/TO/uv",
            "args": [
                "--directory",
                "/YOUR/SOURCE/PATH/mcp-server-mariadb/src/mcp_server_mariadb",
                "run",
                "server.py"
            ],
            "env": {
                "MARIADB_HOST": "127.0.0.1",
                "MARIADB_USER": "USER",
                "MARIADB_PASSWORD": "PASSWORD",
                "MARIADB_DATABASE": "DATABASE",
                "MARIADB_PORT": "3306"
            }
        }
    }
}
```

**Note**: Replace these placeholders with actual paths:

- `/PATH/TO/uv`: Full path to UV executable
- `/YOUR/SOURCE/PATH/mcp-server-mariadb/src/mcp_server_mariadb`: Path to server source code

</details>

## License

This MCP server is licensed under the MIT license. Please see the LICENSE file in the repository for more information.
