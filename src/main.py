from textnode import TextNode, TextType

if __name__ == "__main__":
    dummy_node = TextNode("Test Text Node", TextType.LINK, url="http://example.com")
    print(dummy_node)