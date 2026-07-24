from enum import Enum
from textnode import TextNode, TextType
import textwrap

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[TextNode]:
    # Remove common leading indentation from triple-quoted strings
    text = textwrap.dedent(markdown)
    lines = text.splitlines()
    blocks = []

    for line in lines:
        stripped = line.strip()
        if stripped:
            blocks.append(TextNode(stripped, TextType.PLAIN))

    return blocks


def block_to_block_type(block: str) -> BlockType:
    if _is_heading(block):
        return BlockType.HEADING
    if _is_code_block(block):
        return BlockType.CODE
    if _is_quote_block(block):
        return BlockType.QUOTE
    if _is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if _is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def _is_heading(block: str) -> bool:
    if "\n" in block:
        return False
    stripped = block.strip()
    if not stripped.startswith("#"):
        return False
    heading_marker, sep, text = stripped.partition(" ")
    return sep == " " and 1 <= len(heading_marker) <= 6 and heading_marker == "#" * len(heading_marker) and bool(text)


def _is_code_block(block: str) -> bool:
    return block.startswith("```\n") and block.endswith("\n```") and block.count("```") == 2


def _is_quote_block(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    for line in lines:
        if not line.startswith(">"):
            return False
    return True


def _is_unordered_list(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    for line in lines:
        if not line.startswith("- "):
            return False
    return True


def _is_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    expected = 1
    for line in lines:
        parts = line.split(". ", 1)
        if len(parts) != 2:
            return False
        number_text, rest = parts
        if not number_text.isdigit():
            return False
        if int(number_text) != expected:
            return False
        if rest == "":
            return False
        expected += 1
    return True