import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_node_to_html_node(text_node):
    if text_node.text is None:
        raise ValueError("TextNode requires text")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Unknown text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(
                f"Delimiter '{delimiter}' not found in text: {old_node.text}"
            )

        for i, text in enumerate(split_text):
            if text:
                new_nodes.append(
                    TextNode(text, TextType.TEXT if i % 2 == 0 else text_type)
                )

    return new_nodes


def extract_markdown_images(text):
    images = []

    for match in re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text):
        images.append((match.group(1), match.group(2)))

    return images


def extract_markdown_links(text):
    links = []

    for match in re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text):
        links.append((match.group(1), match.group(2)))

    return links


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for alt, url in images:
            split_text = text.split(f"![{alt}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for alt, url in links:
            split_text = text.split(f"[{alt}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if _is_heading(block):
        return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# helper function for block_to_block_type
def _is_heading(block):
    i = 0

    while i < len(block) and block[i] == "#":
        i += 1

    return 1 <= i <= 6 and i < len(block) and block[i] == " "


# helper function for block_to_block_type
def _is_ordered_list(lines):
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            return False

    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            html_nodes.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            html_nodes.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(ordered_list_to_html_node(block))
        else:
            html_nodes.append(paragraph_to_html_node(block))

    return ParentNode("div", html_nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    return [text_node_to_html_node(node) for node in text_nodes]


def heading_to_html_node(block):
    level = 0

    while block[level] == "#":
        level += 1

    return ParentNode(f"h{level}", text_to_children(block[level + 1 :]))


def code_to_html_node(block):
    text = block[4:-3]  # strip the ``` and newline from start, ``` from end
    lines = text.split("\n")
    stripped_lines = [line.strip() for line in lines]
    text = "\n".join(stripped_lines)
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(cleaned_lines)

    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []

    for line in lines:
        text = line[2:]  # strip the "- " prefix
        li_nodes.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []

    for line in lines:
        text = line.split(". ", 1)[1]  # strip the "1. " prefix
        li_nodes.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ol", li_nodes)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(line.strip() for line in lines)

    return ParentNode("p", text_to_children(paragraph))
