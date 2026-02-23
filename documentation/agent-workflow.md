# Agent Workflow

## Overview

The agent autonomously uses tools to analyze code and produce a review. It uses Groq's LLM through [smolagents](https://github.com/huggingface/smolagents) to decide which tools to call and how to synthesize the results.

## Execution Flow

```
1. User runs: python src/code_review_agent.py myfile.py
       ↓
2. Agent receives task prompt with review checklists
       ↓
3. Agent calls read_code_file("myfile.py") → source code
       ↓
4. Agent analyzes code against all checklists (security, style, bugs)
       ↓
5. Agent produces markdown report via final_answer()
       ↓
6. Result saved as markdown report
```

The agent makes 2 LLM calls total: one to decide to read the file (tool call), and one to analyze the code and produce findings.

## How It Works

The `read_code_file` tool handles file I/O — it reads source code from disk, which the LLM can't do on its own. The review checklists are embedded in the task prompt, giving the LLM structured guidance on what to look for.

This design means:
- The tool provides **I/O** (reading files from disk)
- The prompt provides **structure** (categories and checklists)
- The LLM provides **intelligence** (actual code analysis)
- Works for any programming language (the LLM adapts)

## Rate Limit Protection

The agent uses three layers of protection for Groq's free tier (30 RPM):

1. **Built-in rate limiter** — `requests_per_minute=25` throttles API calls
2. **Auto-retry** — 429 errors trigger exponential backoff (up to 3 retries)
3. **Inter-file delay** — 10s pause between files in directory mode

## Customization

```python
# Change the task prompt
task = "Review for security ONLY. Ignore style."

# Adjust agent parameters
agent = create_agent(temperature=0.1, verbose=False)
```

## Agent vs Static Analysis

| Aspect | Static Analysis | AI Agent |
|--------|----------------|----------|
| Rules | Fixed patterns | Context-aware |
| Languages | Language-specific | Any language |
| Explanations | Generic | Code-specific |
| Customization | Rule changes | Natural language |
