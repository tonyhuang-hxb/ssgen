import unittest

# from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from splitnode import split_nodes_delimiter, split_nodes_image, split_nodes_link

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
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with no images at all.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with no images at all.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_images_only_images(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        
    def test_split_images_only_start(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png) followed by text.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" followed by text.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_images_only_end(self):
        node = TextNode(
            "Text before the image ![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("Text before the image ", TextType.PLAIN),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        
    def test_split_images_multiple_middle_only(self):
        node = TextNode(
            "Text before ![img1](http://example.com/img1.png) middle text ![img2](http://example.com/img2.png) text after.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.PLAIN),
                TextNode("img1", TextType.IMAGE, "http://example.com/img1.png"),
                TextNode(" middle text ", TextType.PLAIN),
                TextNode("img2", TextType.IMAGE, "http://example.com/img2.png"),
                TextNode(" text after.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_images_adjacent(self):
        node = TextNode(
            "Text with adjacent images ![img1](http://example.com/img1.png)![img2](http://example.com/img2.png) end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("Text with adjacent images ", TextType.PLAIN),
                TextNode("img1", TextType.IMAGE, "http://example.com/img1.png"),
                TextNode("img2", TextType.IMAGE, "http://example.com/img2.png"),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_images_empty_alt(self):
        node = TextNode(
            "Image with no alt text ![](http://example.com/img.png) end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("Image with no alt text ", TextType.PLAIN),
                TextNode("", TextType.IMAGE, "http://example.com/img.png"),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_images_empty_url(self):
        node = TextNode(
            "Image with no URL ![alt text]() end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("Image with no URL ", TextType.PLAIN),
                TextNode("alt text", TextType.IMAGE, ""),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_images_bad_url(self):
        node = TextNode(
            "Image with bad URL ![alt text](htp:/bad_url) end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("Image with bad URL ", TextType.PLAIN),
                TextNode("alt text", TextType.IMAGE, "htp:/bad_url"),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.PLAIN,
        )
    
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
        
    def test_split_links_no_link(self):
        node = TextNode(
            "This is text with no links at all.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with no links at all.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_links_only_links(self):
        node = TextNode(
            "[link1](https://example.com)[link2](https://example.org)",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode("link2", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
        
    def test_split_links_only_start(self):
        node = TextNode(
            "[link1](https://example.com) followed by text.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode(" followed by text.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_links_only_end(self):
        node = TextNode(
            "Text before the link [link2](https://example.org)",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("Text before the link ", TextType.PLAIN),
                TextNode("link2", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
         
    def test_split_links_multiple_middle_only(self):
        node = TextNode(
            "Text before [link1](http://example.com/link1) middle text [link2](http://example.com/link2) text after.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.PLAIN),
                TextNode("link1", TextType.LINK, "http://example.com/link1"),
                TextNode(" middle text ", TextType.PLAIN),
                TextNode("link2", TextType.LINK, "http://example.com/link2"),
                TextNode(" text after.", TextType.PLAIN),
            ],
            new_nodes,
        )   
        
    def test_split_links_adjacent(self):
        node = TextNode(
            "Text with adjacent links [link1](http://example.com/link1)[link2](http://example.com/link2) end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("Text with adjacent links ", TextType.PLAIN),
                TextNode("link1", TextType.LINK, "http://example.com/link1"),
                TextNode("link2", TextType.LINK, "http://example.com/link2"),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )
        
    def test_split_links_empty_text(self):
        node = TextNode(
            "Link with no text [](http://example.com/link) end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("Link with no text ", TextType.PLAIN),
                TextNode("", TextType.LINK, "http://example.com/link"),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        ) 

    def test_split_links_empty_url(self):
        node = TextNode(
            "Link with no URL [link text]() end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("Link with no URL ", TextType.PLAIN),
                TextNode("link text", TextType.LINK, ""),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )  
        
    def test_split_links_bad_url(self):
        node = TextNode(
            "Link with bad URL [link text](htp:/bad_url) end.",
            TextType.PLAIN,
        )
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("Link with bad URL ", TextType.PLAIN),
                TextNode("link text", TextType.LINK, "htp:/bad_url"),
                TextNode(" end.", TextType.PLAIN),
            ],
            new_nodes,
        )