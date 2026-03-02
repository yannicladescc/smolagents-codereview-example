# Building a Code Review Agent from Scratch

Step-by-step guide to building your own code review agent. Designed for a 1-hour workshop.

## Prerequisites

- Python 3.9+
- Free [Groq API key](https://console.groq.com/keys)

## Step 1: Project Setup (10 min)

```bash
mkdir code-review-agent && cd code-review-agent
uv venv && source .venv/bin/activate

cat > requirements.txt << EOF
smolagents[litellm]>=1.24.0
groq>=0.15.0
python-dotenv>=1.0.0
EOF
uv pip install -r requirements.txt

export GROQ_API_KEY="your-key-here"
```

## Step 2: Create Tools (15 min)

Create `src/tools.py`:

```python
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
        return f"Error reading file: {e}"
```

**Key points:**

- `@tool` makes functions callable by the agent
- Type hints generate the tool schema
- Docstrings tell the LLM when/how to use the tool
- `print()` helps the LLM track execution
- Tools should do things the LLM can't do on its own (file I/O, API calls, etc.)

## Step 3: Create the Agent (15 min)

Create `src/code_review_agent.py`:

```python
import os
from pathlib import Path
from smolagents import CodeAgent, LiteLLMModel
from tools import read_code_file


def create_agent(verbose=True):
    """Create the code review agent with Groq."""
    model = LiteLLMModel(
        model_id=os.getenv("GROQ_MODEL_NAME", "groq/meta-llama/llama-4-scout-17b-16e-instruct"),
        temperature=float(os.getenv("GROQ_TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "1024")),
        timeout=60,
        requests_per_minute=25,  # Groq free tier: 30 RPM
    )

    return CodeAgent(
        tools=[read_code_file],
        model=model,
        max_steps=2,
        verbosity_level=2 if verbose else 0,
        add_base_tools=False,
    )


def review_code_file(file_path, save_report=True, output_dir="reports"):
    """Review a code file and return the result."""
    print(f"\n{'='*60}")
    print(f"Reviewing: {file_path}")
    print(f"{'='*60}\n")

    agent = create_agent()

    task = f"""Review the code file at '{file_path}'.

Steps:
1. Use read_code_file to load the file
2. Analyze the code for issues in these categories:

Security — Check for: dangerous functions (eval, exec), injection vulnerabilities, hardcoded secrets, missing input validation
Style — Check for: missing documentation, naming conventions, code duplication, complexity, missing type annotations
Bugs — Check for: missing error handling, resource leaks, edge cases (null, zero division, bounds), mutable default arguments

Your final answer must be a readable markdown report.
Use headings (## Security, ## Style, ## Bugs) and bullet points for each finding.
Include specific actionable recommendations for each issue found."""

    result = agent.run(task)

    if save_report:
        Path(output_dir).mkdir(exist_ok=True)
        report_path = Path(output_dir) / f"{Path(file_path).stem}_review.md"
        with open(report_path, "w") as f:
            f.write(str(result))
        print(f"\nReport saved to: {report_path}")

    return result


if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set!")
        exit(1)

    result = review_code_file("examples/bad_code.py")
    print(f"\n{'='*60}")
    print(result)
```

## Step 4: Test It (10 min)

Create `examples/bad_code.py` with some intentional issues:

```python
def unsafe(user_input):
    result = eval(user_input)  # Security issue!
    print(result)              # Style: use logging
    return result

def read_config(filename="config.txt"):
    f = open(filename)         # Bug: no context manager
    data = f.read()
    return data                # Bug: file not closed

def add_to_list(item, items=[]):  # Bug: mutable default
    items.append(item)
    return items
```

Run:

```bash
python src/code_review_agent.py
```

The agent will autonomously read the file, analyze it against all three checklists, and produce a summary.

## Step 5: Add Directory Support (10 min)

Add to `src/code_review_agent.py`:

```python
import time

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".go"}

def review_directory(directory, save_reports=True, output_dir="reports"):
    files = sorted(
        f for f in Path(directory).rglob("*")
        if f.suffix in SUPPORTED_EXTENSIONS and f.is_file()
    )
    results = []
    for i, f in enumerate(files):
        print(f"\n[{i+1}/{len(files)}] {f}")
        try:
            result = review_code_file(str(f), save_report=save_reports, output_dir=output_dir)
            results.append((str(f), result))
        except Exception as e:
            print(f"Error: {e}")
        if i < len(files) - 1:
            time.sleep(10)  # Rate limit protection
    return results
```

## Workshop Timeline

| Time  | Activity                            |
| ----- | ----------------------------------- |
| 0-10  | Setup (venv, dependencies, API key) |
| 10-25 | Build tool in `tools.py`            |
| 25-40 | Create agent + review function      |
| 40-50 | Test with example file              |
| 50-55 | Add directory support               |
| 55-60 | Q&A                                 |

## Bonus: Add Linting (Advanced)

For Python files, integrate [ruff](https://docs.astral.sh/ruff/) to detect concrete style violations automatically:

```python
# Add to tools.py
import subprocess

@tool
def lint_code_file(file_path: str) -> str:
    """Run ruff linter on Python files."""
    if file_path.endswith(".py"):
        result = subprocess.run(["ruff", "check", file_path], capture_output=True, text=True)
        return f"Ruff output:\n{result.stdout}" if result.stdout else "No issues found"
    return f"Linting not available for {Path(file_path).suffix}"

# Update create_agent() to include the tool
return CodeAgent(
    tools=[read_code_file, lint_code_file],  # Add lint_code_file
    model=model,
    max_steps=4,  # Increase for linting step
    ...
)

# Update the task prompt to mention linting
task = f"""Review the code file at '{file_path}'.
Steps:
1. Use read_code_file to load the file
2. If Python file: Use lint_code_file to run ruff
3. Analyze for security, style (integrate ruff findings), and bugs
...
"""
```

Install ruff: `pip install ruff`

Now the agent will automatically run linting for Python files and integrate findings into the report.

## What You've Learned

- Creating tools with `@tool` decorator
- Configuring a `CodeAgent` with an LLM
- Rate limit handling for free APIs
- Autonomous agent task execution

## Resources

- [smolagents docs](https://smolagents.org/docs)
- [Groq docs](https://console.groq.com/docs)
- [Tool best practices](https://smolagents.org/docs/tools)
