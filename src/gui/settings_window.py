# -*- coding: utf-8 -*-
"""
Панель настроек приложения с 5 пунктами меню.
Позволяет настроить: таймаут сканирования, автосканирование,
периодичность, уведомления, путь для отчётов.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QCheckBox, QSpinBox,
                               QFileDialog, QMessageBox)
from PySide6.QtCore import Qt


class SettingsWindow(QWidget):
    """
    Окно настроек приложения.
    Содержит 5 пунктов конфигурации системы.
    """

    def __init__(self):
        """Инициализация окна настроек."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса настроек."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок окна
        header = QLabel("Настройки системы")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(header)

        # === Пункт 1: Таймаут сканирования ===
        layout.addWidget(QLabel("1. Таймаут сканирования (секунды):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        layout.addWidget(self.timeout_spin)

        # === Пункт 2: Автоматическое сканирование ===
        self.auto_scan_check = QCheckBox("2. Включить автоматическое сканирование по расписанию")
        layout.addWidget(self.auto_scan_check)

        # === Пункт 3: Периодичность автосканирования ===
        layout.addWidget(QLabel("3. Периодичность автосканирования (дни):"))
        self.period_spin = QSpinBox()
        self.period_spin.setRange(1, 30)
        self.period_spin.setValue(7)
        layout.addWidget(self.period_spin)

        # === Пункт 4: Уведомления ===
        self.notifications_check = QCheckBox("4. Включить уведомления о критических уязвимостях")
        self.notifications_check.setChecked(True)
        layout.addWidget(self.notifications_check)

        # === Пункт 5: Путь для сохранения отчётов ===
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("5. Путь для сохранения отчётов:"))
        self.path_input = QLineEdit("C:/NetworkAuditor/Reports")
        path_layout.addWidget(self.path_input)
        # Кнопка выбора папки через диалог
        self.browse_btn = QPushButton("Обзор...")
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        layout.addStretch()

        # Кнопка сохранения настроек
        self.save_btn = QPushButton("Сохранить настройки")
        self.save_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def browse_path(self):
        """
        Открытие диалога выбора папки для сохранения отчётов.
        Обновляет поле ввода выбранным путём.
        """
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для отчётов")
        if folder:
            self.path_input.setText(folder)

    def save_settings(self):
        """
        Сохранение настроек.
        В реальной системе настройки сохраняются в таблицу system_settings БД.
        """
        # TODO: Реализовать сохранение в БД через DatabaseManager
        QMessageBox.information(self, "Успех", "Настройки успешно сохранены")