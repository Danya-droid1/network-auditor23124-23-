# -*- coding: utf-8 -*-
"""
Окно дашборда со статистикой и быстрыми действиями.
Отображает карточки: всего сканирований, открытых портов,
высокого риска, активов. Предоставляет кнопки быстрого доступа.
Автор: Голуб Д.Н., группа о.ИЗДтс 23.1/Б4-23
"""

# Импорт компонентов PySide6 для построения интерфейса
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QPushButton, QGridLayout)
from PySide6.QtCore import Qt


class DashboardWindow(QWidget):
    """
    Главный дашборд приложения.
    Показывает статистику и предоставляет быстрые действия для пользователя.
    """

    def __init__(self, user_data: dict):
        """
        Инициализация дашборда.

        :param user_data: Словарь с данными авторизованного пользователя
        """
        super().__init__()
        # Сохраняем данные пользователя для отображения приветствия
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса дашборда."""
        # Основной вертикальный layout с отступами
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок дашборда
        header = QLabel("Панель управления")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)

        # Приветствие пользователя
        welcome = QLabel(f"Добро пожаловать, {self.user_data.get('full_name', 'Пользователь')}!")
        welcome.setStyleSheet("font-size: 16px; color: #7f8c8d; margin-bottom: 20px;")
        layout.addWidget(welcome)

        # === Сетка статистических карточек ===
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        # Карточки со статистикой (цвет, значение, название)
        stats_grid.addWidget(self.create_stat_card("Всего сканирований", "12", "#3498db"), 0, 0)
        stats_grid.addWidget(self.create_stat_card("Открытых портов", "47", "#e74c3c"), 0, 1)
        stats_grid.addWidget(self.create_stat_card("Высокий риск", "8", "#e67e22"), 1, 0)
        stats_grid.addWidget(self.create_stat_card("Активов в сети", "156", "#27ae60"), 1, 1)

        layout.addLayout(stats_grid)

        layout.addSpacing(30)

        # === Блок быстрых действий ===
        quick_actions = QLabel("Быстрые действия")
        quick_actions.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(quick_actions)

        # Кнопки быстрого доступа
        actions_layout = QHBoxLayout()

        self.btn_new_scan = QPushButton("Начать новое сканирование")
        self.btn_new_scan.setStyleSheet("background-color: #27ae60; color: white; padding: 12px; font-size: 14px;")

        self.btn_view_reports = QPushButton("Просмотреть отчёты")
        self.btn_view_reports.setStyleSheet("background-color: #3498db; color: white; padding: 12px; font-size: 14px;")

        self.btn_manage_assets = QPushButton("Управление активами")
        self.btn_manage_assets.setStyleSheet("background-color: #9b59b6; color: white; padding: 12px; font-size: 14px;")

        actions_layout.addWidget(self.btn_new_scan)
        actions_layout.addWidget(self.btn_view_reports)
        actions_layout.addWidget(self.btn_manage_assets)

        layout.addLayout(actions_layout)

        # Растягиваем пустое пространство внизу
        layout.addStretch()
        self.setLayout(layout)

    def create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """
        Создание цветной карточки со статистикой.

        :param title: Название показателя
        :param value: Числовое значение
        :param color: Цвет фона карточки
        :return: Настроенный QFrame
        """
        # Создаём контейнер карточки
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        card.setFixedHeight(120)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        # Большое число
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        value_label.setAlignment(Qt.AlignCenter)

        # Подпись
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: white;")
        title_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)

        return card