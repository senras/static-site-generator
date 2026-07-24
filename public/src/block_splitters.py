from textnode import TextNode, TextType
import textwrap

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