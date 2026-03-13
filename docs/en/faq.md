# Frequently Asked Questions

## General Questions

### What is EXO?

EXO is an AI Agent skill development platform that provides tools for:
- Converting web pages to Markdown
- Creating AI skills from natural language descriptions
- Evolving and improving existing skills using advanced AI
- Crawling websites for resource collection

### How is EXO different from other AI platforms?

EXO combines several unique features:
- **Evolution Engine**: Inspired by GEPA, it uses LLM-based reflection for intelligent improvement
- **Dual Interface**: Use via Python API or command-line, whichever is more convenient
- **Built-in Crawling**: Integrated web crawling for resource collection
- **OpenRouter Integration**: Access to hundreds of AI models through a single API

### Do I need coding experience to use EXO?

Basic coding experience is helpful for the Python API, but the CLI interface is accessible to beginners. We provide extensive examples and documentation to help you get started.

## Installation & Setup

### How do I install EXO?

```bash
pip install exo
```

Or from source:
```bash
git clone https://github.com/Yuan-ManX/EXO.git
cd EXO
pip install -e .
```

### What API key do I need?

You need an OpenRouter API key. Sign up at [openrouter.ai](https://openrouter.ai) to get one.

### How do I set my API key?

Set it as an environment variable:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
OPENROUTER_API_KEY=your-api-key-here
```

## Usage Questions

### Which model should I use?

- **openai/gpt-5.4** (default): Good balance of cost and quality for most tasks
- **openai/gpt-5**: Best quality for complex evolution and creation
- **anthropic/claude-4.6-sonnet**: Good alternative for coding tasks
- **google/gemini-3-pro**: Another solid option

### How much does EXO cost?

EXO itself is free and open-source. You only pay for the AI model usage through OpenRouter. Costs vary by model:
- GPT-5.4: ~$0.15 per 1M input tokens
- GPT-5: ~$5 per 1M input tokens

### Can I use EXO offline?

No, EXO requires API access to AI models. However, you can cache results to minimize API calls.

### How long does skill evolution take?

It depends on:
- Number of iterations (default: 3)
- Model used (GPT-5.4 is slower but better)
- Complexity of the skill

Typical times:
- Simple skill: 1-2 minutes
- Complex skill with 5 iterations: 5-10 minutes

## Technical Questions

### What is the Evolution Engine?

The Evolution Engine is EXO's advanced feature inspired by GEPA. It uses a three-stage pipeline:
1. **Executor**: Runs candidates and captures traces
2. **Reflector**: Analyzes failures and successes
3. **Optimizer**: Generates improved candidates

This allows for intelligent, directed improvement rather than random search.

### What is Actionable Side Information (ASI)?

ASI is diagnostic feedback that helps the evolution engine understand why something succeeded or failed. Examples include:
- Error messages
- Performance metrics
- Reasoning traces
- Constraint violations

Providing good ASI significantly improves evolution quality.

### Can I customize the evolution process?

Yes! You can:
- Create custom evaluators
- Adjust the number of iterations
- Choose different models for different stages
- Define custom evaluation tasks

See the [Advanced Topics](./advanced-topics.md) section for details.

### How does the web crawler work?

The crawler:
1. Fetches the HTML page
2. Extracts all resources (images, CSS, JS)
3. Downloads them to a local directory
4. Returns a structured resource object

You can customize the crawler's behavior - see [Advanced Topics](./advanced-topics.md).

## Troubleshooting

### I'm getting an API authentication error

Make sure your OpenRouter API key is correctly set:
```bash
echo $OPENROUTER_API_KEY  # Should show your key
```

If not, set it:
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### The evolution isn't improving my skill

Try these steps:
1. Increase the number of iterations (`-i 5` or more)
2. Use a better model (`model="openai/gpt-5.4"`)
3. Provide more specific feedback in your prompt
4. Ensure your evaluator provides good ASI

### My crawled files are incomplete

Check:
- Your internet connection
- The website's robots.txt rules
- Website's anti-scraping measures
- Try increasing timeout settings

### The CLI isn't found

Make sure EXO is installed:
```bash
pip show exo
```

If installed, check your PATH. You may need to add Python's bin directory to your PATH.

## Advanced Usage

### Can I integrate EXO into my existing project?

Absolutely! EXO is designed to be imported and used as a library:

```python
from exo import EXO

exo = EXO()
skill = exo.create_skill("My custom skill")
```

See the [API Reference](./api-reference.md) for full documentation.

### How can I contribute to EXO?

We welcome contributions! Please see our GitHub repository for:
- Issue tracker
- Contribution guidelines
- Code of conduct

### Is EXO production-ready?

EXO is suitable for:
- Prototyping and development
- Skill creation and evolution
- Documentation processing
- Web crawling

For critical production systems, we recommend thorough testing.

## More Help

Still have questions?

- Check our [GitHub Issues](https://github.com/Yuan-ManX/EXO/issues)
- Join our community discussions
- Review the [Examples](./examples.md) for practical use cases
- Read the [Advanced Topics](./advanced-topics.md) for deep dives
