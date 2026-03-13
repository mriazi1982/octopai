# Getting Started

This guide will help you get up and running with EXO in minutes.

## Prerequisites

- Python 3.8 or higher
- API keys for Cloudflare and OpenRouter

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Yuan-ManX/EXO.git
cd EXO
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
# or for development installation
pip install -e .
```

### 3. Configure API Keys

Create a `.env` file in the project root directory:

```env
# Cloudflare API Configuration
CLOUDFLARE_API_KEY=your_cloudflare_api_key
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id

# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Quick Start

### Using the Python API

The simplest way to use EXO is through the Python API:

```python
import exo

# Convert a URL to a skill
skill_dir = exo.convert("https://example.com")
print(f"Skill created at: {skill_dir}")

# Full processing pipeline
final_skill_dir = exo.process("https://example.com", evolve=True)
print(f"Final skill at: {final_skill_dir}")
```

### Using the CLI

Or use EXO from your terminal:

```bash
# Convert URL to skill
exo convert --url https://example.com --name my-skill

# Evolve a skill
exo evolve --skill ./skills/my-skill

# Batch process
exo batch --urls urls.txt --output ./skills/
```

## Next Steps

- Explore the [API Reference](./api-reference.md) for comprehensive documentation
- Check out the [CLI Usage](./cli-usage.md) guide
- See [Examples](./examples.md) for more use cases
- Dive into [Advanced Topics](./advanced-topics.md) for in-depth features
