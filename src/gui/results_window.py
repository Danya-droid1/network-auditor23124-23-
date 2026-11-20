# -*- coding: utf-8 -*-
"""
Окно результатов сканирования в виде таблицы.
Цветовая индикация рисков: зелёный/жёлтый/красный.
Кнопки экспорта в DOCX и XLSX форматы.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton, QHeaderView)
from PySide6.QtCore import Qt


class ResultsWindow(QWidget):
    """
    Окно отображения результатов сканирования.
    Показывает таблицу с IP, портами, сервисами и уровнями риска.
    """

    def __init__(self):
        """Инициализация окна результатов."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header_label = QLabel("Результаты сканирования")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header_label)

        # Таблица результатов с 5 колонками
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "IP-адрес", "Порт", "Сервис", "Уровень риска", "Время обнаружения"
        ])

        # Растягиваем последнюю колонку на всё доступное пространство
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Кнопки экспорта отчётов
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_export_docx = QPushButton("Экспорт в DOCX")
        self.btn_export_xlsx = QPushButton("Экспорт в XLSX")

        # Стили для кнопок экспорта
        self.btn_export_docx.setStyleSheet("background-color: #2980b9; color: white; padding: 8px;")
        self.btn_export_xlsx.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")

        btn_layout.addWidget(self.btn_export_docx)
        btn_layout.addWidget(self.btn_export_xlsx)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Загружаем демонстрационные данные
        self.load_dummy_data()

    def load_dummy_data(self):
        """
        Загрузка демонстрационных данных в таблицу.
        В реальной системе данные берутся из базы PostgreSQL.
        """
        # Пример результатов сканирования
        sample_data = [
            ("192.168.1.10", "22", "SSH", "Средний", "2026-11-19 10:00:00"),
            ("192.168.1.10", "80", "HTTP", "Низкий", "2026-11-19 10:00:01"),
            ("192.168.1.15", "445", "SMB", "Высокий", "2026-11-19 10:00:05"),
        ]

        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)

                # Цветовая индикация уровня риска
                if col == 3:
                    if value == "Высокий":
                        # Красный фон для высокого риска
                        item.setBackground(Qt.red)
                        item.setForeground(Qt.white)
                    elif value == "Средний":
                        # Жёлтый фон для среднего риска
                        item.setBackground(Qt.yellow)

                self.table.setItem(row, col, item)