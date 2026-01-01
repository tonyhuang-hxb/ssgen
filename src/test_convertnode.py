import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from convertnode import convert_textnode_to_htmlnode


class TestConvertNode(unittest.TestCase):
    def test_simple_text_to_html_conversion(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = convert_textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold_text_to_html_conversion(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = convert_textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, "strong")
        self.assertEqual(html_node.value, "Bold text")
        
    def test_italic_text_to_html_conversion(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = convert_textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, "em")
        self.assertEqual(html_node.value, "Italic text")
        
    def test_link_text_to_html_conversion(self):
        node = TextNode("Click here", TextType.LINK, url="http://example.com")
        html_node = convert_textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "http://example.com"})
        
    def test_image_text_to_html_conversion(self):
        node = TextNode("An image", TextType.IMAGE, url="http://example.com/image.png")
        html_node = convert_textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "An image"})