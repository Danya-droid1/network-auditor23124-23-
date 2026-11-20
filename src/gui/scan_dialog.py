# -*- coding: utf-8 -*-
"""
Диалоговое окно настройки сканирования.
Позволяет ввести IP-диапазон, выбрать набор портов и таймаут.
Валидирует введённые данные перед запуском сканирования.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6 для диалогового окна
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox, QMessageBox, QSpinBox)
from PySide6.QtCore import Qt


class ScanDialog(QDialog):
    """
    Диалог настройки нового сканирования сети.
    Возвращает параметры сканирования после нажатия кнопки "Начать".
    """

    def __init__(self, parent=None):
        """Инициализация диалога настройки сканирования."""
        super().__init__(parent)
        self.setWindowTitle("Настройка сканирования сети")
        self.resize(400, 250)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса диалога."""
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Поле ввода IP-диапазона
        layout.addWidget(QLabel("Целевой диапазон IP (например, 192.168.1.0/24):"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.0/24")
        layout.addWidget(self.ip_input)

        # Выбор профиля портов
        layout.addWidget(QLabel("Выбор портов:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems([
            "Стандартные порты (21, 22, 80, 443, 445, 3389)",
            "Все распространённые порты (1-1024)",
            "Произвольный список"
        ])
        layout.addWidget(self.port_combo)

        # Настройка таймаута
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Таймаут (секунды):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)

        layout.addStretch()

        # Кнопки действий
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Начать сканирование")
        self.btn_start.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        self.btn_cancel = QPushButton("Отмена")

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Подключаем обработчики кнопок
        self.btn_start.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

    def validate_and_accept(self):
        """
        Валидация введённых данных перед закрытием диалога.
        Проверяет, что IP-диапазон не пустой.
        """
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "Ошибка валидации", "Диапазон IP не может быть пустым.")
            return
        # Если всё ок - принимаем диалог
        self.accept()

    def get_scan_params(self) -> dict:
        """
        Получение параметров сканирования из полей диалога.

        :return: Словарь с параметрами сканирования
        """
        return {
            "ip_range": self.ip_input.text().strip(),
            "port_profile": self.port_combo.currentText(),
            "timeout": self.timeout_spin.value()
        }