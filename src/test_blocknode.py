import unittest

from blocknode import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        self.assertEqual(markdown_to_blocks(md), [])

    def test_whitespace_only(self):
        md = " \n\n "
        self.assertEqual(markdown_to_blocks(md), [])

    def test_single_newline(self):
        md = "Line one.\nLine two."
        self.assertEqual(markdown_to_blocks(md), ["Line one.\nLine two."])

    def test_code_blocks(self):
        md = 'Here is some code:\n\n```\ndef hello():\n    print("Hello, world!")\n```\n\nEnd of code.'
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Here is some code:",
                '```\ndef hello():\n    print("Hello, world!")\n```',
                "End of code.",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_empty_block(self):
        """Test an empty block."""
        with self.assertRaises(ValueError):
            block_to_block_type("")

    def test_whitespace_only_block(self):
        """Test a block with only whitespace."""
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)

    def test_one_line_quote(self):
        block = """> Test a block with only whitespace."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_multi_line_quote(self):
        block = """\
> Test a block with only whitespace.
> Test a block with only whitespace.
> Test a block with only whitespace."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_heading_with_no_space(self):
        """Test a heading without a space after the #."""
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_code_block_with_incorrect_closing(self):
        """Test a code block with mismatched backticks."""
        self.assertEqual(block_to_block_type("```\ncode\n``"), BlockType.PARAGRAPH)

    def test_quote_with_leading_spaces(self):
        """Test a quote block with leading spaces before >."""
        self.assertEqual(block_to_block_type("   > This is a quote"), BlockType.QUOTE)

    def test_unordered_list_with_inconsistent_format(self):
        """Test an unordered list with inconsistent formatting."""
        block = "- Item 1\nItem 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_inconsistent_format(self):
        """Test an ordered list with inconsistent formatting."""
        block = "1. Item 1\n2 Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_blockquote_and_text(self):
        """Test a block with mixed blockquote and normal text."""
        block = "> This is a quote\nThis is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
