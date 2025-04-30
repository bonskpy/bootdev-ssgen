import functools


class HTMLNode:
    """
    Represents a node in an HTML document tree, either block or inline.

    Attributes:
        tag (str): The HTML tag name (e.g., "p", "a", "h1").
        value (str): The value of the HTML tag (e.g., the text inside a paragraph).
        children (list[HTMLNode]): A list of HTMLNode objects representing the children of this node.
        props (dict): A dictionary of key-value pairs representing the attributes of the HTML tag.
                      For example: {"href": "https://www.google.com"}.
    """

    # annotating class as a forward reference 'ClassName'
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = [],
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag={self.tag},value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        """Child classes should override this method to render themselves as HTML"""
        raise NotImplementedError

    def props_to_html(self):
        return functools.reduce(
            lambda i, j: i + f' {j[0]}="{j[1]}"', self.props.items(), ""
        )
