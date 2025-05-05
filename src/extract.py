import re


def extract_markdown_images(text: str) -> list:
    """Extracting url and alt text of images in markdown text"""

    img_match = re.findall(
        r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text,
    )
    return img_match


def extract_markdown_links(text: str) -> list:
    """Extracts anchor text and url from markdown formatted links"""

    link_match = re.findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text,
    )
    return link_match
