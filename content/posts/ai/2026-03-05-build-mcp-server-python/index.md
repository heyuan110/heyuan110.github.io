+++
date = '2026-03-05T14:00:00+08:00'
draft = false
title = 'Build MCP Servers in Python: Complete Step-by-Step Tutorial'
description = 'Learn to build MCP servers in Python with FastMCP. Complete tutorial covering tools, resources, prompts, testing with MCP Inspector, and deployment.'
toc = true
tags = ['MCP', 'Python', 'Claude Code', 'AI Agent', 'Tutorial']
categories = ['AI Guides']
keywords = ['build MCP server Python', 'MCP server Python tutorial', 'Python MCP server', 'FastMCP tutorial', 'Model Context Protocol Python', 'MCP Python SDK', 'create MCP tools Python']

[[params.faqItems]]
question = "What Python version do I need to build MCP servers?"
answer = "You need Python 3.10 or higher. The MCP Python SDK officially supports Python 3.10, 3.11, 3.12, and 3.13. The SDK uses modern Python features like type hints and match statements that require 3.10+."

[[params.faqItems]]
question = "What is FastMCP and how does it relate to the MCP Python SDK?"
answer = "FastMCP is the high-level framework included in the official MCP Python SDK (the mcp package on PyPI). It provides a decorator-based API for building MCP servers — you use @mcp.tool(), @mcp.resource(), and @mcp.prompt() to register capabilities. It is the recommended way to build Python MCP servers."

[[params.faqItems]]
question = "Can I use pip instead of uv to install the MCP Python SDK?"
answer = "Yes. Install with pip install mcp[cli] for the full package including CLI tools, or pip install mcp for just the library. However, uv is recommended because it is significantly faster, handles virtual environments automatically, and is the tool used in the official MCP documentation."

[[params.faqItems]]
question = "How do I test my Python MCP server before connecting it to Claude Code?"
answer = "Run mcp dev server.py to launch the MCP Inspector, a web-based testing interface at http://127.0.0.1:6274. You can test each tool, resource, and prompt interactively. Once satisfied, connect to Claude Code with claude mcp add."

[[params.faqItems]]
question = "What is the difference between building MCP servers in Python vs TypeScript?"
answer = "Both languages have official SDKs. Python uses decorator-based registration (@mcp.tool()) while TypeScript uses method calls (server.registerTool()). Python is better for data science, ML pipelines, and scripting tasks. TypeScript has a slightly more mature SDK. The protocol is identical — servers built in either language work with any MCP client."
+++

![Build MCP servers in Python with FastMCP step by step tutorial](cover.webp)

Python is the most popular language for AI developers, and the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) makes it remarkably easy to build custom MCP servers. With the decorator-based FastMCP framework, you can go from zero to a working server in under 50 lines of code.

This tutorial walks you through building MCP servers in Python from scratch. You will create tools, resources, and prompts, handle errors properly, test with the MCP Inspector, connect to Claude Code, and build a practical SQLite database server. Every code example is complete and runnable.

## What Is MCP and Why Build Custom Servers

**MCP (Model Context Protocol)** is the open standard that lets AI models connect to external tools, databases, and services. Think of it as USB-C for AI — one universal protocol that works across Claude Code, Cursor, VS Code Copilot, and any MCP-compatible client.

An MCP server exposes three types of capabilities:

| Capability | What It Does | Example |
|-----------|-------------|---------|
| **Tools** | Let AI perform actions | Query a database, call an API |
| **Resources** | Let AI read data | Config files, logs, system info |
| **Prompts** | Reusable interaction templates | Code review template, analysis template |

For a deep dive into MCP architecture, see [MCP Protocol Explained: The Universal Standard for AI Tools](/posts/ai/2026-02-28-mcp-protocol-explained/). If you have already built servers in TypeScript, see [Building MCP Servers with TypeScript](/posts/ai/2026-03-02-building-mcp-servers-typescript/) for a comparison.

