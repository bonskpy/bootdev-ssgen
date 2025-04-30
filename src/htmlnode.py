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
        props: dict = None,  # maybe this should be an empty string?
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
        """
        Returns props as HTML formatted string.
        Example:
            input: {'class':'some-container-class'}
            output:  class="some-container-class"
        """
        return functools.reduce(
            lambda i, j: i + f' {j[0]}="{j[1]}"', self.props.items(), ""
        )


class LeafNode(HTMLNode):
    """This class represents a HTML node with no children"""

    def __init__(
        self,
        tag: str,
        value: str | None,
        props: dict = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self):
        """Renders a LeafNode as HTML string or raw string if tag is not present"""
        if not self.value:
            raise ValueError("LeafNode must have a value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"


# LeafNode("p", "This is a paragraph of text.").to_html()
# "<p>This is a paragraph of text.</p>"
