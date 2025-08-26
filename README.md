# Apertus Format

A Python library for working with the Apertus chat format - a custom conversational format designed for agentic AI models.

## Features

- Multi-layered assistant messages with thinking, tool calls, and responses
- Support for both simple strings and structured content
- Native tool integration with parallel calls
- Chat template formatting for Apertus models

## Installation

```bash
pip install apertus-format
```

## Quick Start

```python
from apertus_format import Message, Conversation, ApertusFormatter

# Create a conversation
messages = [
    Message.system("You are a helpful assistant."),
    Message.user("What is 2 + 2?"),
    Message.assistant("The answer is 4.")
]

conversation = Conversation(messages)

# Format for model consumption
formatter = ApertusFormatter(enable_thinking=True)
formatted = formatter.format_conversation(conversation)
print(formatted)
```

## Documentation

- **[API Reference](API.md)** - Complete API documentation
- **[Examples](examples/)** - Usage examples

## License

MIT License - see LICENSE file for details.