This tutorial focuses on **Python** — ideal for data science workflows, ML pipelines, and scripting tasks where Python is already your primary language.

## Prerequisites

| Dependency | Minimum Version | Check Command |
|-----------|----------------|---------------|
| Python | >= 3.10 | `python3 --version` |
| uv (recommended) | Latest | `uv --version` |
| pip (alternative) | >= 22.0 | `pip --version` |
| Claude Code | Latest | `claude --version` |

### Install uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that handles virtual environments automatically. The MCP documentation uses it as the default tool.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Verify installation
uv --version
```

If you prefer pip, every `uv` command in this tutorial has a pip equivalent shown alongside it.

## Project Setup

### Step 1: Initialize the Project

```bash
# Create project with uv
uv init weather-mcp-server
cd weather-mcp-server

# Add the MCP SDK with CLI tools
uv add "mcp[cli]"
```

With pip instead:

```bash
mkdir weather-mcp-server
cd weather-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]"
```

### Step 2: Configure pyproject.toml

Edit the `pyproject.toml` that `uv init` created:

```toml
[project]
name = "weather-mcp-server"
version = "1.0.0"
description = "MCP server providing weather data to AI assistants"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
weather-mcp-server = "weather_mcp_server.server:main"
```

The `[project.scripts]` entry point is important — it lets users run your server as a command after installing the package.

### Step 3: Create the Project Structure

```bash
mkdir -p src/weather_mcp_server
touch src/weather_mcp_server/__init__.py
touch src/weather_mcp_server/server.py
```

Your project layout:

```
weather-mcp-server/
├── pyproject.toml
├── src/
│   └── weather_mcp_server/
│       ├── __init__.py
│       └── server.py       # Main server code
└── README.md
```

## Building Your First Server: A Weather Tool

Open `src/weather_mcp_server/server.py` and write the server:

```python
"""Weather MCP Server — provides weather data to AI assistants."""

from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("weather-server")

