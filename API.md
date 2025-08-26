# Apertus Format Python API Reference

The `apertus-format` package provides Python utilities for working with the Apertus chat format, a custom conversational format designed for agentic AI models. It exposes dataclasses, parsing utilities, and rendering helpers to work with the multi-layered assistant message structure.

## Enumerations

### `Role`
Represents the author of a message. Possible values are `SYSTEM`, `USER`, `ASSISTANT`, `TOOL`.

### `BlockType`
Defines the types of blocks within an assistant message:
- `THOUGHTS` - reasoning content (always in inner section)
- `TOOL_CALLS` - parallel tool calls (can be in inner or outer)
- `TOOL_OUTPUTS` - parallel tool outputs (can be in inner or outer)
- `RESPONSE` - actual response to user (always in outer section)

### `ContentFormat`
Defines the content format being used:
- `STRING` - simple string content
- `MAPPING` - structured mapping content with parts/blocks

### `SectionType`
Defines the section within assistant messages:
- `INNER` - for reasoning content and internal tool calls
- `OUTER` - for final responses and external tool calls

## Dataclasses

### `TextPart`
```python
TextPart(type: str = "text", text: str)
```
Represents a text part within user content parts.

### `UserContent`
```python
UserContent(parts: List[TextPart])
```
Structured user content with multiple parts. Can be serialized to `{"parts": [...]}` format.

### `SystemContent`
```python
SystemContent(text: str)
```
System message content. Can be serialized to `{"text": "..."}` format.

### `AssistantBlock`
```python
AssistantBlock(type: BlockType, text: Optional[str] = None, calls: Optional[List[ToolCall]] = None, outputs: Optional[List[ToolOutput]] = None)
```
Represents a single block within an assistant message. The content depends on the block type:
- For `THOUGHTS` and `RESPONSE`: uses `text` field
- For `TOOL_CALLS`: uses `calls` field
- For `TOOL_OUTPUTS`: uses `outputs` field

### `ToolCall`
```python
ToolCall(name: str, arguments: str)
```
Represents a single tool call with function name and JSON arguments.

### `ToolOutput`
```python
ToolOutput(output: str)
```
Represents the output from a tool execution.

### `AssistantContent`
```python
AssistantContent(blocks: List[AssistantBlock])
```
Structured assistant content with multiple blocks. Can be serialized to `{"blocks": [...]}` format.

### `Message`
```python
Message(role: Role, content: Union[str, SystemContent, UserContent, AssistantContent])
```
A single chat message that can contain different content types based on the role.

Convenience methods:
- `Message.system(text: str)` - create a system message
- `Message.user(text: str)` - create a simple user message
- `Message.user_with_parts(parts: List[TextPart])` - create structured user message
- `Message.assistant(text: str)` - create simple assistant message
- `Message.assistant_with_blocks(blocks: List[AssistantBlock])` - create structured assistant message
- `Message.tool(content: str)` - create tool message

### `Conversation`
```python
Conversation(messages: List[Message])
```
Sequence of messages representing a complete conversation.

Methods:
- `to_dict()` - convert to dictionary format
- `from_dict(data: dict)` - create from dictionary
- `to_json()` - serialize to JSON string
- `from_json(json_str: str)` - deserialize from JSON string

## Formatting and Parsing

### `ApertusFormatter`
Main class for rendering conversations using the Apertus chat template with Jinja2 templating.

```python
ApertusFormatter(enable_thinking: bool = True, tools: Optional[List[dict]] = None)
```

Methods:
- `format_conversation(conversation: Conversation, add_generation_prompt: bool = False)` - render conversation to chat template format
- `format_assistant_content(assistant_content: AssistantContent)` - format structured assistant content as string
- `format_assistant_message_as_string(message: Message)` - format assistant message content as string for standard chat formats
- `parse_conversation(formatted_text: str)` - parse formatted text back to Conversation object

