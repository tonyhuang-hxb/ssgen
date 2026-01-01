from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType

def convert_textnode_to_htmlnode(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be an instance of TextNode")
    
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(tag=None, value=text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="strong", value=text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="em", value=text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")