# Simulated weather data (replace with a real API in production)
WEATHER_DATA = {
    "New York": {"temp_c": 2, "condition": "Cloudy", "humidity": 65, "wind_kmh": 20},
    "San Francisco": {"temp_c": 14, "condition": "Sunny", "humidity": 70, "wind_kmh": 15},
    "London": {"temp_c": 8, "condition": "Rainy", "humidity": 85, "wind_kmh": 25},
    "Tokyo": {"temp_c": 10, "condition": "Clear", "humidity": 55, "wind_kmh": 10},
    "Sydney": {"temp_c": 25, "condition": "Sunny", "humidity": 60, "wind_kmh": 18},
    "Berlin": {"temp_c": 5, "condition": "Overcast", "humidity": 75, "wind_kmh": 22},
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: City name, e.g. "New York", "London", "Tokyo"

    Returns:
        Weather report including temperature, condition, humidity, and wind speed.
    """
    data = WEATHER_DATA.get(city)
    if not data:
        return f"No weather data available for '{city}'. Available cities: {', '.join(WEATHER_DATA.keys())}"

    return (
        f"Weather in {city}:\n"
        f"  Temperature: {data['temp_c']}°C\n"
        f"  Condition: {data['condition']}\n"
        f"  Humidity: {data['humidity']}%\n"
        f"  Wind: {data['wind_kmh']} km/h"
    )


@mcp.tool()
def compare_weather(city1: str, city2: str) -> str:
    """Compare weather between two cities.

    Args:
        city1: First city name
        city2: Second city name

    Returns:
        Side-by-side weather comparison with temperature difference.
    """
    data1 = WEATHER_DATA.get(city1)
    data2 = WEATHER_DATA.get(city2)

    if not data1:
        return f"No data for '{city1}'. Available: {', '.join(WEATHER_DATA.keys())}"
    if not data2:
        return f"No data for '{city2}'. Available: {', '.join(WEATHER_DATA.keys())}"

    diff = data1["temp_c"] - data2["temp_c"]
    warmer = city1 if diff > 0 else city2

    return (
        f"Weather Comparison: {city1} vs {city2}\n"
        f"{'─' * 40}\n"
        f"{city1}: {data1['condition']}, {data1['temp_c']}°C, "
        f"humidity {data1['humidity']}%, wind {data1['wind_kmh']} km/h\n"
        f"{city2}: {data2['condition']}, {data2['temp_c']}°C, "
        f"humidity {data2['humidity']}%, wind {data2['wind_kmh']} km/h\n"
        f"{'─' * 40}\n"
        f"Temperature difference: {abs(diff)}°C ({warmer} is warmer)"
    )


def main():
    """Entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main()
```

Key concepts in this code:

- **`FastMCP("weather-server")`** creates the server instance. The name identifies your server to MCP clients.
- **`@mcp.tool()`** registers a function as an MCP tool. The function's docstring becomes the tool description that AI clients use to decide when to call it.
- **Type hints matter.** The SDK reads `city: str` to generate the input schema. AI clients use this schema to construct correct tool calls.
- **`mcp.run()`** starts the server with STDIO transport by default — the standard for local MCP servers.

That is all it takes. No boilerplate JSON-RPC handling, no manual schema definitions. FastMCP derives everything from your function signatures and docstrings.

## Adding Resources

Resources let AI clients read data from your server. Unlike tools (which perform actions), resources are for exposing information.

Add these to your `server.py`:

```python
@mcp.resource("weather://cities")
def list_cities() -> str:
    """List all cities with available weather data.

    Returns a JSON array of supported city names.
    """
    import json
    return json.dumps(list(WEATHER_DATA.keys()), indent=2)


@mcp.resource("weather://city/{city_name}")
def get_city_details(city_name: str) -> str:
    """Get detailed weather data for a specific city as JSON.

    This resource template accepts any city name in the URL.
    """
    import json
    data = WEATHER_DATA.get(city_name)
    if not data:
        return json.dumps({"error": f"City '{city_name}' not found"})
    return json.dumps({"city": city_name, **data}, indent=2)
```

The second resource uses a **resource template** — the `{city_name}` in the URI is a dynamic parameter. When a client requests `weather://city/Tokyo`, FastMCP passes `"Tokyo"` as `city_name`.

Resources vs tools:

| Aspect | Resources | Tools |
|--------|-----------|-------|
| Purpose | Read data | Perform actions |
| Analogy | GET request | POST request |
| Side effects | None | May have side effects |
| Discovery | Client browses available resources | Client sees tool list with schemas |

## Adding Prompts

Prompts are reusable interaction templates. They help users (and AI clients) invoke your server's capabilities in a structured way.

```python
@mcp.prompt()
def travel_advisory(destination: str) -> str:
    """Get a travel advisory based on current weather at the destination.

    Args:
        destination: The city you plan to travel to
    """
    data = WEATHER_DATA.get(destination)
    if not data:
        return f"Check weather conditions for {destination} and suggest appropriate clothing and travel tips."

    return (
        f"The current weather in {destination} is {data['condition']} "
        f"at {data['temp_c']}°C with {data['humidity']}% humidity "
        f"and winds of {data['wind_kmh']} km/h.\n\n"
        f"Based on these conditions, please suggest:\n"
        f"1. Appropriate clothing to pack\n"
        f"2. Weather-related travel tips\n"
        f"3. Best time of day for outdoor activities"
    )


@mcp.prompt()
def weather_report(cities: str = "all") -> str:
    """Generate a comprehensive weather report.

    Args:
        cities: Comma-separated city names, or "all" for every city
    """
    if cities == "all":
        city_list = list(WEATHER_DATA.keys())
    else:
        city_list = [c.strip() for c in cities.split(",")]

    city_str = ", ".join(city_list)
    return (
        f"Generate a professional weather report for the following cities: {city_str}.\n\n"
        f"Include:\n"
        f"- Current conditions summary\n"
        f"- Temperature trends\n"
        f"- Travel recommendations\n"
        f"- Any weather warnings"
    )
```

Prompts are user-invoked — they appear in the client's prompt library and can be selected manually. They are not called automatically by the AI like tools are.

## Error Handling and Logging Best Practices

Production MCP servers need proper error handling. Here are the patterns that work.

### Return Errors, Do Not Raise Them

MCP tools should return error messages as strings rather than raising exceptions. This gives the AI model context to understand what went wrong.

```python
import httpx

@mcp.tool()
async def fetch_weather_api(city: str) -> str:
    """Fetch real weather data from an external API.

    Args:
        city: City name to look up
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.weatherapi.com/v1/current.json",
                params={"key": "YOUR_API_KEY", "q": city},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()

            current = data["current"]
            return (
                f"Weather in {city}:\n"
                f"  Temperature: {current['temp_c']}°C\n"
                f"  Condition: {current['condition']['text']}\n"
                f"  Humidity: {current['humidity']}%\n"
                f"  Wind: {current['wind_kph']} km/h"
            )

    except httpx.TimeoutException:
        return f"Error: Request timed out while fetching weather for '{city}'. Try again later."
    except httpx.HTTPStatusError as e:
        return f"Error: API returned status {e.response.status_code} for '{city}'."
    except Exception as e:
        return f"Error: Failed to fetch weather for '{city}': {str(e)}"
```

### Use the Context Object for Logging

FastMCP provides a `Context` object for structured logging and progress reporting:

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def analyze_weather_trends(city: str, ctx: Context) -> str:
    """Analyze weather trends for a city with progress reporting.

    Args:
        city: City name to analyze
    """
    # Log messages (sent to the MCP client)
    await ctx.info(f"Starting weather analysis for {city}")

    # Report progress (useful for long-running operations)
    await ctx.report_progress(0, 3)

    await ctx.debug("Fetching current data...")
    data = WEATHER_DATA.get(city)
    if not data:
        await ctx.warning(f"No data found for {city}")
        return f"No data available for '{city}'"

    await ctx.report_progress(1, 3)

    await ctx.debug("Computing analysis...")
    # Simulate analysis work
    analysis = f"Weather analysis for {city}: {data['condition']} conditions, {data['temp_c']}°C"

    await ctx.report_progress(2, 3)

    await ctx.info(f"Analysis complete for {city}")
    await ctx.report_progress(3, 3)

    return analysis
```

The Context object provides these logging methods:

| Method | Use For |
|--------|---------|
| `ctx.debug()` | Detailed debug information |
| `ctx.info()` | General information |
| `ctx.warning()` | Warning messages |
| `ctx.error()` | Error messages |
| `ctx.report_progress(current, total)` | Progress updates for long tasks |

### Use stderr for Print Debugging

Just like in TypeScript MCP servers, **never use `print()` for debugging**. MCP uses STDIO for communication — anything on stdout is interpreted as protocol messages.

```python
import sys

# WRONG — breaks STDIO protocol
print("Debug: processing request")

# CORRECT — uses stderr, does not interfere
print("Debug: processing request", file=sys.stderr)
```

In practice, prefer the Context logging methods over print statements. They send structured log messages through the MCP protocol to the client.

## Testing Your Server Locally

### Using the MCP Inspector

The MCP SDK includes a built-in testing tool called the **MCP Inspector**. It launches a web interface where you can interactively test every tool, resource, and prompt.

```bash
# Start the Inspector
mcp dev src/weather_mcp_server/server.py

# Or with uv (if not in the activated venv)
uv run mcp dev src/weather_mcp_server/server.py
```

This opens a web interface at `http://127.0.0.1:6274`. From there you can:

1. **Click Connect** to establish a connection to your server
2. **Browse the Tools tab** — see all registered tools and their schemas
3. **Test a tool** — fill in parameters and click Execute
4. **Browse Resources** — list and read all registered resources
5. **Test Prompts** — select a prompt and provide arguments

The Inspector is your primary debugging tool during development. Use it to verify:

- Tool parameters are correctly defined
- Return values are formatted properly
- Error handling works as expected

### Running the Server Directly

For quick tests without the Inspector:

```bash
# Run with stdio transport (default)
mcp run src/weather_mcp_server/server.py
```

## Connecting to Claude Code

Once your server works in the Inspector, connect it to Claude Code.

### Register the Server

```bash
# Using uv (recommended — handles virtual env automatically)
claude mcp add weather-server -- uv run --directory /absolute/path/to/weather-mcp-server mcp run src/weather_mcp_server/server.py

# Or if using a script entry point defined in pyproject.toml
claude mcp add weather-server -- uv run --directory /absolute/path/to/weather-mcp-server weather-mcp-server
```

If you installed with pip into a virtual env:

```bash
claude mcp add weather-server /absolute/path/to/weather-mcp-server/.venv/bin/python -m weather_mcp_server.server
```

### Verify and Test

```bash
# Check that the server is registered
claude mcp list
```

Now open Claude Code and test:

```
> What's the weather in Tokyo?

> Compare the weather in New York and London

> List all available cities in the weather server
```

Claude Code automatically discovers your tools and calls them. For more details on MCP configuration in Claude Code, see [Claude Code MCP Setup: Connect AI to Any External Service](/posts/ai/2026-02-28-claude-code-mcp-setup/).

### Restart After Changes

When you modify your server code, restart it:

```bash
claude mcp remove weather-server
claude mcp add weather-server -- uv run --directory /absolute/path/to/weather-mcp-server mcp run src/weather_mcp_server/server.py
```

## Practical Example: A SQLite Database Server

Let's build something you would actually use in production — an MCP server that lets AI assistants query a SQLite database. This is one of the most common use cases for custom MCP servers.

Create a new file `src/weather_mcp_server/db_server.py`:

```python
"""SQLite MCP Server — gives AI assistants read access to a SQLite database."""

import sqlite3
import json
from pathlib import Path
from contextlib import closing

from mcp.server.fastmcp import FastMCP, Context

# Create the server
mcp = FastMCP("sqlite-server")

# Database path — configure this for your project
DB_PATH = Path("./data/example.db")


def get_connection() -> sqlite3.Connection:
    """Create a database connection with safety settings."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent read performance
    return conn


def init_sample_db():
    """Create a sample database for demonstration."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            owner_id INTEGER REFERENCES users(id),
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            project_id INTEGER REFERENCES projects(id),
            assignee_id INTEGER REFERENCES users(id),
            status TEXT DEFAULT 'todo',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Insert sample data if tables are empty
        INSERT OR IGNORE INTO users (id, name, email, role) VALUES
            (1, 'Alice Chen', 'alice@example.com', 'admin'),
            (2, 'Bob Smith', 'bob@example.com', 'developer'),
            (3, 'Carol Wu', 'carol@example.com', 'developer'),
            (4, 'Dave Brown', 'dave@example.com', 'designer');

        INSERT OR IGNORE INTO projects (id, name, description, owner_id, status) VALUES
            (1, 'MCP Server', 'Build custom MCP servers', 1, 'active'),
            (2, 'Web Dashboard', 'Admin dashboard redesign', 4, 'active'),
            (3, 'API Migration', 'Migrate REST to GraphQL', 2, 'completed');

        INSERT OR IGNORE INTO tasks (id, title, project_id, assignee_id, status, priority) VALUES
            (1, 'Set up project structure', 1, 1, 'done', 'high'),
            (2, 'Implement weather tool', 1, 2, 'in_progress', 'high'),
            (3, 'Write unit tests', 1, 3, 'todo', 'medium'),
            (4, 'Design dashboard layout', 2, 4, 'in_progress', 'high'),
            (5, 'Implement auth flow', 2, 2, 'todo', 'high'),
            (6, 'Write API docs', 3, 3, 'done', 'low'),
            (7, 'Performance optimization', 1, 2, 'todo', 'medium');
    """)

    conn.commit()
    conn.close()


@mcp.tool()
def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the database.

    Only SELECT statements are allowed. The query runs in a read-only
    transaction to prevent any data modifications.

    Args:
        sql: A SELECT SQL query to execute

    Returns:
        Query results as a formatted JSON string, or an error message.
    """
    # Security: only allow SELECT statements
    normalized = sql.strip().upper()
    if not normalized.startswith("SELECT"):
        return "Error: Only SELECT queries are allowed. This server provides read-only access."

    # Block dangerous keywords even in subqueries
    dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "EXEC"]
    for keyword in dangerous_keywords:
        if keyword in normalized:
            return f"Error: '{keyword}' statements are not allowed."

    try:
        with closing(get_connection()) as conn:
            cursor = conn.execute(sql)
            columns = [description[0] for description in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return json.dumps({
                "columns": columns,
                "row_count": len(rows),
                "rows": rows,
            }, indent=2, default=str)

    except sqlite3.OperationalError as e:
        return f"SQL Error: {str(e)}"
    except Exception as e:
        return f"Error executing query: {str(e)}"


@mcp.tool()
def list_tables() -> str:
    """List all tables in the database with their column definitions.

    Returns:
        A formatted description of every table and its columns.
    """
    try:
        with closing(get_connection()) as conn:
            # Get all table names
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]

            result = []
            for table in tables:
                # Get column info for each table
                cursor = conn.execute(f"PRAGMA table_info({table})")
                columns = []
                for col in cursor.fetchall():
                    col_name = col[1]
                    col_type = col[2]
                    not_null = "NOT NULL" if col[3] else ""
                    pk = "PRIMARY KEY" if col[5] else ""
                    columns.append(f"    {col_name} {col_type} {pk} {not_null}".strip())

                # Get row count
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]

                result.append(
                    f"Table: {table} ({row_count} rows)\n" +
                    "\n".join(columns)
                )

            return "\n\n".join(result)

    except Exception as e:
        return f"Error listing tables: {str(e)}"


@mcp.tool()
async def describe_table(table_name: str, ctx: Context) -> str:
    """Get detailed schema and sample data for a specific table.

    Args:
        table_name: Name of the table to describe

    Returns:
        Table schema, sample rows, and basic statistics.
    """
    await ctx.info(f"Describing table: {table_name}")

    try:
        with closing(get_connection()) as conn:
            # Verify table exists
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if not cursor.fetchone():
                return f"Error: Table '{table_name}' does not exist."

            # Get schema
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            schema_lines = [f"Schema for '{table_name}':"]
            for col in columns:
                schema_lines.append(
                    f"  {col[1]} ({col[2]})"
                    + (" PRIMARY KEY" if col[5] else "")
                    + (" NOT NULL" if col[3] else "")
                    + (f" DEFAULT {col[4]}" if col[4] else "")
                )

            # Get row count
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            # Get sample rows (first 5)
            cursor = conn.execute(f"SELECT * FROM {table_name} LIMIT 5")
            col_names = [desc[0] for desc in cursor.description]
            sample_rows = [dict(zip(col_names, row)) for row in cursor.fetchall()]

            result = "\n".join(schema_lines)
            result += f"\n\nTotal rows: {count}"
            result += f"\n\nSample data (first 5 rows):\n{json.dumps(sample_rows, indent=2, default=str)}"

            return result

    except Exception as e:
        return f"Error describing table: {str(e)}"


@mcp.resource("db://schema")
def get_full_schema() -> str:
    """Get the complete database schema as a resource.

    This is useful for AI assistants that need to understand the
    database structure before writing queries.
    """
    try:
        with closing(get_connection()) as conn:
            cursor = conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
            )
            statements = [row[0] for row in cursor.fetchall()]
            return "\n\n".join(statements)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.prompt()
def data_analysis(question: str) -> str:
    """Generate a data analysis prompt based on the database schema.

    Args:
        question: The data question you want to answer
    """
    schema = get_full_schema()
    return (
        f"You have access to a SQLite database with the following schema:\n\n"
        f"{schema}\n\n"
        f"The user wants to know: {question}\n\n"
        f"Write and execute the appropriate SQL query using the query_database tool. "
        f"Then explain the results clearly."
    )


def main():
    """Initialize the sample database and start the server."""
    init_sample_db()
    mcp.run()


if __name__ == "__main__":
    main()
```

### Test the Database Server

```bash
# Test with the MCP Inspector
mcp dev src/weather_mcp_server/db_server.py
```

Connect to Claude Code:

```bash
claude mcp add sqlite-server -- uv run --directory /absolute/path/to/weather-mcp-server python src/weather_mcp_server/db_server.py
```

Now you can ask Claude Code natural language questions about your data:

```
> What tables are in the database?

> Show me all active projects with their owners

> How many tasks does each developer have? Group by status

> Find all high-priority tasks that are not done yet
```

The AI writes SQL queries, calls your `query_database` tool, and presents the results — all automatically.

This pattern works with any SQLite database. Point `DB_PATH` at your project's database file, and Claude Code instantly gains the ability to query it. For security best practices when exposing databases through MCP, see [MCP Security Guide](/posts/ai/2026-02-23-mcp-security-guide/).

## Deployment Options

### Local STDIO (Default)

The standard transport for local development. The server runs as a subprocess and communicates via stdin/stdout.

```python
# This is the default when you call mcp.run()
mcp.run()

# Explicitly specifying stdio transport
mcp.run(transport="stdio")
```

This is what Claude Code and most local clients use. No network configuration needed.

### SSE for Remote Access

Server-Sent Events transport enables remote connections over HTTP:

```python
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

Connect from Claude Code over the network:

```bash
claude mcp add remote-weather --url http://your-server:8000/sse
```

### Streamable HTTP (Newest)

The latest transport option — bidirectional HTTP with streaming:

```python
mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

Streamable HTTP is the recommended transport for production remote deployments. It supports bidirectional communication and works through standard HTTP proxies and load balancers.

### Docker Deployment

For production servers, Docker provides isolation and reproducibility:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv for fast dependency resolution
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/

# Install dependencies
RUN uv pip install --system -e .

# Run with streamable-http transport for remote access
EXPOSE 8000
CMD ["python", "-m", "weather_mcp_server.server"]
```

Modify your server to use the appropriate transport in production:

```python
import os

def main():
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "stdio":
        mcp.run()
    else:
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("MCP_PORT", "8000")),
        )
