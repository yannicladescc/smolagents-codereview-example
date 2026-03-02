"""
Code Review Agent using smolagents and Groq API.

A minimal AI code review agent that analyzes source code files
for security issues, style problems, and potential bugs.
Works with any programming language.
"""

import argparse
import os
import time
from pathlib import Path

import yaml
from smolagents import CodeAgent, LiteLLMModel

from tools import read_code_file, lint_code_file

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".go", ".rs", ".rb",
    ".cpp", ".c", ".cs", ".swift", ".kt",
}


def load_prompts():
    """
    Load prompts from the prompts.yaml file.

    Returns:
        Dictionary containing all prompts
    """
    prompt_file = Path(__file__).resolve().parent / "prompts.yaml"
    with open(prompt_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("prompts", {})


def get_code_review_prompt(file_path):
    """
    Get the code review prompt template, formatted with the given file path.

    Args:
        file_path: Path to the code file being reviewed

    Returns:
        Formatted prompt string
    """
    prompts = load_prompts()
    template = prompts["code_review"]["template"]
    return template.format(file_path=file_path)


def create_agent(model_name=None, temperature=None, max_tokens=None, verbose=True):
    """
    Creates and configures the code review agent.

    Args:
        model_name: Groq model identifier (env: GROQ_MODEL_NAME)
        temperature: LLM temperature 0.0-1.0 (env: GROQ_TEMPERATURE)
        max_tokens: Max output tokens (env: GROQ_MAX_TOKENS)
        verbose: Show detailed agent logs

    Returns:
        Configured CodeAgent instance
    """
    if model_name is None:
        model_name = os.getenv("GROQ_MODEL_NAME", "groq/meta-llama/llama-4-scout-17b-16e-instruct")
    if temperature is None:
        temperature = float(os.getenv("GROQ_TEMPERATURE", "0.2"))
    if max_tokens is None:
        max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "2000"))

    model = LiteLLMModel(
        model_id=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=60,
        requests_per_minute=25,  # Stay under Groq's 30 RPM free tier limit
    )

    return CodeAgent(
        tools=[read_code_file, lint_code_file],
        model=model,
        max_steps=4,
        verbosity_level=2 if verbose else 0,
        add_base_tools=False,
    )


def _format_result(result, file_path):
    """Convert agent result to readable markdown, handling dict/list outputs."""
    if isinstance(result, str):
        return result

    # Agent returned a dict/list instead of text — convert to markdown
    lines = [f"# Code Review: {file_path}\n"]
    if isinstance(result, dict):
        for category, findings in result.items():
            lines.append(f"## {category.replace('_', ' ').title()}\n")
            if isinstance(findings, list):
                for item in findings:
                    lines.append(f"- {item}")
            else:
                lines.append(f"- {findings}")
            lines.append("")
    else:
        lines.append(str(result))
    return "\n".join(lines)


def review_code_file(file_path, save_report=True, output_dir="reports"):
    """
    Reviews a single code file using the AI agent.

    The agent reads the file via read_code_file tool, then analyzes it
    for security, style, and bug issues in a single pass.

    Args:
        file_path: Path to the code file to review
        save_report: Whether to save the report to disk
        output_dir: Directory for saved reports

    Returns:
        Review result as a string
    """
    print(f"\n{'='*60}")
    print(f"Reviewing: {file_path}")
    print(f"{'='*60}\n")

    agent = create_agent()

    task = get_code_review_prompt(file_path)

    try:
        result = agent.run(task)
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except TimeoutError:
        return "Error: LLM request timed out. Check your internet or reduce GROQ_MAX_TOKENS."
    except Exception as e:
        print(f"\nError during review: {e}")
        return f"Error: {e}"

    report = _format_result(result, file_path)

    if save_report:
        Path(output_dir).mkdir(exist_ok=True)
        report_path = Path(output_dir) / f"{Path(file_path).stem}_review.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport saved to: {report_path}")

    return report


def review_directory(directory, save_reports=True, output_dir="reports"):
    """
    Reviews all code files in a directory.

    Processes files sequentially with delays between reviews
    to respect Groq free tier rate limits.

    Args:
        directory: Path to directory to scan
        save_reports: Whether to save reports to disk
        output_dir: Directory for saved reports

    Returns:
        List of (file_path, result) tuples
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"Error: {directory} is not a directory")
        return []

    files = sorted(
        f for f in dir_path.rglob("*")
        if f.suffix in SUPPORTED_EXTENSIONS and f.is_file()
    )

    if not files:
        print(f"No code files found in {directory}")
        return []

    print(f"Found {len(files)} code files to review\n")
    results = []

    for i, file_path in enumerate(files):
        print(f"[{i + 1}/{len(files)}] {file_path}")
        try:
            result = review_code_file(str(file_path), save_report=save_reports, output_dir=output_dir)
            results.append((str(file_path), result))
        except Exception as e:
            print(f"Error reviewing {file_path}: {e}")
            results.append((str(file_path), f"Error: {e}"))

        if i < len(files) - 1:
            print("\nWaiting 10s before next file (rate limit protection)...\n")
            time.sleep(10)

    return results


if __name__ == "__main__":
    # Ensure we run from the project root (parent of src/)
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument(
        "path", nargs="?", default="examples/bad_code.py",
        help="File or directory to review (default: examples/bad_code.py)",
    )
    parser.add_argument("--no-save", action="store_true", help="Don't save reports to disk")
    parser.add_argument("--output-dir", default="reports", help="Directory for saved reports")
    args = parser.parse_args()

    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable not set!")
        print("Get your free API key at: https://console.groq.com/keys")
        exit(1)

    target = Path(args.path)
    if target.is_dir():
        results = review_directory(str(target), save_reports=not args.no_save, output_dir=args.output_dir)
        print(f"\nReviewed {len(results)} files")
    elif target.is_file():
        result = review_code_file(str(target), save_report=not args.no_save, output_dir=args.output_dir)
        print(f"\n{'='*60}")
        print(result)
    else:
        print(f"Error: {args.path} not found")
        exit(1)
