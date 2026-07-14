from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag: str, value: str, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = []
        self.props = props if props is not None else {}

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

