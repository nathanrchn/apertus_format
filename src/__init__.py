"""Apertus Format Python Library.

A Python library for working with the Apertus chat format, providing utilities
for parsing, formatting, and working with structured conversational data.
"""

from .enums import Role, BlockType, ContentFormat, SectionType
from .models import (
    TextPart,
    SystemContent,
    UserContent,
    ToolCall,
    ToolOutput,
    AssistantBlock,
    AssistantContent,
    Message,
    Conversation,
)
from .formatter import ApertusFormatter

__version__ = "0.1.0"

__all__ = [
    # Core classes
    "Message",
    "Conversation",
    "ApertusFormatter",
    # Content types
    "SystemContent",
    "UserContent",
    "AssistantContent",
    "TextPart",
    "AssistantBlock",
    "ToolCall",
    "ToolOutput",
    # Enums
    "Role",
    "BlockType",
    "ContentFormat",
    "SectionType",
    # Version
    "__version__",
]
