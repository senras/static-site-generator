import tempfile
import unittest
from pathlib import Path

from main import copy_directory_contents, extract_title, generate_page


class CopyDirectoryContentsTests(unittest.TestCase):
    def test_copy_directory_contents_cleans_destination_and_recurses(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_dir = root / "static"
            destination_dir = root / "public"

            (source_dir / "images").mkdir(parents=True)
            (source_dir / "images" / "tolkien.png").write_bytes(b"png-data")
            (source_dir / "index.css").write_text("body {}", encoding="utf-8")

            destination_dir.mkdir(parents=True, exist_ok=True)
            (destination_dir / "old.txt").write_text("stale", encoding="utf-8")
            (destination_dir / "old-folder").mkdir()
            (destination_dir / "old-folder" / "nested.txt").write_text(
                "stale", encoding="utf-8"
            )

            copy_directory_contents(source_dir, destination_dir)

            self.assertTrue((destination_dir / "index.css").exists())
            self.assertTrue((destination_dir / "images" / "tolkien.png").exists())
            self.assertFalse((destination_dir / "old.txt").exists())
            self.assertFalse((destination_dir / "old-folder").exists())


class ExtractTitleTests(unittest.TestCase):
    def test_extract_title_returns_stripped_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_extract_title_raises_when_missing(self):
        with self.assertRaises(ValueError):
            extract_title("No title here")


class GeneratePageTests(unittest.TestCase):
    def test_generate_page_writes_html_using_template(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            markdown_path = root / "content" / "index.md"
            template_path = root / "template.html"
            destination_path = root / "public" / "index.html"

            markdown_path.parent.mkdir(parents=True)
            markdown_path.write_text("# Hello\n\nThis is text", encoding="utf-8")
            template_path.write_text(
                "<title>{{ Title }}</title><article>{{ Content }}</article>",
                encoding="utf-8",
            )

            generate_page(markdown_path, template_path, destination_path)

            self.assertTrue(destination_path.exists())
            html = destination_path.read_text(encoding="utf-8")
            self.assertIn("<title>Hello</title>", html)
            self.assertIn("<h1>Hello</h1>", html)
            self.assertIn("This is text", html)


if __name__ == "__main__":
    unittest.main()
