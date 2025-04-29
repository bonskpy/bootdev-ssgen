import textnode


def main():
    print("Hello from bootdev-ssgen!")
    new_node = textnode.TextNode(
        "A special sentence", textnode.TextType.LINK, "www.special.se"
    )
    print(new_node)


if __name__ == "__main__":
    main()
