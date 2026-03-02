# Agent Workflow

## Overview

The agent autonomously uses tools to analyze code and produce a review. It uses Groq's LLM through [smolagents](https://github.com/huggingface/smolagents) to decide which tools to call and how to synthesize the results.

## Execution Flow

```
1. User runs: python src/code_review_agent.py myfile.py
       ↓
2. Agent receives task prompt with review checklists
       ↓
3. Agent enters loop (max 4 steps):
   ┌─────────────────────────────────────┐
   │ LLM decides: Call tool OR generate  │
   │ output?                             │
   │                                     │
   │ If TOOL:                            │
   │  → read_code_file("myfile.py")      │
   │  → lint_code_file() [if Python]     │
   │  → Continue loop with results       │
   │                                     │
   │ If OUTPUT:                          │
   │  → Generate markdown report         │
   │  → Exit loop                        │
   └─────────────────────────────────────┘
       ↓
4. Result saved as markdown report
```

The agent makes **up to 4 LLM calls** (one per loop iteration): the LLM decides dynamically at each step whether to invoke tools or generate the final review.

## How It Works

The `read_code_file` tool handles file I/O. For Python files, `lint_code_file` runs ruff to detect concrete style violations. The LLM analyzes code against semantic checklists (security, bugs, design patterns) and integrates linting findings into the report.

This design means:

- Tools provide **I/O + linting** (file access, concrete violations)
- The **prompts.yaml** file provides **structure** (externalized prompt templates with categories and checklists)
- The LLM provides **intelligence** (context-aware analysis)
- Works for any programming language (linting for Python, semantic analysis for all)

## Rate Limit Protection

The agent uses three layers of protection for Groq's free tier (30 RPM):

1. **Built-in rate limiter** — `requests_per_minute=25` throttles API calls
2. **Auto-retry** — 429 errors trigger exponential backoff (up to 3 retries)
3. **Inter-file delay** — 10s pause between files in directory mode

## Customization

**Update prompts:** Edit `src/prompts.yaml` to modify review categories, guidelines, or checklists without touching Python code.

```yaml
# src/prompts.yaml
prompts:
  code_review:
    template: |
      Review the code file at '{file_path}'.
      # Customize categories and guidelines here
```

**Adjust agent parameters:**

```python
# Adjust temperature, verbosity, rate limits
agent = create_agent(temperature=0.1, verbose=False)
```

## Agent vs Static Analysis

| Aspect        | Static Analysis   | AI Agent         |
| ------------- | ----------------- | ---------------- |
| Rules         | Fixed patterns    | Context-aware    |
| Languages     | Language-specific | Any language     |
| Explanations  | Generic           | Code-specific    |
| Customization | Rule changes      | Natural language |
