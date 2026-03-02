# Architecture

## System Overview

```
┌────────────────────────────────────────────────────┐
│                Code Review Agent                    │
├────────────────────────────────────────────────────┤
│  CLI Layer                                          │
│  ┌──────────────────────────────────────────────┐  │
│  │ argparse: file or directory path             │  │
│  │ review_code_file() • review_directory()      │  │
│  └──────────────────┬───────────────────────────┘  │
│                     ↓                               │
│  Agent Decision Loop (max 4 steps)                  │
│  ┌──────────────────────────────────────────────┐  │
│  │ LiteLLM → Groq API (Llama 4 Scout 17B)      │  │
│  │ CodeAgent (smolagents)                       │  │
│  │   • Max 4 LLM calls per file                 │  │
│  │   • Rate limiter (25 RPM)                    │  │
│  │   • Auto-retry on 429                        │  │
│  │   • Decides: Call tools OR generate output?  │  │
│  └──────────────────┬───────────────────────────┘  │
│                     ↓                               │
│  Tools (called as needed)                           │
│  ┌──────────────────────────────────────────────┐  │
│  │ read_code_file: loads files from disk        │  │
│  │ lint_code_file: runs ruff on Python files    │  │
│  └──────────────────┬───────────────────────────┘  │
│                     ↓                               │
│  Output: markdown report (saved as .md)             │
└────────────────────────────────────────────────────┘
```

## File Structure

```
src/
  code_review_agent.py   # Agent creation, review functions, CLI
  tools.py               # Tool definitions (read_code_file, lint_code_file)
  prompts.yaml           # Prompt templates (externalized for easy customization)
examples/              # Test code files
documentation/         # Guides
reports/               # Generated review reports
```

## Technology Stack

| Component            | Technology                                              | Why                                |
| -------------------- | ------------------------------------------------------- | ---------------------------------- |
| Agent framework      | [smolagents](https://github.com/huggingface/smolagents) | Simple, code-first, model-agnostic |
| LLM provider         | [Groq](https://groq.com)                                | Free tier, fast inference          |
| Provider abstraction | [LiteLLM](https://github.com/BerriAI/litellm)           | Easy provider switching            |

## Design Decisions

**2 tools for complementary strengths:** `read_code_file` handles file I/O. `lint_code_file` runs ruff on Python files for concrete style findings. The LLM does semantic analysis (security, complex bugs, design patterns). This hybrid approach combines the speed and consistency of linting with the context-awareness of AI reasoning.

**Single agent.run() per file:** The agent enters a decision loop (up to 4 steps) where each iteration makes an LLM call to decide whether to invoke tools or generate the final report. This dynamic approach minimizes unnecessary LLM calls while staying flexible for complex code analysis, and respects Groq's free tier rate limits.

**Plain text output:** The LLM generates readable markdown directly. No JSON parsing, no dataclasses — simpler and more reliable.

**Sequential directory processing:** Files are reviewed one at a time with delays between them, respecting Groq's free tier rate limits.

**Built-in rate limiting:** smolagents' `LiteLLMModel` supports `requests_per_minute` and automatic retry with exponential backoff. No custom retry code needed.
