import re


def extract_markdown_images(text: str) -> list[tuple]:
    """Extracting url and alt text of images in markdown text"""

    img_match = re.findall(
        r"!\[([\w|\s]*)\]\(((?:ftp|http|https):\/\/[\w\-.\/]*\.(?:jpg|png|gif|jpeg|bmp|webp))\s*.*\)",
        text,
    )
    return img_match


def extract_markdown_links(text: str) -> list[tuple]:
    """Extracts anchor text and url from markdown formatted links"""

    link_match = re.findall(
        r"(?:\[(.+)\])\(((?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$]))\)",
        text,
        re.IGNORECASE,
    )
    return link_match
