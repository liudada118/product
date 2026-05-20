#!/usr/bin/env python
"""
Convert Markdown documents to editable Word .docx and Excel .xlsx files.

This script intentionally uses only the Python standard library so it can run
on a clean Windows machine without installing pip packages.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


MAX_EXCEL_CELL = 32767


@dataclass
class Block:
    kind: str
    text: str = ""
    level: int = 0
    rows: list[list[str]] = field(default_factory=list)
    ordered: bool = False
    language: str = ""


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_text(value: str) -> str:
    value = value.strip()
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r'<span[^>]*style=["\'][^"\']*color\s*:\s*#?d32f2f[^"\']*["\'][^>]*>\s*<strong>(.*?)</strong>\s*</span>', r"**\1**", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", value)
    value = html.unescape(value)
    return value


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if "|" not in stripped:
        return False
    stripped = stripped.strip("|").strip()
    if not stripped:
        return False
    cells = [c.strip() for c in stripped.split("|")]
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    reader = csv.reader([stripped], delimiter="|", quotechar='"', escapechar="\\")
    return [normalize_text(cell) for cell in next(reader)]


def parse_markdown(text: str) -> list[Block]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[Block] = []
    paragraph: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block(kind="paragraph", text=normalize_text(" ".join(paragraph))))
            paragraph = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        fence = re.match(r"^```([A-Za-z0-9_-]*)\s*$", stripped)
        if fence:
            flush_paragraph()
            if not in_code:
                in_code = True
                code_lang = fence.group(1)
                code_lines = []
            else:
                blocks.append(Block(kind="code", text="\n".join(code_lines), language=code_lang))
                in_code = False
                code_lang = ""
                code_lines = []
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            flush_paragraph()
            rows = [split_table_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            blocks.append(Block(kind="table", rows=rows))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", stripped)
        if heading:
            flush_paragraph()
            blocks.append(Block(kind="heading", level=len(heading.group(1)), text=normalize_text(heading.group(2))))
            i += 1
            continue

        quote = re.match(r"^>\s*(.+)$", stripped)
        if quote:
            flush_paragraph()
            blocks.append(Block(kind="quote", text=normalize_text(quote.group(1))))
            i += 1
            continue

        item = re.match(r"^\s*((?:[-*+])|(?:\d+[.)]))\s+(.+)$", line)
        if item:
            flush_paragraph()
            marker = item.group(1)
            blocks.append(Block(kind="list", text=normalize_text(item.group(2)), ordered=bool(re.match(r"\d", marker))))
            i += 1
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    if in_code:
        blocks.append(Block(kind="code", text="\n".join(code_lines), language=code_lang))
    return blocks


def inline_runs(markdown_text: str) -> list[tuple[str, bool]]:
    text = normalize_text(markdown_text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    runs: list[tuple[str, bool]] = []
    pos = 0
    pattern = re.compile(r"(\*\*|__)(.+?)\1")
    for match in pattern.finditer(text):
        if match.start() > pos:
            runs.append((text[pos : match.start()], False))
        runs.append((match.group(2), True))
        pos = match.end()
    if pos < len(text):
        runs.append((text[pos:], False))
    return [(chunk, bold) for chunk, bold in runs if chunk]


def docx_run(text: str, bold: bool = False) -> str:
    props = "<w:rPr><w:b/></w:rPr>" if bold else ""
    escaped = escape(text)
    preserve = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f"<w:r>{props}<w:t{preserve}>{escaped}</w:t></w:r>"


def docx_paragraph(text: str = "", style: str | None = None, bullet: bool = False, quote: bool = False) -> str:
    props: list[str] = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if bullet:
        props.append('<w:ind w:left="720" w:hanging="360"/>')
    if quote:
        props.append('<w:ind w:left="720"/><w:color w:val="666666"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
    runs = "".join(docx_run(part, bold) for part, bold in inline_runs(text))
    return f"<w:p>{ppr}{runs}</w:p>"


def docx_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    col_count = max(len(r) for r in rows)
    grid = "".join('<w:gridCol w:w="2400"/>' for _ in range(col_count))
    xml_rows = []
    for row in rows:
        cells = []
        for idx in range(col_count):
            value = row[idx] if idx < len(row) else ""
            cells.append(
                "<w:tc>"
                '<w:tcPr><w:tcW w:w="2400" w:type="dxa"/></w:tcPr>'
                f"{docx_paragraph(value)}"
                "</w:tc>"
            )
        xml_rows.append(f"<w:tr>{''.join(cells)}</w:tr>")
    return (
        "<w:tbl>"
        '<w:tblPr><w:tblW w:w="0" w:type="auto"/>'
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>{''.join(xml_rows)}</w:tbl>"
    )


def make_docx(blocks: list[Block], out_path: Path) -> None:
    body: list[str] = []
    for block in blocks:
        if block.kind == "heading":
            body.append(docx_paragraph(block.text, style=f"Heading{min(block.level, 6)}"))
        elif block.kind == "paragraph":
            body.append(docx_paragraph(block.text))
        elif block.kind == "quote":
            body.append(docx_paragraph(block.text, quote=True))
        elif block.kind == "list":
            prefix = "1. " if block.ordered else "- "
            body.append(docx_paragraph(prefix + block.text, bullet=True))
        elif block.kind == "code":
            body.append(docx_paragraph(block.text, style="Code"))
        elif block.kind == "table":
            body.append(docx_table(block.rows))

    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(body)}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading5"><w:name w:val="heading 5"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading6"><w:name w:val="heading 6"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
</w:styles>"""

    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document)
        zf.writestr("word/styles.xml", styles)


