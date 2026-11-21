# -*- coding: utf-8 -*-
"""
Окно прогресса сканирования с прогресс-баром.
Отображает текущий статус, количество просканированных хостов,
найденные устройства и оценку оставшегося времени.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar,
                               QPushButton)
from PySide6.QtCore import Qt, QTime


class ScanProgressWindow(QWidget):
    """
    Окно отображения прогресса сканирования.
    Обновляется через сигналы от ScanWorker.
    """

    def __init__(self, total_hosts: int = 0):
        """
        Инициализация окна прогресса.

        :param total_hosts: Общее количество хостов для сканирования (для отображения до первого сигнала)
        """
        super().__init__()
        self.setWindowTitle("Идёт сканирование")
        self.resize(500, 320)
        self.start_time = QTime.currentTime()
        self.total_hosts = total_hosts
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

        # Детальная информация — теперь использует переданное total_hosts
        if self.total_hosts > 0:
            initial_text = f"Просканировано хостов: 0 / {self.total_hosts}"
        else:
            initial_text = "Просканировано хостов: 0 / ..."

        self.details_label = QLabel(initial_text)
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setStyleSheet("font-size: 13px; color: #a0a0b0;")
        layout.addWidget(self.details_label)

        # Информация о найденных устройствах
        self.found_label = QLabel("Найдено устройств: 0")
        self.found_label.setAlignment(Qt.AlignCenter)
        self.found_label.setStyleSheet("font-size: 13px; color: #27ae60; font-weight: bold;")
        layout.addWidget(self.found_label)

        # Оценка оставшегося времени
        self.time_label = QLabel("Оставшееся время: рассчитывается...")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 13px; color: #f39c12; font-weight: bold;")
        layout.addWidget(self.time_label)

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

        # Рассчитываем оставшееся время
        if scanned > 0 and percent < 100:
            elapsed = self.start_time.msecsTo(QTime.currentTime()) / 1000  # секунды
            if elapsed > 0:
                remaining_seconds = (elapsed / scanned) * (total - scanned)
                self.time_label.setText(f"Оставшееся время: {self._format_time(remaining_seconds)}")
            else:
                self.time_label.setText("Оставшееся время: рассчитывается...")
        else:
            self.time_label.setText("Сканирование завершено!")

        # Обновляем статус
        if percent < 100:
            self.status_label.setText(f"🔍 Сканирование сети... ({percent}%)")
        else:
            self.status_label.setText("✓ Сканирование завершено!")

    def _format_time(self, seconds: float) -> str:
        """
        Форматирование времени в читаемый вид.

        :param seconds: Количество секунд
        :return: Строка с форматированным временем
        """
        if seconds < 60:
            return f"{int(seconds)} сек"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes} мин {secs} сек"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours} ч {minutes} мин"