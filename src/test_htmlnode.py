import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def setUp(self):
        self.leaf_node = LeafNode(
            "a", "A child leaf link", {"href": "https://www.google.com"}
        )
        self.leaf_node_2 = LeafNode("p", "A child leaf paragraph")
        self.parent_node = ParentNode(
            "div", [self.leaf_node], {"class": "parent-node1"}
        )
        self.parent_node_2 = ParentNode(
            "div", [self.leaf_node, self.leaf_node_2], {"class": "multi-parent"}
        )
        self.parent_node_grand = ParentNode(
            "div", [self.parent_node_2], {"class": "grand-parent"}
        )

    def test_init(self):
        self.assertEqual(self.parent_node.tag, "div")
        self.assertEqual(self.parent_node.children, [self.leaf_node])
        self.assertEqual(self.parent_node.props, {"class": "parent-node1"})

    def test_repr(self):
        self.assertEqual(
            repr(self.parent_node),
            "ParentNode(tag=div, children=[LeafNode(tag=a, children=A child leaf link, props={'href': 'https://www.google.com'})], props={'class': 'parent-node1'})",
        )

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            self.parent_node.tag = ""
            self.parent_node.to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            self.parent_node.children = []
            self.parent_node.to_html()

    def test_to_html_two_children(self):
        self.assertEqual(
            self.parent_node_2.to_html(),
            '<div class="multi-parent"><a href="https://www.google.com">A child leaf link</a><p>A child leaf paragraph</p></div>',
        )

    def test_to_html_grand_parent(self):
        self.assertEqual(
            self.parent_node_grand.to_html(),
            '<div class="grand-parent"><div class="multi-parent"><a href="https://www.google.com">A child leaf link</a><p>A child leaf paragraph</p></div></div>',
        )

    def test_to_html_grand_modern_parent(self):
        """Test for handling mixed chindren: parent and leaf nodes"""

    # original boot.dev tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