```

## Publishing to the MCP Ecosystem

When your server is ready for others to use, publish it.

### Publish to PyPI

```bash
# Build the package
uv build

# Publish to PyPI
uv publish
```

After publishing, anyone can use your server:

```bash
# Users install and run with uvx (uv's tool runner)
claude mcp add weather-server -- uvx weather-mcp-server

# Or with pip
pip install weather-mcp-server
claude mcp add weather-server weather-mcp-server
```

### Share with the Community

Submit your server to the [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) repository and the [MCP official server registry](https://modelcontextprotocol.io/examples). Check out [Best MCP Servers for Claude Code](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) to see what a well-documented MCP server listing looks like.

## Common Errors and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Server does not start | Python < 3.10 | Upgrade to Python 3.10+ |
| `ModuleNotFoundError: mcp` | SDK not installed in the right env | Run `uv add "mcp[cli]"` or activate venv |
| Tools not discovered | Missing type hints on function parameters | Add type hints: `def my_tool(name: str)` |
| `print()` breaks protocol | stdout used for debugging | Use `print(..., file=sys.stderr)` or `ctx.info()` |
| Server crashes silently | Unhandled exception in tool | Wrap with try/except and return error string |
| Resource not found | Wrong URI scheme | Check URI matches exactly, e.g. `weather://cities` |
| Connection refused | Server not running or wrong path | Verify with `claude mcp list` and check path |
| Stale tools after code change | Server needs restart | `claude mcp remove` then `claude mcp add` again |

