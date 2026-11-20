# -*- coding: utf-8 -*-
"""
Окно прогресса сканирования с прогресс-баром.
Отображает текущий статус, количество просканированных хостов,
найденные устройства и позволяет отменить сканирование.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar,
                               QPushButton, QFrame)
from PySide6.QtCore import Qt


class ScanProgressWindow(QWidget):
    """
    Окно отображения прогресса сканирования.
    Обновляется через сигналы от ScanWorker.
    """

    def __init__(self):
        """Инициализация окна прогресса."""
        super().__init__()
        self.setWindowTitle("Идёт сканирование")
        self.resize(500, 280)
        # Тёмный фон
        self.setStyleSheet("background-color: #1e1e2e; color: #e6e6f0;")
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок статуса
        self.status_label = QLabel("🔍 Сканирование сети...")
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4a9eff;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2a2a3e;
                border: 1px solid #3a3a52;
                border-radius: 5px;
                text-align: center;
                color: #e6e6f0;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a9eff;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Детальная информация
        self.details_label = QLabel("Просканировано хостов: 0 / 254")
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setStyleSheet("font-size: 13px; color: #a0a0b0;")
        layout.addWidget(self.details_label)

        # Информация о найденных устройствах
        self.found_label = QLabel("Найдено устройств: 0")
        self.found_label.setAlignment(Qt.AlignCenter)
        self.found_label.setStyleSheet("font-size: 13px; color: #27ae60; font-weight: bold;")
        layout.addWidget(self.found_label)

        layout.addSpacing(15)

        # Кнопка отмены
        self.cancel_btn = QPushButton("✖ Отменить сканирование")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; 
                padding: 10px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #ec7063; }
        """)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

    def update_progress(self, percent: int, scanned: int, total: int, found: int = 0):
        """
        Обновление прогресса сканирования.
        Вызывается из ScanWorker через сигнал.

        :param percent: Процент выполнения (0-100)
        :param scanned: Количество просканированных хостов
        :param total: Общее количество хостов
        :param found: Количество найденных устройств
        """
        self.progress_bar.setValue(percent)
        self.details_label.setText(f"Просканировано хостов: {scanned} / {total}")
        self.found_label.setText(f"Найдено устройств с открытыми портами: {found}")

        # Обновляем статус
        if percent < 100:
            self.status_label.setText(f"🔍 Сканирование сети... ({percent}%)")
        else:
            self.status_label.setText("✓ Сканирование завершено!")