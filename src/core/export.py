"""
Report export module supporting DOCX and XLSX formats.

Author: Golub Daniil Nikolaevich
"""

import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill


class ReportExporter:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_to_docx(self, scan_data: list, filename: str = None) -> str:
        # Generate a DOCX report from scan results
        if not filename:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = os.path.join(self.output_dir, filename)

        doc = Document()
        doc.add_heading('Network Security Audit Report', 0)
        doc.add_paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'IP Address'
        hdr_cells[1].text = 'Port'
        hdr_cells[2].text = 'Service'
        hdr_cells[3].text = 'Risk Level'

        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True

        for item in scan_data:
            row_cells = table.add_row().cells
            row_cells[0].text = str(item.get('ip', 'N/A'))
            row_cells[1].text = str(item.get('port', 'N/A'))
            row_cells[2].text = str(item.get('service', 'Unknown'))
            row_cells[3].text = str(item.get('risk', 'Unknown'))

        doc.save(filepath)
        return filepath

    def export_to_xlsx(self, scan_data: list, filename: str = None) -> str:
        # Generate an XLSX report from scan results
        if not filename:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.output_dir, filename)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Scan Results"

        headers = ['IP Address', 'Port', 'Service', 'Risk Level', 'Timestamp']
        ws.append(headers)

        # Style headers
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")

        for item in scan_data:
            ws.append([
                item.get('ip', 'N/A'),
                item.get('port', 'N/A'),
                item.get('service', 'Unknown'),
                item.get('risk', 'Unknown'),
                item.get('detected_at', 'N/A')
            ])

        wb.save(filepath)
        return filepath