### Token Definitions
The formatter uses these special tokens:
- `<|system_start|>` / `<|system_end|>` - system message boundaries
- `<|user_start|>` / `<|user_end|>` - user message boundaries  
- `<|assistant_start|>` / `<|assistant_end|>` - assistant message boundaries
- `<|developer_start|>` / `<|developer_end|>` - developer message boundaries
- `<|inner_prefix|>` / `<|inner_suffix|>` - inner/outer section boundaries
- `<|tools_prefix|>` / `<|tools_suffix|>` - tool call boundaries

## Usage Examples

### Basic Usage

```python
from apertus_format import Message, Conversation, ApertusFormatter, Role

# Create messages
system_msg = Message.system("You are a helpful assistant.")
user_msg = Message.user("What is 2 + 2?")

# Create conversation
conversation = Conversation([system_msg, user_msg])

# Format using the chat template
formatter = ApertusFormatter(enable_thinking=True)
formatted = formatter.format_conversation(conversation, add_generation_prompt=True)
print(formatted)
```

### Structured Assistant Response

```python
from apertus_format import AssistantBlock, BlockType, ToolCall, ToolOutput

# Create assistant message with structured blocks
blocks = [
    AssistantBlock(type=BlockType.THOUGHTS, text="I need to calculate 2 + 2"),
    AssistantBlock(type=BlockType.TOOL_CALLS, calls=[
        ToolCall(name="calculator", arguments='{"expression": "2 + 2"}')
    ]),
    AssistantBlock(type=BlockType.TOOL_OUTPUTS, outputs=[
        ToolOutput(output="4")
    ]),
    AssistantBlock(type=BlockType.RESPONSE, text="The answer is 4.")
]

assistant_msg = Message.assistant_with_blocks(blocks)
conversation = Conversation([system_msg, user_msg, assistant_msg])

formatted = formatter.format_conversation(conversation)
print(formatted)
```

### Converting Structured Assistant Content to String

For compatibility with standard chat formats where content must be a string:

```python
from apertus_format import AssistantBlock, BlockType, AssistantContent

# Create structured assistant content
blocks = [
    AssistantBlock(type=BlockType.THOUGHTS, text="Let me think about this..."),
    AssistantBlock(type=BlockType.TOOL_CALLS, calls=[
        ToolCall(name="calculator", arguments='{"expr": "2+2"}')
    ]),
    AssistantBlock(type=BlockType.TOOL_OUTPUTS, outputs=[
        ToolOutput(output="4")
    ]),
    AssistantBlock(type=BlockType.RESPONSE, text="The answer is 4.")
]

assistant_content = AssistantContent(blocks)
assistant_message = Message.assistant_with_blocks(blocks)

formatter = ApertusFormatter(enable_thinking=True)

# Method 1: Format just the content
content_string = formatter.format_assistant_content(assistant_content)

# Method 2: Format the entire message content
message_string = formatter.format_assistant_message_as_string(assistant_message)

# Use in standard chat format
standard_message = Message(role=Role.ASSISTANT, content=content_string)
```

### Tool Messages Outside Assistant Blocks

The format also supports tool messages that appear outside of assistant message blocks:

```python
# Assistant makes tool call
assistant_msg = Message.assistant("I'll help you with that.")
assistant_msg.tool_calls = [ToolCall(name="search", arguments='{"query": "python"}')]

# Tool response as separate message
tool_msg = Message.tool("Here are the search results...")

conversation = Conversation([system_msg, user_msg, assistant_msg, tool_msg])
```

### Content Format Consistency

**IMPORTANT**: Only assistant messages must use consistent content formats within conversations:

