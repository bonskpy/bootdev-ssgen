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
[Link with a title](https://example.com "Title text")
[Another link](http://www.example.org/path)
[FTP link](ftp://user:password@example.net:21/file.txt)
[Link with no protocol](www.example.co.uk)
[Link in parentheses]( (https://sub.example.info) )
This line has [an inline link](https://one.example/page) in it.
Here's a reference link: [a reference][ref1]

[ref1]: https://reference.example.com
[Another reference link][ref2] with surrounding text.

[ref2]: http://anothersite.example/
[Link with query parameters](https://example.com/search?q=test&lang=en)
[Link with anchor/fragment](https://example.com/page#section-1)
[Link with both query and fragment](https://example.com/item?id=123#details)
[Link with special characters in text](http://pl.wikipedia.org/wiki/Prawo_Lewisa-Mogridge’a)
[Link with spaces in text](https://example.com/spaced%20url)
[Mailto link](mailto:test@example.com)
[Angle bracket link](<https://special.example.gov>)


This is just plain text with no link.
Just some brackets and parentheses: []()
Missing URL: [Link text]()
Missing link text: [](https://example.com)
Incomplete link syntax: [Link text]
Another incomplete link syntax: (https://example.com)
Link syntax with extra brackets: [[Link text](https://example.com)]
Link syntax with extra parentheses: ([Link text](https://example.com))
Text resembling link syntax but with a space in the bracket-parenthesis: [Link text] (https://example.com)
Text resembling link syntax but with a space in the opening bracket: [ Link text](https://example.com)
Text resembling link syntax but with a space in the closing parenthesis: [Link text](https://example.com )
An image: ![Image alt](image.jpg)
Image syntax that looks like a link: ![Alt text](https://image.example.com)
A reference link definition without a corresponding inline link: [ref3]: http://unused.example.com
Just a bracketed word: [word]
Just a parenthesized URL: (https://example.com)
A URL in plain text: https://justanurl.com
A file path: C:\Users\User\Documents\file.md
Relative path: ../another/page.html
Link in a code block: `[Code link](https://code.example.com)`
Link as part of image alt text: ![Link in alt [text](url)](image.png)"""
