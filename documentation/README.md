# Documentation Index

## Quick Start

1. [Main README](../README.md) — Overview & setup
2. [From-Scratch Setup](from-scratch-setup.md) — Build your own (workshop guide)

## Docs

| Document | Description |
|----------|-------------|
| [Agent Workflow](agent-workflow.md) | How the agent makes decisions |
| [Tools](tools-and-capabilities.md) | Tool architecture & custom tools |
| [Architecture](architecture.md) | System design |
| [Configuration](configuration.md) | Models, parameters, rate limits |

## Key Concepts

- **Agent:** AI system that autonomously uses tools to complete tasks ([details](agent-workflow.md))
- **Tool:** Python function with `@tool` decorator callable by the agent ([details](tools-and-capabilities.md))
- **smolagents:** HuggingFace's lightweight agent framework ([details](architecture.md))
- **Groq:** Free, fast LLM API provider ([details](configuration.md))

## External Resources

- [smolagents docs](https://smolagents.org/docs)
- [Groq docs](https://console.groq.com/docs)
- [Groq API keys](https://console.groq.com/keys)
