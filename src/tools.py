"""
Tools for the code review agent.

Provides one tool:
- read_code_file: Reads source code files from disk
"""

from smolagents import tool


@tool
def read_code_file(file_path: str) -> str:
    """
    Reads a source code file from the filesystem.

    Args:
        file_path: Path to the code file to read

    Returns:
        Contents of the file as a string
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
