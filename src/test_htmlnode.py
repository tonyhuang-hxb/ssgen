import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_base_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode(tag="div")
            res = node.to_html()
            print(res)
            
    def test_props_to_html_simple(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        res = node.props_to_html()
        print(node)
        self.assertEqual(res, ' class="container" id="main"')
        
    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", props=None)
        res = node.props_to_html()
        self.assertEqual(res, "")
        
        
if __name__ == "__main__":
    unittest.main()        