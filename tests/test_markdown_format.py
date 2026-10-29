"""Markdown convention: one paragraph or list item per line, never hard-wrapped.

Known limit: a line that starts with `<` is treated as an HTML block and is not checked.
"""

import re
import subprocess
import unittest

from fixtures import ROOT

LIST_ITEM = re.compile(r"([-*+]|\d+[.)])\s")
OPAQUE = re.compile(r"(#|\||<|```|~~~)|(-{3,}|\*{3,}|_{3,})$")
QUOTE = re.compile(r"^\s*>\s?")


def wrapped_lines(text):
    """Line numbers where a paragraph, list item, or quote continues on a plain next line."""
    found, fence, comment, prev = [], False, False, None
    lines = text.split("\n")
    front = lines[0] == "---" and "---" in lines[1:]
    for number, line in enumerate(lines, 1):
        if front:
            front = number == 1 or line != "---"
            continue
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
            prev = None
            continue
        if fence:
            continue
        if line.strip().startswith("{{!--"):
            comment = True
        if comment:
            comment = "--}}" not in line
            prev = None
            continue
        quoted = bool(QUOTE.match(line))
        stripped = QUOTE.sub("", line, count=1).strip()
        starts_block = bool(LIST_ITEM.match(stripped)) or bool(OPAQUE.match(stripped))
        if stripped and not starts_block and prev == quoted:
            found.append(number)
        if stripped and not OPAQUE.match(stripped) and not line.endswith(("  ", "\\")):
            prev = quoted
        else:
            prev = None
    return found


def tracked_markdown():
    out = subprocess.check_output(["git", "ls-files", "*.md"], cwd=ROOT, text=True)
    return out.split()


class MarkdownFormatTest(unittest.TestCase):
    def test_detector_flags_wrapped_paragraph_list_item_and_quote(self):
        self.assertEqual(wrapped_lines("a b\nc d\n"), [2])
        self.assertEqual(wrapped_lines("- a b\n  c d\n"), [2])
        self.assertEqual(wrapped_lines("> a b\n> c d\n"), [2])
        self.assertEqual(wrapped_lines("> a b\nc d\n"), [])

    def test_detector_ignores_intentional_line_structure(self):
        self.assertEqual(wrapped_lines("a b  \nc d\n\n```\nx\ny\n```\n"), [])
        self.assertEqual(wrapped_lines("---\nname: x\ndescription: y\n---\n\nbody\n"), [])
        self.assertEqual(wrapped_lines("{{!--\nline one\nline two\n--}}\n\nbody\n"), [])
        self.assertEqual(wrapped_lines("| a | b |\n| - | - |\n| c | d |\n"), [])

    def test_repository_markdown_is_not_hard_wrapped(self):
        for path in tracked_markdown():
            with open(f"{ROOT}/{path}", encoding="utf-8") as f:
                text = f.read().replace("\r\n", "\n")
            with self.subTest(file=path):
                self.assertEqual(wrapped_lines(text), [], "join wrapped lines into one line per paragraph or list item")


if __name__ == "__main__":
    unittest.main()
