#!/usr/bin/env python3
"""
md2pdf.py — 一键将 Markdown 导出为 PDF（移动端友好）

用法:
    python3 scripts/md2pdf.py chapters/01-flash-sale-crash.md
    python3 scripts/md2pdf.py chapters/01-flash-sale-crash.md -o output.pdf
    python3 scripts/md2pdf.py --all

依赖:
    pip3 install fpdf2
"""

import sys
import os
import re
import argparse
from pathlib import Path

FPDF = None

# ── 自动安装依赖 ──────────────────────────────────
def ensure_fpdf2():
    global FPDF
    try:
        from fpdf import FPDF as _FPDF
        FPDF = _FPDF
        return
    except ImportError:
        print("[md2pdf] 安装依赖: fpdf2")
        import subprocess
        install_cmds = [
            [sys.executable, "-m", "pip", "install", "--quiet", "--user", "fpdf2"],
            [sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages", "fpdf2"],
            [sys.executable, "-m", "pip", "install", "--quiet", "--user", "--break-system-packages", "fpdf2"],
        ]
        for cmd in install_cmds:
            try:
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
                break
            except subprocess.CalledProcessError:
                continue
        else:
            print("[md2pdf] 错误: 自动安装 fpdf2 失败，请手动执行 `python3 -m pip install --user fpdf2`")
            sys.exit(1)
        from fpdf import FPDF as _FPDF
        FPDF = _FPDF
        print("[md2pdf] 完成")


# ── Markdown 解析器 ──────────────────────────────
class MDParser:
    """轻量 Markdown 解析，产出结构化 token 列表"""
    
    def __init__(self, text: str):
        self.lines = text.split("\n")
        self.pos = 0
        self.tokens = []

    @staticmethod
    def _is_table_separator(line: str) -> bool:
        return bool(re.match(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$", line.strip()))

    def _is_table_start(self, line: str) -> bool:
        if not (line.strip().startswith("|") and line.strip().endswith("|")):
            return False
        if self.pos + 1 >= len(self.lines):
            return False
        return self._is_table_separator(self.lines[self.pos + 1])

    @staticmethod
    def _needs_space_between(left: str, right: str) -> bool:
        # 仅在中英文/数字断行时补空格，避免中文段落出现不自然空隙
        return bool(re.match(r"[A-Za-z0-9]", left) and re.match(r"[A-Za-z0-9]", right))

    def _join_soft_wrapped_lines(self, lines: list) -> str:
        if not lines:
            return ""
        merged = lines[0].rstrip()
        for raw_line in lines[1:]:
            current = raw_line.strip()
            prev = merged.rstrip()
            if not prev:
                merged += current
                continue
            if self._needs_space_between(prev[-1], current[:1]):
                merged += " " + current
            else:
                merged += current
        return merged
    
    def parse(self):
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            
            # 空行
            if not line.strip():
                self.pos += 1
                continue
            
            # 代码块 ```
            if line.strip().startswith("```"):
                self._parse_code_block()
                continue
            
            # 标题
            if line.startswith("#"):
                self._parse_heading(line)
                self.pos += 1
                continue
            
            # 水平线
            if line.strip() in ("---", "***", "___"):
                self.tokens.append(("hr", ""))
                self.pos += 1
                continue
            
            # 引用 >
            if line.strip().startswith(">"):
                self._parse_blockquote()
                continue
            
            # 表格 |
            if self._is_table_start(line):
                self._parse_table()
                continue
            
            # 无序列表
            if re.match(r"^\s*[-*+]\s", line):
                self._parse_list()
                continue
            
            # 有序列表
            if re.match(r"^\s*\d+\.\s", line):
                self._parse_ordered_list()
                continue
            
            # 普通段落
            self._parse_paragraph()
        
        return self.tokens
    
    def _parse_code_block(self):
        lang = self.lines[self.pos].strip()[3:].strip()
        self.pos += 1
        code_lines = []
        while self.pos < len(self.lines):
            if self.lines[self.pos].strip().startswith("```"):
                self.pos += 1
                break
            code_lines.append(self.lines[self.pos])
            self.pos += 1
        self.tokens.append(("code", lang, "\n".join(code_lines)))
    
    def _parse_heading(self, line):
        level = 0
        for ch in line:
            if ch == "#":
                level += 1
            else:
                break
        text = line[level:].strip()
        self.tokens.append((f"h{level}", text))
    
    def _parse_blockquote(self):
        lines = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if line.strip().startswith(">"):
                content = re.sub(r"^>\s?", "", line.strip())
                lines.append(content)
                self.pos += 1
            elif not line.strip():
                self.pos += 1
                break
            else:
                break
        self.tokens.append(("blockquote", self._join_soft_wrapped_lines(lines)))
    
    def _parse_table(self):
        header = self.lines[self.pos]
        self.pos += 1
        
        # 跳过分隔行
        if self.pos < len(self.lines) and self._is_table_separator(self.lines[self.pos]):
            self.pos += 1
        
        rows = []
        rows.append([c.strip() for c in header.strip().strip("|").split("|")])
        
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if line.strip().startswith("|") and line.strip().endswith("|"):
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
                self.pos += 1
            else:
                break
        
        # 保持每行列数一致，避免渲染时错位
        col_count = max(1, len(rows[0]))
        normalized_rows = []
        for row in rows:
            if len(row) < col_count:
                row = row + [""] * (col_count - len(row))
            elif len(row) > col_count:
                row = row[:col_count]
            normalized_rows.append(row)

        self.tokens.append(("table", normalized_rows))
    
    def _parse_list(self):
        items = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            m = re.match(r"^\s*[-*+]\s+(.*)", line)
            if m:
                items.append(m.group(1))
                self.pos += 1
            elif not line.strip():
                self.pos += 1
                break
            else:
                break
        self.tokens.append(("ul", items))
    
    def _parse_ordered_list(self):
        items = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            m = re.match(r"^\s*\d+\.\s+(.*)", line)
            if m:
                items.append(m.group(1))
                self.pos += 1
            elif not line.strip():
                self.pos += 1
                break
            else:
                break
        self.tokens.append(("ol", items))
    
    def _parse_paragraph(self):
        lines = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if not line.strip():
                self.pos += 1
                break
            if line.startswith("#") or line.startswith("```") or \
               line.startswith(">") or re.match(r"^\s*[-*+]\s", line) or \
               re.match(r"^\s*\d+\.\s", line) or \
               self._is_table_start(line) or \
               line.strip() in ("---", "***", "___"):
                break
            lines.append(line)
            self.pos += 1
        if lines:
            self.tokens.append(("p", self._join_soft_wrapped_lines(lines)))


# ── 行内格式处理 ─────────────────────────────────
def inline_to_fpdf(pdf, text: str, font_size: int, bold: bool = False, 
                   left: float = None, max_w: float = None):
    """处理行内格式（**bold**, *italic*, `code`）并写到 PDF"""
    # 先用占位符替换代码片段，避免代码内的 ** 被误解析
    codes = []
    def save_code(m):
        codes.append(m.group(1))
        return f"\x00CODE{len(codes)-1}\x00"
    
    text = re.sub(r"`([^`]+?)`", save_code, text)
    
    parts = re.split(r"(\*\*.*?\*\*|\*.*?\*)", text)
    
    if left is None:
        left = pdf.get_x()
    if max_w is None:
        max_w = pdf.w - pdf.r_margin - left
    
    # 简单起见，用 write 方法逐段写
    for part in parts:
        if part.startswith("\x00CODE"):
            idx = int(part.split("\x00")[1].replace("CODE", ""))
            pdf.set_font("Courier", "", font_size - 1)
            if pdf.get_string_width(codes[idx]) > max_w:
                # 长代码换行
                pdf.set_font("", "", font_size)
            pdf.write(font_size, codes[idx])
        elif part.startswith("**") and part.endswith("**"):
            pdf.set_font("", "B", font_size)
            pdf.write(font_size, part[2:-2])
        elif part.startswith("*") and part.endswith("*"):
            pdf.set_font("", "I", font_size)
            pdf.write(font_size, part[1:-1])
        else:
            pdf.set_font("", "", font_size)
            pdf.write(font_size, part)


# ── PDF 生成器 ───────────────────────────────────
class MD2PDF:
    def __init__(self, font_path: str = None):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(True, 15)
        
        # 注册中文字体
        if font_path and os.path.exists(font_path):
            self.pdf.add_font("CJK", "", font_path)
            self.pdf.add_font("CJK", "B", font_path)
            self.body_font = "CJK"
        else:
            # 尝试找系统字体
            font = self._find_cjk_font()
            if font:
                self.pdf.add_font("CJK", "", font)
                self.pdf.add_font("CJK", "B", font)
                self.body_font = "CJK"
            else:
                print("[md2pdf] 警告: 未找到中文字体，将使用内置字体（中文可能显示为方块）")
                self.body_font = "Helvetica"
        
        self.pdf.add_page()
    
    def _find_cjk_font(self):
        """查找系统中可用的中文字体"""
        candidates = [
            # macOS
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Supplemental/PingFang.ttc",
            "/System/Library/Fonts/PingFang SC.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            # 常见备选
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        ]
        for path in candidates:
            if os.path.exists(path):
                print(f"[md2pdf] 使用字体: {path}")
                return path
        
        # 在 macOS 系统字体目录搜索
        import glob
        for pattern in ["/System/Library/Fonts/*.ttc", "/System/Library/Fonts/*.ttf",
                        "/Library/Fonts/*.ttc", "/Library/Fonts/*.ttf"]:
            for f in glob.glob(pattern):
                if any(kw in f.lower() for kw in ["ping", "hei", "song", "ming", "cjk", "noto"]):
                    print(f"[md2pdf] 使用字体: {f}")
                    return f
        
        return None
    
    def render(self, tokens: list, title: str = ""):
        p = self.pdf
        F = self.body_font
        L = p.l_margin
        W = p.w - p.l_margin - p.r_margin
        
        # 跟踪上一个 token 类型，用于上下文感知间距
        prev_type = None
        
        for i, token in enumerate(tokens):
            ttype = token[0]
            
            # ── 上下文间距：仅在不同类型块之间添加必要分隔 ──
            if prev_type and ttype != prev_type:
                if ttype in ("h1","h2","h3","h4"):
                    p.ln(2)  # 标题前统一 2mm
                elif prev_type in ("h1","h2","h3","h4") and ttype in ("p","blockquote","ul","ol","code","table"):
                    pass  # 标题后紧跟内容，不额外加空行
                elif prev_type == "p" and ttype == "p":
                    pass  # 连续段落紧凑排列
                elif ttype == "hr":
                    p.ln(1)
                else:
                    p.ln(1.5)
            
            # ── 渲染 ──
            if ttype == "h1":
                p.set_font(F, "B", 16)
                p.set_x(L)
                p.multi_cell(W, 8, token[1], align="L")
                p.line(L, p.get_y() + 0.5, L + W, p.get_y() + 0.5)
                p.ln(1.5)
            
            elif ttype == "h2":
                p.set_font(F, "B", 13)
                p.set_x(L)
                p.multi_cell(W, 6.5, token[1], align="L")
                p.ln(0.5)
            
            elif ttype == "h3":
                p.set_font(F, "B", 11.5)
                p.set_x(L)
                p.multi_cell(W, 6, token[1], align="L")
                p.ln(0.3)
            
            elif ttype == "h4":
                p.set_font(F, "B", 10.5)
                p.set_text_color(80, 80, 80)
                p.set_x(L)
                p.multi_cell(W, 5.5, token[1], align="L")
                p.set_text_color(0, 0, 0)
                p.ln(0.2)
            
            elif ttype == "p":
                p.set_font(F, "", 10)
                p.set_x(L)
                p.multi_cell(W, 5.5, token[1], align="L", wrapmode="CHAR")
                # Markdown 中空行分隔段落；这里保留明显的段间距
                ni = i + 1
                if ni < len(tokens) and tokens[ni][0] == "p":
                    p.ln(2.4)
            
            elif ttype == "blockquote":
                p.set_fill_color(248, 248, 248)
                p.set_text_color(100, 100, 100)
                p.set_font(F, "", 9)
                y0 = p.get_y()
                p.set_x(L + 2)
                p.multi_cell(W - 4, 5, token[1], align="L", fill=True, wrapmode="CHAR")
                p.set_draw_color(200, 200, 200)
                p.set_line_width(1)
                p.line(L, y0, L, p.get_y())
                p.set_draw_color(0, 0, 0)
                p.set_text_color(0, 0, 0)
            
            elif ttype == "code":
                _, code = token[1], token[2]
                p.set_fill_color(242, 242, 242)
                p.set_font(F, "", 7)
                p.set_text_color(70, 70, 70)
                for cline in code.split("\n"):
                    p.set_x(L + 2)
                    p.cell(W - 4, 3.8, cline[:95], fill=True)
                    p.ln()
                p.set_text_color(0, 0, 0)
                p.ln(0.5)
            
            elif ttype == "table":
                rows = token[1]
                col_w = W / len(rows[0])
                p.set_font(F, "", 8)
                for ri, row in enumerate(rows):
                    bg = (235, 235, 235) if ri == 0 else (250, 250, 250) if ri % 2 == 0 else (255, 255, 255)
                    p.set_fill_color(*bg)
                    for cell in row:
                        p.cell(col_w, 5.5, cell[:30], border=1, fill=True, align="L")
                    p.ln()
                p.ln(0.5)
            
            elif ttype == "ul":
                p.set_font(F, "", 10)
                for item in token[1]:
                    p.set_x(L + 4)
                    p.cell(3, 5, "•")
                    p.multi_cell(W - 7, 5, item, align="L", wrapmode="CHAR")
                p.ln(0.3)
            
            elif ttype == "ol":
                p.set_font(F, "", 10)
                for i, item in enumerate(token[1], 1):
                    p.set_x(L + 2)
                    p.cell(5, 5, f"{i}.")
                    p.multi_cell(W - 7, 5, item, align="L", wrapmode="CHAR")
                p.ln(0.3)
            
            elif ttype == "hr":
                p.ln(1)
                p.set_draw_color(210, 210, 210)
                p.set_line_width(0.3)
                p.line(L, p.get_y(), L + W, p.get_y())
                p.set_draw_color(0, 0, 0)
                p.set_line_width(0.2)
                p.ln(1)
            
            prev_type = ttype
    
    def save(self, path: str):
        self.pdf.output(path)


# ── 主流程 ──────────────────────────────────────
def convert_file(md_path: str, output_path: str = None, font_path: str = None):
    md_path = Path(md_path)
    if not md_path.exists():
        print(f"[md2pdf] 错误: 文件不存在 {md_path}")
        sys.exit(1)
    
    if output_path is None:
        output_path = md_path.with_suffix(".pdf")
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    # 提取标题
    title = md_path.stem
    for line in md_text.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    print(f"[md2pdf] 转换: {md_path.name} → {Path(output_path).name}")
    
    parser = MDParser(md_text)
    tokens = parser.parse()
    
    gen = MD2PDF(font_path)
    gen.render(tokens, title)
    gen.save(str(output_path))
    
    size_kb = Path(output_path).stat().st_size / 1024
    print(f"[md2pdf] ✅ 完成: {output_path} ({size_kb:.0f} KB)")


def convert_all(base_dir: str = "chapters", output_dir: str = "pdf_output"):
    base = Path(base_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    md_files = sorted(base.glob("*.md"))
    print(f"[md2pdf] 批量转换 {len(md_files)} 个文件...")
    for md_path in md_files:
        pdf_name = md_path.with_suffix(".pdf").name
        convert_file(str(md_path), str(out / pdf_name))


def main():
    parser = argparse.ArgumentParser(description="md2pdf — Markdown 一键导出 PDF")
    parser.add_argument("input", nargs="?", help="Markdown 文件路径")
    parser.add_argument("-o", "--output", help="输出 PDF 路径")
    parser.add_argument("--all", action="store_true", help="批量导出 chapters/ 下所有文件")
    parser.add_argument("--outdir", default="pdf_output", help="批量导出目录")
    parser.add_argument("--font", help="指定中文字体路径")
    
    args = parser.parse_args()
    ensure_fpdf2()
    
    if args.all:
        convert_all(output_dir=args.outdir)
    elif args.input:
        convert_file(args.input, args.output, args.font)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