## FAQ

### What Python version do I need to build MCP servers?

You need Python 3.10 or higher. The MCP Python SDK officially supports Python 3.10, 3.11, 3.12, and 3.13. The SDK uses modern Python features like type hints and match statements that require 3.10+.

### What is FastMCP and how does it relate to the MCP Python SDK?

FastMCP is the high-level framework included in the official MCP Python SDK (the `mcp` package on PyPI). It provides a decorator-based API for building MCP servers — you use `@mcp.tool()`, `@mcp.resource()`, and `@mcp.prompt()` to register capabilities. It is the recommended way to build Python MCP servers.

### Can I use pip instead of uv to install the MCP Python SDK?

Yes. Install with `pip install "mcp[cli]"` for the full package including CLI tools, or `pip install mcp` for just the library. However, uv is recommended because it is significantly faster, handles virtual environments automatically, and is the tool used in the official MCP documentation.

### How do I test my Python MCP server before connecting it to Claude Code?

Run `mcp dev server.py` to launch the MCP Inspector, a web-based testing interface at `http://127.0.0.1:6274`. You can test each tool, resource, and prompt interactively. Once satisfied, connect to Claude Code with `claude mcp add`.

### What is the difference between building MCP servers in Python vs TypeScript?

Both languages have official SDKs. Python uses decorator-based registration (`@mcp.tool()`) while TypeScript uses method calls (`server.registerTool()`). Python is better for data science, ML pipelines, and scripting tasks. TypeScript has a slightly more mature SDK. The protocol is identical — servers built in either language work with any MCP client.

