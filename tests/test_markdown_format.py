"""Markdown convention: one paragraph or list item per line, never hard-wrapped.

Known limit: a line that starts with `<` is treated as an HTML block and is not checked.
Indented code blocks, setext heading underlines, thematic breaks, and link reference
definitions are not paragraph text and are skipped.
"""

import os
import re
import subprocess
import unittest

from fixtures import ROOT

LIST_ITEM = re.compile(r"([-*+]|\d+[.)])\s")
OPAQUE = re.compile(r"(#|\||<|```|~~~)|([-*_])(\s*\2){2,}$|(=+|-+)$|\[[^\]]+\]:\s")
QUOTE = re.compile(r"^\s*>\s?")


def wrapped_lines(text):
    """Line numbers where a paragraph, list item, or quote continues on a plain next line."""
    found, fence, comment, prev, in_list = [], False, False, None, False
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
        body = QUOTE.sub("", line, count=1)
        stripped = body.strip()
        if stripped and not body.startswith((" ", "	")) and not LIST_ITEM.match(stripped):
            in_list = False
        if LIST_ITEM.match(stripped):
            in_list = True
        if prev is None and not in_list and body.startswith(("    ", "	")):
            continue
        starts_block = bool(LIST_ITEM.match(stripped)) or bool(OPAQUE.match(stripped))
        if stripped and not starts_block and prev == quoted:
            found.append(number)
        if stripped and not OPAQUE.match(stripped) and not line.endswith(("  ", "\\")):
            prev = quoted
        else:
            prev = None
    return found


def tracked_markdown():
    """Tracked `.md` files; outside a git checkout, every `.md` file not under a dot-directory."""
    try:
        return subprocess.check_output(["git", "ls-files", "*.md"], cwd=ROOT, text=True).split()
    except (OSError, subprocess.CalledProcessError):
        found = []
        for folder, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            found += [os.path.relpath(os.path.join(folder, f), ROOT) for f in files if f.endswith(".md")]
        return found


class MarkdownFormatTest(unittest.TestCase):
    def test_detector_flags_wrapped_paragraph_list_item_and_quote(self):
        self.assertEqual(wrapped_lines("a b\nc d\n"), [2])
        self.assertEqual(wrapped_lines("- a b\n  c d\n"), [2])
        self.assertEqual(wrapped_lines("> a b\n> c d\n"), [2])
        self.assertEqual(wrapped_lines("> a b\nc d\n"), [])
        self.assertEqual(wrapped_lines("- a\n\n  b\n  c\n"), [4])

    def test_detector_ignores_intentional_line_structure(self):
        self.assertEqual(wrapped_lines("a b  \nc d\n\n```\nx\ny\n```\n"), [])
        self.assertEqual(wrapped_lines("---\nname: x\ndescription: y\n---\n\nbody\n"), [])
        self.assertEqual(wrapped_lines("{{!--\nline one\nline two\n--}}\n\nbody\n"), [])
        self.assertEqual(wrapped_lines("    code\n    more code\n"), [])
        self.assertEqual(wrapped_lines("Title\n=====\n\nSub\n---\n"), [])
        self.assertEqual(wrapped_lines("a\n\n* * *\n\nb\n"), [])
        self.assertEqual(wrapped_lines("[x]: http://a\n[y]: http://b\n"), [])
        self.assertEqual(wrapped_lines("- a\n\n  b c\n"), [])
        self.assertEqual(wrapped_lines("| a | b |\n| - | - |\n| c | d |\n"), [])

    def test_repository_markdown_is_not_hard_wrapped(self):
        for path in tracked_markdown():
            with open(f"{ROOT}/{path}", encoding="utf-8") as f:
                text = f.read().replace("\r\n", "\n")
            with self.subTest(file=path):
                self.assertEqual(wrapped_lines(text), [], "join wrapped lines into one line per paragraph or list item")


if __name__ == "__main__":
    unittest.main()
