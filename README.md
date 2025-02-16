# MCP MariaDB Server

## dependency

### install mariadb

- mac
  - when install mariadb,
maybe raise os error below.
you can resolve by installing mariadb-connector-c.

```bash

OSError: mariadb_config not found.

      This error typically indicates that MariaDB Connector/C, a dependency which
      must be preinstalled, is not found.
      If MariaDB Connector/C is not installed, see installation instructions
      If MariaDB Connector/C is installed, either set the environment variable
      MARIADB_CONFIG or edit the configuration file 'site.cfg' to set the
       'mariadb_config' option to the file location of the mariadb_config utility.


```

1. execute `brew install mariadb-connector-c`
2. execute `echo 'export PATH="/opt/homebrew/opt/mariadb-connector-c/bin:$PATH"' >> ~/.bashrc`
3. set environment variable `export MARIADB_CONFIG=$(brew --prefix mariadb-connector-c)/bin/mariadb_config`
4. execute `uv add mariadb` again.

## setting claude desktop

```json

{
    "mcpServers": {
        "mcp_server_mariadb": {
            "command": "/PATH/uv",
            "args": [
                "--directory",
                "SOURCECODE_PATH/mcp-server-mariadb",
                "run",
                "mariadb_server.py"
            ]
        }
    }
}

```
