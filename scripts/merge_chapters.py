#!/usr/bin/env python3
"""merge_chapters.py — 合并多个章节 .md 为一份临时 .md，去掉 H1 之后紧跟的写作元数据 blockquote。

用法:
    python3 scripts/merge_chapters.py chapters/00-prologue.md chapters/01-flash-sale-crash.md -o /tmp/book.md
"""
import argparse
import sys
from pathlib import Path


def strip_meta_blockquote(text: str) -> str:
    """跳过第一个 H1 (# ...) 之后紧跟的 blockquote 段（连续 `> ` 行 + 紧跟的水平线和空行）。"""
    lines = text.split("\n")
    out = []
    i = 0
    seen_h1 = False
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if not seen_h1 and line.startswith("# "):
            seen_h1 = True
            i += 1
            # 跳过 H1 之后的空行
            while i < len(lines) and not lines[i].strip():
                i += 1
            # 跳过紧跟的 blockquote 块（任意数量的 `> ` 行 + 中间空行）
            while i < len(lines) and (lines[i].startswith(">") or not lines[i].strip()):
                # 但若空行后不再是 `>`，停止
                if not lines[i].strip():
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j >= len(lines) or not lines[j].startswith(">"):
                        break
                i += 1
            # 跳过紧跟的水平线 + 空行
            while i < len(lines) and (lines[i].strip() in ("---", "***", "___") or not lines[i].strip()):
                i += 1
            # 留一个空行作为分隔
            out.append("")
            continue
        i += 1
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()

    chunks = []
    for p in args.inputs:
        path = Path(p)
        if not path.exists():
            print(f"[merge] 错误: {path} 不存在", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        chunks.append(strip_meta_blockquote(text))

    merged = "\n\n".join(chunks)
    Path(args.output).write_text(merged, encoding="utf-8")
    print(f"[merge] 合并 {len(args.inputs)} 个文件 → {args.output}（{len(merged)} 字）")


if __name__ == "__main__":
    main()
