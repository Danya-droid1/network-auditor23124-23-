# -*- coding: utf-8 -*-
"""
Окно результатов сканирования в виде таблицы.
Принимает реальные данные от сканера и отображает их
с цветовой индикацией уровней риска.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QHeaderView, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# Импорт экспортёра отчётов
from src.core.export import ReportExporter


class ResultsWindow(QWidget):
    """
    Окно отображения результатов сканирования.
    Показывает таблицу с реальными данными об открытых портах.
    """

    def __init__(self):
        """Инициализация окна результатов."""
        super().__init__()
        # Хранилище текущих результатов
        self.current_results = []
        # Экспортёр отчётов
        self.exporter = ReportExporter()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header_label = QLabel("Результаты сканирования")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #e6e6f0;")
        layout.addWidget(header_label)

        # Информационная метка
        self.info_label = QLabel("Запустите сканирование, чтобы увидеть результаты")
        self.info_label.setStyleSheet("font-size: 13px; color: #a0a0b0; margin-bottom: 10px;")
        layout.addWidget(self.info_label)

        # Таблица результатов с 5 колонками
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "IP-адрес", "Порт", "Сервис", "Уровень риска", "Время обнаружения"
        ])

        # Растягиваем последнюю колонку
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        # Включаем чередование цвета строк
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        # Кнопки экспорта отчётов
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_export_docx = QPushButton("📄 Экспорт в DOCX")
        self.btn_export_xlsx = QPushButton("📊 Экспорт в XLSX")

        # Стили для кнопок (яркие акцентные цвета)
        self.btn_export_docx.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 10px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3498db; }
        """)
        self.btn_export_xlsx.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)

        # Подключаем обработчики экспорта
        self.btn_export_docx.clicked.connect(self.export_docx)
        self.btn_export_xlsx.clicked.connect(self.export_xlsx)

        btn_layout.addWidget(self.btn_export_docx)
        btn_layout.addWidget(self.btn_export_xlsx)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_real_data(self, results: list):
        """
        Загрузка реальных результатов сканирования в таблицу.

        :param results: Список словарей с результатами сканирования
        """
        self.current_results = results

        # Обновляем информационную метку
        if results:
            self.info_label.setText(f"Найдено открытых портов: {len(results)}")
        else:
            self.info_label.setText("Открытых портов не обнаружено")

        # Очищаем таблицу
        self.table.setRowCount(0)

        # Заполняем таблицу реальными данными
        self.table.setRowCount(len(results))
        for row, data in enumerate(results):
            # IP-адрес
            ip_item = QTableWidgetItem(str(data.get('ip', 'N/A')))
            ip_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, ip_item)

            # Порт
            port_item = QTableWidgetItem(str(data.get('port', 'N/A')))
            port_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, port_item)

            # Сервис
            service_item = QTableWidgetItem(str(data.get('service', 'Неизвестно')))
            service_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, service_item)

            # Уровень риска (определяем по порту)
            risk = self.get_risk_level(data.get('port', 0))
            risk_item = QTableWidgetItem(risk)
            risk_item.setTextAlignment(Qt.AlignCenter)

            # Цветовая индикация риска
            if risk == "Критический":
                risk_item.setBackground(QColor("#e74c3c"))  # Красный
                risk_item.setForeground(QColor("white"))
            elif risk == "Высокий":
                risk_item.setBackground(QColor("#e67e22"))  # Оранжевый
                risk_item.setForeground(QColor("white"))
            elif risk == "Средний":
                risk_item.setBackground(QColor("#f39c12"))  # Жёлто-оранжевый
                risk_item.setForeground(QColor("black"))
            else:
                risk_item.setBackground(QColor("#27ae60"))  # Зелёный
                risk_item.setForeground(QColor("white"))

            self.table.setItem(row, 3, risk_item)

            # Время обнаружения
            time_item = QTableWidgetItem(str(data.get('detected_at', 'N/A')))
            time_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, time_item)

    def get_risk_level(self, port: int) -> str:
        """
        Определение уровня риска по номеру порта.
        Основано на типичных уязвимостях сервисов.

        :param port: Номер порта
        :return: Уровень риска (Критический/Высокий/Средний/Низкий)
        """
        # Критические порты — устаревшие протоколы без шифрования
        if port in [23]:  # Telnet
            return "Критический"
        # Высокий риск — уязвимые к шифровальщикам и утечкам
        if port in [21, 445, 5432, 3306]:  # FTP, SMB, PostgreSQL, MySQL
            return "Высокий"
        # Средний риск — требуют усиленной аутентификации
        if port in [22, 3389, 8080]:  # SSH, RDP, HTTP-Alt
            return "Средний"
        # Низкий риск — стандартные веб-порты
        if port in [80, 443]:  # HTTP, HTTPS
            return "Низкий"
        return "Средний"

    def export_docx(self):
        """Экспорт результатов в формат DOCX."""
        if not self.current_results:
            QMessageBox.warning(self, "Нет данных", "Сначала выполните сканирование")
            return

        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            try:
                # Подготавливаем данные с уровнем риска
                data_with_risk = []
                for item in self.current_results:
                    item_copy = item.copy()
                    item_copy['risk'] = self.get_risk_level(item.get('port', 0))
                    data_with_risk.append(item_copy)

                filepath = self.exporter.export_to_docx(data_with_risk)
                QMessageBox.information(
                    self, "Успех",
                    f"DOCX-отчёт успешно сохранён:\n{filepath}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт:\n{str(e)}")

    def export_xlsx(self):
        """Экспорт результатов в формат XLSX."""
        if not self.current_results:
            QMessageBox.warning(self, "Нет данных", "Сначала выполните сканирование")
            return

        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            try:
                # Подготавливаем данные с уровнем риска
                data_with_risk = []
                for item in self.current_results:
                    item_copy = item.copy()
                    item_copy['risk'] = self.get_risk_level(item.get('port', 0))
                    data_with_risk.append(item_copy)

                filepath = self.exporter.export_to_xlsx(data_with_risk)
                QMessageBox.information(
                    self, "Успех",
                    f"XLSX-отчёт успешно сохранён:\n{filepath}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт:\n{str(e)}")