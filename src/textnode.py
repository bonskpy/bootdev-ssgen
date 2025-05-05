import re
from enum import Enum
from typing import Optional

import extract
import htmlnode


class TextType(Enum):
    """
    Enum representing different types of html inline text types.
    """

    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "image"


class TextNode:
    """
    Represents a node of text with a specific type and optional URL.

    Attributes:
        text (str): The content of the text node.
        text_type (TextType): The type of the text (e.g., normal, bold, italic).
        url (Optional[str]): An optional URL associated with the text node (e.g., for links or images).
    """

    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: callable) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text!r}, {self.text_type.value}, {self.url!r})"
        # used r! to escape possible special characters in the output


def text_node_to_html_node(text_node: TextNode) -> htmlnode.LeafNode:
    """This function converts TextNode to an LeafNode"""

    match text_node.text_type:
        case TextType.NORMAL:
            return htmlnode.LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return htmlnode.LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return htmlnode.LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return htmlnode.LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return htmlnode.LeafNode(tag="a", value=None, props={"href": text_node.url})
        case TextType.IMG:
            return htmlnode.LeafNode(
                tag="img",
                value=None,
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError("invalid text type")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Splits TextNode to a list of nodes separated with delimiter according to Markdown syntax
    Does not support nested delimiters
    ...

    """

    result = []

    for node in old_nodes:
        # if node is not normal/text add to result
        # there is no support for nested nodes at the moment
        if node.text_type != TextType.NORMAL:
            result.append(node)

        else:
            # check for matching number of markdown delimiters
            delimiter_count = node.text.count(delimiter)

            if delimiter_count % 2 != 0:
                raise Exception(
                    f"Delimtiers ( {delimiter} ) do not match, which indicates invalid markdown syntax."
                )
            # split text by delimiter
            node_splitted = node.text.split(delimiter, maxsplit=delimiter_count)

            for i in range(len(node_splitted)):
                # skip empty nodes
                if node_splitted[i] == "":
                    pass
                elif i % 2 != 0:
                    result.append(TextNode(node_splitted[i], text_type))
                else:
                    result.append(TextNode(node_splitted[i], node.text_type))

    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split each TextNode so that images are extracted to separate TextNode"""
    result = []
    img_pattern = re.compile(r"(!\[[^\[\]]*\]\([^\(\)]*\))")  # link pattern

    for node in old_nodes:
        # extraction should happen from TextType.NORMAL only
        # this might change later if nesting will be implemented
        if node.text_type != TextType.NORMAL:
            result.append(node)
        elif node.text_type == TextType.NORMAL:
            node_parts = img_pattern.split(node.text)

            for part in node_parts:
                # do not add an empty node to the result list
                if not part:
                    continue
                if img_pattern.match(part):
                    # extract markdown returns a list of tuples
                    anchor, url = extract.extract_markdown_images(part)[0]
                    result.append(TextNode(anchor, TextType.IMG, url))
                else:
                    result.append(TextNode(text=part, text_type=TextType.NORMAL))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split each TextNode so that links are extracted to separate TextNode"""
    result = []
    link_pattern = re.compile(r"(\[[^\]]+]\([^)]+\))")  # link pattern

    for node in old_nodes:
        # extraction should happen from TextType.NORMAL only
        # this might change later if nesting will be implemented
        if node.text_type != TextType.NORMAL:
            result.append(node)
        elif node.text_type == TextType.NORMAL:
            node_parts = link_pattern.split(node.text)

            for part in node_parts:
                # do not add an empty node to the result list
                if not part:
                    continue
                if link_pattern.match(part):
                    # extract markdown returns a list of tuples
                    label, url = extract.extract_markdown_links(part)[0]
                    result.append(TextNode(label, TextType.LINK, url))
                else:
                    result.append(TextNode(text=part, text_type=TextType.NORMAL))

    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts text to TextNodes which parse markdown syntax and prepare for HTML conversion

    param text: str: markdown string to be coverted to HTML
    return list[TextNode]: TextNode class used for markdown syntax parsing
    """
    # creating TextNode for syntax processing
    text_node = TextNode(text=text, text_type=TextType.NORMAL)
    # preparing delimiter config
    # config part might be moved later in order to make code more reusable and maintainable
    delimiter_config = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}

    processed_nodes = [text_node]
    for delimiter, text_type in delimiter_config.items():
        processed_nodes = split_nodes_delimiter(
            processed_nodes, delimiter=delimiter, text_type=text_type
        )

    processed_nodes = split_nodes_image(processed_nodes)
    processed_nodes = split_nodes_link(processed_nodes)

    return processed_nodes
