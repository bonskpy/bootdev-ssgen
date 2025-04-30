# href="https://www.google.com" target="_blank"

import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def setUp(self):
        self.node = HTMLNode(
            tag="p", value="Some test string", props={"class": "container"}
        )
        self.node_empy = HTMLNode()
        self.node_children = HTMLNode(
            tag="div", children=[self.node_empy], props={"class": "container"}
        )

    def test_init(self):
        self.assertEqual(self.node.tag, "p")
        self.assertEqual(self.node.value, "Some test string")
        self.assertEqual(self.node.children, [])
        self.assertEqual(self.node.props, {"class": "container"})

    def test_repr(self):
        expected_repr = "HTMLNode(tag=p,value=Some test string, children=[], props={'class': 'container'})"
        expected_repr_empty_node = (
            "HTMLNode(tag=None,value=None, children=[], props=None)"
        )
        expected_repr_children = "HTMLNode(tag=div,value=None, children=[HTMLNode(tag=None,value=None, children=[], props=None)], props={'class': 'container'})"
        self.assertEqual(repr(self.node), expected_repr)
        self.assertEqual(repr(self.node_empy), expected_repr_empty_node)
        self.assertEqual(repr(self.node_children), expected_repr_children)

    def test_props_to_html(self):
        self.node.props.update({"id": "new-id"})
        # alterantive: 'href="https://www.google.com" target="_blank"'
        props = ' class="container" id="new-id"'
        self.assertEqual(self.node.props_to_html(), props)

    def test_to_html(self):
        self.assertRaises(NotImplementedError, self.node.to_html)


class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

    def test_init(self):
        self.assertEqual(self.leaf_node.tag, "a")
        self.assertEqual(self.leaf_node.value, "Click me!")
        self.assertEqual(self.leaf_node.children, [])
        self.assertEqual(self.leaf_node.props, {"href": "https://www.google.com"})

    def test_init_required_values(self):
        with self.assertRaises(TypeError):
            self.leaf_node_empty = LeafNode()

    def test_to_html(self):
        self.assertEqual(
            self.leaf_node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_no_tag(self):
        self.leaf_node.tag = None
        self.assertEqual(self.leaf_node.to_html(), "Click me!")

    def test_to_html_no_value(self):
        self.leaf_node.value = None
        with self.assertRaises(ValueError):
            self.leaf_node.to_html()


if __name__ == "__main__":
    unittest.main()
