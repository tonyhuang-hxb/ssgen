import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    
    def test_base_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode(tag="div")
            res = node.to_html()
            
    def test_props_to_html_simple(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        res = node.props_to_html()
        self.assertEqual(res, ' class="container" id="main"')
        
    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", props=None)
        res = node.props_to_html()
        self.assertEqual(res, "")
        
    def test_leaf_basic_to_html(self):
        node = LeafNode("p", "Hello, World!")
        res = node.to_html()
        self.assertEqual(res, "<p>Hello, World!</p>")
        
    def test_leaf_link_to_html(self):
        node = LeafNode("a", "Click here", props={"href": "http://example.com"})
        res = node.to_html()
        self.assertEqual(res, '<a href="http://example.com">Click here</a>')
    
    def test_leaf_no_tag_to_html(self):
        node = LeafNode(None, "Just some text")
        res = node.to_html()
        self.assertEqual(res, "Just some text")
        
        

if __name__ == "__main__":
    unittest.main()        