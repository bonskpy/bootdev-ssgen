import unittest

from htmlnode import LeafNode
from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://different.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        expected_repr = "TextNode('This is a text node', bold, 'http://example.com')"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode('This is a text node', bold, None)"
        self.assertEqual(repr(node), expected_repr)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_img(self):
        node = TextNode("This is a img node", TextType.IMG, "images/image.png")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props, {"src": "images/image.png", "alt": "This is a img node"}
        )

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.pl")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "www.link.pl"})


class TestSplitNodesDelimiter(unittest.TestCase):
    def setUp(self):
        self.node_text_code = TextNode(
            "This is text with a `code block` word", TextType.NORMAL
        )
        self.node_text_code2 = TextNode(
            "This is text with another `code block` word", TextType.NORMAL
        )
        self.node_only_code = TextNode("print('This is a test code!')", TextType.CODE)
        self.node_text_bold = TextNode(
            "This is text with a **bold** word", TextType.NORMAL
        )

        self.node_text_bold2 = TextNode(
            "**This** is text with a bold word", TextType.NORMAL
        )

        self.node_text_bold3 = TextNode(
            "This is **text** with a **bold** word", TextType.NORMAL
        )

    def test_text_code_block(self):
        self.assertEqual(
            split_nodes_delimiter([self.node_text_code], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_text_bold_block(self):
        self.assertEqual(
            split_nodes_delimiter([self.node_text_bold], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_delimiter_as_first_char(self):
        self.node = TextNode("`This is text` with a code block word", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([self.node], "`", TextType.CODE),
            [
                TextNode("This is text", TextType.CODE),
                TextNode(" with a code block word", TextType.NORMAL),
            ],
        )

    def test_delimiter_as_last_char(self):
        self.node = TextNode("This is text `with a code block word`", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([self.node], "`", TextType.CODE),
            [
                TextNode("This is text ", TextType.NORMAL),
                TextNode("with a code block word", TextType.CODE),
            ],
        )

    def test_same_two_code_blocks(self):
        self.assertEqual(
            split_nodes_delimiter(
                [self.node_text_code, self.node_text_code2], "`", TextType.CODE
            ),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
                TextNode("This is text with another ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_different_bold_blocks(self):
        self.assertEqual(
            split_nodes_delimiter(
                [self.node_text_bold, self.node_text_bold2, self.node_text_bold3],
                "**",
                TextType.BOLD,
            ),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
                TextNode("This", TextType.BOLD),
                TextNode(" is text with a bold word", TextType.NORMAL),
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_non_text_block(self):
        self.assertEqual(
            split_nodes_delimiter([self.node_only_code], "`", TextType.CODE),
            [TextNode("print('This is a test code!')", TextType.CODE)],
        )

    def test_missing_delimiter(self):
        self.node_text_code.text = "This is a `bad syntax"
        with self.assertRaises(Exception):
            split_nodes_delimiter(self.node_text_code, "`", TextType.CODE)

    def test_additional__delimiter(self):
        self.node_text_code.text = "This is a `bad`` syntax"
        with self.assertRaises(Exception):
            split_nodes_delimiter(self.node_text_code, "`", TextType.CODE)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TextTextToMarkdown(unittest.TestCase):
    def test_all_types(self):
        markdown_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)."
        expected = [
            TextNode("This is ", TextType.NORMAL, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.NORMAL, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.NORMAL, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.NORMAL, None),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL, None),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(".", TextType.NORMAL, None),
        ]
        self.assertEqual(text_to_textnodes(markdown_text), expected)

    def test_white_space(self):
        markdown_text = " "
        expected = [TextNode(" ", TextType.NORMAL, None)]
        self.assertEqual(text_to_textnodes(markdown_text), expected)

    def test_empty_string(self):
        markdown_text = ""
        expected = []
        self.assertEqual(text_to_textnodes(markdown_text), expected)


if __name__ == "__main__":
    unittest.main()
