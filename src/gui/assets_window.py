# -*- coding: utf-8 -*-
"""
Окно реестра сетевых активов.
Отображает таблицу всех учтённых сетевых узлов с их характеристиками.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QHeaderView)
from PySide6.QtCore import Qt


class AssetsWindow(QWidget):
    """
    Окно реестра сетевых активов.
    Показывает список серверов, рабочих станций и другого оборудования.
    """

    def __init__(self):
        """Инициализация окна реестра активов."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header = QLabel("Реестр сетевых активов")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header)

        # Таблица активов с 6 колонками
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "IP-адрес", "Имя хоста", "Тип ОС", "Сегмент", "Последний скан"
        ])

        # Растягиваем последнюю колонку
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(5, QHeaderView.Stretch)

        layout.addWidget(self.table)

        # Кнопки управления
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить актив")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")

        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        # Загружаем демонстрационные данные
        self.load_dummy_data()

    def load_dummy_data(self):
        """Загрузка демонстрационных данных в таблицу активов."""
        # Пример сетевых активов
        sample = [
            ("1", "192.168.1.10", "srv-db-01", "Windows Server 2019", "Административный", "2026-11-19"),
            ("2", "192.168.1.15", "srv-file-01", "Windows Server 2016", "Административный", "2026-11-19"),
            ("3", "192.168.2.100", "ws-student-01", "Windows 10", "Учебный", "2026-11-18"),
            ("4", "10.0.1.5", "branch-srv-01", "Ubuntu 20.04", "Филиал", "2026-11-17"),
        ]

        self.table.setRowCount(len(sample))
        for row, data in enumerate(sample):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)