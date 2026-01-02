import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from convertnode import (convert_textnode_to_htmlnode, 
                        extract_markdown_images,
                        extract_markdown_links)


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
        
    def test_extract_markdown_image_basic(self):
        markdown_text = "Here is an image: ![Alt text](http://example.com/image.png)"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [("Alt text", "http://example.com/image.png")])
        
    def test_extract_markdown_image_multiple(self):
        markdown_text = "Image one: ![First](http://example.com/first.png) and Image two: ![Second](http://example.com/second.png)"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [("First", "http://example.com/first.png"), ("Second", "http://example.com/second.png")])

    def test_extract_markdown_image_none(self):
        markdown_text = "This text has no images."
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [])
        
    def test_extract_markdown_image_missing_bang(self):
        markdown_text = "This is not an image: [Alt text](http://example.com/image.png)"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [])
        
    def test_extract_markdown_image_missing_alt(self):
        markdown_text = "Image with no alt: ![](http://example.com/image.png)"
        images = extract_markdown_images(markdown_text)
        
        # Image can have no alt text but must have a URL
        self.assertEqual(images, [("", "http://example.com/image.png")])
        
    def test_extract_markdown_image_missing_url(self):
        markdown_text = "Image with no URL: ![Alt text]()"
        images = extract_markdown_images(markdown_text)
    
        # Image can have no alt text but must have a URL
        # Do not throw error as we are just extracing, the HTMLNode will handle validation
        self.assertEqual(images, [("Alt text", "")])
    
    def test_extract_markdown_image_bad_url(self):
        markdown_text = "Bad image format: ![Alt text](not a url)"
        images = extract_markdown_images(markdown_text)
        
        # Should still extract the alt text and URL as is
        self.assertEqual(images, [("Alt text", "not a url")])
        
    def test_extract_markdown_image_wrong_brackets(self):
        markdown_text = "Wrong brackets: !{Alt text}(http://example.com/image.png)"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [])
    
    def test_extract_markdown_image_wrong_brackets_2(self):
        markdown_text = "Wrong brackets: ![Alt text]{http://example.com/image.png}"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [])
        
    def test_extract_markdown_image_wrong_brackets_3(self):
        markdown_text = "Wrong brackets: !(Alt text)(http://example.com/image.png)"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [])
        
    def test_extract_markdown_link_basic(self):
        markdown_text = "Here is a link: [Link text](http://example.com)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [("Link text", "http://example.com")])
        
    def test_extract_markdown_link_multiple(self):
        markdown_text = "Link one: [First](http://example.com/first) and Link two: [Second](http://example.com/second)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [("First", "http://example.com/first"), ("Second", "http://example.com/second")])
        
    def test_extract_markdown_link_none(self):
        markdown_text = "This text has no links."
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [])
    
    def test_extract_markdown_missing_brackets(self):
        markdown_text = "Missing brackets: Link text(http://example.com)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [])
        
    def test_extract_markdown_link_missing_url(self):
        markdown_text = "Link with no URL: [Link text]()"
        links = extract_markdown_links(markdown_text)
        
        # Link can have no text but must have a URL
        # Do not throw error as we are just extracing, the HTMLNode will handle validation
        self.assertEqual(links, [("Link text", "")])
        
    def test_extract_markdown_link_wrong_brackets(self):
        markdown_text = "Wrong brackets: {Link text}(http://example.com)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [])
        
    def test_extract_markdown_link_wrong_brackets_2(self):
        markdown_text = "Wrong brackets: [Link text]{http://example.com}"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [])
        
    def test_extract_markdown_link_wrong_brackets_3(self):
        markdown_text = "Wrong brackets: (Link text)(http://example.com)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [])
        
    def test_extract_markdown_link_bad_url(self):
        markdown_text = "Bad link format: [Link text](not a url)"
        links = extract_markdown_links(markdown_text)
        
        # Should still extract the link text and URL as is
        self.assertEqual(links, [("Link text", "not a url")])
        
    def test_extract_markdown_link_missing_alt_text(self):
        markdown_text = "Link with no text: [](http://example.com)"
        links = extract_markdown_links(markdown_text)
        
        # Link can have no text but must have a URL
        self.assertEqual(links, [("", "http://example.com")])
        
        
    def test_extract_markdown_link_from_image(self):
        markdown_text = "This is an image link: ![Alt text](http://example.com/image.png)"
        links = extract_markdown_links(markdown_text)

        # Ignore image links
        self.assertEqual(links, [])
        
        