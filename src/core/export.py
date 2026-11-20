# -*- coding: utf-8 -*-
"""
Модуль экспорта отчётов в форматы DOCX и XLSX.
Использует библиотеки python-docx и openpyxl
для генерации регламентированной документации.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля os для работы с файловой системой
import os

# Импорт модуля datetime для генерации имён файлов
from datetime import datetime

# Импорт компонентов библиотеки python-docx для работы с Word-документами
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Импорт компонентов библиотеки openpyxl для работы с Excel-файлами
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill


class ReportExporter:
    """
    Класс для экспорта результатов сканирования в форматы документов.
    Поддерживает генерацию отчётов в форматах DOCX и XLSX.
    """

    def __init__(self, output_dir: str = "reports"):
        """
        Инициализация экспортера отчётов.

        :param output_dir: Директория для сохранения отчётов
        """
        self.output_dir = output_dir
        # Создаём директорию, если она не существует
        os.makedirs(self.output_dir, exist_ok=True)

    def export_to_docx(self, scan_data: list, filename: str = None) -> str:
        """
        Генерация отчёта в формате DOCX (Word).

        :param scan_data: Список результатов сканирования
        :param filename: Имя файла (если None, генерируется автоматически)
        :return: Путь к созданному файлу
        """
        # Генерируем имя файла, если оно не указано
        if not filename:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = os.path.join(self.output_dir, filename)

        # Создаём новый документ Word
        doc = Document()
        # Добавляем заголовок документа
        doc.add_heading('Отчёт по аудиту сетевой безопасности', 0)
        # Добавляем дату генерации
        doc.add_paragraph(f'Дата создания: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        # Создаём таблицу с 4 колонками
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        # Заполняем заголовки таблицы
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'IP-адрес'
        hdr_cells[1].text = 'Порт'
        hdr_cells[2].text = 'Сервис'
        hdr_cells[3].text = 'Уровень риска'

        # Делаем заголовки жирными
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True

        # Заполняем таблицу данными из результатов сканирования
        for item in scan_data:
            row_cells = table.add_row().cells
            row_cells[0].text = str(item.get('ip', 'N/A'))
            row_cells[1].text = str(item.get('port', 'N/A'))
            row_cells[2].text = str(item.get('service', 'Неизвестно'))
            row_cells[3].text = str(item.get('risk', 'Неизвестно'))

        # Сохраняем документ
        doc.save(filepath)
        return filepath

    def export_to_xlsx(self, scan_data: list, filename: str = None) -> str:
        """
        Генерация отчёта в формате XLSX (Excel).

        :param scan_data: Список результатов сканирования
        :param filename: Имя файла (если None, генерируется автоматически)
        :return: Путь к созданному файлу
        """
        # Генерируем имя файла, если оно не указано
        if not filename:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.output_dir, filename)

        # Создаём новую Excel-книгу
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Результаты сканирования"

        # Добавляем заголовки колонок
        headers = ['IP-адрес', 'Порт', 'Сервис', 'Уровень риска', 'Время обнаружения']
        ws.append(headers)

        # Стилизуем заголовки (жирный шрифт, серый фон, центрирование)
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")

        # Заполняем таблицу данными
        for item in scan_data:
            ws.append([
                item.get('ip', 'N/A'),
                item.get('port', 'N/A'),
                item.get('service', 'Неизвестно'),
                item.get('risk', 'Неизвестно'),
                item.get('detected_at', 'N/A')
            ])

        # Сохраняем книгу
        wb.save(filepath)
        return filepath