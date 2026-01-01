import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        
    def test_leaf_image_to_html(self):
        node = LeafNode("img", "", props={"src": "http://example.com/image.png", "alt": "An image"})
        res = node.to_html()
        self.assertEqual(res, '<img src="http://example.com/image.png" alt="An image">')
        
    def test_parent_basic_to_html(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent = ParentNode("div", [child1, child2], props={"class": "content"})
        res = parent.to_html()
        self.assertEqual(res, '<div class="content"><p>Paragraph 1</p><p>Paragraph 2</p></div>')
        
    def test_parent_no_children_to_html(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            res = parent.to_html()
            
    def test_parent_no_tag_to_html(self):
        child = LeafNode("p", "A paragraph")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            res = parent.to_html()
    
    def test_parent_nested_to_html(self):
        child1 = LeafNode("span", "Nested text")
        child2 = ParentNode("div", [child1], props={"style": "color:red;"})
        parent = ParentNode("section", [child2])
        res = parent.to_html()
        self.assertEqual(res, '<section><div style="color:red;"><span>Nested text</span></div></section>')
        
    def test_parent_wide_to_html(self):
        child1 = LeafNode("h1", "Title")
        child2 = LeafNode("p", "This is a paragraph.")
        child3 = ParentNode("div", [LeafNode("a", "Link", props={"href": "http://example.com"})])
        parent = ParentNode("article", [child1, child2, child3], props={"class": "post"})
        res = parent.to_html()
        self.assertEqual(res, '<article class="post"><h1>Title</h1><p>This is a paragraph.</p><div><a href="http://example.com">Link</a></div></article>')
        
    def test_parent_deeply_nested_to_html(self):
        leaf = LeafNode("em", "Deep text")
        parent3 = ParentNode("span", [leaf])
        parent2 = ParentNode("div", [parent3])
        parent1 = ParentNode("section", [parent2])
        res = parent1.to_html()
        self.assertEqual(res, '<section><div><span><em>Deep text</em></span></div></section>')            
        
    def test_parent_multiple_props_to_html(self):
        child = LeafNode("p", "Content")
        parent = ParentNode("div", [child], props={"class": "box", "data-type": "example", "id": "unique"})
        res = parent.to_html()
        self.assertEqual(res, '<div class="box" data-type="example" id="unique"><p>Content</p></div>')
        
        
    def test_parent_empty_children_to_html(self):
        parent = ParentNode("div", [])
        res = parent.to_html()
        self.assertEqual(res, '<div></div>')
        
    def test_parent_empty_children_content_to_html(self):
        child1 = LeafNode("p", "")
        child2 = LeafNode("span", " ")
        parent = ParentNode("div", [child1, child2])
        res = parent.to_html()
        self.assertEqual(res, '<div><p></p><span> </span></div>')
        
    def test_parent_custom_tags_to_html(self):
        child1 = LeafNode("custom-tag", "Custom Content", props={"data-info": "123"})
        parent = ParentNode("wrapper", [child1], props={"role": "main"})
        res = parent.to_html()
        self.assertEqual(res, '<wrapper role="main"><custom-tag data-info="123">Custom Content</custom-tag></wrapper>')
        
if __name__ == "__main__":
    unittest.main()        