## Summary

Building MCP servers in Python follows a clean workflow:

1. **Set up** — `uv init` + `uv add "mcp[cli]"` + create `pyproject.toml`
2. **Build tools** — Use `@mcp.tool()` with typed parameters and docstrings
3. **Add resources** — Use `@mcp.resource()` for read-only data access
4. **Add prompts** — Use `@mcp.prompt()` for reusable templates
5. **Test** — `mcp dev server.py` launches the MCP Inspector
6. **Connect** — `claude mcp add` registers your server with Claude Code
7. **Deploy** — STDIO for local, streamable-http for remote, Docker for production
8. **Publish** — `uv build` + `uv publish` to PyPI

The MCP ecosystem is growing fast — the Python SDK alone is downloaded millions of times per month. Every server you build works instantly with Claude Code, Cursor, VS Code Copilot, and any future MCP-compatible tool. Start building today.

## Related Articles

- [MCP Protocol Explained: The Universal Standard for AI Tools](/posts/ai/2026-02-28-mcp-protocol-explained/) — Deep dive into MCP architecture and concepts
- [Building MCP Servers with TypeScript: Zero to Deploy Tutorial](/posts/ai/2026-03-02-building-mcp-servers-typescript/) — The TypeScript version of this tutorial
- [Claude Code MCP Setup: Connect AI to Any External Service](/posts/ai/2026-02-28-claude-code-mcp-setup/) — Complete guide to MCP configuration in Claude Code
- [Best MCP Servers for Claude Code: 18 Tools You Need in 2026](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — Curated list of the best community MCP servers

## Related Reading

- [MCP Protocol Explained: The Universal Standard for AI Integration](/posts/ai/2026-02-20-mcp-protocol-guide/) — Deep dive into MCP protocol architecture and design
- [MCP Security Guide: Attack Patterns, Real CVEs, and Defense Strategies](/posts/ai/2026-02-23-mcp-security-guide/) — Security considerations for your MCP servers
- [Build an MCP Server with Claude Code: TypeScript Tutorial](/posts/ai/2026-02-22-claude-code-mcp-server-tutorial/) — Alternative approach using Claude Code as the development tool
- [Chrome DevTools MCP Setup 2026](/posts/ai/2026-03-17-chrome-devtools-mcp-guide/) — Real-world MCP server connecting to browser DevTools
