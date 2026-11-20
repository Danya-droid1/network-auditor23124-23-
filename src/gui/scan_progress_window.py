# -*- coding: utf-8 -*-
"""
Окно прогресса сканирования с прогресс-баром.
Отображает текущий статус, количество просканированных хостов
и позволяет отменить сканирование.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar,
                               QPushButton)
from PySide6.QtCore import Qt, QTimer


class ScanProgressWindow(QWidget):
    """
    Окно отображения прогресса сканирования.
    Использует QTimer для симуляции обновления прогресса.
    """

    def __init__(self):
        """Инициализация окна прогресса."""
        super().__init__()
        self.setWindowTitle("Идёт сканирование")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок статуса
        self.status_label = QLabel("Сканирование сети...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Прогресс-бар (0-100%)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Детальная информация о прогрессе
        self.details_label = QLabel("Просканировано хостов: 0 / 254")
        self.details_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.details_label)

        layout.addSpacing(20)

        # Кнопка отмены сканирования
        self.cancel_btn = QPushButton("Отменить сканирование")
        self.cancel_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        self.cancel_btn.clicked.connect(self.cancel_scan)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

        # Таймер для симуляции обновления прогресса (каждые 500 мс)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(500)

    def update_progress(self):
        """
        Обновление прогресс-бара каждые 500 мс.
        Увеличивает значение на 5% до достижения 100%.
        """
        current = self.progress_bar.value()
        if current < 100:
            # Увеличиваем прогресс на 5%
            self.progress_bar.setValue(current + 5)
            # Пересчитываем количество просканированных хостов
            hosts = int((current + 5) / 100 * 254)
            self.details_label.setText(f"Просканировано хостов: {hosts} / 254")
        else:
            # Останавливаем таймер при завершении
            self.timer.stop()
            self.status_label.setText("Сканирование завершено!")

    def cancel_scan(self):
        """Отмена процесса сканирования пользователем."""
        self.timer.stop()
        self.status_label.setText("Сканирование отменено")
        self.close()