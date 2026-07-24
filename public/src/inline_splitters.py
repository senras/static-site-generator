import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing delimiter '{delimiter}'")

        for i, part in enumerate(parts):
            if i == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                if i % 2 == 1:
                    new_nodes.append(TextNode(parts[i], text_type))
                else:
                    new_nodes.append(TextNode(parts[i], TextType.PLAIN))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            alt_text, url = match
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.PLAIN))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt_text}]({url})")

        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            anchor_text, url = match
            start_index = node.text.find(f"[{anchor_text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.PLAIN))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            last_index = start_index + len(f"[{anchor_text}]({url})")

        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.PLAIN))

    return new_nodes