import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        self.assertEqual(
            repr(node),
            "TextNode(This is a text node, bold, https://www.example.com)",
        )

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://www.example.com"
        )
        self.assertEqual(node, node2)

    def test_eq_url_false(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://www.example.org"
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
