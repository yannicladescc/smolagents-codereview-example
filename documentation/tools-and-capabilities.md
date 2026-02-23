# Tools

## How Tools Work

Tools are Python functions decorated with `@tool` from smolagents. The decorator automatically:
- Generates a schema from type hints
- Extracts descriptions from docstrings
- Makes the function callable by the agent

See [smolagents tool docs](https://smolagents.org/docs/tools) for details.

## Available Tools

### read_code_file

Reads a source code file from disk. This is the agent's only tool — it provides the I/O capability that the LLM can't do on its own.

```python
@tool
def read_code_file(file_path: str) -> str:
```

Returns file contents as a string, or an error message if the file can't be read.

The review checklists (what to check for in security, style, bugs) are embedded directly in the task prompt since they're static data — no tool needed.

## Adding Custom Tools

```python
from smolagents import tool

@tool
def check_complexity(code: str) -> str:
    """
    Checks code for complexity issues.

    Args:
        code: Source code to analyze

    Returns:
        Complexity analysis guidance
    """
    print("[Complexity] Analyzing...")
    return f"Check this code for complexity:\n- Deep nesting\n- Long functions\n- High cyclomatic complexity\n\nCode:\n{code}"

# Add to agent
agent = CodeAgent(tools=[read_code_file, check_complexity], model=model)
```

## Tool Best Practices

1. **Use print() for logging** — helps the LLM track execution
2. **Detailed docstrings** — the LLM reads these to decide when to use the tool
3. **Type hints on all parameters** — generates the tool schema
4. **Return errors as strings, not exceptions** — keeps the agent running
5. **Only make tools for things the LLM can't do** — file I/O, API calls, database queries. Don't wrap static data in a tool.