def excel_col_name(index: int) -> str:
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def xlsx_cell(row: int, col: int, value: str) -> str:
    value = normalize_text(str(value))[:MAX_EXCEL_CELL]
    ref = f"{excel_col_name(col)}{row}"
    if value == "":
        return f'<c r="{ref}"/>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'


def xlsx_sheet(rows: list[list[str]]) -> str:
    xml_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = "".join(xlsx_cell(r_idx, c_idx, value) for c_idx, value in enumerate(row, start=1))
        xml_rows.append(f'<row r="{r_idx}">{cells}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<sheetData>{''.join(xml_rows)}</sheetData>"
        "</worksheet>"
    )


def safe_sheet_name(name: str, used: set[str]) -> str:
    name = re.sub(r"[\[\]\:\*\?/\\]", "_", normalize_text(name)).strip() or "Sheet"
    name = name[:31]
    base = name
    suffix = 2
    while name in used:
        tail = f"_{suffix}"
        name = (base[: 31 - len(tail)] + tail)[:31]
        suffix += 1
    used.add(name)
    return name


def outline_rows(blocks: list[Block]) -> list[list[str]]:
    rows = [["Order", "Type", "Level", "Text"]]
    for idx, block in enumerate(blocks, start=1):
        if block.kind == "table":
            text = f"Table with {len(block.rows)} rows"
        else:
            text = block.text
        rows.append([str(idx), block.kind, str(block.level or ""), text])
    return rows


def make_xlsx(blocks: list[Block], out_path: Path) -> None:
    sheets: list[tuple[str, list[list[str]]]] = []
    used: set[str] = set()
    sheets.append((safe_sheet_name("Outline", used), outline_rows(blocks)))

    table_index = 1
    recent_heading = ""
    for block in blocks:
        if block.kind == "heading":
            recent_heading = block.text
        elif block.kind == "table":
            name = safe_sheet_name(recent_heading or f"Table {table_index}", used)
            sheets.append((name, block.rows))
            table_index += 1

    workbook_sheets = []
    workbook_rels = []
    content_overrides = []
    for idx, (name, _) in enumerate(sheets, start=1):
        workbook_sheets.append(f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>')
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        )
        content_overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{''.join(workbook_sheets)}</sheets></workbook>"
    )

    workbook_rel_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f"{''.join(workbook_rels)}</Relationships>"
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        f"{''.join(content_overrides)}</Types>"
    )

    rels = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rel_xml)
        for idx, (_, rows) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", xlsx_sheet(rows))


def output_paths(input_path: Path, out_arg: str | None, target: str) -> dict[str, Path]:
    if out_arg:
        out = Path(out_arg)
        if target == "both":
            if out.suffix:
                base = out.with_suffix("")
                return {"docx": base.with_suffix(".docx"), "xlsx": base.with_suffix(".xlsx")}
            out.mkdir(parents=True, exist_ok=True)
            return {"docx": out / f"{input_path.stem}.docx", "xlsx": out / f"{input_path.stem}.xlsx"}
        if out.suffix:
            return {target: out}
        out.mkdir(parents=True, exist_ok=True)
        return {target: out / f"{input_path.stem}.{target}"}

    if target == "both":
        return {"docx": input_path.with_suffix(".docx"), "xlsx": input_path.with_suffix(".xlsx")}
    return {target: input_path.with_suffix(f".{target}")}


def convert(input_path: Path, target: str, out_arg: str | None) -> list[Path]:
    text = read_text(input_path)
    blocks = parse_markdown(text)
    paths = output_paths(input_path, out_arg, target)
    written: list[Path] = []
    if "docx" in paths:
        paths["docx"].parent.mkdir(parents=True, exist_ok=True)
        make_docx(blocks, paths["docx"])
        written.append(paths["docx"])
    if "xlsx" in paths:
        paths["xlsx"].parent.mkdir(parents=True, exist_ok=True)
        make_xlsx(blocks, paths["xlsx"])
        written.append(paths["xlsx"])
    return written


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Markdown to Word .docx and Excel .xlsx.")
    parser.add_argument("input", help="Path to a Markdown file.")
    parser.add_argument("--to", choices=("docx", "xlsx", "both"), default="both", help="Output format.")
    parser.add_argument("--out", help="Output file or directory. Defaults next to the input file.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2
    if input_path.suffix.lower() not in {".md", ".markdown", ".txt"}:
        print(f"Warning: input extension is not Markdown-like: {input_path.suffix}", file=sys.stderr)
    written = convert(input_path, args.to, args.out)
    for path in written:
        print(path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
