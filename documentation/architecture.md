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
│  Agent Layer                                        │
│  ┌──────────────────────────────────────────────┐  │
│  │ LiteLLM → Groq API (Llama 3.3 70B)          │  │
│  │ CodeAgent (smolagents)                       │  │
│  │   • Rate limiter (25 RPM)                    │  │
│  │   • Auto-retry on 429                        │  │
│  └──────────────────┬───────────────────────────┘  │
│                     ↓                               │
│  Tool Layer                                         │
│  ┌──────────────────────────────────────────────┐  │
│  │ read_code_file: loads source files from disk │  │
│  └──────────────────┬───────────────────────────┘  │
│                     ↓                               │
│  Output: plain text report (saved as .md)           │
└────────────────────────────────────────────────────┘
```

## File Structure

```
src/
  code_review_agent.py   # Agent creation, review functions, CLI
  tools.py               # Tool definition (read_code_file)
examples/              # Test code files
documentation/         # Guides
reports/               # Generated review reports
```

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Agent framework | [smolagents](https://github.com/huggingface/smolagents) | Simple, code-first, model-agnostic |
| LLM provider | [Groq](https://groq.com) | Free tier, fast inference |
| Provider abstraction | [LiteLLM](https://github.com/BerriAI/litellm) | Easy provider switching |

## Design Decisions

**1 tool, not many:** `read_code_file` handles file I/O — the one thing the LLM can't do on its own. The review checklists are embedded in the task prompt since they're static data, not dynamic operations. The LLM does the actual analysis.

**Single agent.run() per file:** The agent reads the file (1 tool call) and produces the full report (1 final answer) in 2 LLM calls. This minimizes token usage and stays within Groq's free tier rate limits.

**Plain text output:** The LLM generates readable markdown directly. No JSON parsing, no dataclasses — simpler and more reliable.

**Sequential directory processing:** Files are reviewed one at a time with delays between them, respecting Groq's free tier rate limits.

**Built-in rate limiting:** smolagents' `LiteLLMModel` supports `requests_per_minute` and automatic retry with exponential backoff. No custom retry code needed.
