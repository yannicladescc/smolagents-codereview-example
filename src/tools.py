"""
Tools for the code review agent.

Provides two tools:
- read_code_file: Reads source code files from disk
- lint_code_file: Runs language-specific linters (ruff for Python, eslint for TS/JS)
"""

import subprocess
from pathlib import Path

from smolagents import tool


@tool
def read_code_file(file_path: str) -> str:
    """
    Reads a source code file from the filesystem (UTF-8 encoding).

    Args:
        file_path: Path to the code file. Must exist and be readable.

    Returns:
        File contents as string, or error message if file unavailable.
    """
    print(f"[File Reader] Reading: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"[File Reader] Read {len(content)} characters")
        return content
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {e}"
        print(f"[File Reader] {error_msg}")
        return error_msg


@tool
def lint_code_file(file_path: str) -> str:
    """
    Runs ruff linter on Python code files to detect concrete style violations.
    
    This tool uses ruff (a fast Python linter) to find issues like:
    - Undefined names and undefined imports
    - Bare except clauses
    - Style violations
    
    For Python files (.py): Returns ruff linting output with specific line numbers and error codes.
    For non-Python files: Returns a message that linting is unavailable for that language.
    
    Use this before or alongside semantic code analysis to get concrete, actionable findings.

    Args:
        file_path: Path to the code file to lint

    Returns:
        Ruff linting output or message indicating linting unavailable for language
    """
    file_ext = Path(file_path).suffix.lower()
    print(f"[Linter] Linting: {file_path}")

    # Python: use ruff
    if file_ext == ".py":
        try:
            result = subprocess.run(
                ["ruff", "check", file_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = result.stdout + result.stderr
            if output.strip():
                print(f"[Linter] Ruff found issues")
                return f"Ruff linting results:\n{output}"
            else:
                print(f"[Linter] No ruff issues found")
                return "Ruff: No linting issues found"
        except FileNotFoundError:
            return "Ruff not installed. Install with: pip install ruff"
        except subprocess.TimeoutExpired:
            return "Ruff linting timed out"
        except Exception as e:
            return f"Ruff error: {e}"

    # Other languages
    else:
        return f"Linting not available for {file_ext} files. Currently supported: Python (.py)"
