# Apertus Format

A comprehensive Python library for working with the Apertus chat format - a custom conversational format designed for agentic AI models. The Apertus models were trained on this format to enable sophisticated reasoning, tool usage, and multi-layered responses.

## Overview

The Apertus format extends standard chat formats with powerful features for AI agents:

- **Multi-layered Assistant Messages**: Structured responses with thinking, tool calls, outputs, and final responses
- **Inner/Outer Sections**: Separate reasoning (inner) from final responses (outer)
- **Flexible Content Formats**: Support for both simple strings and structured mappings
- **Tool Integration**: Native support for parallel tool calls and outputs within assistant messages
- **Agentic Design**: Purpose-built for AI models that need to think, use tools, and provide comprehensive responses

## Key Features

### 🧠 **Structured Reasoning**
Assistant messages can contain separate thinking/reasoning sections that are distinct from the final response.

### 🔧 **Advanced Tool Usage**
- Parallel tool calls within assistant messages
- Tool outputs embedded in the conversation flow
- Support for both block-structured and legacy tool calling formats

### 📝 **Flexible Content**
- **String Format**: Simple text content for basic use cases
- **Mapping Format**: Structured content with parts, blocks, and metadata

### 🎯 **Chat Template Integration**
Built-in formatter that converts conversations to the exact token format expected by Apertus models.

## Installation

```bash
pip install apertus-format
```

**Dependencies**: The library requires Jinja2 for template rendering. Install manually if needed:

```bash
pip install jinja2>=3.0.0
```

Or install from source with dependencies:

```bash
git clone <repository-url>
cd apertus-format
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from apertus_format import Message, Conversation, ApertusFormatter

# Create a simple conversation
messages = [
    Message.system("You are a helpful assistant."),
    Message.user("What is 2 + 2?"),
    Message.assistant("The answer is 4.")
]

conversation = Conversation(messages)

# Format for model consumption
formatter = ApertusFormatter(enable_thinking=True)
formatted = formatter.format_conversation(conversation, add_generation_prompt=True)
print(formatted)
```

### Structured Assistant Response

```python
from apertus_format import AssistantBlock, BlockType, ToolCall, ToolOutput

# Create a structured assistant response with reasoning and tool usage
blocks = [
    AssistantBlock(type=BlockType.THOUGHTS, text="I need to calculate this..."),
    AssistantBlock(type=BlockType.TOOL_CALLS, calls=[
        ToolCall(name="calculator", arguments='{"expr": "2+2"}')
    ]),
    AssistantBlock(type=BlockType.TOOL_OUTPUTS, outputs=[
        ToolOutput(output="4")
    ]),
    AssistantBlock(type=BlockType.RESPONSE, text="The answer is 4.")
]

assistant_msg = Message.assistant_with_blocks(blocks)
```

### Tool Configuration

```python
# Define available tools
tools = [{
    "name": "calculator",
    "description": "Perform mathematical calculations",
    "parameters": {
        "type": "object",
        "properties": {
            "expr": {"type": "string", "description": "Mathematical expression"}
        },
        "required": ["expr"]
    }
}]

formatter = ApertusFormatter(enable_thinking=True, tools=tools)
```

### Standard Chat Compatibility

Convert structured assistant content to strings for use with standard chat formats:

```python
from apertus_format import AssistantBlock, BlockType, AssistantContent

# Create structured assistant response
blocks = [
    AssistantBlock(type=BlockType.THOUGHTS, text="Let me think..."),
    AssistantBlock(type=BlockType.RESPONSE, text="Here's my answer!")
]

assistant_content = AssistantContent(blocks)
formatter = ApertusFormatter(enable_thinking=True)

# Convert to string for standard chat formats
content_string = formatter.format_assistant_content(assistant_content)
# Result: "<|inner_prefix|>Let me think...<|inner_suffix|>Here's my answer!"

# Use in standard message format
standard_message = Message(role=Role.ASSISTANT, content=content_string)
```

## Format Comparison

### Standard Chat Format
```
System: You are helpful.
User: What is 2+2?
Assistant: The answer is 4.
```

### Apertus Format
```
<|system_start|>You are helpful.<|system_end|>
<|user_start|>What is 2+2?<|user_end|>
<|assistant_start|><|inner_prefix|>I need to calculate 2+2.<|inner_suffix|>
<|tools_prefix|>[{"calculator": {"expr": "2+2"}}]<|tools_suffix|>
[4]
The answer is 4.<|assistant_end|>
```

## Assistant Message Structure

The Apertus format's key innovation is the structured assistant message with four types of blocks:

| Block Type | Location | Purpose |
|------------|----------|---------|
| `thoughts` | Inner | Reasoning and planning |
| `tool_calls` | Inner/Outer | Parallel tool invocations |
| `tool_outputs` | Inner/Outer | Results from tool calls |
| `response` | Outer | Final response to user |

## Content Formats

**IMPORTANT**: Only assistant messages must use the same content format. System and user messages can be mixed freely.

### Format Flexibility
```python
# ✅ VALID: Mixed system/user formats, consistent assistants
conversation = Conversation([
    Message.system("String system"),                          # String
    Message.user_with_parts([TextPart(text="Mapping user")]), # Mapping - OK!
    Message.assistant("String assistant 1"),                  # String
    Message.assistant("String assistant 2")                   # String - consistent!
])
```

### String Format (Simple)
```python
Message.system("You are helpful.")
Message.user("Hello")
Message.assistant("Hi there!")
```

### Mapping Format (Structured)
```python
Message.system_with_mapping("You are helpful.")  # {"text": "..."}
Message.user_with_parts([TextPart(text="Hello")])  # {"parts": [...]}
Message.assistant_with_blocks([...])  # {"blocks": [...]}
```

### Format Consistency Rules

- ✅ **Valid**: System and user messages can use any format combination
- ✅ **Valid**: Assistant messages must all use the same format (string OR structured)
- ❌ **Invalid**: Mixing string and structured assistant messages
- ✅ **Exception**: Tool messages are always strings and don't affect any validation

## Documentation

- **[API Reference](API.md)** - Complete API documentation
- **[Examples](examples/)** - Comprehensive usage examples
- **[Chat Template Details](API.md#formatting-and-parsing)** - Technical details of the format

## Examples

Explore the `examples/` directory for comprehensive demonstrations:

- `basic_usage.py` - Simple string and mapping format examples
- `structured_assistant.py` - Multi-block assistant responses with tools
- `tool_messages.py` - Tool messages outside assistant blocks
- `format_consistency.py` - Format validation and consistency requirements
- `assistant_string_formatting.py` - Converting structured content to strings for standard chat formats

## Advanced Features

### Inner vs Outer Sections
- **Inner**: Reasoning, thinking, internal tool calls
- **Outer**: Final responses, external tool calls, user-facing content

### Tool Integration
- Tools calls within assistant message blocks
- Tool messages as separate conversation entries
- Parallel tool execution support

### Format Validation
The library validates that assistant messages use consistent content formats and raises errors if you mix string and structured assistant messages.

## Contributing

We welcome contributions! Please see our contributing guidelines for details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please open an issue on our GitHub repository.
