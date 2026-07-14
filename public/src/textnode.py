from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        if not isinstance(text_type, TextType):
            raise ValueError(f"Invalid text type: {text_type}. Must be an instance of TextType Enum.")
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"
    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
        # TextType.PLAIN: This should return a LeafNode with no tag, just a raw text value.
        # TextType.BOLD: This should return a LeafNode with a "b" tag and the text
        # TextType.ITALIC: "i" tag, text
        # TextType.CODE: "code" tag, text
        # TextType.LINK: "a" tag, anchor text, and "href" prop
        # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)

        if text_node.text_type == TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        elif text_node.text_type == TextType.LINK:
            if not text_node.url:
                raise ValueError("URL must be provided for LINK text type.")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            if not text_node.url:
                raise ValueError("URL must be provided for IMAGE text type.")
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
