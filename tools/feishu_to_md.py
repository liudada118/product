#!/usr/bin/env python
"""
Convert text copied from Feishu docs back into Markdown.

Feishu often copies tables as tab-separated text, not Markdown tables. This
script turns those tab-separated blocks into Markdown tables and optionally
restores simple numbered headings such as "1. 文档说明" and "1.1 模块目标".
It only uses the Python standard library.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_cell(value: str) -> str:
    value = value.strip()
    value = value.replace("\u00a0", " ")
    value = value.replace("|", "\\|")
    value = re.sub(r"\s+", " ", value)
    return value


def split_tab_row(line: str) -> list[str]:
    return [normalize_cell(cell) for cell in line.rstrip("\n").split("\t")]


def looks_like_table_row(line: str) -> bool:
    if "\t" not in line:
        return False
    cells = split_tab_row(line)
    filled = [cell for cell in cells if cell]
    return len(cells) >= 2 and len(filled) >= 2


def markdown_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    col_count = max(len(row) for row in rows)
    normalized = []
    for row in rows:
        padded = row + [""] * (col_count - len(row))
        normalized.append([normalize_cell(cell) for cell in padded])

    header = normalized[0]
    body = normalized[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * col_count) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def heading_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""

    if stripped.startswith("#"):
        return stripped

    numbered = re.match(r"^(\d+(?:\.\d+){0,5})[.、]?\s+(.+)$", stripped)
    if numbered:
        number = numbered.group(1)
        title = numbered.group(2).strip()
        level = min(number.count(".") + 1, 6)
        return f"{'#' * level} {number} {title}"

    chinese_numbered = re.match(r"^([一二三四五六七八九十]+)[、.]\s*(.+)$", stripped)
    if chinese_numbered:
        return f"# {stripped}"

    return stripped


def convert_feishu_text(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    output: list[str] = []
    table_rows: list[list[str]] = []

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        if output and output[-1] != "":
            output.append("")
        output.extend(markdown_table(table_rows))
        output.append("")
        table_rows = []

    for raw_line in lines:
        line = raw_line.rstrip()
        if looks_like_table_row(line):
            table_rows.append(split_tab_row(line))
            continue

        flush_table()

        if not line.strip():
            if output and output[-1] != "":
                output.append("")
            continue

        output.append(heading_line(line))

    flush_table()

    while output and output[-1] == "":
        output.pop()
    return "\n".join(output) + "\n"


def default_out_path(input_path: Path) -> Path:
    stem = input_path.stem
    if stem.endswith("-飞书粘贴"):
        stem = stem[: -len("-飞书粘贴")]
    return input_path.with_name(f"{stem}-转换为Markdown.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Feishu copied text to Markdown.")
    parser.add_argument("input", type=Path, help="Text file pasted from Feishu.")
    parser.add_argument("--out", type=Path, help="Output Markdown file.")
    args = parser.parse_args()

    input_path = args.input
    out_path = args.out or default_out_path(input_path)

    text = read_text(input_path)
    markdown = convert_feishu_text(text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(out_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
