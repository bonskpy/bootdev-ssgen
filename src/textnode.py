from enum import Enum
from typing import Optional


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
