EXAMPLES_IMGS = r"""
![A beautiful landscape](https://external.example.com/images/landscape.jpg)
![Website logo](http://another-site.org/logos/logo.png)
![Image from a CDN](https://cdn.example.net/image123.gif)
![Secure external image](https://secure.example.com/image.jpeg "Secure Image")
![External image with complex URL](https://subdomain.example.co.uk:8080/path/to/image?param1=value1&param2=value2)
![Alt text for external image](ftp://ftp.example.com/pub/image.bmp)
![External image with no extension](https://some-api.com/image/get/123)
![Relative alt text for external image](https://yet-another.example/../images/icon.png)
![External image with no extension](http://some-api.com/image/get/123)
![Relative alt text for external image](http://yet-another.example/../images/icon.png)

This is just plain text with no image.
A regular link: [Click here](https://example.com)
Just an exclamation mark: !
Just brackets and parentheses: ![]()
Missing link: ![Description]()
Missing description: ![](link.png)
Incomplete image syntax: ![Description]
Another incomplete image syntax: !(link.png)
Image syntax with extra brackets: ![Description](link.png))
Image syntax with extra parentheses: ![[Description](link.png)
Text resembling image syntax but with a space in the bang-bracket: ! [Description](link.png)
Text resembling image syntax but with a space in the bracket-parenthesis: ![Description] (link.png)
A link with an image inside (should capture the link, not the image): [![Inner image](inner.png)](https://inner-link.com)
An image in a code block: `![Code image](code.jpg)`
An image as part of a list item: - ![List image](list.png)
"""


EXAMPLES_LINKS = r"""
[An example](https://example.com)
[Another link](http://www.example.org/path)
[FTP link](ftp://user:password@example.net:21/file.txt)
[Link with no protocol](www.example.co.uk)
This line has [an inline link](https://one.example/page) in it."""
