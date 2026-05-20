# Markdown Office Converter

本工具用于把 Markdown 文档转换成可编辑的 Word `.docx` 和 Excel `.xlsx` 文件。

脚本位置：

```powershell
tools\md_office_converter.py
```

## 基本用法

把一个 Markdown 同时转换成 Word 和 Excel：

```powershell
python tools\md_office_converter.py PRD-JQ-Tools-V2-Implementation-Aligned.md --to both --out converted
```

只导出 Word：

```powershell
python tools\md_office_converter.py PRD-JQ-Tools-V2-Implementation-Aligned.md --to docx
```

只导出 Excel：

```powershell
python tools\md_office_converter.py PRD-JQ-Tools-V2-Implementation-Aligned.md --to xlsx
```

指定输出文件：

```powershell
python tools\md_office_converter.py opt.md --to docx --out opt.docx
```

## 转换规则

Word `.docx`：

- Markdown 标题会转成 Word 标题样式。
- 普通段落会转成 Word 正文。
- Markdown 表格会转成 Word 表格。
- 列表会保留为缩进文本。
- 代码块会用等宽字体样式。

Excel `.xlsx`：

- `Outline` sheet 会保存整篇文档结构。
- 每个 Markdown 表格会自动拆成单独 sheet。
- sheet 名称优先取表格前最近的标题。

## 当前限制

- 不依赖第三方库，因此样式较轻量。
- Word 里的复杂 Markdown 样式不会完全还原。
- Excel 主要用于编辑表格和需求清单，不适合还原整篇排版。
- 图片暂不导出。

## 飞书内容转回 Markdown

如果在飞书里编辑完，再复制回 `.md`，表格通常会变成制表符文本，标题也不会自动带 `#`。可以先把飞书复制出来的内容粘到 `.txt`，再运行：

```powershell
python tools\feishu_to_md.py shroom\飞书粘贴内容.txt --out shroom\飞书转回Markdown.md
```

转换规则：

- 制表符分隔的连续行会转成 Markdown 表格。
- `1. 标题`、`1.1 标题` 会转成 Markdown 标题。
- 普通段落会保留为普通文本。
- 表格里的 `|` 会自动转义，避免破坏 Markdown 表格。