```python
# ✅ VALID: Mixed system/user formats, but consistent assistant formats
conversation = Conversation([
    Message.system("String format system"),                    # String
    Message.user_with_parts([TextPart(text="Mapping user")]),  # Mapping  
    Message.assistant("String assistant 1"),                   # String
    Message.assistant("String assistant 2")                    # String - consistent!
])

# ✅ VALID: Mixed system/user formats with structured assistants
conversation = Conversation([
    Message.system_with_mapping("Mapping system"),             # Mapping
    Message.user("String user"),                               # String
    Message.assistant_with_blocks([                            # Structured
        AssistantBlock(type=BlockType.RESPONSE, text="Response 1")
    ]),
    Message.assistant_with_blocks([                            # Structured - consistent!
        AssistantBlock(type=BlockType.RESPONSE, text="Response 2")
    ])
])

# ❌ INVALID: Inconsistent assistant formats (will raise ValueError)
conversation = Conversation([
    Message.system("Any format is fine"),
    Message.user_with_parts([TextPart(text="Any format here too")]),
    Message.assistant("String assistant"),                     # String
    Message.assistant_with_blocks([                            # Structured - ERROR!
        AssistantBlock(type=BlockType.RESPONSE, text="Mixed!")
    ])
])

# ✅ ALWAYS VALID: Tool messages are always strings and don't affect any validation
conversation = Conversation([
    Message.system("You are helpful."),
    Message.user_with_parts([TextPart(text="Mixed formats OK")]),
    Message.assistant("String assistant"),
    Message.tool("Tool output"),                               # Always fine
    Message.assistant("Another string assistant")              # Must match other assistants
])
```

## Advanced Features

### Inner vs Outer Sections

The Apertus format distinguishes between inner (thinking) and outer (final response) sections:

```python
# Thoughts are always in inner section
thoughts_block = AssistantBlock(type=BlockType.THOUGHTS, text="Let me think...")

# Response is always in outer section  
response_block = AssistantBlock(type=BlockType.RESPONSE, text="Here's my answer")

# Tool calls can be in either section depending on context
tool_call_block = AssistantBlock(type=BlockType.TOOL_CALLS, calls=[...])
```

### Format Validation

The formatter validates that assistant messages use consistent content formats:

```python
formatter = ApertusFormatter()

# ✅ Mixed system/user formats with consistent assistants
mixed_conversation = Conversation([
    Message.system("String system"),                           # String format
    Message.user_with_parts([TextPart(text="Mapping user")]),  # Mapping format - OK!
    Message.assistant("String assistant 1"),                   # String format
    Message.assistant("String assistant 2")                    # String format - consistent!
])
formatted = formatter.format_conversation(mixed_conversation)  # Works

# ✅ Any system/user mix with structured assistants
conversation = Conversation([
    Message.system_with_mapping("Mapping system"),             # Mapping format
    Message.user("String user"),                               # String format - OK!
    Message.assistant_with_blocks([                            # Structured
        AssistantBlock(type=BlockType.RESPONSE, text="Response 1")
    ]),
    Message.assistant_with_blocks([                            # Structured - consistent!
        AssistantBlock(type=BlockType.RESPONSE, text="Response 2")
    ])
])
formatted = formatter.format_conversation(conversation)  # Works

# ❌ Inconsistent assistant formats
inconsistent_assistants = Conversation([
    Message.system("Any system format"),
    Message.user("Any user format"),
    Message.assistant("String assistant"),                     # String
    Message.assistant_with_blocks([                            # Structured - ERROR!
        AssistantBlock(type=BlockType.RESPONSE, text="Inconsistent!")
    ])
])
# This will raise ValueError: "Format inconsistency: Assistant message uses structured content..."
formatter.format_conversation(inconsistent_assistants)
```

## Error Handling

The library raises standard Python exceptions:

- `ValueError` - for invalid message roles, block types, or malformed content
- `TypeError` - for incorrect content types or missing required fields
- `RuntimeError` - for parsing failures or template rendering errors

```python
try:
    conversation = Conversation.from_json(json_data)
    formatted = formatter.format_conversation(conversation)
except ValueError as e:
    print(f"Invalid conversation format: {e}")
except RuntimeError as e:
    print(f"Formatting failed: {e}")
```

## Exports

The package exports all main classes and utilities:

```python
from apertus_format import (
    # Core classes
    Message, Conversation, ApertusFormatter,
    
    # Content types
    SystemContent, UserContent, AssistantContent,
    TextPart, AssistantBlock, ToolCall, ToolOutput,
    
    # Enums
    Role, BlockType, ContentFormat, SectionType
)
```
