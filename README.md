# Code Review Agent with smolagents & Groq

AI-powered code review agent built with [smolagents](https://github.com/huggingface/smolagents) and [Groq's free API](https://console.groq.com). Works with any programming language.

## Quick Start

```bash
# 1. Install dependencies
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. Get free API key from https://console.groq.com/keys
export GROQ_API_KEY="your-key-here"

# 3. Run review
python src/code_review_agent.py examples/bad_code.py
```

## Usage

```bash
# Review a single file
python src/code_review_agent.py myfile.py

# Review a directory (processes files sequentially, respects rate limits)
python src/code_review_agent.py my_project/

# Skip saving reports
python src/code_review_agent.py myfile.js --no-save
```

```python
# Programmatic usage
from src.code_review_agent import review_code_file, review_directory

result = review_code_file("mycode.py")
results = review_directory("my_project/")
```

## Architecture

```
User → review_code_file() → CodeAgent → Tools → Text Report
                                ↓
                         Groq LLM (Llama 3.3 70B)
```

**Tools:** `read_code_file` (loads files), `analyze_code` (guides analysis by category)

The agent reads code, then calls `analyze_code` for each category (security, style, bugs). The LLM performs the actual analysis — tools provide structure, the LLM provides intelligence.

## Configuration

```bash
GROQ_API_KEY=your_key                         # Required
GROQ_MODEL_NAME=groq/llama-3.3-70b-versatile  # Optional
GROQ_TEMPERATURE=0.2                          # Optional
GROQ_MAX_TOKENS=2048                          # Optional
```

## Documentation

- **[From-Scratch Setup](documentation/from-scratch-setup.md)** — Workshop guide (build your own)
- **[Agent Workflow](documentation/agent-workflow.md)** — How the agent makes decisions
- **[Tools](documentation/tools-and-capabilities.md)** — Tool architecture & custom tools
- **[Architecture](documentation/architecture.md)** — System design
- **[Configuration](documentation/configuration.md)** — Models, parameters, rate limits

## Project Structure

```
src/
  code_review_agent.py   # Agent logic (CLI, agent creation, review functions)
  tools.py               # Tool definitions (read_code_file, analyze_code)
examples/                # Test files
documentation/           # Guides
reports/                 # Generated outputs
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| API key not set | `export GROQ_API_KEY="your-key"` or add to `.env` |
| Module not found | `source .venv/bin/activate && uv pip install -r requirements.txt` |
| Rate limit (429) | Built-in retry handles this automatically. Reduce `GROQ_MAX_TOKENS` if persistent |
| Inconsistent results | Lower `GROQ_TEMPERATURE` to 0.1 |

## Workshop Guide (1 Hour)

| Time | Activity |
|------|----------|
| 0-10 | Setup (dependencies, API key) |
| 10-25 | Build tools (`read_code_file`, `analyze_code`) |
| 25-40 | Create agent, write review function |
| 40-55 | Test with examples, add directory support |
| 55-60 | Q&A |

Guide: [documentation/from-scratch-setup.md](documentation/from-scratch-setup.md)

## Resources

- [smolagents](https://github.com/huggingface/smolagents) — Agent framework
- [Groq](https://groq.com) — Free LLM API
- [LiteLLM](https://github.com/BerriAI/litellm) — LLM provider abstraction
