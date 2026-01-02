import re

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
    
    
def extract_markdown_images(text):
    """Takes raw markdown text and returns a list of tuples. 
    Each tuple should contain the alt text and the URL of any markdown images. 
    
    Args:
        text (string): Raw markdown text containing image(s).

    Returns:
        List[Tuple]: Returns a list of tuples with (alt_text, url) for each image found.
    """
    
    results = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return results


def extract_markdown_links(text):
    """Takes raw markdown text and returns a list of tuples. 
    Each tuple should contain the link text and the URL of any markdown links. 
    
    Args:
        text (string): Raw markdown text containing link(s).
    Returns:
        List[Tuple]: Returns a list of tuples with (link_text, url) for each
        link found.
    """
    
    results = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return results