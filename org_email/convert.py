#!/bin/env python
from typing import List
from dataclasses import dataclass


@dataclass
class OrgLine(object):
    title_level: int
    status: str
    content: str


class Converter(object):
    lines: List[str] = []

    def __init__(self, lines: List[str]):
        self.lines = lines

    def convert(self) -> List[OrgLine]:
        org_lines: List[OrgLine] = []
        for line in self.lines:
            # ignore the content
            if not line.startswith("*"):
                continue

            segments = line.split(" ")
            title_level = self._get_title_level(segments[0])
            status, index = self._get_status(segments[1])
            content = " ".join(segments[index:])

            org_lines.append(OrgLine(title_level, status, content))

        return org_lines

    def _get_title_level(self, segment: str) -> int:
        return segment.count("*")

    def _get_status(self, segment: str) -> (str, int):
        if segment == "DONE":
            return "DONE", 2
        if segment == "TODO":
            return "TODO", 2
        return "", 1
