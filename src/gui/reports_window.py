# -*- coding: utf-8 -*-
"""
Окно истории отчётов.
Отображает список сгенерированных отчётов и позволяет их открыть.
Генерация отчётов происходит из окна "Результаты" после сканирования.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт модуля os для открытия файлов через ОС
import os
# Импорт subprocess для кроссплатформенного открытия файлов
import subprocess
import sys

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QHeaderView)
from PySide6.QtCore import Qt

# Импорт обёртки диалогов с русскими кнопками
from src.utils.dialogs import info, warning, critical


class ReportsWindow(QWidget):
    """
    Окно истории отчётов.
    Показывает список сгенерированных отчётов и позволяет открыть выбранный.
    """

    def __init__(self):
        """Инициализация окна отчётов."""
        super().__init__()
        # Хранилище путей к сгенерированным файлам
        self.report_files = []
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header = QLabel("История отчётов")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #e6e6f0; background: transparent;")
        layout.addWidget(header)

        # Информационная метка
        self.info_label = QLabel(
            "Отчётов пока нет — выполните сканирование и экспортируйте результаты из вкладки 'Результаты'")
        self.info_label.setStyleSheet("font-size: 13px; color: #a0a0b0; background: transparent;")
        layout.addWidget(self.info_label)

        # Таблица истории отчётов с 5 колонками
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Тип отчёта", "Автор", "Дата создания", "Путь к файлу"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)

        # Растягиваем последнюю колонку
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Оставляем только кнопку открытия выбранного отчёта
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.open_btn = QPushButton("📂 Открыть выбранный отчёт")
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; color: white; 
                padding: 10px 16px; border: none;
                border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #af7ac5; }
        """)
        self.open_btn.clicked.connect(self.open_selected)
        btn_layout.addWidget(self.open_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def add_report(self, report_type: str, filepath: str, author: str):
        """
        Добавление нового отчёта в историю.
        Вызывается из ResultsWindow после успешной генерации файла.

        :param report_type: Тип отчёта (DOCX/XLSX)
        :param filepath: Полный путь к файлу
        :param author: Логин автора отчёта
        """
        from datetime import datetime
        row = self.table.rowCount()
        self.table.insertRow(row)

        report_id = str(row + 1)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Заполняем ячейки
        self.table.setItem(row, 0, QTableWidgetItem(report_id))
        self.table.setItem(row, 1, QTableWidgetItem(report_type))
        self.table.setItem(row, 2, QTableWidgetItem(author))
        self.table.setItem(row, 3, QTableWidgetItem(date_str))
        self.table.setItem(row, 4, QTableWidgetItem(filepath))

        # Сохраняем путь в список
        self.report_files.append(filepath)

        # Обновляем информационную метку
        self.info_label.setText(f"Всего отчётов: {len(self.report_files)}")

    def open_selected(self):
        """
        Открытие выбранного отчёта в стандартной программе по умолчанию.
        На Windows использует os.startfile, на macOS — open, на Linux — xdg-open.
        """
        # Получаем выбранную строку
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            warning(self, "Файл не выбран",
                    "Пожалуйста, выберите отчёт в таблице для открытия.")
            return

        row = selected_rows[0].row()
        path_item = self.table.item(row, 4)

        if path_item is None:
            warning(self, "Ошибка", "Путь к файлу не определён.")
            return

        filepath = path_item.text()

        # Проверяем существование файла
        if not os.path.exists(filepath):
            critical(self, "Файл не найден",
                     f"Файл не существует по пути:\n{filepath}\n\n"
                     f"Возможно, он был перемещён или удалён.")
            return

        # Открываем файл в зависимости от ОС
        try:
            if sys.platform == 'win32':
                # Windows — открываем через ассоциацию файлов
                os.startfile(filepath)
            elif sys.platform == 'darwin':
                # macOS
                subprocess.call(['open', filepath])
            else:
                # Linux
                subprocess.call(['xdg-open', filepath])

            info(self, "Успех", f"Отчёт открыт:\n{filepath}")
        except Exception as e:
            critical(self, "Ошибка открытия",
                     f"Не удалось открыть файл:\n{str(e)}")