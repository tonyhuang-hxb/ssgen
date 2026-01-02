from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from convertnode import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split plain-text nodes into alternating text segments based on a delimiter.

    This function iterates through a list of TextNode objects and processes only
    those whose `text_type` is `TextType.PLAIN`. For each such node, the text is
    split on the given delimiter. The resulting segments alternate between:

        - TextType.PLAIN
        - the provided `text_type`

    beginning with TextType.PLAIN.

    The delimiter is expected to appear an even number of times within a node.
    If it does not appear, or appears an odd number of times, the function raises
    a ValueError to signal invalid or unmatched Markdown-style formatting.

    Nodes that are not `TextType.PLAIN` are copied to the output unchanged.

    Args:
        old_nodes (List[TextNode]): 
            A list of TextNode objects to process.
        delimiter (str): 
            The delimiter marking text that should receive the new `text_type`
            (e.g., "*" for italics, "**" for bold).
        text_type (TextType): 
            The TextType to assign to the delimited text segments.

    Raises:
        ValueError: If `text_type` is LINK or IMAGE, as these types cannot be
            applied inline via delimiter formatting.
        ValueError: If the delimiter does not appear in a plain-text node.
        ValueError: If the delimiter appears an odd number of times, resulting
            in unmatched formatting markers.

    Returns:
        List[TextNode]: 
            A new list of TextNode objects with delimited segments converted
            to the specified `text_type`, and all other text preserved as
            `TextType.PLAIN`.
    """
    
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

def split_nodes_image(old_nodes):
    """
    Split plain-text nodes into text and image nodes based on Markdown image syntax.

    This function scans each node in the provided list. For any node whose
    `text_type` is `TextType.PLAIN`, it looks for Markdown image patterns of the form:

        ![alt text](image_url)

    Each match is replaced by a new `TextNode` of type `TextType.IMAGE`
    containing the image alt text and URL. Any surrounding plain text is preserved
    as separate `TextNode` objects of type `TextType.PLAIN`.

    Non-plain nodes are left untouched and copied directly to the result.

    Args:
        old_nodes (list[TextNode]):
            A list of TextNode objects to be processed.

    Returns:
        list[TextNode]:
            A new list of TextNode objects where Markdown image syntax in
            plain-text nodes has been converted into `TextType.IMAGE` nodes,
            with surrounding text preserved as `TextType.PLAIN` nodes.
    """
    
    new_nodes = []
    
    for node in old_nodes:

        # If the node is not TextType.PLAIN, just append it
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        all_images = extract_markdown_images(node.text)
        
        if len(all_images) == 0:
            # No more images, just append original TextNode if nonempty
            if node.text != "":
                new_nodes.append(node)
            break
        
        image_alt, image_link = all_images[0]
        splitted = node.text.split(f"![{image_alt}]({image_link})", 1)

        # Add TextNode only if non-empty as per spec
        if len(splitted[0]) != 0:
            new_nodes.append(TextNode(splitted[0], TextType.PLAIN))
            
        # Add image node
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))
        
        # Recursively repeat for remaining substring
        remaining = splitted[1]
        out = split_nodes_image([TextNode(remaining, TextType.PLAIN)])
        
        if len(out) > 0:
            new_nodes.extend(out)
                    
    return new_nodes
    
def split_nodes_link(old_nodes):
    """
    Split plain-text nodes into text and link nodes based on Markdown link syntax.

    This function scans each node in the provided list. For any node whose
    `text_type` is `TextType.PLAIN`, it looks for Markdown link patterns of the form:

        [link text](url)

    Each match is replaced by a new `TextNode` of type `TextType.LINK`
    containing the link text and URL. Any surrounding plain text is preserved
    as separate `TextNode` objects of type `TextType.PLAIN`.

    The function processes one link at a time recursively until all links in the
    node have been converted. Nodes that are not `TextType.PLAIN` are copied
    directly into the output list without modification.

    Args:
        old_nodes (List[TextNode]):
            A list of TextNode objects to be processed.

    Returns:
        List[TextNode]:
            A new list of TextNode objects where Markdown link syntax in
            plain-text nodes has been converted into `TextType.LINK` nodes,
            with surrounding text preserved as `TextType.PLAIN` nodes.
    """
    new_nodes = []
    
    for node in old_nodes:

        # If the node is not TextType.PLAIN, just append it
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        all_links = extract_markdown_links(node.text)
        
        if len(all_links) == 0:
            # No more images, just append original TextNode if nonempty
            if node.text != "":
                new_nodes.append(node)
            break
        
        link_text, link_url = all_links[0]
        splitted = node.text.split(f"[{link_text}]({link_url})", 1)

        # Add TextNode only if non-empty as per spec
        if len(splitted[0]) != 0:
            new_nodes.append(TextNode(splitted[0], TextType.PLAIN))
            
        # Add link node
        new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
        
        # Recursively repeat for remaining substring
        remaining = splitted[1]
        out = split_nodes_link([TextNode(remaining, TextType.PLAIN)])

        if len(out) > 0:
            new_nodes.extend(out)
                    
    return new_nodes