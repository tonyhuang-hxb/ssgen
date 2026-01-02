import unittest

# from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from splitnode import split_nodes_delimiter

class TestSplitNode(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        nodes = [
            TextNode("Hello, **world!** This is a test.", TextType.PLAIN),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
        expected_texts = [TextNode("Hello, ", TextType.PLAIN), 
                          TextNode("world!", TextType.BOLD), 
                          TextNode(" This is a test.", TextType.PLAIN)]
        
        
        self.assertEqual(split_nodes, expected_texts)
        
    def test_split_nodes_delimiter_no_closing(self):
        nodes = [
            TextNode("Hello, **world! This is a test.", TextType.PLAIN),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, text_type)
            
    def test_split_nodes_delimiter_missing_delimiter(self):
        nodes = [
            TextNode("Hello, world! This is a test.", TextType.PLAIN),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, text_type)
            
    def test_split_nodes_delimiter_non_plain(self):
        nodes = [
            TextNode("Hello, world!", TextType.BOLD),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
        self.assertEqual(split_nodes, nodes)
        
    def test_split_nodes_delimiter_multiple(self):
        nodes = [
            TextNode("This is **bold** and this is **also bold**.", TextType.PLAIN),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
        expected_texts = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.PLAIN),
            TextNode("also bold", TextType.BOLD),
            TextNode(".", TextType.PLAIN)
        ]
        
        self.assertEqual(split_nodes, expected_texts)
        
    def test_split_nodes_delimiter_adjacent(self):
        nodes = [
            TextNode("**Bold1****Bold2**", TextType.PLAIN),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
        # Keep empty text nodes after splitting
        expected_texts = [
            TextNode("", TextType.PLAIN),
            TextNode("Bold1", TextType.BOLD),
            TextNode("", TextType.PLAIN),
            TextNode("Bold2", TextType.BOLD),
            TextNode("", TextType.PLAIN),
        ]
        
        self.assertEqual(split_nodes, expected_texts)
        
    def test_split_nodes_delimiter_empty_between(self):
        nodes = [
            TextNode("This is **** empty bold.", TextType.PLAIN),
        ]
        
        delimiter = "**"
        text_type = TextType.BOLD
        
        split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
        expected_texts = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("", TextType.BOLD),
            TextNode(" empty bold.", TextType.PLAIN)
        ]
        
        self.assertEqual(split_nodes, expected_texts)
        
    def test_split_nodes_delimiter_type_italic(self):
        nodes = [
            TextNode("This is __italic__ text.", TextType.PLAIN),
        ]
        
        delimiter = "__"
        text_type = TextType.ITALIC
        
        split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
        expected_texts = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.PLAIN)
        ]
        
        self.assertEqual(split_nodes, expected_texts)
        
    def test_split_nodes_delimiter_type_link(self):
        nodes = [
            TextNode("[Click here](http://example.com) for more info.", TextType.PLAIN),
        ]
        
        delimiter = "["
        text_type = TextType.LINK
        
        # Links are not inline, so throw an error
        with self.assertRaises(ValueError):
            split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
            
    def test_split_nodes_delimiter_type_image(self):
        nodes = [
            TextNode("![Alt text](http://example.com/image.png) is an image.", TextType.PLAIN),
        ]
        
        delimiter = "!["
        text_type = TextType.IMAGE
        
        # Images are not inline, so throw an error
        with self.assertRaises(ValueError):
            split_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
    def test_split_nodes_delimiter_mixed_types(self):
        nodes = [
            TextNode("This is **bold** and __italic__ text.", TextType.PLAIN),
        ]
        
        delimiter_bold = "**"
        text_type_bold = TextType.BOLD
        
        split_nodes_bold = split_nodes_delimiter(nodes, delimiter_bold, text_type_bold)
        
        expected_texts_bold = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and __italic__ text.", TextType.PLAIN)
        ]
        
        self.assertEqual(split_nodes_bold, expected_texts_bold)
        
        # Now split the remaining plain text for italic
        split_nodes_italic = split_nodes_delimiter(
            [TextNode(" and __italic__ text.", TextType.PLAIN)],
            "__",
            TextType.ITALIC
        )
        
        expected_texts_italic = [
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.PLAIN)
        ]
        
        self.assertEqual(split_nodes_italic, expected_texts_italic)
        
    # TODO: Later implement nested delimiter handling    
    # def test_split_nodes_delimiter_mixed_nested(self):
    #     nodes = [
    #         TextNode("This is **bold and __italic__ inside bold** text.", TextType.PLAIN),
    #     ]
        
    #     delimiter_bold = "**"
    #     text_type_bold = TextType.BOLD
        
    #     # This should error for now since nested is not handled yet
    #     with self.assertRaises(ValueError):
    #         split_nodes_bold = split_nodes_delimiter(nodes, delimiter_bold, text_type_bold)
        
        