import re

def block_to_block_type(block):
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "codeblock"
    block_type_quote = "quote"
    block_type_olist =  "ordered_list"
    block_type_ulist = "unordered_list"
    
    if block.startswith("#") and any(block[i:i+2] == ("# ") for i in range(0, 6)):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif block.startswith(">"):
        return block_type_quote
    elif block.startswith("* ") or block.startswith ("+ "):
        return block_type_ulist
    elif re.match(r"^\d+\. ", block):
        return block_type_olist
    else:
        return block_type_paragraph

def markdown_to_blocks(markdown):
    newline_split = markdown.split("\n\n")
    block_strings = []

    for line in newline_split:
        if line == "":
            continue
        line = line.strip()
        block_strings.append(line)

    return block_strings