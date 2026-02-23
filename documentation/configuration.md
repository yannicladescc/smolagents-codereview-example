# Configuration

## Environment Variables

```bash
# Required
GROQ_API_KEY=your_key_here

# Optional (defaults shown)
GROQ_MODEL_NAME=groq/llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.2
GROQ_MAX_TOKENS=1024
```

Set via `.env` file or `export`.

## Model Options

| Model | Best For |
|-------|----------|
| `groq/llama-3.3-70b-versatile` | Default, reliable, 12K TPM free tier |
| `groq/llama-3.1-8b-instant` | Faster, lower quality, 6K TPM free tier |
| `groq/deepseek-r1-distill-llama-70b` | Code reasoning |

[Get free API key](https://console.groq.com/keys)

## Rate Limits (Groq Free Tier)

- **30 RPM** (requests per minute) — agent uses `requests_per_minute=25`
- **~12K TPM** for llama-3.3-70b — agent uses `max_tokens=1024`
- Auto-retry on 429 with exponential backoff (built into smolagents)
- 10s delay between files in directory mode

## Programmatic Usage

```python
from src.code_review_agent import create_agent, review_code_file, review_directory

# Custom agent
agent = create_agent(
    model_name="groq/llama-3.1-8b-instant",
    temperature=0.1,
    verbose=False,
)

# Single file
result = review_code_file("mycode.py")

# Directory
results = review_directory("src/")
```

## Agent Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `max_steps` | 2 | Max LLM calls per review (read file + analyze) |
| `verbosity_level` | 2 | 0=silent, 1=info, 2=debug |
| `requests_per_minute` | 25 | Stay under Groq's 30 RPM |
| `temperature` | 0.2 | Lower = more deterministic |
| `max_tokens` | 1024 | Max output tokens per call |
