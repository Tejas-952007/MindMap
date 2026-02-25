"""utils/report_generator.py – PDF generation using fpdf2 with Unicode support"""
from fpdf import FPDF
import os
import re


def _clean_text(text: str) -> str:
    """Strip / replace characters that would break Latin-1 PDF encoding."""
    # Replace common Unicode dashes and special chars with ASCII equivalents
    replacements = {
        "\u2013": "-",   # en-dash
        "\u2014": "--",  # em-dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2022": "*",   # bullet
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u2192": "->",  # arrow
        "\u2764": "<3",  # heart
    }
    for uni, ascii_rep in replacements.items():
        text = text.replace(uni, ascii_rep)
    # Remove remaining non-latin-1 characters (emoji, Devanagari, etc.)
    text = text.encode("latin-1", errors="ignore").decode("latin-1")
    return text


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(79, 70, 229)
        self.cell(0, 10, "MindMap - Student Psychological Assessment",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(79, 70, 229)
        self.set_line_width(0.5)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10,
                  f"Page {self.page_no()} | Confidential - For self-reflection only, not a clinical diagnosis",
                  align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 238, 255)
        self.set_text_color(79, 70, 229)
        self.cell(0, 8, _clean_text(title), fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text: str):
        self.set_font("Helvetica", size=10)
        self.multi_cell(0, 6, _clean_text(text))
        self.ln(1)

    def info_row(self, label: str, value: str):
        """Two-column key: value row."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(60, 60, 120)
        self.cell(55, 6, _clean_text(label + ":"), new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", size=10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, _clean_text(value))

    def score_bar(self, label: str, value: float, max_val: float = 100):
        """Visual progress bar for a score."""
        pct = min(1.0, value / max_val)
        bar_width = 120
        filled = int(bar_width * pct)

        self.set_font("Helvetica", size=9)
        self.set_text_color(60, 60, 60)
        self.cell(55, 6, _clean_text(label))

        x, y = self.get_x(), self.get_y()
        # Background bar
        self.set_fill_color(220, 220, 240)
        self.rect(x, y + 1.5, bar_width, 3.5, "F")
        # Filled bar
        if pct < 0.4:
            self.set_fill_color(240, 70, 90)
        elif pct < 0.65:
            self.set_fill_color(245, 158, 11)
        else:
            self.set_fill_color(16, 185, 129)
        self.rect(x, y + 1.5, filled, 3.5, "F")

        self.set_xy(x + bar_width + 4, y)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "B", 9)
        self.cell(20, 6, f"{value:.0f}/{max_val:.0f}", new_x="LMARGIN", new_y="NEXT")


def generate_pdf(report_text: str, filename: str = "/tmp/student_report.pdf") -> str:
    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # Split by section markers (───...)
    section_sep = re.compile(r"─{5,}")
    sections = section_sep.split(report_text)

    for section in sections:
        lines = [l.strip() for l in section.strip().splitlines() if l.strip()]
        if not lines:
            continue
        title_candidate = lines[0]
        if title_candidate.isupper() and len(title_candidate) < 65:
            pdf.section_title(title_candidate)
            lines = lines[1:]
        for line in lines:
            pdf.body_text(line)
        pdf.ln(2)

    pdf.output(filename)
    return filename
