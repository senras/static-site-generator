from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from text_to_textnode import text_to_textnodes
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


def markdown_to_document_blocks(markdown: str) -> list[str]:
    text = textwrap.dedent(markdown).strip("\n")
    if not text:
        return []

    lines = text.splitlines()
    blocks = []
    current_block_lines = []
    in_code_block = False

    def flush_block():
        nonlocal current_block_lines
        if current_block_lines:
            blocks.append("\n".join(current_block_lines))
            current_block_lines = []

    for line in lines:
        if in_code_block:
            current_block_lines.append(line)
            if line.strip() == "```":
                in_code_block = False
                flush_block()
            continue

        if line.strip().startswith("```"):
            flush_block()
            in_code_block = True
            current_block_lines.append(line)
            continue

        if line.strip() == "":
            flush_block()
            continue

        current_block_lines.append(line.strip())

    flush_block()
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
        if not line.lstrip().startswith(">"):
            return False
    return True


def _is_unordered_list(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    for line in lines:
        if not line.lstrip().startswith("- "):
            return False
    return True


def _is_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    expected = 1
    for line in lines:
        stripped = line.lstrip()
        parts = stripped.split(". ", 1)
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


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_document_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            stripped = block.strip()
            marker, _, text = stripped.partition(" ")
            level = max(1, min(6, len(marker)))
            children.append(ParentNode(f"h{level}", text_to_children(text)))
            continue

        if block_type == BlockType.CODE:
            lines = block.splitlines()
            inner_lines = lines[1:-1]
            inner = "\n".join(inner_lines)
            if inner_lines:
                inner += "\n"
            code_node = text_node_to_html_node(TextNode(inner, TextType.CODE))
            children.append(ParentNode("pre", [code_node]))
            continue

        if block_type == BlockType.QUOTE:
            quote_children = []
            lines = block.splitlines()
            for idx, line in enumerate(lines):
                content = line.lstrip()[1:]
                if content.startswith(" "):
                    content = content[1:]
                quote_children.extend(text_to_children(content))
                if idx < len(lines) - 1:
                    quote_children.append(LeafNode(None, "\n"))
            children.append(ParentNode("blockquote", quote_children))
            continue

        if block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.splitlines():
                text = line.lstrip()[2:]
                items.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ul", items))
            continue

        if block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.splitlines():
                text = line.lstrip().split(". ", 1)[1]
                items.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ol", items))
            continue

        paragraph_text = " ".join(line.strip() for line in block.splitlines())
        children.append(ParentNode("p", text_to_children(paragraph_text)))

    if not children:
        return ParentNode("div", [LeafNode(None, "")])

    return ParentNode("div", children)
