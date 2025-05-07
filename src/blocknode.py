# the regex approach seem to be not a good idea here due to numerous possible recompilations
from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split a raw markdown document to blocks.

    :param markdown: str - a string representing  markdown document that
                           is going to be converted.

    :returns: list[str] - a list of markdown blocks with preserved formatting
    """
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(markdown_block: str) -> "BlockType":
    """Pair a markdown block string with a right BlockType.

    :param markdown_block: str - string representing a markdown block

    :returns: BlockType - enum class representing markdown block types
    """
    if not markdown_block:
        raise ValueError("Block seems to be empty.")

    if not isinstance(markdown_block, str):
        raise ValueError("Block should be string")

    markdown_block = markdown_block.strip()

    # helper functions for markdown syntax
    def code_block_check(multiline_block: str) -> bool:
        """Check if the block is a code block"""
        lines = multiline_block.split("\n")
        return lines[0].startswith("```") and lines[-1].startswith("```")

    def quote_check(multiline_block: str) -> bool:
        """Check quote syntax rule for each line"""
        lines = multiline_block.split("\n")
        return all(ln.startswith("> ") for ln in lines)

    def unordered_list_check(multiline_block: str) -> bool:
        """Check unordered list syntax rule for each line"""
        lines = multiline_block.split("\n")
        return all(ln.startswith("- ") for ln in lines)

    def ordered_list_check(multiline_block: str) -> bool:
        """Check ordered list syntax rule for each line"""
        lines = multiline_block.split("\n")
        return all(ln.startswith(f"{num}. ") for num, ln in enumerate(lines, start=1))

    # ruleset withevery markdown syntax rule
    # lambdas are used due to efficiency, not elegance
    markdown_syntax_ruleset = [
        (lambda s: s.startswith("# "), BlockType.HEADING),
        (lambda s: s.startswith("## "), BlockType.HEADING),
        (lambda s: s.startswith("### "), BlockType.HEADING),
        (lambda s: s.startswith("#### "), BlockType.HEADING),
        (lambda s: s.startswith("##### "), BlockType.HEADING),
        (lambda s: s.startswith("###### "), BlockType.HEADING),
        (code_block_check, BlockType.CODE),
        (quote_check, BlockType.QUOTE),
        (unordered_list_check, BlockType.UNO_LIST),
        (ordered_list_check, BlockType.ORD_LIST),
    ]

    for syntax_rule, block_type in markdown_syntax_ruleset:
        if syntax_rule(markdown_block):
            return block_type

    return BlockType.PARAGRAPH


class BlockType(Enum):
    """Enum class representing different types of markdown blocks."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNO_LIST = "unordered_list"
    ORD_LIST = "ordered_list"
