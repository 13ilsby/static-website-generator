from textnode import *
from htmlnode import *
from split_delimiter import *
from markdown_blocks import *
import re

def markdown_to_html_node(markdown):
    filtered_blocks = markdown_to_blocks(markdown)

    htmlnodes_block_typed = []

    for f_block in filtered_blocks:
        htmlnodes_block_typed.append(HTMLnode_helper(f_block))

    top_parent = ParentNode("div", htmlnodes_block_typed)
    return top_parent


def HTMLnode_helper(block):
    if block_to_block_type(block) == "paragraph":
        return paragraph_helper(block)
    if block_to_block_type(block) == "heading":
        return heading_helper(block)
    if block_to_block_type(block) == "codeblock":
        return codeblock_helper(block)
    if block_to_block_type(block) == "quote":
        return quote_helper(block)
    if block_to_block_type(block) == "ordered_list":
        return olist_helper(block)
    if block_to_block_type(block) == "unordered_list":
        return ulist_helper(block)
    
def quote_helper(block):
    block_split = block.split("\n")
    block_rejoined = []
    child_nodes = []

    for section in block_split:
        if section == "":
            continue
        stripped_block = section.strip()
        stripped_block = stripped_block[2::]
        block_rejoined.append(stripped_block)
    block_rejoined = "\n".join(block_rejoined)

    text_nodes = text_to_textnodes(block_rejoined)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        child_nodes.append(html_node)
    
    parent = ParentNode("blockquote", child_nodes)
            
    return parent
    
def codeblock_helper(block):
    c_block = block.replace("```", "")
    sections = c_block.split("\n")
    child_nodes = []
    parent_code = []

    for section in sections:
        section = section.strip()
        if not section:
            continue
        section = "".join(section)

        text_nodes = text_to_textnodes(section)
        for node in text_nodes:
            html_node = text_node_to_html_node(node)
            child_nodes.append(html_node)

    parent_code = [ParentNode("code", child_nodes)]
    parent_node = ParentNode("pre", parent_code)
    return parent_node

def olist_helper(block):
    sections = block.split("\n")

    child_nodes = []
    parent_child_nodes = []

    for section in sections:
        section = section.strip()
        if not section:
            continue
        starting_numbers = "".join(re.findall(r"^\d+\. ", section))
        section = section.strip(starting_numbers)
    
        text_nodes = text_to_textnodes(section)
        for node in text_nodes:
            html_node = text_node_to_html_node(node)
            child_nodes.append(html_node)
        parent_child_nodes.append(ParentNode("li", child_nodes))
        child_nodes = []


    parent_node = ParentNode("ol", parent_child_nodes)
    return parent_node

def ulist_helper(block):
    split_sections = block.split("\n")

    child_nodes = []
    parent_child_nodes = []

    for section in split_sections:
        section = section.strip()
        if not section:
            continue

        section = section[2::]

        text_nodes = text_to_textnodes(section)
        for node in text_nodes:
            html_node = text_node_to_html_node(node)
            child_nodes.append(html_node)

        parent_child_nodes.append(ParentNode("li", child_nodes))

        child_nodes = []

    
    parent_node = ParentNode("ul", parent_child_nodes)
    return parent_node


def paragraph_helper(block):
    block_split = block.split("\n")
    block_rejoined = []
    child_nodes = []
    
    for section in block_split:
        if not section:
            continue
        stripped_block = section.strip()
        block_rejoined.append(stripped_block)

    joined_block = " ".join(block_rejoined)

    text_nodes = text_to_textnodes(joined_block)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        child_nodes.append(html_node)
    
    return ParentNode("p", child_nodes)


def heading_helper(block):
    child_nodes = []


    for i in range(0, 5):
        heading_count = block[0:6].count("#")
        clean_block = block[heading_count + 1::]
    heading_tag = f"h{heading_count}"
    if heading_count > 0:
        text_nodes = text_to_textnodes(clean_block)
        for node in text_nodes:
            if node == text_nodes[-1]:
                html_node = text_node_to_html_node(node)
                child_nodes.append(html_node)
            else:
                html_node = text_node_to_html_node(node)
                child_nodes.append(html_node)


        parent_node = ParentNode(heading_tag, child_nodes)
        return parent_node
    else:
        raise Exception("Invalid heading syntax")