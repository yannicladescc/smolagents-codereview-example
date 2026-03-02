# Configuration

## Environment Variables

```bash
# Required
GROQ_API_KEY=your_key_here

# Optional (defaults shown)
GROQ_MODEL_NAME=groq/meta-llama/llama-4-scout-17b-16e-instruct
GROQ_TEMPERATURE=0.2
GROQ_MAX_TOKENS=2000
```

Set via `.env` file or `export`.

## Model Selection

The default model is `groq/meta-llama/llama-4-scout-17b-16e-instruct` with a 30K token-per-minute limit. You can use any other Groq model as long as it has a context window large enough for your code files. Adjust `GROQ_MAX_TOKENS` if using a model with different rate limits.

[Get free API key](https://console.groq.com/keys)

## Rate Limits

- **25 RPM** — requests per minute (Groq's free tier: 30 RPM)
- **30K TPM** — tokens per minute (Groq's free tier limit)
- **2000 tokens** — `max_tokens` configured to safely stay under TPM limit
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

| Parameter             | Default | Purpose                                        |
| --------------------- | ------- | ---------------------------------------------- |
| `max_steps`           | 2       | Max LLM calls per review (read file + analyze) |
| `verbosity_level`     | 2       | 0=silent, 1=info, 2=debug                      |
| `requests_per_minute` | 25      | Stay under Groq's 30 RPM                       |
| `temperature`         | 0.2     | Lower = more deterministic                     |
| `max_tokens`          | 4096    | Max output tokens per call                     |
