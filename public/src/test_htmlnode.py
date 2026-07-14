import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_no_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_prop(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com"')

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://example.com", "target": "_blank", "class": "link"},
        )
        self.assertEqual(
            node.props_to_html(),
            'href="https://example.com" target="_blank" class="link"',
        )

    def test_props_to_html_with_empty_string_values(self):
        node = HTMLNode(tag="input", props={"value": "", "type": "text"})
        self.assertEqual(node.props_to_html(), 'value="" type="text"')


if __name__ == "__main__":
    unittest.main()