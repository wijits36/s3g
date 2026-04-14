import unittest

from gencontent import extract_title


class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_with_leading_whitespace(self):
        markdown = "    # Title"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_not_first_line(self):
        markdown = "Paragraph\n    # Title"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_no_title(self):
        markdown = "Paragraph\n    ## Second Title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_ignores_h2(self):
        markdown = "## Second Title\n    # Title"
        self.assertEqual(extract_title(markdown), "Title")
