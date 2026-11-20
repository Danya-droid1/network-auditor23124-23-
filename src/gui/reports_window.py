# -*- coding: utf-8 -*-
"""
Окно генерации отчётов.
Содержит историю отчётов и кнопки создания новых отчётов в форматах DOCX/XLSX.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QFileDialog, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt


class ReportsWindow(QWidget):
    """
    Окно истории и генерации отчётов.
    Позволяет создавать новые отчёты в форматах DOCX и XLSX.
    """

    def __init__(self):
        """Инициализация окна отчётов."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header = QLabel("История отчётов")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header)

        # Таблица истории отчётов с 5 колонками
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Тип отчёта", "Автор", "Дата создания", "Путь к файлу"
        ])

        # Растягиваем последнюю колонку
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Кнопки генерации отчётов
        btn_layout = QHBoxLayout()

        self.generate_docx_btn = QPushButton("Создать DOCX-отчёт")
        self.generate_docx_btn.setStyleSheet("background-color: #2980b9; color: white; padding: 8px;")
        self.generate_docx_btn.clicked.connect(self.generate_docx)

        self.generate_xlsx_btn = QPushButton("Создать XLSX-отчёт")
        self.generate_xlsx_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        self.generate_xlsx_btn.clicked.connect(self.generate_xlsx)

        self.open_btn = QPushButton("Открыть выбранный")
        self.open_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")

        btn_layout.addWidget(self.generate_docx_btn)
        btn_layout.addWidget(self.generate_xlsx_btn)
        btn_layout.addWidget(self.open_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        # Загружаем демонстрационные данные
        self.load_dummy_data()

    def load_dummy_data(self):
        """Загрузка демонстрационных данных в таблицу истории."""
        # Пример истории отчётов
        sample = [
            ("1", "DOCX", "analyst", "2026-11-19 10:30", "C:/Reports/audit_20261119.docx"),
            ("2", "XLSX", "admin", "2026-11-18 14:15", "C:/Reports/audit_20261118.xlsx"),
        ]

        self.table.setRowCount(len(sample))
        for row, data in enumerate(sample):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def generate_docx(self):
        """
        Генерация отчёта в формате DOCX.
        Открывает диалог выбора папки для сохранения.
        """
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            # TODO: Вызвать метод export_to_docx из ReportExporter
            QMessageBox.information(self, "Успех", f"DOCX-отчёт сохранён в {folder}")

    def generate_xlsx(self):
        """
        Генерация отчёта в формате XLSX.
        Открывает диалог выбора папки для сохранения.
        """
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            # TODO: Вызвать метод export_to_xlsx из ReportExporter
            QMessageBox.information(self, "Успех", f"XLSX-отчёт сохранён в {folder}")