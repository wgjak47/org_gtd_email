#!/bin/env python3

from yattag import Doc
from typing import List
from org_email.convert import OrgLine
from dataclasses import dataclass


color_map = {
    "TODO": "color:blue",
    "DONE": "color:green",
    "HOLD": "color:red",
}


@dataclass
class OrgTree(object):
    line: OrgLine
    children: List['OrgLine']

class Generator(object):
    lines: List[OrgLine]

    def __init__(self, lines: List[OrgLine]):
        self.lines = lines
        doc, tag, text, line = Doc().ttl()
        self.doc = doc
        self.tag = tag
        self.text = text
        self.line = line

    def generate(self) -> str:
        tree = OrgTree(self.lines[0], children=[])
        stack = [tree]

        for line in self.lines:
            node = OrgTree(line, [])
            if line.title_level > stack[-1].line.title_level:
                if len(stack) >= 1:
                    stack[-1].children.append(node)
                stack.append(node)
            elif line.title_level == stack[-1].line.title_level:
                stack[-1] = node
                if len(stack) >= 2:
                    stack[-2].children.append(node)
            elif line.title_level < stack[-1].line.title_level:
                stack[line.title_level-1] = node
                stack = stack[0:line.title_level]
                if len(stack) > line.title_level - 2:
                    stack[line.title_level-2].children.append(node)

        self.build_doc(stack[0])

        return self.doc.getvalue()

    def build_doc(self, tree):
        tag = self.tag
        text = self.text
        line = self.line

        if tree.line.title_level == 1:
            with tag("h2"):
                text(tree.line.content)

        if len(tree.children) != 0:
            with tag("ul", id=tree.line.content):
                for child in tree.children:
                    with tag("li"):
                        status = child.line.status
                        content = child.line.content
                        if status != "":
                            line(
                                "span",
                                status + "  ",
                                style=color_map.get(status, None)
                            )
                        text(content)
                        self.build_doc(child)
