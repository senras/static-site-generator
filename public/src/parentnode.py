from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list, props: dict = None):
        self.tag = tag
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag.")
        if not self.children:
            raise ValueError("Parent nodes must have at least one child.")
        props_str = self.props_to_html()
        children_html = ''.join(child.to_html() for child in self.children)
        if props_str:
            return f"<{self.tag} {props_str}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"