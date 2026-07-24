import unittest
from block_splitters import *
from textnode import TextNode, TextType

class TestBlockSplitters(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = """This is the first block.
                    This is the second block.
                    This is the third block."""
        expected_blocks = [
            TextNode("This is the first block.", TextType.PLAIN),
            TextNode("This is the second block.", TextType.PLAIN),
            TextNode("This is the third block.", TextType.PLAIN)
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, expected_blocks)

    def test_markdown_to_blocks_with_empty_lines(self):
        markdown = """This is the first block.

                    This is the second block.

                    This is the third block."""
        expected_blocks = [
            TextNode("This is the first block.", TextType.PLAIN),
            TextNode("This is the second block.", TextType.PLAIN),
            TextNode("This is the third block.", TextType.PLAIN)
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, expected_blocks)

    def test_markdown_to_blocks_with_leading_and_trailing_empty_lines(self):
        markdown = """

                    This is the first block.

                    This is the second block.

                    This is the third block.

                    """
        expected_blocks = [
            TextNode("This is the first block.", TextType.PLAIN),
            TextNode("This is the second block.", TextType.PLAIN),
            TextNode("This is the third block.", TextType.PLAIN)
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, expected_blocks)