"""Markdown convention: one paragraph or list item per line, never hard-wrapped."""

import glob
import os
import re
import unittest

from fixtures import ROOT

BLOCK_START = re.compile(r"^\s*([-*+]|\d+[.)])\s|^\s*(#|\||>|<|```|~~~)|^\s*(-{3,}|\*{3,}|_{3,})\s*$")


def wrapped_lines(text):
    """Line numbers where a paragraph or list item continues on a plain next line."""
    found, fence, comment, prev = [], False, False, None
    lines = text.split("\n")
    front = lines[0] == "---" and "---" in lines[1:]
    for number, line in enumerate(lines, 1):
        if front:
            front = number == 1 or line != "---"
            continue
        stripped = line.strip()
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
            prev = None
            continue
        if fence:
            continue
        if stripped.startswith("{{!--"):
            comment = True
        if comment:
            comment = "--}}" not in stripped
            prev = None
            continue
        if not stripped or BLOCK_START.match(line):
            prev = None
        elif prev is not None:
            found.append(number)
        if stripped and not stripped.startswith(("---", "#", "|", "<")) and not line.endswith(("  ", "\\")):
            prev = number
        else:
            prev = None
    return found


class MarkdownFormatTest(unittest.TestCase):
    def test_detector_flags_wrapped_paragraph_and_list_item(self):
        self.assertEqual(wrapped_lines("a b\nc d\n"), [2])
        self.assertEqual(wrapped_lines("- a b\n  c d\n"), [2])
        self.assertEqual(wrapped_lines("a b  \nc d\n\n```\nx\ny\n```\n"), [])

    def test_repository_markdown_is_not_hard_wrapped(self):
        paths = glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
        for path in sorted(paths):
            if os.sep + "." in path[len(ROOT):]:
                continue
            with open(path, encoding="utf-8") as f:
                text = f.read().replace("\r\n", "\n")
            with self.subTest(file=os.path.relpath(path, ROOT)):
                self.assertEqual(wrapped_lines(text), [], "join wrapped lines into one line per paragraph or list item")


if __name__ == "__main__":
    unittest.main()
