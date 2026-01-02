from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    for node in old_nodes:
        
        # If the node is not TextType.PLAIN, just append it
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        if text_type == TextType.LINK or text_type == TextType.IMAGE:
            raise ValueError("Cannot split nodes for LINK or IMAGE text types as they are not inline types.")
        
        # Else, if the MATCHING CLOSING delimiter is not found, raise an exception
        # for invalid Markdown syntax.
        if delimiter not in node.text:
            raise ValueError(f"Delimiter '{delimiter}' not found in text: {node.text}")
        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        else:
            # Split and then add nodes
            parts = node.text.split(delimiter)
            
            for i, part in enumerate(parts):
                # We keep empty strings, so first substring is always plain
                # With alternating parts being of custom type
                if (i + 1) % 2 == 0:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.PLAIN))
                    
    return new_nodes
