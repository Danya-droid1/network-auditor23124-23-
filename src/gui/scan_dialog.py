# -*- coding: utf-8 -*-
"""
Диалоговое окно настройки сканирования.
Позволяет ввести IP-диапазон, выбрать набор портов и таймаут.
Валидирует введённые данные перед запуском сканирования.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox, QSpinBox)
from PySide6.QtCore import Qt

# Импорт обёртки диалогов с русскими кнопками
from src.utils.dialogs import warning


class ScanDialog(QDialog):
    """
    Диалог настройки нового сканирования сети.
    """

    def __init__(self, parent=None):
        """Инициализация диалога настройки сканирования."""
        super().__init__(parent)
        self.setWindowTitle("Настройка сканирования сети")
        self.resize(450, 280)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса диалога."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Параметры сканирования")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a9eff; background: transparent;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Целевой диапазон IP (например, 192.168.1.0/24):"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.0/24")
        layout.addWidget(self.ip_input)

        layout.addWidget(QLabel("Выбор портов:"))
        self.port_combo = QComboBox()
        self.port_combo.addItems([
            "Стандартные порты (21, 22, 23, 80, 443, 445, 3389)",
            "Все распространённые порты (1-1024)",
            "Произвольный список"
        ])
        layout.addWidget(self.port_combo)

        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Таймаут (секунды):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("▶ Начать сканирование")
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.btn_cancel = QPushButton("✖ Отмена")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white; 
                padding: 10px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #95a5a6; }
        """)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_start.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

    def validate_and_accept(self):
        """
        Валидация введённых данных перед закрытием диалога.
        """
        ip = self.ip_input.text().strip()

        if not ip:
            warning(self, "Ошибка валидации", "Диапазон IP не может быть пустым.")
            return

        parts = ip.split('/')[0].split('.')
        if len(parts) != 4:
            warning(
                self, "Ошибка валидации",
                "Некорректный формат IP-диапазона.\nПример: 192.168.1.0/24"
            )
            return

        try:
            for part in parts:
                num = int(part)
                if not 0 <= num <= 255:
                    raise ValueError
        except ValueError:
            warning(
                self, "Ошибка валидации",
                "Каждая часть IP-адреса должна быть числом от 0 до 255."
            )
            return

        self.accept()

    def get_scan_params(self) -> dict:
        """
        Получение параметров сканирования из полей диалога.
        """
        return {
            "ip_range": self.ip_input.text().strip(),
            "port_profile": self.port_combo.currentText(),
            "timeout": self.timeout_spin.value()
        }