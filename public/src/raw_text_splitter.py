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