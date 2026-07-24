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

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Hello World"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Nested Level"), BlockType.HEADING)

    def test_block_to_block_type_code_block(self):
        code_block = "```\nprint(\"Hello\")\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        quote_block = "> Hello\n> World"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        list_block = "- First\n- Second\n- Third"
        self.assertEqual(block_to_block_type(list_block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        list_block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(list_block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("Just a simple paragraph."), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_invalid_sequence(self):
        invalid_block = "1. First\n3. Second\n4. Third"
        self.assertEqual(block_to_block_type(invalid_block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_must_start_with_gt(self):
        invalid_quote = "> Valid\nInvalid"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)
