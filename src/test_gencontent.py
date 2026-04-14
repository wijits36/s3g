import os
import tempfile
import unittest

from gencontent import extract_title, generate_page, generate_pages_recursive


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

    def test_generate_pages_recursive_creates_html_for_markdown_file(self):
        with (
            tempfile.TemporaryDirectory() as content_dir,
            tempfile.TemporaryDirectory() as dest_dir,
            tempfile.NamedTemporaryFile("w", delete=False) as template_file,
        ):
            template_file.write("<html><body>{{ Content }}</body></html>")
            template_file.close()

            md_path = os.path.join(content_dir, "index.md")
            with open(md_path, "w") as f:
                f.write("# Hello")

            generate_pages_recursive("/", content_dir, template_file.name, dest_dir)

            output_path = os.path.join(dest_dir, "index.html")
            self.assertTrue(os.path.exists(output_path))

    def test_generate_pages_recursive_preserves_nested_directory_structure(self):
        with (
            tempfile.TemporaryDirectory() as content_dir,
            tempfile.TemporaryDirectory() as dest_dir,
            tempfile.NamedTemporaryFile("w", delete=False) as template_file,
        ):
            template_file.write("<html><body>{{ Content }}</body></html>")
            template_file.close()

            nested_dir = os.path.join(content_dir, "blog", "post")
            os.makedirs(nested_dir)

            md_path = os.path.join(nested_dir, "index.md")
            with open(md_path, "w") as f:
                f.write("# Nested")

            generate_pages_recursive("/", content_dir, template_file.name, dest_dir)

            output_path = os.path.join(dest_dir, "blog", "post", "index.html")
            self.assertTrue(os.path.exists(output_path))

    def test_generate_pages_recursive_ignores_non_markdown_files(self):
        with (
            tempfile.TemporaryDirectory() as content_dir,
            tempfile.TemporaryDirectory() as dest_dir,
            tempfile.NamedTemporaryFile("w", delete=False) as template_file,
        ):
            template_file.write("<html><body>{{ Content }}</body></html>")
            template_file.close()

            txt_path = os.path.join(content_dir, "notes.txt")
            with open(txt_path, "w") as f:
                f.write("not markdown")

            generate_pages_recursive("/", content_dir, template_file.name, dest_dir)

            output_path = os.path.join(dest_dir, "notes.html")
            self.assertFalse(os.path.exists(output_path))

    def test_generate_pages_recursive_creates_parent_directories_for_output(self):
        with (
            tempfile.TemporaryDirectory() as content_dir,
            tempfile.TemporaryDirectory() as dest_dir,
            tempfile.NamedTemporaryFile("w", delete=False) as template_file,
        ):
            template_file.write("<html><body>{{ Content }}</body></html>")
            template_file.close()

            nested_dir = os.path.join(content_dir, "docs", "guide")
            os.makedirs(nested_dir)

            md_path = os.path.join(nested_dir, "index.md")
            with open(md_path, "w") as f:
                f.write("# Guide")

            generate_pages_recursive("/", content_dir, template_file.name, dest_dir)

            output_dir = os.path.join(dest_dir, "docs", "guide")
            self.assertTrue(os.path.exists(output_dir))

    def test_generate_pages_recursive_generates_multiple_pages_from_content_tree(self):
        with (
            tempfile.TemporaryDirectory() as content_dir,
            tempfile.TemporaryDirectory() as dest_dir,
            tempfile.NamedTemporaryFile("w", delete=False) as template_file,
        ):
            template_file.write("<html><body>{{ Content }}</body></html>")
            template_file.close()

            with open(os.path.join(content_dir, "index.md"), "w") as f:
                f.write("# Home")

            nested_dir = os.path.join(content_dir, "blog", "post")
            os.makedirs(nested_dir)

            with open(os.path.join(nested_dir, "index.md"), "w") as f:
                f.write("# Post")

            generate_pages_recursive("/", content_dir, template_file.name, dest_dir)

            self.assertTrue(os.path.exists(os.path.join(dest_dir, "index.html")))
            self.assertTrue(
                os.path.exists(os.path.join(dest_dir, "blog", "post", "index.html"))
            )

    def _make_temp_page(self, basepath):
        """Helper to generate a page with a given basepath and return the HTML."""
        template = """<html>
<head><title>{{ Title }}</title></head>
<body>
<a href="/about">About</a>
<img src="/images/photo.png">
{{ Content }}
</body>
</html>"""
        markdown = "# Test Page\n\nHello world"

        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "test.md")
            tpl_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "output.html")

            with open(md_path, "w") as f:
                f.write(markdown)
            with open(tpl_path, "w") as f:
                f.write(template)

            generate_page(basepath, md_path, tpl_path, dest_path)

            with open(dest_path, "r") as f:
                return f.read()

    def test_basepath_default(self):
        result = self._make_temp_page("/")
        self.assertIn('href="/about"', result)
        self.assertIn('src="/images/photo.png"', result)

    def test_basepath_custom(self):
        result = self._make_temp_page("/my-repo/")
        self.assertIn('href="/my-repo/about"', result)
        self.assertIn('src="/my-repo/images/photo.png"', result)
        self.assertNotIn('href="/about"', result)
