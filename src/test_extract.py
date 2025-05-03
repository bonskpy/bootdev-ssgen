import unittest

from constants import EXAMPLES_LINKS
from extract import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_image_from_cdn(self):
        matches = extract_markdown_images(
            "![Image from a CDN](https://cdn.example.net/image123.gif)"
        )
        self.assertListEqual(
            [("Image from a CDN", "https://cdn.example.net/image123.gif")], matches
        )

    def test_ftp_image(self):
        matches = extract_markdown_images(
            "![Alt text for external image](ftp://ftp.example.com/pub/image.bmp)"
        )
        self.assertListEqual(
            [("Alt text for external image", "ftp://ftp.example.com/pub/image.bmp")],
            matches,
        )

    # discarding title
    def test_image_with_title(self):
        matches = extract_markdown_images(
            '![Secure external image](https://secure.example.com/image.jpeg "Secure Image")'
        )
        self.assertListEqual(
            [("Secure external image", "https://secure.example.com/image.jpeg")],
            matches,
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_large_set(self):
        matches = extract_markdown_links(EXAMPLES_LINKS)
        expected_matches = [
            ("An example", "https://example.com"),
            ("Another link", "http://www.example.org/path"),
            ("FTP link", "ftp://user:password@example.net:21/file.txt"),
            ("Link with no protocol", "www.example.co.uk"),
            ("an inline link", "https://one.example/page"),
            ("Link with query parameters", "https://example.com/search?q=test&lang=en"),
            ("Link with anchor/fragment", "https://example.com/page#section-1"),
            (
                "Link with both query and fragment",
                "https://example.com/item?id=123#details",
            ),
            ("Link with spaces in text", "https://example.com/spaced%20url"),
            ("[Link text", "https://example.com"),
            ("Link text", "https://example.com"),
            (" Link text", "https://example.com"),
            ("Alt text", "https://image.example.com"),
            ("Code link", "https://code.example.com"),
        ]

        self.assertEqual(matches, expected_matches)
