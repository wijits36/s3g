import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # HTMLNode Tests
    def test_htmlnode_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "intro"})
        self.assertEqual(repr(node), "HTMLNode(p, Hello, None, {'class': 'intro'})")

    def test_htmlnode_eq(self):
        node = HTMLNode("p", "Hello")
        node2 = HTMLNode("p", "Hello")
        self.assertEqual(node, node2)

    def test_htmlnode_eq_false(self):
        node = HTMLNode("p", "Hello")
        node2 = HTMLNode("a", "Hello")
        self.assertNotEqual(node, node2)

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_props(self):
        node = HTMLNode("p", "Hello", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a", "click me", None, {"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://example.com" target="_blank"'
        )

    # LeafNode Tests
    def test_leafnode_repr(self):
        node = LeafNode("p", "Hello", {"class": "intro"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, {'class': 'intro'})")

    def test_leafnode_eq(self):
        node = LeafNode("p", "Hello")
        node2 = LeafNode("p", "Hello")
        self.assertEqual(node, node2)

    def test_leafnode_eq_false(self):
        node = LeafNode("p", "Hello")
        node2 = LeafNode("a", "Hello")
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "click me", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">click me</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    # ParentNode Tests
    def test_parentnode_repr(self):
        node = ParentNode("div", [LeafNode("p", "Hello")], {"class": "intro"})
        self.assertEqual(
            repr(node),
            "ParentNode(div, [LeafNode(p, Hello, None)], {'class': 'intro'})",
        )

    def test_parentnode_eq(self):
        node = ParentNode("div", [LeafNode("p", "Hello")], {"class": "intro"})
        node2 = ParentNode("div", [LeafNode("p", "Hello")], {"class": "intro"})
        self.assertEqual(node, node2)

    def test_parentnode_eq_false(self):
        node = ParentNode("div", [LeafNode("p", "Hello")], {"class": "intro"})
        node2 = ParentNode("div", [LeafNode("a", "Hello")], {"class": "intro"})
        self.assertNotEqual(node, node2)

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

    def test_to_html_with_missing_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("p", "Hello")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_props(self):
        parent_node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(parent_node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_with_props(self):
        parent_node = ParentNode("div", [LeafNode("p", "Hello")], {"class": "intro"})
        self.assertEqual(parent_node.to_html(), '<div class="intro"><p>Hello</p></div>')

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>"
        )

    def test_to_html_with_nested_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>"
        )

    def test_to_html_with_nested_parent(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>"
        )

    def test_to_html_with_nested_parent_and_props(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2], {"class": "intro"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="intro"><span>child1</span><span>child2</span></div>',
        )

    def test_to_html_with_nested_parent_and_children_props(self):
        child_node1 = LeafNode("span", "child1", {"class": "child1"})
        child_node2 = LeafNode("span", "child2", {"class": "child2"})
        parent_node = ParentNode("div", [child_node1, child_node2], {"class": "intro"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="intro"><span class="child1">child1</span><span class="child2">child2</span></div>',
        )


if __name__ == "__main__":
    unittest.main()
