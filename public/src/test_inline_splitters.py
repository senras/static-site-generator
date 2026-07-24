import unittest
from inline_splitters import *
from textnode import TextNode, TextType


class TestSplitters(unittest.TestCase):
    def test_split_bold_delimiter(self):
        old_nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_italic_delimiter(self):
        old_nodes = [TextNode("Before _italic_ after", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        expected_nodes = [
            TextNode("Before ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" after", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_code_delimiter(self):
        old_nodes = [TextNode("This is a `code block` word", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_leaves_non_plain_nodes_unchanged(self):
        old_nodes = [
            TextNode("This is text", TextType.BOLD),
            TextNode("plain text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(new_nodes[0], TextNode("This is text", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode("plain text", TextType.PLAIN))

    def test_raises_for_unclosed_delimiter(self):
        old_nodes = [TextNode("This has an opening **delimiter", TextType.PLAIN)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
